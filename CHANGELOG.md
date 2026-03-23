# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-03-24

### Added

- Initial release of the Python SDK for the Le New Black Wholesale API v2
- `LnbClient` entry point with 13 resource services as lazy properties
- OAuth2 client credentials token management (`TokenManager`) with thread-safe refresh and 60-second proactive buffer
- `HttpTransport` wrapping `httpx` with exponential backoff retry (configurable `max_retries`), `Retry-After` header support, and per-request options (`timeout`, `extra_headers`)
- `ResultSet[T]` for single-page list results with pagination metadata
- `paginate()` auto-paginating generator for all list endpoints
- `BatchResult[T]` for bulk create/update operations with per-item error tracking
- Pydantic v2 response models for all 13 resources (`extra="ignore"` for forward-compatibility with new API fields)
- `LnbClient.VERSION` class constant and `LnbClient.version()` method to retrieve API version from the server
- Resources: `products`, `orders`, `inventory`, `prices`, `collections`, `fabrics`, `retailers`, `files`, `sales_documents`, `sales_catalogs`, `selections`, `sizings`, `invoices`
- 42 tests covering auth, HTTP transport, pagination, and product service (82% coverage)

[Unreleased]: https://github.com/lenewblack/lnb-python/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/lenewblack/lnb-python/releases/tag/v0.1.0
