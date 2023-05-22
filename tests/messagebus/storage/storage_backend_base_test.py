import time
from abc import ABC, abstractmethod

from rustic_ai.messagebus import Message, StorageBackend
from rustic_ai.messagebus.utils import IDGenerator, Priority


class AbstractTests(object):
    class TestStorageBackendABC(ABC):
        @abstractmethod
        def get_storage_backend(self) -> StorageBackend:
            pass

        def setUp(self):
            self.storage = self.get_storage_backend()
            self.id_generator = IDGenerator(1)

        def _get_id(self, priority: Priority) -> int:
            return self.id_generator.get_id(priority).to_int()

        def test_create_and_remove_inbox(self):
            self.storage.create_inbox("test_client")
            self.storage.add_message_to_inbox(
                "test_client", Message(self._get_id(Priority.NORMAL), "test_client", {"content": "Hello!"})
            )
            self.assertIsNotNone(self.storage.get_next_unread_message("test_client", 0))
            self.storage.remove_inbox("test_client")
            self.assertIsNone(self.storage.get_next_unread_message("test_client", 0))

        def test_add_and_get_message(self):
            self.storage.create_inbox("test_client")
            msg = Message(self._get_id(Priority.NORMAL), "test_client", {"content": "Hello!"})
            self.storage.add_message_to_inbox("test_client", msg)
            retrieved_msg = self.storage.get_next_unread_message("test_client", 0)
            self.assertEqual(msg, retrieved_msg)
            self.storage.remove_inbox("test_client")

        def test_add_and_get_multiple_messages(self):
            self.storage.create_inbox("test_client")
            msg1 = Message(self._get_id(Priority.NORMAL), "test_client", {"content": "Hello!"})
            time.sleep(0.001)
            msg2 = Message(self._get_id(Priority.NORMAL), "test_client", {"content": "Hello again!"})
            self.storage.add_message_to_inbox("test_client", msg1)
            self.storage.add_message_to_inbox("test_client", msg2)
            retrieved_msg1 = self.storage.get_next_unread_message("test_client", 0)
            retrieved_msg2 = self.storage.get_next_unread_message("test_client", retrieved_msg1.id)
            retrieved_msg3 = self.storage.get_next_unread_message("test_client", retrieved_msg2.id)
            self.assertEqual(msg1, retrieved_msg1)
            self.assertEqual(msg2, retrieved_msg2)
            self.assertIsNone(retrieved_msg3)
            self.storage.remove_inbox("test_client")

        def test_remove_received_message(self):
            self.storage.create_inbox("test_client")
            msg = Message(self._get_id(Priority.NORMAL), "test_client", {"content": "Hello!"})
            self.storage.add_message_to_inbox("test_client", msg)
            self.storage.remove_received_message("test_client", ["test_client"], msg.id)
            self.assertIsNone(self.storage.get_next_unread_message("test_client", 0))
            self.storage.remove_inbox("test_client")
