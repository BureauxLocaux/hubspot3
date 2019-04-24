"""
hubspot owners api
"""
from hubspot3.associations import AssociationsClient
from hubspot3.base import BaseClient


OWNERS_API_VERSION = "v2"


class OwnersClient(BaseClient):
    """allows access to the owners api"""

    def _get_path(self, subpath):
        return "owners/{}/owners".format(OWNERS_API_VERSION)

    def get_owners(self, **options):
        """*Only* returns the list of owners, does not include additional metadata"""
        return self._call("owners", **options)

    def get_owner_by_id(self, owner_id, **options):
        """Retrieve an owner by its id."""
        owners = self.get_owners(**options)
        for owner in owners:
            if int(owner["ownerId"]) == int(owner_id):
                return owner
        return None

    def get_owner_name_by_id(self, owner_id, **options):
        """given an id of an owner, return their name"""
        owner_name = "value_missing"
        owner = self.get_owner_by_id(owner_id, **options)
        if owner:
            owner_name = "{} {}".format(owner["firstName"], owner["lastName"])
        return owner_name

    def get_owner_email_by_id(self, owner_id, **options):
        """given an id of an owner, return their email"""
        owner_email = "value_missing"
        owner = self.get_owner_by_id(owner_id, **options)
        if owner:
            owner_email = owner["email"]
        return owner_email

    def get_owner_by_email(self, owner_email, **options):
        """
        Retrieve an owner by its email.
        """
        owners = self.get_owners(
            method='GET',
            params={
                'email': owner_email,
            },
            **options,
        )
        if owners:
            return owners[0]
        return None

    def link_owner_to_company(self, owner_id, company_id):
        if not self.api_key:
            return False
        associations_client = AssociationsClient(api_key=self.api_key)
        return associations_client.link_owner_to_company(owner_id, company_id)
