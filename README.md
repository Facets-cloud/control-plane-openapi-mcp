# Control Plane OpenAPI MCP

MCP server for Facets Control Plane OpenAPI specification.

## Features

- Fetches OpenAPI 3.0 specification from Facets Control Plane
- Exposes API operations and schemas through MCP protocol
- Supports fuzzy search across operations and schemas
- Provides detailed operation and schema information to LLMs

## Installation

```bash
uv add control-plane-openapi-mcp
```

## Usage

```bash
control-plane-openapi-mcp
```

## Tools

1. `refresh-api-catalog` - Refresh the API catalog
2. `get-api-catalog` - Get complete API catalog
3. `search-api-operations` - Search for operations
4. `search-api-schemas` - Search for schemas
5. `load-api-operation-by-operationId` - Load operation by ID
6. `load-api-operation-by-path-and-method` - Load operation by path/method
7. `load-api-schema-by-schemaName` - Load schema by name

## Configuration

Set environment variables:
- `FACETS_OPENAPI_URL` - OpenAPI specification URL (default: Facets demo)
- `CACHE_TTL` - Cache TTL in seconds (default: 3600)
