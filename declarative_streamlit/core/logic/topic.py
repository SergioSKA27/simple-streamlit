"""
topic.py - Event-Driven Topic System for Streamlit Applications

A robust publish-subscribe implementation designed specifically for Streamlit applications.
Enables true event-driven architecture with declarative YAML configuration support.

Key Features:
- Decorator-based handler registration (@topic.register)
- Priority-based handler execution
- Error strategies (RAISE, WARN, IGNORE, CUSTOM)
- Semantic versioning for topics
- Dead Letter Queue for debugging
- Performance metrics tracking
- Async/await support
- Blacklist/whitelist security model
"""

from enum import Enum
from typing import (
    Dict,
    List,
    Any,
    Union,
    Optional,
    Callable,
    TypeVar,
    overload,
    cast,
    Set,
    Tuple,
    TYPE_CHECKING,
)
import logging
import queue
import time
import asyncio
from functools import wraps

if TYPE_CHECKING:
    from .broker import BaseBroker
    from .message import TopicMessage

logger = logging.getLogger(__name__)


class ErrorStrategy(Enum):
    """Error handling strategies for topics"""

    RAISE = "raise"  # Raise exception (critical for production)
    WARN = "warn"  # Log warning (non-critical)
    IGNORE = "ignore"  # Silently ignore errors
    CUSTOM = "custom"  # Use custom error handler


class TopicProcessingError(Exception):
    """Custom exception for topic processing errors"""

    pass


class BaseTopicHandler(Dict[str, Any]):
    """Type alias for topic handler metadata dictionary"""
    pass


# Type variable for handler functions
HandlerType = TypeVar("HandlerType", bound=Callable[[Any], None])


