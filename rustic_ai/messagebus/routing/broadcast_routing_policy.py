from typing import TYPE_CHECKING, Dict, List

from ..message import Message
from .routing import RoutingPolicy

if TYPE_CHECKING:
    from ..client.client import Client


class BroadcastRoutingPolicy(RoutingPolicy):
    """
    This class implements the RoutingPolicy for broadcast messaging.
    In a broadcast messaging system, messages are sent to all clients,
    excluding the sender of the message.
    """

    def get_recipients(self, message: Message, clients: Dict[str, 'Client']) -> List[str]:
        """
        Returns the list of all clients except the sender for a given message.

        :param message: The message to be routed.
        :param clients: A dictionary of available clients, keyed by client ID.
        :return: A list of recipient client IDs.
        """
        # For broadcast, we return the IDs of all clients except the sender
        return [client_id for client_id in clients.keys() if client_id != message.sender]
