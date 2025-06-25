#!/usr/bin/env python3
"""Test script for the MCP server."""

import subprocess
import json
import sys
import time

def test_mcp_tool(tool_name: str, args: dict = None):
    """Test an MCP tool by running the server and sending a request."""
    cmd = ["uv", "run", "control-plane-openapi-mcp"]
    
    # Create the MCP request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args or {}
        }
    }
    
    try:
        # Start the MCP server
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/Users/anujhydrabadi/work/repos/control-plane-openapi-mcp"
        )
        
        # Send the request
        request_json = json.dumps(request) + "\n"
        stdout, stderr = process.communicate(input=request_json, timeout=30)
        
        if stderr:
            print(f"STDERR: {stderr}")
        
        if stdout:
            print(f"STDOUT: {stdout}")
            # Try to parse the JSON response
            for line in stdout.strip().split('\n'):
                if line.strip():
                    try:
                        response = json.loads(line)
                        if response.get("id") == 1:
                            return response
                    except json.JSONDecodeError:
                        print(f"Could not parse line: {line}")
        
        return None
        
    except subprocess.TimeoutExpired:
        process.kill()
        print("Request timed out")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing refresh_api_catalog...")
    response = test_mcp_tool("refresh_api_catalog")
    if response:
        print("Response:", json.dumps(response, indent=2))
    else:
        print("No response received")
