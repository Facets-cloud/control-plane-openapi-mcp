# Control Plane OpenAPI MCP Server

This MCP (Model Context Protocol) Server provides seamless integration with the Facets Control Plane API through its OpenAPI specification. It enables AI assistants to understand, explore, and interact with the complete Facets Control Plane API, making infrastructure management and API integration more accessible through natural language interactions.

## Key Features

* **Real-time OpenAPI Integration**  
  Automatically fetches and processes the latest OpenAPI specification from Facets Control Plane, ensuring you always have access to current API documentation.

* **Built-in Script Generation Guidance**  
  Includes an MCP prompt that provides step-by-step guidance for creating production-ready scripts that interact with Control Plane APIs, with best practices for authentication, testing, and error handling.

* **Intelligent Operation Filtering**  
  Automatically excludes deprecated operations (17 filtered out of 566 total) to provide clean, relevant results and improved search performance.

* **Advanced Fuzzy Search**  
  Search through 549 active operations and 500+ schemas using natural language queries with intelligent matching across summaries, descriptions, tags, and operation IDs.

* **Comprehensive API Coverage**  
  Access complete operation details including parameters, request bodies, response schemas, and authentication requirements for all Facets Control Plane endpoints.

* **Smart Caching System**  
  Intelligent TTL-based caching minimizes API calls while ensuring fresh data, with configurable cache duration for optimal performance.

* **Detailed Schema Exploration**  
  Explore complex data structures with property listings, type information, and relationship mappings for all API schemas.

## Available MCP Tools

| Tool Name                               | Description                                                                                                       |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `refresh_api_catalog`                   | Refreshes the API catalog by fetching the latest OpenAPI specification from the control plane.                   |
| `get_api_catalog`                       | Returns complete API catalog overview with all active operations and schemas (deprecated operations excluded).   |
| `search_api_operations`                 | Search for operations using fuzzy matching across operation IDs, summaries, descriptions, and tags.             |
| `search_api_schemas`                    | Search for schemas by name and description to find relevant data structures.                                     |
| `load_api_operation_by_operationId`     | Load detailed operation information by its unique operation ID including parameters and responses.               |
| `load_api_operation_by_path_and_method` | Load operation details by specifying the exact API path and HTTP method.                                        |
| `load_api_schema_by_schemaName`         | Load comprehensive schema details including properties, types, and validation requirements.                      |
| `call_control_plane_api`                | Make authenticated GET requests to the Control Plane API using the provided path.                               |

## Available MCP Prompts

| Prompt Name                               | Description                                                                                                     |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `Control Plane API Script Generation`    | Provides step-by-step guidance for creating production-ready scripts that interact with Control Plane APIs.   |

## Prerequisites

The MCP Server requires [uv](https://github.com/astral-sh/uv) for dependency management and execution.

#### Install `uv` with Homebrew:
```bash
brew install uv
```

For other installation methods, see the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

## Integration with Claude

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "control-plane-openapi": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/your/cloned/control-plane-openapi-mcp", "control-plane-openapi-mcp"],
      "env": {
        "CONTROL_PLANE_URL": "https://facetsdemo.console.facets.cloud",
        "FACETS_USERNAME": "<YOUR_USERNAME>",
        "FACETS_TOKEN": "<YOUR_TOKEN>",
        "FACETS_PROFILE": "default",
        "CACHE_TTL": "3600"
      }
    }
  }
}
```

⚠️ Replace `<YOUR_USERNAME>` and `<YOUR_TOKEN>` with your actual Facets credentials.

### Environment Variables

- `CONTROL_PLANE_URL`: Base URL of the Facets Control Plane (default: demo instance)
- `FACETS_USERNAME`: Your Facets username for API authentication
- `FACETS_TOKEN`: Your Facets access token for API authentication
- `FACETS_PROFILE`: Facets profile to use from credentials file (default: "default")
- `CACHE_TTL`: Cache time-to-live in seconds (default: 3600)

### Authentication

The server supports two authentication methods:

1. **Environment Variables**: Set `FACETS_USERNAME` and `FACETS_TOKEN`
2. **Credentials File**: Configure `~/.facets/credentials` with profile-based credentials

For credential setup, refer to the [Facets Authentication Guide](https://readme.facets.cloud/reference/authentication-setup).

## Usage Highlights

- Use `get_api_catalog` to get an overview of all available operations and schemas
- Use `search_api_operations` and `search_api_schemas` to find relevant endpoints using natural language
- Use specific load operations to get detailed parameter and response information
- Use `call_control_plane_api` to make actual API calls and get real data from your Facets environment
- Leverage the fuzzy search to find operations even with partial or approximate terms
- All results exclude deprecated operations for cleaner, more relevant responses

## API Coverage

The server provides access to the complete Facets Control Plane API including:

- **Stack Management**: Create, update, delete, and manage infrastructure stacks
- **Cluster Operations**: Deploy, monitor, and manage Kubernetes clusters  
- **Artifact Management**: Handle CI/CD artifacts and routing rules
- **User & Access Control**: Manage users, groups, roles, and permissions
- **Resource Management**: Handle cloud resources and configurations
- **Monitoring & Alerts**: Access deployment logs, metrics, and monitoring data
- **Authentication**: OAuth integrations, tokens, and account management

## Example Prompts

When using with Claude, try these example prompts:

```
"Show me all stack-related operations in the Facets API"
"What are the required parameters for creating a new stack?"
"Find operations related to cluster deployments"
"Show me the Stack schema structure with all its properties"
"Generate a TypeScript interface for the Stack model"
"Get the current list of stacks from my environment"
"Show me details of a specific stack named 'my-production-stack'"
"What clusters are running in my Facets environment?"
"Create an example API call to get stack information"
"Find all endpoints that handle artifact routing"
"What authentication methods are available in the API?"
```

## Local Development

### Setting Up Development Environment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd control-plane-openapi-mcp
   ```

