import unittest

from rustic_ai.messagebus import MessageBus
from rustic_ai.messagebus.client import SimpleClient


class TestSimpleClient(unittest.TestCase):
    def setUp(self):
        self.message_bus = MessageBus()
        self.client_1 = SimpleClient('client_1', self.message_bus)
        self.client_2 = SimpleClient('client_2', self.message_bus)

    def test_client_initialization(self):
        client = SimpleClient('client_3', self.message_bus)

        self.assertEqual(client.client_id, 'client_3')
        self.assertEqual(client.message_bus, self.message_bus)
        self.assertEqual(client.last_read_message_id, 0)

    def test_send_message(self):
        self.client_1.send_message({"message": "Hello"}, ['client_2'])

        self.assertEqual(len(self.message_bus.storage.inboxes['client_2']), 1)
        self.assertEqual(self.message_bus.storage.inboxes['client_2'][0].content, {'message': 'Hello'})

    def test_get_next_unread_message(self):
        self.client_1.send_message({"message": "Hello"}, ['client_2'])

        message = self.client_2.get_next_unread_message()
        self.assertEqual(message.content['message'], "Hello")
        self.assertEqual(self.client_2.last_read_message_id, message.id)

    def test_remove_sent_message(self):
        message = self.client_1.send_message({"message": "Hello"}, ['client_2'])
        self.client_1.remove_sent_message(["client_2"], message.id)

        self.assertListEqual(self.message_bus.storage.inboxes['client_2'], [])

    def test_send_message_to_non_existent_client(self):
        with self.assertRaises(Exception):  # Adjust this based on your implementation
            self.client_1.send_message({"message": "Hello"}, ['non_existent_client'])

    def test_send_malformed_message(self):
        with self.assertRaises(Exception):  # Adjust this based on your implementation
            self.client_1.send_message('{"message": "Hello",}', ['client_2'])  # malformed JSON


if __name__ == '__main__':
    unittest.main()
