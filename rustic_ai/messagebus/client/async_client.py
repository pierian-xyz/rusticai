import asyncio
from typing import Optional

from ..message import Message
from ..message_bus import MessageBus
from .client import Client


class AsyncClient(Client):
    """
    An asynchronous implementation of the Client, using asyncio's Queue to manage messages.
    """

    def __init__(self, client_id: str, message_bus: MessageBus) -> None:
        """
        Initialize the asynchronous client with a unique ID and a reference to the message bus.

        :param client_id: Unique identifier for this client
        :param message_bus: Reference to the message bus instance
        """
        super().__init__(client_id, message_bus)
        self.message_queue: asyncio.Queue = asyncio.Queue()

    async def fetch_next_unread_message(self) -> None:
        """
        Asynchronously fetch the next unread message for this client and put it into the queue.

        :return: None
        """
        message = self.message_bus.get_next_unread_message(self.client_id, self.last_read_message_id)

        if message is not None:
            self.last_read_message_id = message.id
            await self.message_queue.put(message)

    def get_next_unread_message(self) -> Optional[Message]:
        """
        Synchronously get the next unread message from the queue for this client.
        DO NOT USE THIS METHOD UNLESS NECESSARY.
        :return: The next unread message, if one exists
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.async_get_next_unread_message())

    async def async_get_next_unread_message(self) -> Optional[Message]:
        """
        Asynchronously get the next unread message from the queue for this client.

        :return: The next unread message, if one exists
        """
        return await self.message_queue.get()  # type: ignore

    def notify_new_message(self) -> None:
        """
        Schedule a new task to fetch and process the new message asynchronously.
        """
        asyncio.create_task(self.fetch_next_unread_message())
