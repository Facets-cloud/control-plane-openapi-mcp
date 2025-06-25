#!/usr/bin/env python3
"""
Example usage of the Control Plane OpenAPI MCP tools.
This script demonstrates how to use the tools directly (outside of MCP context).
"""

import json
from control_plane_openapi_mcp.tools import (
    refresh_api_catalog,
    get_api_catalog, 
    search_api_operations,
    search_api_schemas,
    load_api_operation_by_operationId,
    load_api_operation_by_path_and_method,
    load_api_schema_by_schemaName
)


def main():
    print("🚀 Control Plane OpenAPI MCP Example")
    print("=" * 50)
    
    # 1. Refresh the catalog
    print("\n1. Refreshing API catalog...")
    refresh_result = refresh_api_catalog()
    print(f"   Result: {json.loads(refresh_result)['message']}")
    
    # 2. Get catalog overview
    print("\n2. Getting API catalog overview...")
    catalog_result = get_api_catalog()
    catalog = json.loads(catalog_result)['catalog']
    print(f"   📊 Found {len(catalog['operations'])} operations")
    print(f"   📄 Found {len(catalog['schemas'])} schemas")
    
    # 3. Search for stack operations
    print("\n3. Searching for 'stack' operations...")
    stack_ops = json.loads(search_api_operations("stack"))['operations']
    print(f"   🔍 Found {len(stack_ops)} stack-related operations")
    for i, op in enumerate(stack_ops[:3]):
        print(f"   {i+1}. {op['method']} {op['path']}")
    
    # 4. Get specific operation details
    print("\n4. Loading details for 'getStack' operation...")
    stack_detail = json.loads(load_api_operation_by_operationId("getStack"))
    if stack_detail:
        op_info = stack_detail['operation']
        print(f"   📋 Operation: {stack_detail['method']} {stack_detail['path']}")
        print(f"   📝 Description: {op_info.get('description', 'N/A')}")
        print(f"   🏷️  Tags: {', '.join(op_info.get('tags', []))}")
    
    # 5. Search schemas
    print("\n5. Searching for 'Stack' schemas...")
    stack_schemas = json.loads(search_api_schemas("Stack"))['schemas']
    print(f"   📦 Found {len(stack_schemas)} Stack-related schemas")
    for schema in stack_schemas[:3]:
        print(f"   - {schema['name']}")
    
    # 6. Get schema details
    print("\n6. Loading 'Stack' schema details...")
    stack_schema = json.loads(load_api_schema_by_schemaName("Stack"))
    if stack_schema:
        schema_data = stack_schema['schema_data']
        print(f"   📚 Schema: {stack_schema['name']}")
        print(f"   🏗️  Type: {schema_data.get('type', 'N/A')}")
        print(f"   🔧 Properties: {len(schema_data.get('properties', []))} fields")
        print(f"   ✅ Required: {len(schema_data.get('required', []))} fields")
    
    # 7. Load operation by path and method
    print("\n7. Loading operation by path and method...")
    deployment_op = json.loads(load_api_operation_by_path_and_method(
        "/cc-ui/v1/stacks/{stackName}", "GET"
    ))
    if deployment_op:
        print(f"   🛠️  Operation: {deployment_op['operation']['operationId']}")
        print(f"   📍 URI: {deployment_op['uri']}")
    
    print("\n✅ Example completed successfully!")
    print("\n💡 Pro tip: Use these tools in your LLM prompts to get API information!")


if __name__ == "__main__":
    main()
