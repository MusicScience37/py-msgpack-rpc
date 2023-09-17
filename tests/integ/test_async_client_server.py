"""Test of communication of asynchronous clients and servers."""

import typing

import pytest

from py_msgpack_rpc import AsyncClientBuilder, AsyncServerBuilder


def echo(*args: typing.Any) -> typing.Iterable[typing.Any]:
    """Return arguments.

    Returns:
        typing.Iterable[typing.Any]: Arguments.
    """
    return args


@pytest.mark.asyncio
async def test_async_client_server() -> None:
    """Test of communication of asynchronous clients and servers."""
    server_builder = AsyncServerBuilder()
    server_builder.add_method("echo", echo)
    server_builder.listen_tcp(host="localhost", port=0)
    server = await server_builder.build()
    async with server:
        server_endpoints = server.local_endpoints()
        server_host, server_port = server_endpoints[0]

        client_builder = AsyncClientBuilder()
        client_builder.connect_tcp(host=server_host, port=server_port)
        client = await client_builder.build()
        async with client:
            result = await client.call("echo", "abc")
            assert list(result) == ["abc"]
