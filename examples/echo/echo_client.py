"""Example of a client."""

import asyncio
import logging

from constants import HOST, PORT_NUMBER

import py_msgpack_rpc

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Main function."""
    builder = py_msgpack_rpc.AsyncClientBuilder()
    builder.connect_tcp(host=HOST, port=PORT_NUMBER)
    client = await builder.build()
    async with client:
        result = await client.call("echo", "abc")
        LOGGER.info("Result: %s", result)


if __name__ == "__main__":
    asyncio.run(main())
