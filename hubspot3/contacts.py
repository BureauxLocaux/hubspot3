"""
hubspot contacts api
"""
from hubspot3 import logging_helper
from hubspot3.associations import AssociationsClient
from hubspot3.base import BaseClient
from hubspot3.utils import prettify


CONTACTS_API_VERSION = "1"


class ContactsClient(BaseClient):
    """
    The hubspot3 Contacts client uses the _make_request method to call the
    API for data.  It returns a python object translated from the json return
    """

    def __init__(self, *args, **kwargs):
        self.api_key = kwargs.get('api_key')

        super(ContactsClient, self).__init__(*args, **kwargs)
        self.log = logging_helper.get_log("hapi.contacts")

    def _get_path(self, subpath):
        return "contacts/v{}/{}".format(CONTACTS_API_VERSION, subpath)

    def create_or_update_a_contact(self, email, data=None, **options):
        """Creates or Updates a client with the supplied data."""
        data = data or {}
        return self._call(
            "contact/createOrUpdate/email/{email}".format(email=email),
            data=data,
            method="POST",
            **options
        )

    def get_contact_by_email(self, email, **options):
        """Gets contact specified by email address."""
        return self._call(
            "contact/email/{email}/profile".format(email=email), method="GET", **options
        )

    def get_contact_by_id(self, contact_id, **options):
        """Gets contact specified by ID"""
        return self._call(
            "contact/vid/{}/profile".format(contact_id), method="GET", **options
        )

    def update_a_contact(self, contact_id, data=None, **options):
        """Updates the contact by contact_id with the given data."""
        data = data or {}
        return self._call(
            "contact/vid/{contact_id}/profile".format(contact_id=contact_id),
            data=data,
            method="POST",
            **options
        )

    def delete(self, contact_id, **options):
        """Deletes a contact by contact_id."""
        return self._call(
            "contact/vid/{contact_id}".format(contact_id=contact_id),
            method="DELETE",
            **options
        )

    def delete_a_contact(self, contact_id, **options):
        return self.delete(contact_id, **options)

    def create(self, data=None, **options):
        data = data or {}
        return self._call("contact", data=data, method="POST", **options)

    def update(self, key, data=None, **options):
        if not data:
            data = {}
        return self._call(
            "contact/vid/{}/profile".format(key), data=data, method="POST", **options
        )

    def link_contact_to_company(self, contact_id, company_id):
        if not self.api_key:
            return False
        asso_client = AssociationsClient(api_key=self.api_key)
        return asso_client.link_contact_to_company(contact_id, company_id)

    def get_batch(self, ids, extra_props=None):
        properties = [
            "email",
            "firstname",
            "lastname",
            "company",
            "website",
            "phone",
            "address",
            "city",
            "state",
            "zip",
            "associatedcompanyid",
        ]
        properties.extend(extra_props or [])

        batch = self._call(
            "contact/vids/batch",
            method="GET",
            doseq=True,
            params={
                "vid": ids,
                "property": properties,
            },
        )
        # It returns a dict with IDs as keys
        return [prettify(batch[contact], id_key="vid") for contact in batch]

    def get_all(self, extra_props=None, **options):
        # Can't get phone number from a get-all, so we just grab IDs and
        # then have to make ANOTHER call in batches
        finished = False
        output = []
        offset = 0
        querylimit = 100  # Max value according to docs
        properties = [
            "email",
            "firstname",
            "lastname",
            "company",
            "website",
            "phone",
            "address",
            "city",
            "state",
            "zip",
            "associatedcompanyid",
        ]
        properties.extend(extra_props or [])

        while not finished:
            batch = self._call(
                "lists/all/contacts/all",
                method="GET",
                params={
                    "count": querylimit,
                    "vidOffset": offset,
                    "properties": properties,
                },
                **options
            )
            output.extend(
                self.get_batch([contact["vid"] for contact in batch["contacts"]], extra_props)
            )
            finished = not batch["has-more"]
            offset = batch["vid-offset"]

        return output

    def search(self, search_query, **options):
        """
        Search among contacts for matches with the given `search_query`.

        Cf: https://developers.hubspot.com/docs/methods/contacts/search_contacts

        Parameters
        ----------
        search_query: str

        Returns
        -------
        list of dict
            The result of the search as a list of contacts.
        """
        finished = False
        offset = 0
        query_limit = 100       # Max value according to docs

        output = []

        while not finished:
            batch = self._call(
                "search/query",
                method="GET",
                params={
                    "count": query_limit,
                    "offset": offset,
                    "q": search_query,
                },
                **options,
            )

            output += batch['contacts']

            finished = not batch["has-more"]
            offset = batch["offset"]

        return output

    def delete_all(self):
        for contact in self.get_all():
            self.delete_a_contact(contact['vid'])
