"""Example of a server."""

import asyncio
import logging
import typing

from constants import HOST, PORT_NUMBER

import py_msgpack_rpc

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


def echo(*args: typing.Any) -> typing.Iterable[typing.Any]:
    """Return arguments.

    Returns:
        typing.Iterable[typing.Any]: Arguments.
    """
    return args


async def main() -> None:
    """Main function."""
    builder = py_msgpack_rpc.AsyncServerBuilder()
    builder.add_method("echo", echo)
    builder.listen_tcp(host=HOST, port=PORT_NUMBER)
    server = await builder.build()
    LOGGER.info("Listen %s", server.local_endpoints())
    async with server:
        await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("Stopped the server.")