class BaseTopic:
    """
    Base class for topic implementation in event-driven architecture.

    A topic represents a channel for publishing and subscribing to events.
    It enables decoupled communication between UI components and business logic.

    Key Capabilities:
    - Register handlers with priorities
    - Publish events with version control
    - Blacklist/whitelist security model
    - Error handling strategies
    - Performance metrics tracking
    - Dead Letter Queue for debugging

    Example:
        # Create a topic
        filter_topic = broker.create_topic("filters")

        event=filter_topic.add_event("months_changed")

        # Register handlers
        @filter_topic.handler(priority=100,event="months_changed")
        def validate_selection(months: List[str]):
            # Validation logic
            pass
         # or using the event directly

         @event.handler(priority=100)
        def update_chart_data(months: List[str]):
            # Update chart logic
            pass

        # Publish an event
        filter_topic.publish_event(TopicMessage(
            sender="month_filter",
            data=["Jan", "Feb"]
        ))
    """

    def __init__(
        self,
        _id: str,
        version: str = "1.0.0",
        error_strategy: ErrorStrategy = ErrorStrategy.RAISE,
        error_handler: Optional[Callable[[Exception, Any], None]] = None,
        blacklist: Optional[List[str]] = None,
        whitelist: Optional[List[str]] = None,
        max_dead_letters: int = 100,
        broker: Optional["BaseBroker"] = None,
        debug: bool = False,
    ):
        """
        Initialize a new topic.

        Args:
            _id: Unique identifier for the topic (e.g., "filters/months_changed")
            version: Semantic version for the topic interface
            error_strategy: Strategy for handling errors in handlers
            error_handler: Custom error handler function
            subscribers: Initial list of subscriber IDs
            blacklist: List of sender IDs that are blocked
            whitelist: List of allowed sender IDs (if None, all are allowed)
            max_dead_letters: Maximum number of failed events to retain
            broker: Associated message broker
            debug: Enable debug logging
        """
        self._id = _id
        self.version = version
        self._full_id = f"{_id}@{version}"
        self.error_strategy = error_strategy
        self.error_handler = error_handler
        self._debug = debug

        # Security model (optimized for O(1) lookups)
        self._blacklist: Set[str] = set(blacklist or [])
        self._whitelist: Optional[Set[str]] = set(whitelist or []) if whitelist else None

        # Handler management
        self._handlers: List = []

        # Performance metrics
        self._metrics = {
            "events_processed": 0,
            "errors": 0,
            "last_processed": None,
            "latency_avg": 0.0,  # Exponential moving average
        }

        # Dead Letter Queue for debugging
        self._dead_letters = queue.Queue(maxsize=max_dead_letters)

        self._broker = broker
        if self._debug:
            logger.setLevel(logging.DEBUG)
            logger.debug(f"Topic initialized: {self._full_id}")

    def is_sender_allowed(self, sender_id: str) -> bool:
        """
        Check if a sender is allowed to publish to this topic.

        Uses O(1) set operations for optimal performance.

        Args:
            sender_id: ID of the sender to check

        Returns:
            True if sender is allowed, False otherwise
        """
        if sender_id in self._blacklist:
            return False
        if self._whitelist is not None:
            return sender_id in self._whitelist
        return True  # No whitelist means all senders are allowed

    @overload
    def register(self, handler: HandlerType) -> HandlerType:
        """
        Overload for decorator without parameters.
        Usage: @topic.register
        """
        ...

    @overload
    def register(
        self,
        *,
        aliases: Optional[List[str]] = None,
        priority: int = 0,
        transactional: bool = False,
        generic: bool = False,
    ) -> Callable[[HandlerType], HandlerType]:
        """
        Overload for decorator with parameters.
        Usage: @topic.register(priority=100)
        """
        ...

    def register(
        self,
        handler: Optional[HandlerType] = None,
        *,
        aliases: Optional[List[str]] = None,
        priority: int = 0,
        transactional: bool = False,
        generic: bool = False,
    ) -> Union[HandlerType, Callable[[HandlerType], HandlerType]]:
        """
        Decorator for registering event handlers.

        Supports two usage patterns:
        1. Without parameters: @topic.register
        2. With parameters: @topic.register(priority=100, transactional=True)

        Args:
            handler: The handler function (for direct decoration)
            aliases: Alternative names for the handler
            priority: Execution priority (higher = earlier)
            transactional: Whether to execute in a transaction
            generic: Whether the handler accepts any event type

        Returns:
            The original handler function (for decoration chaining)
        """
        # Case 1: Decorator called without parameters (@topic.register)
        if handler is not None:
            return self._register_handler(
                handler, aliases, priority, transactional, generic
            )

        # Case 2: Decorator called with parameters (@topic.register(priority=100))
        def decorator(func: HandlerType) -> HandlerType:
            return self._register_handler(
                func, aliases, priority, transactional, generic
            )

        return decorator

    def _register_handler(
        self,
        handler: HandlerType,
        aliases: Optional[List[str]] = None,
        priority: int = 0,
        transactional: bool = False,
        generic: bool = False,
    ) -> HandlerType:
        """
        Internal method to register a handler with the topic.

        Args:
            handler: The handler function to register
            aliases: Alternative names for the handler
            priority: Execution priority
            transactional: Whether to execute in a transaction
            generic: Whether the handler accepts any event type

        Returns:
            The original handler function with metadata
        """
        if self._debug:
            logger.debug(
                f"Registering handler '{handler.__name__}' for {self._full_id} "
                f"(priority={priority}, transactional={transactional})"
            )

        # Create handler wrapper with error handling
        handler_wrapper = self._create_handler_wrapper(handler, transactional)

        # Create topic handler with metadata
        topic_handler = cast("BaseTopicHandler", {
            "handler": handler_wrapper,
            "name": handler.__name__,
            "aliases": aliases or [],
            "priority": priority,
            "generic": generic,
            "is_async": asyncio.iscoroutinefunction(handler)
        })

        # Insert handler maintaining priority order
        self._insert_handler_by_priority(topic_handler)

        # Create sender closure for use within handlers
        sender_closure = self._create_sender_closure(handler.__name__, generic)
        self._register_sender(sender_closure, handler.__name__)

        # Add metadata to the original handler for debugging
        handler._topic_registered = True
        handler._topic_id = self._full_id
        handler._topic_priority = priority

        return handler

    def _create_handler_wrapper(
        self, handler: HandlerType, transactional: bool
    ) -> Callable[[Any], None]:
        """Create a wrapper that adds error handling to the handler"""
        is_async = asyncio.iscoroutinefunction(handler)

        @wraps(handler)
        def sync_wrapper(event_data: Any) -> None:
            start_time = time.perf_counter()
            try:
                if transactional and self._broker and hasattr(self._broker, "transaction"):
                    with self._broker.transaction():
                        result = handler(event_data)
                else:
                    result = handler(event_data)

                # Handle async results in sync context
                if is_async:
                    asyncio.ensure_future(result)

                # Update metrics
                self._update_metrics(
                    success=True, latency=time.perf_counter() - start_time
                )

            except Exception as e:
                self._update_metrics(success=False)
                self._handle_error(e, event_data)
                if self.error_strategy == ErrorStrategy.RAISE:
                    raise TopicProcessingError(
                        f"Critical error in topic '{self._full_id}' handler"
                    ) from e

        async def async_wrapper(event_data: Any) -> None:
            start_time = time.perf_counter()
            try:
                if transactional and self._broker and hasattr(self._broker, "transaction"):
                    async with self._broker.transaction():
                        await handler(event_data)
                else:
                    await handler(event_data)

                # Update metrics
                self._update_metrics(
                    success=True, latency=time.perf_counter() - start_time
                )

            except Exception as e:
                self._update_metrics(success=False)
                self._handle_error(e, event_data)
                if self.error_strategy == ErrorStrategy.RAISE:
                    raise TopicProcessingError(
                        f"Critical error in topic '{self._full_id}' handler"
                    ) from e

        return async_wrapper if is_async else sync_wrapper

    def _insert_handler_by_priority(self, new_handler: "BaseTopicHandler") -> None:
        """Insert handler maintaining priority order (descending)"""
        for i, handler in enumerate(self._handlers):
            if new_handler["priority"] > handler["priority"]:
                self._handlers.insert(i, new_handler)
                return
        self._handlers.append(new_handler)

    def _create_sender_closure(
        self, handler_name: str, generic: bool
    ) -> Callable[..., "TopicMessage"]:
        """Create a closure for sending messages from handlers"""

        def sender(data: Any = None, **kwargs) -> "TopicMessage":
            """Send a message to the topic"""
            if not self._broker:
                error_msg = f"No broker assigned to topic {self._full_id}. Cannot send message."
                self._handle_error(RuntimeError(error_msg), None)
                # Create a dummy message for consistency
                return cast("TopicMessage", {"sender": "system", "data": None})

            message = cast("TopicMessage", {
                "sender": f"{self._full_id}.{handler_name}",
                "data": data,
                "destination": handler_name,
                "message_type": "generic" if generic else handler_name,
                **kwargs
            })

            self._broker.publish(self._id, message)
            if self._debug:
                logger.debug(f"Message sent to {self._id}: {message}")

            return message

        return sender

    def _register_sender(self, func: Callable, name: str) -> None:
        """Register sender function as a safe attribute"""
        if hasattr(self, name):
            raise AttributeError(
                f"Attribute '{name}' already exists in topic {self._full_id}"
            )
        setattr(self, name, func)

    def publish_event(self, event: "TopicMessage") -> None:
        """
        Publish an event to the topic.

        Args:
            event: The event/message to publish
        """
        if not self.is_sender_allowed(event["sender"]):
            error_msg = (
                f"Sender '{event['sender']}' blocked by security policy "
                f"in topic '{self._full_id}'"
            )
            self._handle_error(PermissionError(error_msg), event)
            return

        if self._debug:
            logger.debug(f"Event published to {self._full_id}: {event}")

        self.handle_event(event)

    def handle_event(self, event: "TopicMessage") -> None:
        """
        Handle an incoming event by processing all registered handlers.

        Args:
            event: The event to process
        """
        for handler in self._handlers:

            if event.get("destination") != handler["name"] and event.get("destination") not in handler["aliases"] and not handler["generic"]:
                continue  # Skip handlers not matching the destination or not generic
            try:
                if handler["is_async"]:
                    asyncio.create_task(handler["handler"](event["data"]))
                else:
                    handler["handler"](event["data"])
            except Exception as e:
                self._handle_error(e, event["data"])
                if self.error_strategy == ErrorStrategy.RAISE:
                    break  # Stop processing if critical

    def _handle_error(self, exc: Exception, event_data: Any) -> None:
        """Handle errors according to the configured strategy"""
        # Add to Dead Letter Queue
        try:
            self._dead_letters.put_nowait((exc, event_data))
        except queue.Full:
            pass  # Queue is full, ignore

        # Execute error strategy
        if self.error_strategy == ErrorStrategy.CUSTOM and self.error_handler:
            try:
                self.error_handler(exc, event_data)
            except Exception as e:
                logger.critical(
                    f"Error in custom error handler for topic '{self._full_id}': {str(e)}"
                )
        else:
            self._default_error_handler(exc, event_data)

    def _default_error_handler(self, exc: Exception, event_data: Any) -> None:
        """Default error handling behavior"""
        if self.error_strategy == ErrorStrategy.RAISE:
            raise TopicProcessingError(
                f"Critical error in topic '{self._full_id}': {str(exc)}"
            ) from exc
        elif self.error_strategy == ErrorStrategy.WARN:
            logger.warning(
                f"Non-critical error in topic '{self._full_id}': {str(exc)}"
            )

    def _update_metrics(self, success: bool, latency: float = 0.0) -> None:
        """Update performance metrics"""
        self._metrics["events_processed"] += 1
        self._metrics["last_processed"] = time.time()

        if success:
            # Update latency average (exponential moving average)
            alpha = 0.2  # Smoothing factor
            self._metrics["latency_avg"] = (
                alpha * latency
                + (1 - alpha) * self._metrics["latency_avg"]
            )

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for monitoring.

        Returns:
            Dictionary containing topic metrics
        """
        return {
            **self._metrics,
            "id": self._full_id,
            "handler_count": len(self._handlers),
            "error_rate": self._metrics["errors"]
            / max(1, self._metrics["events_processed"]),
        }

    def get_dead_letters(self) -> List[Tuple[Exception, Any]]:
        """
        Get failed events for debugging.

        Returns:
            List of (exception, event_data) tuples
        """
        return list(self._dead_letters.queue)

    def add_to_blacklist(self, sender_id: str) -> None:
        """
        Add a sender to the blacklist.

        Args:
            sender_id: ID to blacklist
        """
        if sender_id not in self._blacklist:
            self._blacklist.add(sender_id)
            if self._debug:
                logger.debug(f"Added '{sender_id}' to blacklist of {self._full_id}")

    def remove_from_blacklist(self, sender_id: str) -> None:
        """
        Remove a sender from the blacklist.

        Args:
            sender_id: ID to remove from blacklist
        """
        if sender_id in self._blacklist:
            self._blacklist.remove(sender_id)
            if self._debug:
                logger.debug(
                    f"Removed '{sender_id}' from blacklist of {self._full_id}"
                )

    def add_to_whitelist(self, sender_id: str) -> None:
        """
        Add a sender to the whitelist.

        Args:
            sender_id: ID to whitelist
        """
        if self._whitelist is None:
            self._whitelist = set()
        if sender_id not in self._whitelist:
            self._whitelist.add(sender_id)
            if self._debug:
                logger.debug(f"Added '{sender_id}' to whitelist of {self._full_id}")

    def remove_from_whitelist(self, sender_id: str) -> None:
        """
        Remove a sender from the whitelist.

        Args:
            sender_id: ID to remove from whitelist
        """
        if self._whitelist and sender_id in self._whitelist:
            self._whitelist.remove(sender_id)
            if self._debug:
                logger.debug(
                    f"Removed '{sender_id}' from whitelist of {self._full_id}"
                )

    @property
    def full_id(self) -> str:
        """Get the full topic ID with version (e.g., 'orders/new@1.0.0')"""
        return self._full_id

    @property
    def active_handlers(self) -> List[Dict[str, Any]]:
        """
        Get a copy of all active handlers.

        Returns:
            List of handler metadata dictionaries
        """
        return [
            {
                "name": h["name"],
                "priority": h["priority"],
                "aliases": h["aliases"],
                "generic": h["generic"],
            }
            for h in self._handlers
        ]

    def get_handler(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a handler by name or alias.

        Args:
            name: Handler name or alias

        Returns:
            Handler metadata if found, None otherwise
        """
        for handler in self._handlers:
            if name == handler["name"] or name in handler["aliases"]:
                return {
                    "name": handler["name"],
                    "priority": handler["priority"],
                    "aliases": handler["aliases"],
                    "generic": handler["generic"],
                }
        return None