import json
import logging
from typing import Optional

from .config import mcp, OPENAPI_URL, CACHE_TTL, SPEC_ID
from .core.service import OpenAPIService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the OpenAPI service
openapi_service = OpenAPIService(OPENAPI_URL, SPEC_ID, CACHE_TTL)


@mcp.tool()
def refresh_api_catalog() -> str:
    """
    Refresh the API catalog by fetching the latest OpenAPI specification.
    
    Returns:
        str: Success message confirming the catalog has been refreshed.
    """
    try:
        openapi_service.refresh()
        return json.dumps({
            "success": True,
            "message": "API catalog refreshed successfully"
        })
    except Exception as e:
        logger.error(f"Failed to refresh API catalog: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_api_catalog() -> str:
    """
    Get the complete API catalog containing metadata about all OpenAPI operations and schemas.
    
    Returns:
        str: JSON string containing the complete API catalog with operations and schemas.
    """
    try:
        catalog = openapi_service.get_api_catalog()
        return json.dumps({
            "catalog": catalog.model_dump()
        }, indent=2)
    except Exception as e:
        logger.error(f"Failed to get API catalog: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def search_api_operations(query: str) -> str:
    """
    Search for operations across the OpenAPI specification using fuzzy matching.
    
    Args:
        query (str): Search query to match against operation summaries, descriptions, tags, and operation IDs.
    
    Returns:
        str: JSON string containing matching operations with their details.
    """
    try:
        operations = openapi_service.search_operations(query)
        return json.dumps({
            "operations": [op.model_dump() for op in operations]
        }, indent=2)
    except Exception as e:
        logger.error(f"Failed to search API operations: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def search_api_schemas(query: str) -> str:
    """
    Search for schemas across the OpenAPI specification using fuzzy matching.
    
    Args:
        query (str): Search query to match against schema names and descriptions.
    
    Returns:
        str: JSON string containing matching schemas with their details.
    """
    try:
        schemas = openapi_service.search_schemas(query)
        return json.dumps({
            "schemas": [schema.model_dump() for schema in schemas]
        }, indent=2)
    except Exception as e:
        logger.error(f"Failed to search API schemas: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def load_api_operation_by_operationId(operation_id: str) -> str:
    """
    Load a specific operation by its operationId.
    
    Args:
        operation_id (str): The unique operation ID to load.
    
    Returns:
        str: JSON string containing the complete operation details or null if not found.
    """
    try:
        operation = openapi_service.find_operation_by_id(operation_id)
        if operation:
            return json.dumps(operation.model_dump(), indent=2)
        else:
            return json.dumps(None)
    except Exception as e:
        logger.error(f"Failed to load operation by ID: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def load_api_operation_by_path_and_method(path: str, method: str) -> str:
    """
    Load a specific operation by its path and HTTP method.
    
    Args:
        path (str): The API endpoint path (e.g., '/cc-ui/v1/stacks/{stackName}').
        method (str): The HTTP method (GET, POST, PUT, DELETE, etc.).
    
    Returns:
        str: JSON string containing the complete operation details or null if not found.
    """
    try:
        operation = openapi_service.find_operation_by_path_and_method(path, method)
        if operation:
            return json.dumps(operation.model_dump(), indent=2)
        else:
            return json.dumps(None)
    except Exception as e:
        logger.error(f"Failed to load operation by path and method: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def load_api_schema_by_schemaName(schema_name: str) -> str:
    """
    Load a specific schema by its name.
    
    Args:
        schema_name (str): The name of the schema to load (e.g., 'Stack', 'ErrorDetails').
    
    Returns:
        str: JSON string containing the complete schema details or null if not found.
    """
    try:
        schema = openapi_service.find_schema_by_name(schema_name)
        if schema:
            return json.dumps(schema.model_dump(), indent=2)
        else:
            return json.dumps(None)
    except Exception as e:
        logger.error(f"Failed to load schema by name: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        })
