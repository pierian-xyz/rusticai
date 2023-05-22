import unittest

from rustic_ai.messagebus import (
    BroadcastRoutingPolicy,
    DirectOrFallbackRoutingPolicy,
    HashBasedRoutingPolicy,
    Message,
    MessageBus,
    MessageProperties,
    Priority,
    SimpleClient,
)


class TestRoutingPolicy(unittest.TestCase):
    def setUp(self):
        self.message_bus = MessageBus(id="test_bus")
        self.clients = {
            "client1": SimpleClient("client1", self.message_bus),
            "client2": SimpleClient("client2", self.message_bus),
            "client3": SimpleClient("client3", self.message_bus),
        }

        self.message = Message(
            id=self.message_bus.generate_message_id(Priority.NORMAL),
            sender="client1",
            content='{"test": "test"}',
        )

        self.message2 = Message(
            id=self.message_bus.generate_message_id(Priority.NORMAL),
            sender="client1",
            content='{"test": "test"}',
            recipients=["client3"],
        )

    def _get_id(self, priority: Priority) -> int:
        return self.message_bus.generate_message_id(priority)

    def test_broadcast_routing_policy(self):
        # Check that all clients receive the message with BroadcastRoutingPolicy
        policy = BroadcastRoutingPolicy()
        recipients = policy.get_recipients(self.message, self.clients)
        self.assertEqual(len(recipients), len(self.clients) - 1)

    def test_direct_or_fallback_policy(self):
        # Check that the message is sent directly to the intended recipient or the fallback client
        fallback_client = "client3"
        policy = DirectOrFallbackRoutingPolicy(fallback_client)

        recipients = policy.get_recipients(self.message, self.clients)
        self.assertEqual(len(recipients), 1)
        self.assertEqual(recipients[0], fallback_client)

        recipients = policy.get_recipients(self.message2, self.clients)
        self.assertEqual(len(recipients), 1)
        self.assertEqual(recipients[0], self.message2.recipients[0])

    def test_hash_based_routing_policy(self):
        # Check that the message is routed to one of the clients based on the hash of its properties
        properties = [MessageProperties.CONTENT]
        policy = HashBasedRoutingPolicy(properties)

        recipients = policy.get_recipients(self.message, self.clients)
        self.assertEqual(len(recipients), 1)
        self.assertIn(recipients[0], self.clients.keys())


if __name__ == "__main__":
    unittest.main()
