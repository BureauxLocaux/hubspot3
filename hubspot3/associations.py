"""
hubspot associations api
"""
from hubspot3 import logging_helper
from hubspot3.base import BaseClient
from hubspot3.globals import (
    ASSOCIATION_TYPE_CONTACT_TO_COMPANY,
    VALID_ASSOCIATION_TYPES,
)
from hubspot3.utils import prettify


ASSOCIATIONS_API_VERSION = '1'

ASSOCIATION_CATEGORY = 'HUBSPOT_DEFINED'  # see: https://developers.hubspot.com/docs/methods/crm-associations/associate-objects  # noqa


class AssociationsClient(BaseClient):
    """
    The hubspot3 Associations client uses the _make_request method to call the
    API for data.  It returns a python object translated from the json return
    """

    def __init__(self, *args, **kwargs):
        super(AssociationsClient, self).__init__(*args, **kwargs)
        self.log = logging_helper.get_log("hapi.properties")

    def _get_path(self, subpath):
        return "crm-associations/v{}/associations{}".format(
            ASSOCIATIONS_API_VERSION,
            subpath,
        )

    def create(self, association_type, from_object_id, to_object_id):
        if association_type not in VALID_ASSOCIATION_TYPES:
            raise ValueError(
                "Invalid association type. Valid association types are: {}".format(
                    VALID_ASSOCIATION_TYPES
                )
            )

        return self._call(
            "", method="PUT", data={
                "category": ASSOCIATION_CATEGORY,
                "definitionId": association_type,
                "fromObjectId": from_object_id,
                "toObjectId": to_object_id,
            }
        )

    def link_contact_to_company(self, contact_id, company_id):
        return self.create(ASSOCIATION_TYPE_CONTACT_TO_COMPANY, contact_id, company_id)
