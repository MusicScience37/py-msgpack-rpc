"""Scratch of implementation of a server."""

import asyncio
import logging

import msgpack

from constants import HOST, PORT_NUMBER

LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


class ServerConnectionProtocol(asyncio.Protocol):
    def __init__(self) -> None:
        LOGGER.debug("ServerConnectionProtocol.__init__")

        self._unpacker = msgpack.Unpacker()

        self._sent_messages = asyncio.Queue()
        self._writer = None

    def connection_made(self, transport: asyncio.Transport) -> None:
        self._writer = asyncio.get_running_loop().create_task(
            self._write_data(transport)
        )

    def connection_lost(self, exc: Exception | None) -> None:
        if self._writer is not None:
            self._writer.cancel()

    def data_received(self, data: bytes) -> None:
        self._unpacker.feed(data)
        for message in self._unpacker:
            LOGGER.info("received %s", message)
            msgid = message[1]
            args = message[3]
            self._sent_messages.put_nowait(msgpack.packb([1, msgid, None, args]))

    async def _write_data(self, transport: asyncio.Transport) -> None:
        while True:
            message = await self._sent_messages.get()
            transport.write(message)


async def main() -> None:
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: ServerConnectionProtocol(), host=HOST, port=PORT_NUMBER
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
