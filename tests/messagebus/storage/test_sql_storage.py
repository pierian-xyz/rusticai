import unittest

from rustic_ai.messagebus import SQLStorage, StorageBackend

from .storage_backend_base_test import AbstractTests


class TestSQLBasedStorage(AbstractTests.TestStorageBackendABC, unittest.TestCase):
    def setUp(self) -> None:
        # self.conn = sqlite3.connect(":memory:")  # Create an in-memory SQLite database
        super().setUp()

    def get_storage_backend(self) -> StorageBackend:
        self.sql_storage = SQLStorage("sqlite://")
        return self.sql_storage

    def tearDown(self):
        # Close the connection after each test
        self.sql_storage.engine.dispose()
