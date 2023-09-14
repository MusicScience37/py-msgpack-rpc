"""Scratch of implementation of a client."""

import asyncio
import logging

import msgpack
from constants import HOST, PORT_NUMBER

LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


class ClientProtocol(asyncio.Protocol):
    def __init__(self) -> None:
        self.sent_messages = asyncio.Queue()
        self.received_messages = asyncio.Queue()
        self._unpacker = msgpack.Unpacker()
        self._writer = None

    def connection_made(self, transport: asyncio.Transport) -> None:
        self._writer = asyncio.get_running_loop().create_task(
            self._write_data(transport)
        )

    def data_received(self, data: bytes) -> None:
        self._unpacker.feed(data)
        for message in self._unpacker:
            self.received_messages.put_nowait(message)

    def connection_lost(self, exc: Exception | None) -> None:
        if self._writer is not None:
            self._writer.cancel()

    async def _write_data(self, transport: asyncio.Transport) -> None:
        while True:
            message = await self.sent_messages.get()
            transport.write(message)


async def main() -> None:
    loop = asyncio.get_running_loop()

    while True:
        try:
            transport, protocol = await loop.create_connection(
                lambda: ClientProtocol(), host=HOST, port=PORT_NUMBER
            )
            break
        except:
            pass
    msgid = 12345
    data = "abc"
    protocol.sent_messages.put_nowait(msgpack.packb([0, msgid, "echo", [data]]))

    received_message = await protocol.received_messages.get()
    LOGGER.info("received %s", received_message)

    transport.close()


if __name__ == "__main__":
    asyncio.run(main())
