"""Test of messages."""

from py_msgpack_rpc._messages import MessageType, Request, Response, parse_message


class TestParseMessage:
    """Tests of parse_message function."""

    def test_parse_request(self) -> None:
        """Test to parse a request."""
        message_type = MessageType.REQUEST.value
        message_id = 12345
        method_name = "test"
        parameters = ["abc", 123]
        data = [message_type, message_id, method_name, parameters]

        message = parse_message(data)

        assert isinstance(message, Request)
        assert message.message_id == message_id
        assert message.method_name == method_name
        assert message.parameters == parameters

    def test_parse_response_without_error(self) -> None:
        """Test to parse a response without an error."""
        message_type = MessageType.RESPONSE.value
        message_id = 12345
        error = None
        result = "abc"
        data = [message_type, message_id, error, result]

        message = parse_message(data)

        assert isinstance(message, Response)
        assert message.message_id == message_id
        assert message.error == error
        assert message.result == result

    def test_parse_response_with_error(self) -> None:
        """Test to parse a response with an error."""
        message_type = MessageType.RESPONSE.value
        message_id = 12345
        error = "Test message."
        result = None
        data = [message_type, message_id, error, result]

        message = parse_message(data)

        assert isinstance(message, Response)
        assert message.message_id == message_id
        assert message.error == error
        assert message.result == result
