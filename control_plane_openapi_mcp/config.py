import os
from mcp.server.fastmcp import FastMCP

# Configuration
CONTROL_PLANE_URL = os.getenv('CONTROL_PLANE_URL', 'https://facetsdemo.console.facets.cloud')
CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))  # 1 hour default
SPEC_ID = "facets-control-plane"

# Authentication configuration
FACETS_USERNAME = os.getenv('FACETS_USERNAME', '')
FACETS_TOKEN = os.getenv('FACETS_TOKEN', '')
FACETS_PROFILE = os.getenv('FACETS_PROFILE', 'default')

# Derived URLs
OPENAPI_URL = f"{CONTROL_PLANE_URL.rstrip('/')}/v3/api-docs"

# Initialize MCP server
mcp = FastMCP("Facets Control Plane OpenAPI")
