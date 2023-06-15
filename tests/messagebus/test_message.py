import unittest

from rustic_ai.messagebus import Message
from rustic_ai.messagebus.utils import GemstoneGenerator, Priority


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.id_generator = GemstoneGenerator(1)

    def _get_id(self, priority: Priority) -> int:
        return self.id_generator.get_id(priority).to_int()

    def test_message_creation(self):
        message = Message(self._get_id(Priority.NORMAL), "test_sender", {"content": "Hello!"})
        self.assertEqual(message.sender, "test_sender")
        self.assertEqual(message.content, {"content": "Hello!"})

    def test_message_serialization(self):
        message = Message(self._get_id(Priority.NORMAL), "test_sender", {"content": "Hello!"})
        serialized = message.serialize()
        self.assertIn("test_sender", serialized)
        self.assertIn("Hello!", serialized)

    def test_message_deserialization(self):
        message = Message(self._get_id(Priority.NORMAL), "test_sender", {"content": "Hello!"})
        serialized = message.serialize()
        deserialized = Message.deserialize(serialized)
        self.assertEqual(message.sender, deserialized.sender)
        self.assertEqual(message.content, deserialized.content)

    def test_set_content(self):
        message = Message(self._get_id(Priority.NORMAL), "test_sender", {"content": "Hello!"})
        message.set_content({"content": "Goodbye!"})
        self.assertEqual(message.content, {"content": "Goodbye!"})

    def test_message_sorting_by_time(self):
        message1 = Message(self._get_id(Priority.NORMAL), "test_sender", '{"content": "Hello!"}')
        message2 = Message(self._get_id(Priority.NORMAL), "test_sender", '{"content": "Hello!"}')
        message3 = Message(self._get_id(Priority.NORMAL), "test_sender", '{"content": "Hello!"}')
        sorted_messages = sorted([message1, message3, message2])
        self.assertEqual(sorted_messages, [message1, message2, message3])

    def test_message_sorting_by_priority(self):
        message1 = Message(self._get_id(Priority.NORMAL), "test_sender", '{"content": "Hello!"}')
        message2 = Message(self._get_id(Priority.HIGH), "test_sender", '{"content": "Hello!"}')
        message3 = Message(self._get_id(Priority.LOW), "test_sender", '{"content": "Hello!"}')
        sorted_messages = sorted([message1, message3, message2])
        self.assertEqual(sorted_messages, [message2, message1, message3])

    def test_message_sorting_by_priority_and_time(self):
        message1 = Message(self._get_id(Priority.NORMAL), "test_sender", '{"content": "Hello!"}')
        message2 = Message(self._get_id(Priority.HIGH), "test_sender", '{"content": "Hello!"}')
        message3 = Message(self._get_id(Priority.LOW), "test_sender", '{"content": "Hello!"}')
        message4 = Message(self._get_id(Priority.NORMAL), "test_sender", '{"content": "Hello!"}')
        message5 = Message(self._get_id(Priority.URGENT), "test_sender", '{"content": "Hello!"}')
        message6 = Message(self._get_id(Priority.LOW), "test_sender", '{"content": "Hello!"}')
        sorted_messages = sorted([message1, message3, message2, message4, message5, message6])
        self.assertEqual(sorted_messages, [message5, message2, message1, message4, message3, message6])


if __name__ == '__main__':
    unittest.main()
