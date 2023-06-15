from abc import ABC, abstractmethod
from typing import List, Optional

from ..message import Message


class StorageBackend(ABC):
    """
    Abstract base class that represents the storage mechanism for the message bus.
    """

    @abstractmethod
    def create_inbox(self, message_bus_id: str, client_id: str) -> None:
        """
        Abstract method to create a new inbox for a client with the given ID.

        :param client_id: The ID of the client for which to create an inbox.
        """
        pass

    @abstractmethod
    def remove_inbox(self, message_bus_id: str, client_id: str) -> None:
        """
        Abstract method to remove the inbox for a client with the given ID.

        :param client_id: The ID of the client whose inbox is to be removed.
        """
        pass

    @abstractmethod
    def add_message_to_inbox(self, message_bus_id: str, recipient_id: str, message: Message) -> None:
        """
        Abstract method to add a message to the inbox of the client with the given ID.

        :param recipient_id: The ID of the recipient client.
        :param message: The message to be added.
        """
        pass

    @abstractmethod
    def get_next_unread_message(
        self, message_bus_id: str, recipient_id: str, last_read_message_id: int
    ) -> Optional[Message]:
        """
        Abstract method to retrieve the next unread message for a client with the given ID.

        :param recipient_id: The ID of the recipient client.
        :param last_read_message_id: The ID of the last read message.
        :return: The next unread message, if one exists.
        """
        pass

    @abstractmethod
    def remove_received_message(
        self, message_bus_id: str, sender_id: str, recipient_ids: List[str], message_id: int
    ) -> None:
        """
        Abstract method to remove a sent message from the recipient's inbox.

        :param sender_id: The ID of the sender client.
        :param recipient_ids: The ID of the recipient client.
        :param message_id: The ID of the message to be removed.
        """
        pass
