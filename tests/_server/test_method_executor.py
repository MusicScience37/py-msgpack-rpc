"""Test of MethodExecutor."""

import typing

import pytest

from py_msgpack_rpc._messages import Request, Response
from py_msgpack_rpc._server._method_executor import MethodExecutor


def echo_all(*args) -> typing.Iterable:
    """Return all arguments.

    Returns:
        typing.Iterable: Arguments.
    """
    return args


def raise_exception(*_) -> None:
    """Raise an exception.

    Raises:
        RuntimeError: Always.
    """
    raise RuntimeError("Test error.")


class TestMethodExecutor:
    """Test of MethodExecutor."""

    @pytest.mark.asyncio
    async def test_process_request(self) -> None:
        """Test to process a request."""
        executor = MethodExecutor()

        method_name = "echo"
        executor.add_method(
            method_name=method_name,
            method_function=echo_all,
        )

        message_id = 12345
        request = Request(
            message_id=message_id,
            method_name=method_name,
            parameters=["abc", 123],
        )

        response = await executor.process_request(request)

        assert isinstance(response, Response)
        assert response.message_id == message_id
        assert response.error is None
        assert list(response.result) == list(request.parameters)

    @pytest.mark.asyncio
    async def test_process_request_to_fail(self) -> None:
        """Test to process a request to fail with an exception."""
        executor = MethodExecutor()

        method_name = "error"
        executor.add_method(
            method_name=method_name,
            method_function=raise_exception,
        )

        message_id = 12345
        request = Request(
            message_id=message_id,
            method_name=method_name,
            parameters=["abc", 123],
        )

        response = await executor.process_request(request)

        assert isinstance(response, Response)
        assert response.message_id == message_id
        assert "Test error." in str(response.error)
        assert response.result is None
