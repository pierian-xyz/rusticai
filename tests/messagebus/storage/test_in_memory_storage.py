import unittest

from rustic_ai.messagebus import InMemoryStorage, StorageBackend

from .storage_backend_base_test import AbstractTests


class TestInMemoryStorage(AbstractTests.TestStorageBackendABC, unittest.TestCase):
    def get_storage_backend(self) -> StorageBackend:
        return InMemoryStorage()


if __name__ == '__main__':
    unittest.main()
