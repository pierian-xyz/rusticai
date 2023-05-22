import unittest

from rustic_ai.messagebus import AsyncClient, MessageBus


class TestAsyncClient(unittest.IsolatedAsyncioTestCase):
    async def setUp(self):
        self.message_bus = MessageBus()
        self.client_1 = AsyncClient('client_1', self.message_bus)
        self.client_2 = AsyncClient('client_2', self.message_bus)

    async def test_client_initialization(self):
        client = AsyncClient('client_3', self.message_bus)

        self.assertEqual(client.client_id, 'client_3')
        self.assertEqual(client.message_bus, self.message_bus)
        self.assertIsNone(client.last_read_message_id)

    async def test_send_message(self):
        await self.client_1.send_message('{"message": "Hello"}', ['client_2'])

        self.assertEqual(len(self.message_bus.storage.inboxes['client_2']), 1)
        self.assertEqual(self.message_bus.storage.inboxes['client_2'][0].content, 'Hello')

    async def test_get_next_unread_message(self):
        await self.client_1.send_message('{"message": "Hello"}', ['client_2'])

        message = await self.client_2.get_next_unread_message()
        self.assertEqual(message.content['message'], 'Hello')
        self.assertEqual(self.client_2.last_read_message_id, message.id)

    async def test_remove_sent_message(self):
        await self.client_1.send_message('{"message": "Hello"}', ['client_2'])

        message = await self.client_2.get_next_unread_message()
        await self.client_2.remove_sent_message(message.id)

        self.assertEqual(len(self.message_bus.storage.inboxes['client_2']), 0)

    async def test_send_message_to_non_existent_client(self):
        with self.assertRaises(Exception):  # Adjust this based on your implementation
            await self.client_1.send_message('{"message": "Hello"}', ['non_existent_client'])

    async def test_send_malformed_message(self):
        with self.assertRaises(Exception):  # Adjust this based on your implementation
            await self.client_1.send_message('{"message": "Hello",}', ['client_2'])  # malformed JSON


if __name__ == '__main__':
    unittest.main()
