#!/usr/bin/env python3
"""
Example usage of the Control Plane OpenAPI MCP tools including API calling.
This script demonstrates how to use the tools directly (outside of MCP context).
"""

import json
import os
from control_plane_openapi_mcp.tools import (
    refresh_api_catalog,
    search_api_operations,
    search_api_schemas,
    load_api_operation_by_operationId,
    load_api_operation_by_path_and_method,
    load_api_schema_by_schemaName,
    call_control_plane_api
)


def main():
    print("🚀 Control Plane OpenAPI MCP Example (Updated)")
    print("=" * 55)
    
    # Check if credentials are available
    has_credentials = all([
        os.getenv('CONTROL_PLANE_URL'),
        os.getenv('FACETS_USERNAME'),
        os.getenv('FACETS_TOKEN')
    ])
    
    if not has_credentials:
        print("⚠️  Note: API calling functionality requires credentials")
        print("   Set CONTROL_PLANE_URL, FACETS_USERNAME, FACETS_TOKEN")
        print("   or configure ~/.facets/credentials file")
        print()
    
    # 1. Refresh the catalog
    print("1. Refreshing API catalog...")
    refresh_result = refresh_api_catalog()
    print(f"   Result: {json.loads(refresh_result)['message']}")
    
    # 2. Search for stack operations
    print("\n2. Searching for 'stack' operations...")
    stack_ops = json.loads(search_api_operations("stack"))['operations']
    print(f"   🔍 Found {len(stack_ops)} stack-related operations")
    for i, op in enumerate(stack_ops[:3]):
        print(f"   {i+1}. {op['method']} {op['path']}")
    
    # 3. Get specific operation details
    print("\n3. Loading details for 'getStack' operation...")
    stack_detail = json.loads(load_api_operation_by_operationId("getStack"))
    if stack_detail:
        op_info = stack_detail['operation']
        print(f"   📋 Operation: {stack_detail['method']} {stack_detail['path']}")
        print(f"   📝 Description: {op_info.get('description', 'N/A')}")
        print(f"   🏷️  Tags: {', '.join(op_info.get('tags', []))}")
    
    # 4. Search schemas
    print("\n4. Searching for 'Stack' schemas...")
    stack_schemas = json.loads(search_api_schemas("Stack"))['schemas']
    print(f"   📦 Found {len(stack_schemas)} Stack-related schemas")
    for schema in stack_schemas[:3]:
        print(f"   - {schema['name']}")
    
    # 5. Get schema details
    print("\n5. Loading 'Stack' schema details...")
    stack_schema = json.loads(load_api_schema_by_schemaName("Stack"))
    if stack_schema:
        schema_data = stack_schema['schema_data']
        print(f"   📚 Schema: {stack_schema['name']}")
        print(f"   🏗️  Type: {schema_data.get('type', 'N/A')}")
        print(f"   🔧 Properties: {len(schema_data.get('properties', []))} fields")
        print(f"   ✅ Required: {len(schema_data.get('required', []))} fields")
    
    # 6. Load operation by path and method
    print("\n6. Loading operation by path and method...")
    deployment_op = json.loads(load_api_operation_by_path_and_method(
        "/cc-ui/v1/stacks/{stackName}", "GET"
    ))
    if deployment_op:
        print(f"   🛠️  Operation: {deployment_op['operation']['operationId']}")
        print(f"   📍 URI: {deployment_op['uri']}")
    
    # 7. Test API calling (if credentials available)
    if has_credentials:
        print("\n7. Testing API calling functionality...")
        try:
            # Try to get stacks list
            api_result = call_control_plane_api("/cc-ui/v1/stacks/")
            api_response = json.loads(api_result)
            
            if api_response.get("success"):
                data = api_response.get("data", [])
                if isinstance(data, list):
                    print(f"   🎯 API Call Success: Found {len(data)} stacks")
                else:
                    print(f"   🎯 API Call Success: Response received")
            else:
                print(f"   ⚠️  API Call Failed: {api_response.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ API Call Error: {e}")
    else:
        print("\n7. Skipping API calling test (credentials not available)")
    
    print("\n✅ Example completed successfully!")
    if has_credentials:
        print("💡 Pro tip: Use these tools in your LLM prompts to get real API data!")
    else:
        print("💡 Pro tip: Add credentials to test the live API calling functionality!")


if __name__ == "__main__":
    main()
