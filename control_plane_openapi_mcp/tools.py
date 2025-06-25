import json
import logging
from typing import Optional

from .config import mcp, OPENAPI_URL, CACHE_TTL, SPEC_ID
from .core.service import OpenAPIService
from .utils.client import api_client

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the OpenAPI service
openapi_service = OpenAPIService(OPENAPI_URL, SPEC_ID, CACHE_TTL)

# Initialize API client (optional - only for call_control_plane_api tool)
api_client_available = False
try:
    api_client.initialize()
    api_client_available = True
    logger.info("API client initialized successfully")
except Exception as e:
    logger.debug(f"API client initialization failed: {e}")
    logger.info("API client not available - only OpenAPI exploration tools will work")


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
    
    Note: Deprecated operations are automatically excluded from the catalog.
    
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
    
    Note: Only searches through active (non-deprecated) operations.
    
    Args:
        query (str): Search query to match against operation summaries, descriptions, tags, and operation IDs.
    
    Returns:
        str: JSON string containing matching operations with their details.
    """
    try:
        operations = openapi_service.search_operations(query)
        # Simplified serialization to avoid JsonRef issues
        serialized_operations = []
        for op in operations:
            serialized_operations.append({
                "path": op.path,
                "method": op.method,
                "spec_id": op.spec_id,
                "uri": op.uri,
                "operation_summary": op.operation.get('summary', ''),
                "operation_description": op.operation.get('description', ''),
                "operation_id": op.operation.get('operationId', ''),
                "tags": op.operation.get('tags', [])
            })
        
        return json.dumps({
            "operations": serialized_operations
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
            # Create a safe serializable version
            safe_operation = {
                "path": operation.path,
                "method": operation.method,
                "spec_id": operation.spec_id,
                "uri": operation.uri,
                "operation": {
                    "operationId": operation.operation.get('operationId', ''),
                    "summary": operation.operation.get('summary', ''),
                    "description": operation.operation.get('description', ''),
                    "tags": operation.operation.get('tags', []),
                    "parameters": operation.operation.get('parameters', []),
                    "responses": {k: {"description": v.get('description', '')} if isinstance(v, dict) else str(v) 
                                for k, v in operation.operation.get('responses', {}).items()},
                    "requestBody": {"description": operation.operation.get('requestBody', {}).get('description', '')} 
                                  if operation.operation.get('requestBody') else None
                }
            }
            return json.dumps(safe_operation, indent=2)
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
            # Create a safe serializable version
            safe_operation = {
                "path": operation.path,
                "method": operation.method,
                "spec_id": operation.spec_id,
                "uri": operation.uri,
                "operation": {
                    "operationId": operation.operation.get('operationId', ''),
                    "summary": operation.operation.get('summary', ''),
                    "description": operation.operation.get('description', ''),
                    "tags": operation.operation.get('tags', []),
                    "parameters": operation.operation.get('parameters', []),
                    "responses": {k: {"description": v.get('description', '')} if isinstance(v, dict) else str(v) 
                                for k, v in operation.operation.get('responses', {}).items()},
                    "requestBody": {"description": operation.operation.get('requestBody', {}).get('description', '')} 
                                  if operation.operation.get('requestBody') else None
                }
            }
            return json.dumps(safe_operation, indent=2)
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
            # Create a safe serializable version
            safe_schema = {
                "name": schema.name,
                "description": schema.description,
                "uri": schema.uri,
                "schema_data": {
                    "type": schema.schema_data.get('type', ''),
                    "description": schema.schema_data.get('description', ''),
                    "properties": list(schema.schema_data.get('properties', {}).keys()) if schema.schema_data.get('properties') else [],
                    "required": schema.schema_data.get('required', [])
                }
            }
            return json.dumps(safe_schema, indent=2)
        else:
            return json.dumps(None)
    except Exception as e:
        logger.error(f"Failed to load schema by name: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def call_control_plane_api(path: str) -> str:
    """
    Make a GET request to the Facets Control Plane API.
    
    Args:
        path (str): API path to call (e.g., '/cc-ui/v1/stacks/my-stack' or 'cc-ui/v1/stacks')
    
    Returns:
        str: JSON string containing the API response or error information.
    """
    try:
        if not api_client_available:
            return json.dumps({
                "success": False,
                "error": "API client not initialized. Authentication credentials are required for this tool.",
                "help": "Set CONTROL_PLANE_URL, FACETS_USERNAME, FACETS_TOKEN environment variables or configure ~/.facets/credentials"
            })
        
        # Make the API call
        response = api_client.get(path)
        
        # Handle response
        if response.status_code == 200:
            try:
                response_data = response.json()
                return json.dumps({
                    "success": True,
                    "status_code": response.status_code,
                    "data": response_data
                }, indent=2)
            except ValueError:
                # Response is not JSON
                return json.dumps({
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.text
                }, indent=2)
        else:
            # Handle error responses
            try:
                error_data = response.json()
            except ValueError:
                error_data = response.text
            
            return json.dumps({
                "success": False,
                "status_code": response.status_code,
                "error": error_data,
                "path": path
            }, indent=2)
            
    except Exception as e:
        logger.error(f"Failed to call Control Plane API: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "path": path
        })
