import threading
import unittest

from rustic_ai.messagebus import CallbackClient, MessageBus


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


if __name__ == '__main__':
    unittest.main()