2. **Create virtual environment and install dependencies**:
   ```bash
   uv sync
   ```

3. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

### Running Tests

```bash
# Run the example script to test functionality
uv run python example.py

# Test direct tool imports
uv run python test_final.py

# Test specific functionality
uv run python -c "
from control_plane_openapi_mcp.tools import search_api_operations
import json
result = search_api_operations('stack')
print(f'Found {len(json.loads(result)[\"operations\"])} operations')
"
```

### Testing the MCP Server

```bash
# Start the MCP server (will wait for stdin input)
uv run control-plane-openapi-mcp

# Test with custom OpenAPI URL
FACETS_OPENAPI_URL="https://your-instance.com/v3/api-docs" uv run control-plane-openapi-mcp
```

### Development Workflow

1. **Make changes** to the source code
2. **Test locally** using the example scripts
3. **Verify MCP integration** with Claude Desktop
4. **Run validation** to ensure no regressions
5. **Commit changes** with descriptive messages

### Project Structure

```
control_plane_openapi_mcp/
├── __init__.py              # Package initialization
├── config.py                # Configuration and MCP setup
├── server.py                # Main MCP server entry point
├── tools.py                 # MCP tool implementations
└── core/                    # Core functionality
    ├── models.py            # Pydantic data models
    ├── spec_loader.py       # OpenAPI spec fetching and processing
    ├── spec_processor.py    # Operation and schema extraction
    ├── search.py            # Fuzzy search engine
    ├── cache.py             # TTL-based caching
    └── service.py           # Main orchestrating service
```

---

## Example Usage

For comprehensive examples of API exploration and integration, check out the included scripts:

- **`example.py`**: Demonstrates all available tools with real API data
- **`test_final.py`**: Validates functionality and shows expected results

These examples show the complete workflow from API discovery to detailed operation analysis.

---

## Architecture

- **`SpecLoader`**: Fetches and processes OpenAPI specifications with JSON reference resolution
- **`SpecProcessor`**: Extracts operations and schemas while filtering deprecated endpoints  
- **`SearchEngine`**: Provides fuzzy search capabilities with configurable matching thresholds
- **`OpenAPIService`**: Main service coordinating all components with intelligent caching
- **`SimpleCache`**: TTL-based caching for performance optimization
- **MCP Tools**: Seven specialized tools exposing functionality to AI assistants

## Comparison with TypeScript Version

This Python implementation provides similar functionality to the TypeScript `@reapi/mcp-openapi` but is:

- **Simpler**: Single API spec focus, no file system operations required
- **Focused**: Specifically designed for Facets Control Plane integration
- **Efficient**: Direct JSON processing with smart caching strategies
- **Lightweight**: Fewer dependencies and cleaner abstractions

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it under its terms.
