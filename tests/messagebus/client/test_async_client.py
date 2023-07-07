import unittest

from rustic_ai.messagebus import AsyncClient, MessageBus


class TestAsyncClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.message_bus = MessageBus()
        self.client_1 = AsyncClient('client_1', self.message_bus)
        self.client_2 = AsyncClient('client_2', self.message_bus)
        self.client_3 = AsyncClient('client_3', self.message_bus)

    async def test_client_initialization(self):
        client = AsyncClient('client_4', self.message_bus)

        self.assertEqual(client.client_id, 'client_4')
        self.assertEqual(client.message_bus, self.message_bus)
        self.assertEqual(client.last_read_message_id, 0)

    async def test_send_and_get_message(self):
        sent = self.client_1.send_message({"message": "Hello"}, ['client_2'])

        received = await self.client_2.async_get_next_unread_message()

        self.assertEqual(sent, received)

    async def test_remove_sent_message(self):
        message1 = self.client_1.send_message({"message": "Hello"}, ['client_2', 'client_3'])
        message2 = self.client_1.send_message({"message": "Hello"}, ['client_2', 'client_3'])

        self.client_1.remove_sent_message(['client_2'], message1.id)

        receive1 = await self.client_2.async_get_next_unread_message()
        receive2 = await self.client_3.async_get_next_unread_message()

        self.assertEqual(message2, receive1)
        self.assertEqual(message1, receive2)

    async def test_send_message_to_non_existent_client(self):
        with self.assertRaises(Exception):  # Adjust this based on your implementation
            await self.client_1.send_message('{"message": "Hello"}', ['non_existent_client'])

    async def test_send_malformed_message(self):
        with self.assertRaises(Exception):  # Adjust this based on your implementation
            await self.client_1.send_message('{"message": "Hello",}', ['client_2'])  # malformed JSON


if __name__ == '__main__':
    unittest.main()
