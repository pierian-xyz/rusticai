import json
from contextlib import contextmanager
from typing import Any, Generator, List, Optional

from sqlalchemy import BigInteger, Column, Enum, Numeric, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.types import TypeDecorator

from ..message import Message
from ..utils import Priority
from .storage import StorageBackend


class BigIntType(TypeDecorator):
    """
    A type decorator for SQLAlchemy to support 64-bit integers.
    """

    impl = BigInteger

    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(Numeric)
        else:
            return dialect.type_descriptor(BigInteger)


Base: Any = declarative_base()


class MessageTable(Base):
    """
    A table to store messages in.
    """

    __tablename__ = 'message'

    id = Column(BigIntType, primary_key=True)
    recipient_id = Column(String, primary_key=True)
    sender_id = Column(String)
    content = Column(String)
    priority = Column(Enum(Priority))


class SQLStorage(StorageBackend):
    """
    A SQL based storage system for the message bus.
    """

    def __init__(self, connection_string: str):
        """
        Initialize the storage system.

        :param connection_string: SQLAlchemy compatible connection string
        """
        self.engine: Engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        self.Session: sessionmaker = sessionmaker(bind=self.engine)

    @contextmanager
    def make_session(self) -> Generator[Any, Any, None]:
        """
        Context manager for session handling.
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_inbox(self, client_id: str) -> None:
        # No action required as inboxes are not explicitly created in this storage
        pass

    def remove_inbox(self, client_id: str) -> None:
        """
        Remove the inbox of a client.

        :param client_id: The ID of the client.
        """
        with self.make_session() as session:
            session.query(MessageTable).filter_by(recipient_id=client_id).delete(synchronize_session=False)

    def add_message_to_inbox(self, recipient_id: str, message: Message) -> None:
        """
        Add a message to the recipient's inbox.

        :param recipient_id: The ID of the recipient client.
        :param message: The message to be added.
        """
        with self.make_session() as session:
            new_message = MessageTable(
                id=message.id,
                sender_id=message.sender,
                recipient_id=recipient_id,
                content=message.get_content(),
                priority=message.priority,
            )
            session.add(new_message)

    def get_next_unread_message(self, recipient_id: str, last_read_message_id: int) -> Optional[Message]:
        """
        Retrieve the next unread message for a client.

        :param recipient_id: The ID of the recipient client.
        :param last_read_message_id: The ID of the last read message.
        :return: The next unread message, if one exists.
        """
        with self.make_session() as session:
            result = (
                session.query(MessageTable)
                .filter(MessageTable.recipient_id == recipient_id, MessageTable.id > last_read_message_id)
                .order_by(MessageTable.id)
                .first()
            )
            if result is not None:
                message = Message(
                    int(result.id), result.sender_id, json.loads(result.content), priority=result.priority
                )
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
        with self.make_session() as session:
            session.query(MessageTable).filter(
                MessageTable.recipient_id.in_(recipient_ids),
                MessageTable.sender_id == sender_id,
                MessageTable.id == message_id,
            ).delete(synchronize_session=False)

    def close_connection(self) -> None:
        """
        Close the connection to the database.
        """
        self.engine.dispose()
