# API Documentation for Modular Message Bus Library

## Table of Contents
1. [Introduction](#introduction)
2. [MessageBus](#messagebus)
   * [Methods](#messagebus-methods)
3. [StorageBackend](#storagebackend)
   * [Methods](#storagebackend-methods)
4. [RoutingPolicy](#routingpolicy)
   * [Methods](#routingpolicy-methods)
5. [Message](#message)
   * [Attributes](#message-attributes)

## 1. Introduction <a name="introduction"></a>
This API documentation provides detailed information about the public interfaces, classes, methods, and data structures of the modular message bus library.

## 2. MessageBus <a name="messagebus"></a>
The `MessageBus` class is the core component of the library, responsible for managing agent connections, message routing, and storage.

### 2.1 Methods <a name="messagebus-methods"></a>
* `__init__(self, storage_backend: StorageBackend, routing_policy: RoutingPolicy)`: Initializes a new `MessageBus` instance with the specified storage backend and routing policy.
* `connect_agent(self, agent_id: str)`: Registers a new agent with the specified agent ID.
* `disconnect_agent(self, agent_id: str)`: Unregisters an agent with the specified agent ID.
* `send_message(self, message: Message)`: Sends a message to the message bus.
* `fetch_messages(self, agent_id: str, last_message_id: Optional[str] = None)`: Fetches messages for the specified agent, optionally starting from a specific message ID.

## 3. StorageBackend <a name="storagebackend"></a>
The `StorageBackend` interface defines the methods required for storing and retrieving messages. Custom storage backends should implement this interface.

### 3.1 Methods <a name="storagebackend-methods"></a>
* `store_message(self, message: Message)`: Stores a message in the backend.
* `fetch_messages(self, agent_id: str, last_message_id: Optional[str] = None)`: Fetches messages for the specified agent, optionally starting from a specific message ID.

## 4. RoutingPolicy <a name="routingpolicy"></a>
The `RoutingPolicy` interface defines the methods required for determining the recipients of a message. Custom routing policies should implement this interface.

### 4.1 Methods <a name="routingpolicy-methods"></a>
* `get_recipients(self, message: Message, connected_agents: Set[str])`: Determines the recipients of a message based on its contents and the set of connected agents.

## 5. Message <a name="message"></a>
The `Message` class represents a message sent between agents in the chatroom.

### 5.1 Attributes <a name="message-attributes"></a>
* `id: str`: A unique identifier for the message.
* `sender: str`: The ID of the agent that sent the message.
* `timestamp: float`: The timestamp when the message was sent.
* `content: Any`: The content of the message.
* `recipients: Optional[Set[str]]`: An optional set of specific recipients for the message.

By following this API documentation, users can interact with and extend the functionality of the modular message bus library.
