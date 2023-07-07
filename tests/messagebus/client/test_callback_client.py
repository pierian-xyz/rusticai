import threading
import unittest

from rustic_ai.messagebus import CallbackClient, Message, MessageBus, Priority, SimpleClient


class TestCallbackClient(unittest.TestCase):
    def setUp(self):
        self.message_bus = MessageBus()
        self.received_messages1 = []
        self.received_messages2 = []
        self.message_received_event = threading.Event()
        self.client_1 = CallbackClient('client_1', self.message_bus, self.callback1)
        self.client_2 = CallbackClient('client_2', self.message_bus, self.callback2)

    def callback1(self, message):
        self.received_messages1.append(message)
        self.message_received_event.set()

    def callback2(self, message):
        self.received_messages2.append(message)
        self.message_received_event.set()

    def test_send_and_receive_message(self):
        message = self.client_1.send_message({"message": "Hello"}, ['client_2'])
        received_message = self.received_messages2[-1]
        self.assertEqual(message, received_message)

    # Tests that the client can receive a message and trigger the callback function
    def test_receive_message(self):
        received_messages = []

        def callback(message):
            received_messages.append(message)

        message_bus = MessageBus()
        client = CallbackClient('client1', message_bus, callback)  # noqa: F841
        message = Message(1, 'sender', {'key': 'value'}, ['client1'])
        message_bus.send_message(message)
        assert len(received_messages) == 1
        assert received_messages[0] == message

    # Tests that the client can receive multiple messages and trigger the callback function for each
    def test_receive_multiple_messages(self):
        received_messages = []

        def callback(message):
            received_messages.append(message)

        message_bus = MessageBus()
        client = CallbackClient('client1', message_bus, callback)  # noqa: F841
        message1 = Message(1, 'sender', {'key': 'value'}, ['client1'])
        message2 = Message(2, 'sender', {'key': 'value'}, ['client1'])
        message_bus.send_message(message1)
        message_bus.send_message(message2)
        assert len(received_messages) == 2
        assert received_messages[0] == message1
        assert received_messages[1] == message2

    # Tests that the client can handle an empty message
    def test_empty_message(self):
        received_messages = []

        def callback(message):
            received_messages.append(message)

        message_bus = MessageBus()
        client = CallbackClient('client1', message_bus, callback)  # noqa: F841
        message = Message(1, 'sender', None, ['client1'])
        message_bus.send_message(message)
        assert len(received_messages) == 1
        assert received_messages[0] == message

    # Tests that the client can handle a message with no content
    def test_message_with_no_content(self):
        received_messages = []

        def callback(message):
            received_messages.append(message)

        message_bus = MessageBus()
        client = CallbackClient('client1', message_bus, callback)  # noqa: F841
        message = Message(1, 'sender', None, ['client1'])
        message.set_content(None)
        message_bus.send_message(message)
        assert len(received_messages) == 1
        assert received_messages[0] == message

    # Tests that the client can handle a message with invalid recipients
    def test_message_with_invalid_recipients(self):
        received_messages = []

        def callback(message):
            received_messages.append(message)

        message_bus = MessageBus()
        message = Message(1, 'sender', {'key': 'value'}, ['invalid_client'])
        with self.assertRaises(ValueError):
            message_bus.send_message(message)

    # Tests that the client can handle a message with a high priority
    def test_message_with_high_priority(self):
        received_messages = []

        def callback(message):
            received_messages.append(message)

        message_bus = MessageBus()
        client = CallbackClient('client1', message_bus, callback)  # noqa: F841
        message2 = Message(2, 'sender', {'key': 'value'}, ['client1'], priority=Priority.LOW)
        message1 = Message(1, 'sender', {'key': 'value'}, ['client1'], priority=Priority.HIGH)
        message_bus.send_message(message1)
        message_bus.send_message(message2)
        assert len(received_messages) == 2
        assert received_messages[0] == message1
        assert received_messages[1] == message2

    # Test explicit message handling with process_all_unread_messages
    def test_process_all_messages(self):
        received_messages = []

        def callback(message):
            received_messages.append(message)

        message_bus = MessageBus()
        # We will register a simple client so we are able to send messages
        # but they don't get handled by the callback handler.
        dummyClient = SimpleClient('client1', message_bus)  # noqa: F841
        message1 = Message(1, 'sender', {'key': 'value'}, ['client1'])
        message2 = Message(2, 'sender', {'key': 'value'}, ['client1'])
        message_bus.send_message(message1)
        message_bus.send_message(message2)

        # Now we create a CallBack client and process all unread messages.
        # This is useful when the client reconnects and may have missed notifications
        # for messages that were sent while it was disconnected.
        client = CallbackClient('client1', message_bus, callback)
        client.process_all_unread_messages()

        assert len(received_messages) == 2
        assert received_messages[0] == message1
        assert received_messages[1] == message2

    # Test error is raised when callback is not callable function
    def test_callback_not_callable(self):
        message_bus = MessageBus()
        with self.assertRaises(TypeError):
            client = CallbackClient('client1', message_bus, 'not_callable')  # noqa: F841

    # Test error is raised when callback raises an exception
    def test_callback_with_exception(self):
        received_messages = []

        def callbackWithErrors(self, message):
            raise Exception('Error in callback')

        message_bus = MessageBus()
        client = CallbackClient('client1', message_bus, callbackWithErrors)  # noqa: F841
        message1 = Message(1, 'sender', {'key': 'value'}, ['client1'])
        message2 = Message(2, 'sender', {'key': 'value'}, ['client1'])
        message_bus.send_message(message1)
        message_bus.send_message(message2)
        assert len(received_messages) == 0


if __name__ == '__main__':
    unittest.main()
