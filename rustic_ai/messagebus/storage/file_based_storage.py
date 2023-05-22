import heapq
import json
import os
from typing import Dict, List, Optional

from ..message import Message
from .storage import StorageBackend


class FileBasedStorage(StorageBackend):
    """
    FileBasedStorage represents a file-based storage system for the message bus.
    """

    def __init__(self, directory: str):
        """
        Initialize the storage with a directory to save the inbox files.

        :param directory: The directory to store inbox files.
        """
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def _get_inbox_file(self, client_id: str) -> str:
        """
        Get the file path for a given client's inbox.

        :param client_id: The ID of the client.
        :return: The file path of the client's inbox.
        """
        return os.path.join(self.directory, f"{client_id}.json")

    def create_inbox(self, client_id: str) -> None:
        """
        Create a new inbox for a client.

        :param client_id: The ID of the client.
        """
        with open(self._get_inbox_file(client_id), 'w') as f:
            json.dump([], f)

    def remove_inbox(self, client_id: str) -> None:
        """
        Remove the inbox of a client.

        :param client_id: The ID of the client.
        """
        os.remove(self._get_inbox_file(client_id))

    def add_message_to_inbox(self, recipient_id: str, message: Message) -> None:
        """
        Add a message to the recipient's inbox.

        :param recipient_id: The ID of the recipient client.
        :param message: The message to be added.
        """
        inbox = self._load_inbox(recipient_id)
        heapq.heappush(inbox, message.serialize())  # type: ignore
        self._save_inbox(recipient_id, inbox)

    def get_next_unread_message(self, recipient_id: str, last_read_message_id: int) -> Optional[Message]:
        """
        Retrieve the next unread message for a client.

        :param recipient_id: The ID of the recipient client.
        :param last_read_message_id: The ID of the last read message.
        :return: The next unread message, if one exists.
        """
        response: Optional[Message] = None

        try:
            inbox = self._load_inbox(recipient_id)
        except FileNotFoundError:
            pass
        else:
            if inbox:
                next_message_serialized = heapq.heappop(inbox)
                next_message = Message.deserialize(next_message_serialized)  # type: ignore
                while next_message.id == last_read_message_id:
                    next_message_serialized = heapq.heappop(inbox)
                    next_message = Message.deserialize(next_message_serialized)  # type: ignore
                response = next_message
                self._save_inbox(recipient_id, inbox)

        return response

    def remove_received_message(self, sender_id: str, recipient_ids: List[str], message_id: int) -> None:
        """
        Remove a sent message from the recipient's inbox.

        :param sender_id: The ID of the sender client.
        :param recipient_ids: The List of IDs for the recipient client.
        :param message_id: The ID of the message to be removed.
        """
        for recipient_id in recipient_ids:
            inbox = self._load_inbox(recipient_id)
            inbox = [m for m in inbox if self._filter_message(m, sender_id, message_id)]  # type: ignore
            heapq.heapify(inbox)
            self._save_inbox(recipient_id, inbox)

    def _filter_message(self, message_serialized: str, sender_id: str, message_id: int):
        message: Message = Message.deserialize(message_serialized)
        return message.sender != sender_id or message.id != message_id

    def _load_inbox(self, client_id: str) -> List[Dict]:
        """
        Load an inbox from a file.

        :param client_id: The ID of the client.
        :return: The list of messages in the client's inbox.
        """
        with open(self._get_inbox_file(client_id), 'r') as f:
            return json.load(f)

    def _save_inbox(self, client_id: str, inbox: List[Dict]) -> None:
        """
        Save an inbox to a file.

        :param client_id: The ID of the client.
        :param inbox: The list of messages to be saved in the client's inbox.
        """
        with open(self._get_inbox_file(client_id), 'w') as f:
            json.dump(inbox, f)
