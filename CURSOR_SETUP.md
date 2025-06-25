# MCP Configuration for Cursor IDE

## Option 1: Project-specific Configuration (Recommended)

Create `.cursor/mcp.json` in your project directory:

```json
{
  "mcpServers": {
    "control-plane-openapi": {
      "command": "uv",
      "args": ["run", "control-plane-openapi-mcp"],
      "cwd": "/Users/anujhydrabadi/work/repos/control-plane-openapi-mcp",
      "env": {
        "FACETS_OPENAPI_URL": "https://facetsdemo.console.facets.cloud/v3/api-docs",
        "CACHE_TTL": "3600"
      }
    }
  }
}
```

## Option 2: Global Configuration

Create or edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "control-plane-openapi": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/anujhydrabadi/work/repos/control-plane-openapi-mcp", "control-plane-openapi-mcp"],
      "env": {
        "FACETS_OPENAPI_URL": "https://facetsdemo.console.facets.cloud/v3/api-docs",
        "CACHE_TTL": "3600"
      }
    }
  }
}
```

## Option 3: Using the Package Directly (if published)

```json
{
  "mcpServers": {
    "control-plane-openapi": {
      "command": "uvx",
      "args": ["control-plane-openapi-mcp"],
      "env": {
        "FACETS_OPENAPI_URL": "https://your-instance.facets.cloud/v3/api-docs"
      }
    }
  }
}
```

## Environment Variables

- `FACETS_OPENAPI_URL`: URL to fetch OpenAPI spec from (default: demo instance)
- `CACHE_TTL`: Cache time-to-live in seconds (default: 3600)

## Usage in Cursor

After configuration, you can use prompts like:

```
"Show me all stack-related operations in the Facets API"
"What parameters does the getStack operation require?"
"Find all operations related to cluster deployments"
"Show me the structure of the Stack schema"
"Generate a TypeScript client for the stack operations"
```

## Troubleshooting

1. **Server not starting**: Check that uv and the project path are correct
2. **No tools available**: Ensure the MCP server is enabled in Cursor settings
3. **Slow responses**: The first request may be slow while fetching the OpenAPI spec
4. **Cache issues**: The server caches the spec for 1 hour by default

## Tools Available

1. `refresh_api_catalog` - Refresh the API catalog
2. `get_api_catalog` - Get complete catalog overview  
3. `search_api_operations` - Search operations by keywords
4. `search_api_schemas` - Search schemas by keywords
5. `load_api_operation_by_operationId` - Get operation details by ID
6. `load_api_operation_by_path_and_method` - Get operation by path/method
7. `load_api_schema_by_schemaName` - Get schema details by name
