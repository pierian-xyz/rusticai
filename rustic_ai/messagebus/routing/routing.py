from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List

from ..message import Message

if TYPE_CHECKING:  # pragma: no cover
    from ..client.client import Client


class RoutingPolicy(ABC):
    """
    Abstract base class representing a routing policy. This class defines the method
    signature for get_recipients, which must be implemented by all subclasses.

    This class is part of the routing mechanism for the message bus system, and
    allows for flexibility in defining how messages should be routed to clients.
    """

    @abstractmethod
    def get_recipients(self, message: Message, clients: Dict[str, 'Client']) -> List[str]:
        """
        Determine the recipients for a given message.

        This method should be implemented by subclasses to define their specific
        routing logic.

        :param message: The message to be routed.
        :param clients: A dictionary of available clients, keyed by client ID.
        :return: A list of recipient client IDs.
        """
        pass  # pragma: no cover
