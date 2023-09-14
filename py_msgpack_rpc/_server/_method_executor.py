"""Implementation of MethodExecutor."""

import typing

from py_msgpack_rpc._messages import Request, Response


class MethodExecutor:
    """Class to execute methods."""

    def __init__(self) -> None:
        self._methods: typing.Dict[str, typing.Callable] = {}

    def add_method(self, method_name: str, method_function: typing.Callable) -> None:
        """Add a method.

        Args:
            method_name (str): Method name.
            method_function (typing.Callable): Function of the method.
        """
        self._methods[method_name] = method_function

    async def process_request(self, request: Request) -> Response:
        """Process a request.

        Args:
            request (Request): Request.

        Returns:
            Response: Response.
        """
        try:
            result = self._methods[request.method_name](*(request.parameters))
            return Response(
                message_id=request.message_id,
                error=None,
                result=result,
            )
        except Exception as exception:  # pylint: disable=broad-exception-caught
            return Response(
                message_id=request.message_id,
                error=exception.args,
                result=None,
            )
