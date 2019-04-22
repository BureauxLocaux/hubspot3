"""
hubspot products api
"""
from hubspot3 import logging_helper
from hubspot3.base import BaseClient
from hubspot3.utils import prettify


PRODUCTS_API_VERSION = "1"


class ProductsClient(BaseClient):
    """
    The hubspot3 Products client uses the _make_request method to call the
    API for data.  It returns a python object translated from the json return
    """

    def __init__(self, *args, **kwargs):
        super(ProductsClient, self).__init__(*args, **kwargs)
        self.log = logging_helper.get_log("hapi.products")

    def _get_path(self, subpath):
        return "crm-objects/v{}/objects/products/{}".format(PRODUCTS_API_VERSION, subpath)

    def get_all(self, **options):
        finished = False
        output = []
        offset = 0
        while not finished:
            batch = self._call(
                "paged", method="GET", params={"offset": offset}, **options
            )
            finished = not batch["has-more"]
            offset = batch["offset"]

        return output

    def get_product_by_id(self, product_id, **options):
        """Gets product specified by ID"""
        return self._call(
            "{}".format(product_id), method="GET", **options
        )

    def create(self, data=None, **options):
        data = data or {}
        return self._call(
            "", data=data, method="POST", **options
        )

    def update(self, product_id, data=None, **options):
        data = data or {}
        return self._call(
             "{}".format(product_id), data=data, method="POST", **options
        )

    def delete(self, product_id, **options):
        """Deletes a product by product_id."""
        return self._call(
            "{}".format(product_id), method="DELETE", **options
        )


    def get_recently_modified(self, offset=0, since=None, **options):
        """
        get recently modified products

        since: must be a UNIX formatted timestamp in milliseconds
        """
        finished = False
        output = []
        querylimit = 100  # max according to the docs

        while not finished:
            params = {
                "offset": offset,
            }
            if since:
                params["since"] = since

            batch = self._call(
                "/crm-objects/v1/change-log/products", method="GET", params=params, **options  # NOTE: this is a different base path!
            )
            finished = not batch["hasMore"] or len(output) >= limit
            offset = batch["offset"]

        return output[:limit]
