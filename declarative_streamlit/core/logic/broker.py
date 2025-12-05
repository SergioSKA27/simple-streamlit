"""
broker.py - Base Broker Interface

Defines the interface for message brokers in the event-driven architecture.
"""

from typing import Any, Callable, List, Optional

from .message import TopicMessage
from .topic import BaseTopic, ErrorStrategy


class BaseBroker:
    """
    Abstract base class for message brokers.

    A broker manages the routing of messages between topics and handlers.
    """

    def __init__(self, name: str = "broker", debug: bool = False) -> None:
        self._name = name
        self._debug = debug
        self._topics = {}

    def publish(self, topic_id: str, message: TopicMessage) -> None:
        """
        Publish a message to a topic.

        Args:
            topic_id: ID of the topic to publish to
            message: Message to publish
        """

        topic = self._get_topic(topic_id)
        if topic:
            topic.publish_event(message)
        else:
            raise ValueError(f"Topic with ID '{topic_id}' not found.")


    def _register_topic(self, topic: BaseTopic) -> None:
        """
        Register a topic with the broker.

        Args:
            topic: Topic instance to register
        """
        self._topics[topic._id] = topic

        setattr(self, topic._id, topic)

    def _get_topic(self, topic_id: str) -> BaseTopic:
        """
        Retrieve a topic by its ID.

        Args:
            topic_id: ID of the topic to retrieve

        Returns:
            The topic instance
        """
        return self._topics.get(topic_id)
    def subscribe(self, topic: BaseTopic) -> None:
        """
        Subscribe a topic to the broker.
        Args:
            topic: Topic instance to subscribe
        """
        topic._broker = self
        self._register_topic(topic)

    def create_topic(
        self,
        _id: str,
        version: str = "1.0.0",
        error_strategy: ErrorStrategy = ErrorStrategy.RAISE,
        error_handler: Optional[Callable[[Exception, Any], None]] = None,
        blacklist: Optional[List[str]] = None,
        whitelist: Optional[List[str]] = None,
        max_dead_letters: int = 100,
        debug: bool = False,
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

        topic = BaseTopic(
            _id,
            version=version,
            error_strategy=error_strategy,
            error_handler=error_handler,
            blacklist=blacklist,
            whitelist=whitelist,
            max_dead_letters=max_dead_letters,
            broker=self,
            debug=debug,
        )
        self._register_topic(topic)

        return topic
