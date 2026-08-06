import asyncio
import os
import sys
import tempfile
import unittest

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class ServerStartupTest(unittest.IsolatedAsyncioTestCase):
    async def test_server_completes_initialize_handshake(self):
        with tempfile.TemporaryDirectory() as temporary_home:
            environment = os.environ.copy()
            environment.update(
                {
                    "CONTROL_PLANE_URL": "https://example.invalid",
                    "FACETS_PROFILE": "startup-test",
                    "FACETS_USERNAME": "",
                    "FACETS_TOKEN": "",
                    "HOME": temporary_home,
                    "USERPROFILE": temporary_home,
                }
            )
            parameters = StdioServerParameters(
                command=sys.executable,
                args=["-m", "control_plane_openapi_mcp.server"],
                env=environment,
            )

            async def initialize_server():
                async with stdio_client(parameters) as (read_stream, write_stream):
                    async with ClientSession(read_stream, write_stream) as session:
                        result = await session.initialize()
                        tools = await session.list_tools()
                        return result, tools

            result, tools = await asyncio.wait_for(initialize_server(), timeout=15)

        self.assertEqual(result.serverInfo.name, "Facets Control Plane OpenAPI")
        self.assertGreater(len(tools.tools), 0)


if __name__ == "__main__":
    unittest.main()
