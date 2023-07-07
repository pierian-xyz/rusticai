import json
from enum import Enum
from typing import Dict, List, Optional, Union

from .utils import Priority

JSONVALUE = Union[int, str, float, bool, List['JSONVALUE'], Dict[str, 'JSONVALUE']]
JSON = Dict[str, JSONVALUE]


class Message:
    """A message that can be sent between clients through the message bus."""

    def __init__(
        self,
        id: int,
        sender: str,
        content: JSON,
        recipients: Optional[List[str]] = None,
        priority: Priority = Priority.NORMAL,
        thread_id: Optional[int] = None,
        in_reply_to: Optional[int] = None,
        topic: Optional[str] = None,
    ):
        """
        Initialize the message with a unique ID, sender, content, recipients, and priority.

        :param sender: The sender of the message
        :param content: The content of the message, either a string or a dict
        :param recipients: A list of recipients for the message
        :param priority: The priority of the message, default is 0
        """
        self.id: int = id
        self.sender: str = sender
        self.content: JSON = content
        self.recipients: List[str] = recipients if recipients else []
        self.priority: int = priority
        self.thread_id: Optional[int] = thread_id if thread_id is not None else id
        self.in_reply_to: Optional[int] = in_reply_to
        self.topic: Optional[str] = topic

    def set_content(self, content: JSON) -> None:
        """
        Set the content of the message.

        :param content: The new content for the message, either a string or a dict
        """
        self.content = content

    def get_content(self) -> str:
        """
        Get the content of the message in JSON string format.

        :return: The content of the message as a JSON string
        """
        return json.dumps(self.content)

    def serialize(self) -> str:
        """
        Serialize the message into a JSON string format.

        :return: The serialized message as a JSON string
        """
        return json.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, message_json: str) -> 'Message':
        """
        Deserialize a JSON string into a Message object.

        :param message_json: The JSON string representing the message
        :return: The deserialized message object
        """
        message_data = json.loads(message_json)
        message = cls(**message_data)
        return message

    def __lt__(self, other: 'Message') -> bool:
        """
        Compare two messages based on priority.

        :param other: The other message to compare to
        :return: True if this message has a lower priority than the other message
        """
        if not isinstance(other, Message):
            return NotImplemented

        return self.id < other.id

    def __eq__(self, other: object) -> bool:
        """
        Compare two messages based on priority.

        :param other: The other message to compare to
        :return: True if this message has a lower priority than the other message
        """
        if not isinstance(other, Message):
            return NotImplemented

        return (
            self.id == other.id
            and self.sender == other.sender
            and self.content == other.content
            and self.recipients == other.recipients
            and self.priority == other.priority
        )


class MessageProperties(Enum):
    """
    Message properties that can be used for routing.
    """

    ID = "id"
    CONTENT = "content"
    RECIPIENTS = "recipients"
    SENDER = "sender"
    PRIORITY = "priority"
