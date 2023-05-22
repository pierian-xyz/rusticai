from typing import TYPE_CHECKING, Dict, List

from ..message import Message
from .routing import RoutingPolicy

if TYPE_CHECKING:
    from ..client.client import Client


class DirectOrFallbackRoutingPolicy(RoutingPolicy):
    """
    This class implements the RoutingPolicy for direct messaging with a fallback option.
    In this policy, a message will be sent to the direct recipients if specified.
    If no recipients are specified, the message is sent to a predefined fallback client.
    """

    def __init__(self, fallback_client_id: str):
        """
        Initializes the DirectOrFallbackRoutingPolicy with a fallback client ID.

        :param fallback_client_id: The ID of the client to be used as a fallback recipient.
        """
        self.fallback_client_id = fallback_client_id

    def get_recipients(self, message: Message, clients: Dict[str, 'Client']) -> List[str]:
        """
        Returns the list of recipients for a given message.
        If the message has specified recipients, those are returned.
        If no recipients are specified, the fallback client ID is returned.

        :param message: The message to be routed.
        :param clients: A dictionary of available clients, keyed by client ID.
        :return: A list of recipient client IDs.
        """
        if message.recipients:
            return message.recipients
        else:
            return [self.fallback_client_id]
