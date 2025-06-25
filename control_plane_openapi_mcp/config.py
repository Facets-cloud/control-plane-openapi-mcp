import os
from mcp.server.fastmcp import FastMCP

# Configuration
OPENAPI_URL = os.getenv(
    'FACETS_OPENAPI_URL', 
    'https://facetsdemo.console.facets.cloud/v3/api-docs'
)
CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))  # 1 hour default
SPEC_ID = "facets-control-plane"

# Initialize MCP server
mcp = FastMCP("Facets Control Plane OpenAPI")
