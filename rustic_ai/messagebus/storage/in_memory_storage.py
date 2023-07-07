import heapq
from typing import Dict, List, Optional

from ..message import Message
from .storage import StorageBackend


class InMemoryStorage(StorageBackend):
    """
    An in-memory storage system for the message bus.
    """

    def __init__(self) -> None:
        """
        Initializes the in-memory storage with an empty dictionary of inboxes.
        """
        self.inboxes: Dict[str, Dict[str, List[Message]]] = {}

    def create_inbox(self, message_bus_id: str, client_id: str) -> None:
        """
        Create a new inbox for a client.

        :param client_id: The ID of the client.
        """
        if message_bus_id not in self.inboxes:
            self.inboxes[message_bus_id] = {}

        if client_id not in self.inboxes[message_bus_id]:
            self.inboxes[message_bus_id][client_id] = []

    def remove_inbox(self, message_bus_id: str, client_id: str) -> None:
        """
        Remove the inbox of a client.

        :param client_id: The ID of the client.
        """
        if client_id in self.inboxes[message_bus_id]:
            del self.inboxes[message_bus_id][client_id]

    def add_message_to_inbox(self, message_bus_id: str, recipient_id: str, message: Message) -> None:
        """
        Add a message to the recipient's inbox.

        :param recipient_id: The ID of the recipient client.
        :param message: The message to be added.
        """
        inbox = self.inboxes[message_bus_id][recipient_id]
        heapq.heappush(inbox, message)

    def get_next_unread_message(
        self, message_bus_id: str, recipient_id: str, last_read_message_id: int
    ) -> Optional[Message]:
        """
        Retrieve the next unread message for a client.

        :param recipient_id: The ID of the recipient client.
        :param last_read_message_id: The ID of the last read message.
        :return: The next unread message, if one exists.
        """
        response: Optional[Message] = None

        if (recipient_id in self.inboxes[message_bus_id]) and (self.inboxes[message_bus_id][recipient_id]):
            next_message = heapq.heappop(self.inboxes[message_bus_id][recipient_id])
            while next_message.id == last_read_message_id:
                next_message = heapq.heappop(self.inboxes[message_bus_id][recipient_id])
            response = next_message

        return response

    def remove_received_message(
        self, message_bus_id: str, sender_id: str, recipient_ids: List[str], message_id: int
    ) -> None:
        """
        Remove a sent message from the recipient's inbox.

        :param sender_id: The ID of the sender client.
        :param recipient_ids: The List of IDs for the recipient client.
        :param message_id: The ID of the message to be removed.
        """
        for recipient_id in recipient_ids:
            filtered = [
                m for m in self.inboxes[message_bus_id][recipient_id] if m.sender != sender_id or m.id != message_id
            ]
            self.inboxes[message_bus_id][recipient_id] = filtered
            heapq.heapify(self.inboxes[message_bus_id][recipient_id])
