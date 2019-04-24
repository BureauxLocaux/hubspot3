from hubspot3 import logging_helper
from hubspot3.associations import AssociationsClient
from hubspot3.base import BaseClient


API_VERSION = "1"


class LinesClient(BaseClient):

    def __init__(self, *args, **kwargs):
        super(LinesClient, self).__init__(*args, **kwargs)
        self.log = logging_helper.get_log("hapi.products")

    def _get_path(self, subpath):
        return f'crm-objects/v1/objects/line_items/{subpath}'

    def create(self, data=None, **options):
        return self._call(
            '',
            data=data,
            method='POST',
            **options,
        )

    def get(self, line_id, **options):
        """Retrieve a line by its id."""
        return self._call('{}'.format(line_id), **options)

    def link_line_item_to_deal(self, line_item_id, deal_id):
        """Link a line item to a deal."""
        if not self.api_key:
            return False

        client = AssociationsClient(api_key=self.api_key)
        return client.link_line_item_to_deal(line_item_id, deal_id)
