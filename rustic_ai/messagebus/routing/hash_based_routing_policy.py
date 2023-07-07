from hashlib import sha256
from typing import TYPE_CHECKING, Dict, List

from ..message import Message, MessageProperties
from .routing import RoutingPolicy

if TYPE_CHECKING:  # pragma: no cover
    from ..client.client import Client


class HashBasedRoutingPolicy(RoutingPolicy):
    """
    This class implements a hash-based routing policy. The policy routes a message
    to recipients based on a hash value derived from specific properties of the message.
    """

    def __init__(self, message_properties: List[MessageProperties]):
        """
        Initializes the HashBasedRoutingPolicy with a list of message properties.

        :param message_properties: List of message properties to be used in generating the hash value.
        """
        self.message_properties = [prop.value for prop in message_properties]

    def get_recipients(self, message: Message, clients: Dict[str, 'Client']) -> List[str]:
        """
        Returns the list of recipients for a given message. The recipients are selected
        based on a hash value derived from specific properties of the message.

        :param message: The message to be routed.
        :param clients: A dictionary of available clients, keyed by client ID.
        :return: A list of recipient client IDs.
        """
        message_dict = message.__dict__
        hash_input = "".join(str(message_dict.get(prop)) for prop in self.message_properties)
        hashed_value = sha256(hash_input.encode('utf-8')).hexdigest()
        client_ids = list(clients.keys())
        chosen_client = client_ids[int(hashed_value, 16) % len(client_ids)]
        return [chosen_client]
