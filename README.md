# lnb-python

Python SDK for the [Le New Black Wholesale API v2](https://developer.lenewblack.com/docs/le-new-black-wholesale-api-v2).

## Installation

```bash
pip install lnb-python
```

## Quick Start

```python
import lnb

client = lnb.LnbClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
)

# Iterate all products (auto-pagination)
for product in client.products.paginate():
    print(product.model, product.name)

# Fetch a single product
product = client.products.get("SHIRT-001")
print(product.variants)

# Use as a context manager (auto-closes HTTP connection)
with lnb.LnbClient("id", "secret") as client:
    order = client.orders.get("ORD-001")
```

## Authentication

The SDK handles OAuth 2.0 Client Credentials automatically. Tokens are cached and proactively refreshed 60 seconds before expiry. The client is thread-safe.

## Resources

All 13 API resources are available as properties on `LnbClient`:

| Property | Methods |
|---|---|
| `client.products` | `list`, `paginate`, `get`, `get_variant`, `upsert`, `update_variant`, `set_variant_alternatives`, `batch_upsert` |
| `client.orders` | `list`, `paginate`, `get`, `upsert`, `update_status`, `archive` |
| `client.inventory` | `list`, `get_by_data`, `get_by_ean`, `get_by_sku`, `set_by_data`, `set_by_ean`, `set_by_sku`, `batch_set_by_data`, `batch_set_by_ean`, `batch_set_by_sku` |
| `client.prices` | `list`, `paginate`, `get`, `upsert`, `batch_upsert` |
| `client.collections` | `list`, `paginate`, `get`, `upsert`, `batch_upsert` |
| `client.fabrics` | `list`, `paginate`, `get` |
| `client.retailers` | `list`, `paginate`, `get`, `upsert` |
| `client.files` | `list`, `paginate`, `get`, `upload`, `delete` |
| `client.sales_documents` | `list`, `paginate`, `get` |
| `client.sales_catalogs` | `list`, `paginate`, `get` |
| `client.selections` | `list`, `paginate`, `get`, `upsert` |
| `client.sizings` | `list`, `paginate`, `get` |
| `client.invoices` | `list`, `paginate`, `get` |

## Pagination

Every list endpoint returns a `ResultSet[T]` with `.meta` (pagination info) and `.items`. Use `paginate()` to automatically walk all pages:

```python
# Single page — manual control
result = client.products.list({"collection": "SS24"})
print(result.meta.total_items, result.meta.has_more)
for item in result:
    print(item.model)

# All pages — automatic
for product in client.products.paginate({"collection": "SS24"}):
    print(product.model)
```

## Batch Operations

```python
result = client.products.batch_upsert([
    {"model": "A001", "name": "Jacket"},
    {"model": "A002", "name": "Trousers"},
])

print(f"{len(result.items)} succeeded, {len(result.errors)} failed")
if result.has_errors:
    for error in result.errors:
        print(f"Item {error.index}: {error.message}")
```

## Error Handling

```python
import lnb

try:
    product = client.products.get("UNKNOWN")
except lnb.NotFoundError:
    print("Product not found")
except lnb.ValidationError as e:
    print(f"Validation failed: {e.errors}")
except lnb.RateLimitError:
    print("Rate limited — retry later")
except lnb.AuthenticationError:
    print("Invalid credentials")
except lnb.LnbApiError as e:
    print(f"API error {e.status_code}: {e}")
```

### Exception Hierarchy

```
LnbError
├── LnbApiError              (HTTP errors from the API)
│   ├── AuthenticationError  (401)
│   ├── NotFoundError        (404)
│   ├── ValidationError      (422) — has .errors dict
│   └── RateLimitError       (429)
└── ConfigurationError       (bad SDK config)
```

## Configuration

```python
client = lnb.LnbClient(
    client_id="...",
    client_secret="...",
    base_url="https://www.lenewblack.com/apis/wholesale/v2",  # default
    timeout=30.0,        # request timeout in seconds (default: 30)
    max_retries=3,       # retries on 429/5xx/network errors (default: 3)
    http_client=None,    # inject a custom httpx.Client if needed
)
```

### Per-request options

```python
product = client.products.get(
    "SHIRT-001",
    options={
        "timeout": 5.0,
        "extra_headers": {"X-Request-Id": "abc123"},
    },
)
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type check
mypy src/lnb

# Lint
ruff check src/lnb
```

## License

Proprietary — requires authorization from Le New Black.
