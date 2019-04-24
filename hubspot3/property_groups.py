"""
hubspot property groups api
"""
from hubspot3 import logging_helper
from hubspot3.base import BaseClient
from hubspot3.globals import (
    OBJECT_TYPE_COMPANIES,
    OBJECT_TYPE_CONTACTS,
    OBJECT_TYPE_DEALS,
    OBJECT_TYPE_PRODUCTS,
)
from hubspot3.utils import prettify


PROPERTY_GROUPS_API_VERSION = {
    OBJECT_TYPE_COMPANIES: '1',
    OBJECT_TYPE_CONTACTS: '1',
    OBJECT_TYPE_DEALS: '1',
    OBJECT_TYPE_PRODUCTS: '2',
    OBJECT_TYPE_DEALS: '1',
}


class PropertyGroupsClient(BaseClient):
    """
    The hubspot3 Property Groups client uses the _make_request method to call the
    API for data.  It returns a python object translated from the json return
    """

    def __init__(self, *args, **kwargs):
        super(PropertyGroupsClient, self).__init__(*args, **kwargs)
        self.log = logging_helper.get_log("hapi.properties")

    def _get_path(self, subpath):
        return "properties/v{}/{}/groups/{}".format(
            PROPERTY_GROUPS_API_VERSION[self.object_type],
            self.object_type,
            subpath,
        )

    def create(self, object_type, code, label, extra_params=None):
        self.object_type = object_type

        extra_params = extra_params or {}

        return self._call(
            "", method="POST", data={
                "name": code,
                "displayName": label,
                **extra_params
            }
        )

    def get_all(self, object_type):
        self.object_type = object_type

        return self._call("", method="GET")

    def delete(self, object_type, code):
        self.object_type = object_type

        return self._call(
            "named/%s" % code, method="DELETE"
        )

    def delete_all_custom(self, object_type):
        groups_data = self.get_all(object_type)

        for group_data in groups_data:
            group_name = group_data['name']
            if (
                not group_data['hubspotDefined']

                # Dirty workaround.
                # Default product properties are currently *not* tagged as `hubspotDefined`... :/
                and not (
                    object_type == 'products'
                    and group_name in (
                        'productinformation',
                        'productlineiteminformation',
                    )
                )
            ):
                self.delete(object_type, group_name)
