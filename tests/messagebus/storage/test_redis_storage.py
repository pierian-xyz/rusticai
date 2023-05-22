import unittest

import fakeredis

from rustic_ai.messagebus import RedisStorage, StorageBackend

from .storage_backend_base_test import AbstractTests


class TestRedisStorage(AbstractTests.TestStorageBackendABC, unittest.TestCase):
    def get_storage_backend(self) -> StorageBackend:
        server = fakeredis.FakeServer()
        return RedisStorage(fakeredis.FakeStrictRedis(server=server))

    def tearDown(self):
        # Clean up fake Redis database after each test
        self.storage.redis.flushall()
