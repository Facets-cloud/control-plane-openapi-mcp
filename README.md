# Control Plane OpenAPI MCP

MCP server for Facets Control Plane OpenAPI specification. This server fetches the OpenAPI 3.0 specification from Facets Control Plane and exposes it through MCP tools for LLM integration.

## Features

- **Real-time OpenAPI fetching**: Automatically fetches the latest OpenAPI spec from Facets Control Plane
- **Comprehensive API catalog**: Provides access to 549+ active operations and 500+ schemas
- **Deprecated operation filtering**: Automatically excludes deprecated operations for cleaner results
- **Fuzzy search**: Search operations and schemas using natural language queries
- **Detailed operation info**: Get complete operation details including parameters, responses, and request bodies
- **Schema exploration**: Access detailed schema information with property lists and descriptions
- **Caching**: Intelligent caching to minimize API calls and improve performance

## Installation

```bash
# Clone and install with uv
git clone <repository-url>
cd control-plane-openapi-mcp
uv sync

# Or install directly
uv add control-plane-openapi-mcp
```

## Usage

### Running the MCP Server

```bash
# Run the server
uv run control-plane-openapi-mcp

# Or with custom configuration
FACETS_OPENAPI_URL="https://your-instance.com/v3/api-docs" uv run control-plane-openapi-mcp
```

### Available Tools

1. **`refresh_api_catalog`** - Refresh the API catalog with latest spec
2. **`get_api_catalog`** - Get complete API catalog with all operations and schemas
3. **`search_api_operations`** - Search operations using fuzzy matching
4. **`search_api_schemas`** - Search schemas by name and description
5. **`load_api_operation_by_operationId`** - Load specific operation by ID
6. **`load_api_operation_by_path_and_method`** - Load operation by path and HTTP method
7. **`load_api_schema_by_schemaName`** - Load detailed schema information

### Example Queries

```python
# Search for stack-related operations
search_api_operations("stacks")

# Get details of a specific operation
load_api_operation_by_operationId("getStack")

# Load operation by path and method
load_api_operation_by_path_and_method("/cc-ui/v1/stacks/{stackName}", "GET")

# Find schema information
search_api_schemas("Stack")
load_api_schema_by_schemaName("Stack")
```

## Configuration

Environment variables:

- `FACETS_OPENAPI_URL` - OpenAPI specification URL (default: Facets demo instance)
- `CACHE_TTL` - Cache TTL in seconds (default: 3600)

## API Coverage

The server provides access to the complete Facets Control Plane API including:

- **Stack Management**: Create, update, delete, and manage stacks
- **Cluster Operations**: Deploy, monitor, and manage clusters
- **Artifact Management**: Handle CI/CD artifacts and routing
- **User & Access Control**: Manage users, groups, and permissions
- **Resource Management**: Handle cloud resources and configurations
- **Monitoring & Alerts**: Access deployment logs and monitoring data

## Architecture

- **`SpecLoader`**: Fetches and processes OpenAPI specifications
- **`SpecProcessor`**: Extracts operations and schemas from specs
- **`SearchEngine`**: Provides fuzzy search capabilities
- **`OpenAPIService`**: Main service coordinating all components
- **`SimpleCache`**: TTL-based caching for performance
- **MCP Tools**: Seven tools exposing functionality to LLMs

## Example LLM Prompts

When using with Cursor or other LLM tools, try these prompts:

```
"Show me all stack-related operations in the Facets API"
"What are the required parameters for creating a new stack?"
"Find operations related to cluster deployments"
"Show me the Stack schema structure"
"Generate a TypeScript interface for the Stack model"
"Create an example API call to get stack information"
```

## Development

```bash
# Install dependencies
uv sync

# Test the tools directly
uv run python -c "from control_plane_openapi_mcp.tools import search_api_operations; print(search_api_operations('stack'))"

# Run tests (when available)
uv run pytest
```

## Comparison with TypeScript Version

This Python implementation provides similar functionality to the TypeScript `@reapi/mcp-openapi` but is:

- **Simpler**: Single API spec, no file system operations
- **Focused**: Specifically designed for Facets Control Plane
- **Efficient**: Direct JSON processing with smart caching
- **Lightweight**: Fewer dependencies and abstractions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
