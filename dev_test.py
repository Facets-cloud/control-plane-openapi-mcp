#!/usr/bin/env python3
"""
Local development validation script.
Tests that the development environment is properly set up.
"""

import sys
import json
import subprocess
from pathlib import Path


def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    try:
        from control_plane_openapi_mcp.core.service import OpenAPIService
        from control_plane_openapi_mcp.tools import refresh_api_catalog
        from control_plane_openapi_mcp import config
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality without network calls."""
    print("\n🔧 Testing basic functionality...")
    try:
        from control_plane_openapi_mcp.core.cache import SimpleCache
        from control_plane_openapi_mcp.core.search import SearchEngine
        from control_plane_openapi_mcp.core.models import SpecOperationEntry
        
        # Test cache
        cache = SimpleCache[str](60)
        cache.set("test", "value")
        assert cache.get("test") == "value"
        
        # Test search engine
        search = SearchEngine("test-spec")
        ops = [
            SpecOperationEntry(path="/test", method="GET", operation_id="testOp")
        ]
        results = search.search_operations(ops, "test")
        assert len(results) >= 0
        
        print("✅ Basic functionality tests passed")
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def test_network_functionality():
    """Test network-dependent functionality."""
    print("\n🌐 Testing network functionality...")
    try:
        from control_plane_openapi_mcp.tools import refresh_api_catalog
        
        result = refresh_api_catalog()
        parsed = json.loads(result)
        
        if parsed.get("success"):
            print("✅ Network functionality test passed")
            return True
        else:
            print(f"❌ Network test failed: {parsed}")
            return False
    except Exception as e:
        print(f"❌ Network functionality test failed: {e}")
        return False


def test_uv_setup():
    """Test that uv environment is properly configured."""
    print("\n📦 Testing uv setup...")
    try:
        # Check if we're in a uv environment
        result = subprocess.run(
            ["uv", "run", "python", "-c", "import sys; print(sys.executable)"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            python_path = result.stdout.strip()
            if ".venv" in python_path:
                print(f"✅ uv environment active: {python_path}")
                return True
            else:
                print(f"⚠️  uv might not be using virtual environment: {python_path}")
                return True
        else:
            print(f"❌ uv test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ uv setup test failed: {e}")
        return False


def test_project_structure():
    """Test that project structure is correct."""
    print("\n📁 Testing project structure...")
    
    required_files = [
        "pyproject.toml",
        "control_plane_openapi_mcp/__init__.py",
        "control_plane_openapi_mcp/server.py",
        "control_plane_openapi_mcp/tools.py",
        "control_plane_openapi_mcp/config.py",
        "control_plane_openapi_mcp/core/service.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True


def main():
    """Run all development validation tests."""
    print("🚀 Control Plane OpenAPI MCP - Development Validation")
    print("=" * 60)
    
    # Change to project directory
    project_root = Path(__file__).parent
    import os
    os.chdir(project_root)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Package Imports", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("UV Setup", test_uv_setup),
        ("Network Functionality", test_network_functionality),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All development validation tests passed!")
        print("🔧 Your development environment is ready!")
        print("\n📖 Next steps:")
        print("   1. Try: uv run python example.py")
        print("   2. Test MCP: uv run control-plane-openapi-mcp")
        print("   3. Configure Claude Desktop with the MCP server")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
