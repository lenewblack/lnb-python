from __future__ import annotations

from typing import Optional

import httpx

from lnb._auth import TokenManager
from lnb._http import HttpTransport
from lnb._version import __version__
from lnb.services.collections import CollectionService
from lnb.services.fabrics import FabricService
from lnb.services.files import FileService
from lnb.services.inventory import InventoryService
from lnb.services.invoices import InvoiceService
from lnb.services.orders import OrderService
from lnb.services.prices import PriceService
from lnb.services.products import ProductService
from lnb.services.retailers import RetailerService
from lnb.services.sales_catalogs import SalesCatalogService
from lnb.services.sales_documents import SalesDocumentService
from lnb.services.selections import SelectionService
from lnb.services.sizings import SizingService

DEFAULT_BASE_URL = "https://www.lenewblack.com/apis/wholesale/v2"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3


class LnbClient:
    """Main entry point for the Le New Black Wholesale API SDK.

    The SDK version is available as ``LnbClient.VERSION``.

    Example::

        import lnb

        client = lnb.LnbClient(
            client_id="your-client-id",
            client_secret="your-client-secret",
        )

        # List products
        for product in client.products.paginate():
            print(product.model, product.name)

        # Or use as a context manager
        with lnb.LnbClient("id", "secret") as client:
            order = client.orders.get("ORD-001")
    """

    VERSION = __version__
    """Current SDK version string."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._token_manager = TokenManager(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
        )
        self._transport = HttpTransport(
            base_url=base_url,
            token_manager=self._token_manager,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
        )
        # Lazy service singletons (constructed on first access)
        self._products: Optional[ProductService] = None
        self._orders: Optional[OrderService] = None
        self._inventory: Optional[InventoryService] = None
        self._prices: Optional[PriceService] = None
        self._collections: Optional[CollectionService] = None
        self._fabrics: Optional[FabricService] = None
        self._retailers: Optional[RetailerService] = None
        self._files: Optional[FileService] = None
        self._sales_documents: Optional[SalesDocumentService] = None
        self._sales_catalogs: Optional[SalesCatalogService] = None
        self._selections: Optional[SelectionService] = None
        self._sizings: Optional[SizingService] = None
        self._invoices: Optional[InvoiceService] = None

    @property
    def products(self) -> ProductService:
        if self._products is None:
            self._products = ProductService(self._transport)
        return self._products

    @property
    def orders(self) -> OrderService:
        if self._orders is None:
            self._orders = OrderService(self._transport)
        return self._orders

    @property
    def inventory(self) -> InventoryService:
        if self._inventory is None:
            self._inventory = InventoryService(self._transport)
        return self._inventory

    @property
    def prices(self) -> PriceService:
        if self._prices is None:
            self._prices = PriceService(self._transport)
        return self._prices

    @property
    def collections(self) -> CollectionService:
        if self._collections is None:
            self._collections = CollectionService(self._transport)
        return self._collections

    @property
    def fabrics(self) -> FabricService:
        if self._fabrics is None:
            self._fabrics = FabricService(self._transport)
        return self._fabrics

    @property
    def retailers(self) -> RetailerService:
        if self._retailers is None:
            self._retailers = RetailerService(self._transport)
        return self._retailers

    @property
    def files(self) -> FileService:
        if self._files is None:
            self._files = FileService(self._transport)
        return self._files

    @property
    def sales_documents(self) -> SalesDocumentService:
        if self._sales_documents is None:
            self._sales_documents = SalesDocumentService(self._transport)
        return self._sales_documents

    @property
    def sales_catalogs(self) -> SalesCatalogService:
        if self._sales_catalogs is None:
            self._sales_catalogs = SalesCatalogService(self._transport)
        return self._sales_catalogs

    @property
    def selections(self) -> SelectionService:
        if self._selections is None:
            self._selections = SelectionService(self._transport)
        return self._selections

    @property
    def sizings(self) -> SizingService:
        if self._sizings is None:
            self._sizings = SizingService(self._transport)
        return self._sizings

    @property
    def invoices(self) -> InvoiceService:
        if self._invoices is None:
            self._invoices = InvoiceService(self._transport)
        return self._invoices

    def version(self) -> "ApiVersion":
        """Return the current API version information from the server."""
        from lnb.models.api_version import ApiVersion  # local import avoids circular dep
        raw = self._transport.request("GET", "/version")
        return ApiVersion.model_validate(raw)

    def close(self) -> None:
        """Close the underlying HTTP client and release resources."""
        self._transport.close()

    def __enter__(self) -> "LnbClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
