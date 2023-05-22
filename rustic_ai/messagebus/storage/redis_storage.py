from typing import List, Optional

import redis

from ..message import Message
from .storage import StorageBackend


class RedisStorage(StorageBackend):
    """
    RedisStorage represents a Redis-based storage system for the message bus.
    """

    def __init__(self, redis_connection: redis.StrictRedis):
        """
        Initialize the storage with Redis connection parameters.

        :param host: The hostname of the Redis server.
        :param port: The port of the Redis server.
        :param db: The database number to use in the Redis server.
        """
        self.redis = redis_connection

    @classmethod
    def create_storage(cls, host: str, port: int, db: int):
        """
        Initialize the storage with Redis connection parameters.

        :param host: The hostname of the Redis server.
        :param port: The port of the Redis server.
        :param db: The database number to use in the Redis server.
        """
        return cls(redis.Redis(host=host, port=port, db=db))

    def create_inbox(self, client_id: str) -> None:
        """
        Create a new inbox for a client. Since Redis creates keys on the fly,
        we don't need to do anything in this method.

        :param client_id: The ID of the client.
        """
        pass

    def remove_inbox(self, client_id: str) -> None:
        """
        Remove the inbox of a client.

        :param client_id: The ID of the client.
        """
        self.redis.delete(client_id)

    def add_message_to_inbox(self, recipient_id: str, message: Message) -> None:
        """
        Add a message to the recipient's inbox.

        :param recipient_id: The ID of the recipient client.
        :param message: The message to be added.
        """
        self.redis.zadd(recipient_id, {message.serialize(): message.id})

    def get_next_unread_message(self, recipient_id: str, last_read_message_id: int) -> Optional[Message]:
        """
        Retrieve the next unread message for a client.

        :param recipient_id: The ID of the recipient client.
        :param last_read_message_id: The ID of the last read message.
        :return: The next unread message, if one exists.
        """
        message_data = self.redis.zrange(recipient_id, 0, 0)
        if message_data:
            message = Message.deserialize(message_data[0])

            while message.id == last_read_message_id:
                self.redis.zrem(recipient_id, message.serialize())
                message_data = self.redis.zrange(recipient_id, 0, 0)
                if not message_data:
                    return None
                message = Message.deserialize(message_data[0])

            return message
        else:
            return None

    def remove_received_message(self, sender_id: str, recipient_ids: List[str], message_id: int) -> None:
        """
        Remove a sent message from the recipient's inbox.

        :param sender_id: The ID of the sender client.
        :param recipient_ids: The List of IDs for the recipient client.
        :param message_id: The ID of the message to be removed.
        """
        for recipient_id in recipient_ids:
            inbox = self.redis.zrange(recipient_id, 0, -1)
            for message_data in inbox:
                message = Message.deserialize(message_data)
                if message.sender == sender_id and message.id == message_id:
                    self.redis.zrem(recipient_id, message_data)
                    break
