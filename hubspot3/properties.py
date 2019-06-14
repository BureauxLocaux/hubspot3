"""
hubspot properties api
"""
from hubspot3 import logging_helper
from hubspot3.base import BaseClient
from hubspot3.globals import (
    OBJECT_TYPE_COMPANIES,
    OBJECT_TYPE_CONTACTS,
    OBJECT_TYPE_DEALS,
    OBJECT_TYPE_LINE_ITEMS,
    OBJECT_TYPE_PRODUCTS,
    VALID_PROPERTY_DATA_TYPES,
    VALID_PROPERTY_WIDGET_TYPES,
)
from hubspot3.utils import prettify


PROPERTIES_API_VERSION = {
    OBJECT_TYPE_COMPANIES: '1',
    OBJECT_TYPE_CONTACTS: '1',
    OBJECT_TYPE_DEALS: '1',
    OBJECT_TYPE_LINE_ITEMS: '2',
    OBJECT_TYPE_PRODUCTS: '2',
}


class PropertiesClient(BaseClient):
    """
    The hubspot3 Properties client uses the _make_request method to call the
    API for data.  It returns a python object translated from the json return
    """

    def __init__(self, *args, **kwargs):
        super(PropertiesClient, self).__init__(*args, **kwargs)
        self.log = logging_helper.get_log("hapi.properties")

    def _get_path(self, subpath):
        return "properties/v{}/{}/properties/{}".format(
            PROPERTIES_API_VERSION[self.object_type],
            self.object_type,
            subpath,
        )

    def create(self, object_type, code, label, description,
               group_code, data_type, widget_type, extra_params=None):

        if data_type not in VALID_PROPERTY_DATA_TYPES:
            raise ValueError(
                "Invalid data type for property. Valid data types are: {}".format(
                    VALID_PROPERTY_DATA_TYPES
                )
            )

        if widget_type not in VALID_PROPERTY_WIDGET_TYPES:
            raise ValueError(
                "Invalid widget type for property. Valid widget types are: {}".format(
                    VALID_PROPERTY_WIDGET_TYPES
                )
            )

        extra_params = extra_params or {}

        self.object_type = object_type
        return self._call(
            "", method="POST", data={
                "name": code,
                "label": label,
                "description": description,
                "groupName": group_code,
                "type": data_type,
                "fieldType": widget_type,
                **extra_params
            }
        )

    def get_all(self, object_type):
        self.object_type = object_type

        return self._call(
            "",
            method="GET",
            params={
                "properties": [
                    "name",
                    "label",
                    "description",
                ]
            }
        )

    def delete(self, object_type, code):
        self.object_type = object_type

        return self._call(
            "named/%s" % code, method="DELETE"
        )

    def delete_all_custom(self, object_type):
        props_data = self.get_all(object_type)

        for prop_data in props_data:
            if not prop_data['hubspotDefined']:
                self.delete(object_type, prop_data['name'])
