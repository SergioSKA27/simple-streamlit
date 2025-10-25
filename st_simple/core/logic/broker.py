"""
broker.py - Base Broker Interface

Defines the interface for message brokers in the event-driven architecture.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

from .message import TopicMessage
from .topic import BaseTopic


class BaseBroker(ABC):
    """
    Abstract base class for message brokers.

    A broker manages the routing of messages between topics and handlers.
    """

    @abstractmethod
    def publish(self, topic_id: str, message: TopicMessage) -> None:
        """
        Publish a message to a topic.

        Args:
            topic_id: ID of the topic to publish to
            message: Message to publish
        """
        pass

    @abstractmethod
    def subscribe(self, topic_id: str, handler: callable) -> None:
        """
        Subscribe a handler to a topic.

        Args:
            topic_id: ID of the topic to subscribe to
            handler: Handler function to call when messages are published
        """
        pass

    @abstractmethod
    def create_topic(
        self,
        _id: str,
        version: str = "1.0.0",
        **kwargs,
    ) -> "BaseTopic":
        """
        Create a new topic.

        Args:
            _id: Unique identifier for the topic
            version: Semantic version for the topic
            **kwargs: Additional topic configuration

        Returns:
            The created topic instance
        """
        pass