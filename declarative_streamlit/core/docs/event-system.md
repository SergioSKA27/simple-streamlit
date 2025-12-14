# Event System Documentation

## Overview

The `logic` submodule implements a sophisticated event-driven architecture based on the publish-subscribe (pub/sub) pattern. It enables decoupled communication between components through a robust topic-based messaging system with priority handlers, error strategies, security controls, and performance monitoring.

## Module Structure

```
logic/
├── __init__.py
├── broker.py         # Message broker (central hub)
├── topic.py          # Topic implementation (pub/sub channels)
├── event.py          # Event abstraction
└── message.py        # Message type definition
```

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────┐
│                  Application                     │
│  ┌────────────┐         ┌────────────┐         │
│  │ Publisher  │         │ Subscriber │         │
│  │ Component  │         │ Component  │         │
│  └──────┬─────┘         └─────▲──────┘         │
│         │                     │                 │
│         │ publish()    handle()│                │
│         ▼                     │                 │
│  ┌──────────────────────────────────┐          │
│  │         BaseBroker                │          │
│  │  ┌────────────────────────────┐  │          │
│  │  │  Topics Dictionary         │  │          │
│  │  │  ┌──────────┐ ┌──────────┐│  │          │
│  │  │  │ Topic 1  │ │ Topic 2  ││  │          │
│  │  │  │          │ │          ││  │          │
│  │  │  │ Handlers │ │ Handlers ││  │          │
│  │  │  │  [...]   │ │  [...]   ││  │          │
│  │  │  └──────────┘ └──────────┘│  │          │
│  │  └────────────────────────────┘  │          │
│  └──────────────────────────────────┘          │
└─────────────────────────────────────────────────┘
```

### Message Flow

```
1. Publisher sends message to broker
        │
        ▼
2. Broker routes to appropriate topic
        │
        ▼
3. Topic validates sender (security check)
        │
        ▼
4. Topic executes handlers by priority
        │
        ▼
5. Each handler processes message data
        │
        ▼
6. Errors handled per strategy
        │
        ▼
7. Metrics updated
```

---

## TopicMessage

**Location**: `core/logic/message.py`

### Purpose

`TopicMessage` defines the structure for messages passed through the event system. It's a type alias for a dictionary with standardized fields.

### Type Definition

```python
from typing import Dict, Any

TopicMessage = Dict[str, Any]
```

### Message Structure

**Required Fields**:
- `sender` (str): Identifier of message sender
- `data` (Any): Message payload

**Optional Fields**:
- `destination` (str): Target handler name
- `message_type` (str): Message classification
- `timestamp` (float): Message creation time
- `priority` (int): Message priority
- `metadata` (dict): Additional contextual data

### Message Examples

**Basic Message**:
```python
message: TopicMessage = {
    "sender": "filter_component",
    "data": {"selected_months": ["Jan", "Feb", "Mar"]}
}
```

**Full Message**:
```python
message: TopicMessage = {
    "sender": "user_dashboard",
    "data": {"user_id": 12345, "action": "view_report"},
    "destination": "analytics_handler",
    "message_type": "user_action",
    "timestamp": 1702563421.123,
    "priority": 5,
    "metadata": {
        "session_id": "abc123",
        "source_page": "dashboard"
    }
}
```

---

## BaseEvent

**Location**: `core/logic/event.py`

### Purpose

`BaseEvent` is an abstract base class for event implementations. It provides the foundation for creating typed events with handler management.

### Class Definition

```python
class BaseEvent(ABC):
    """
    Abstract base class for events.
    
    An event represents a significant occurrence within a topic
    that can trigger registered handlers.
    """
```

### Constructor

```python
def __init__(
    self,
    name: str,
    topic: "BaseTopic",
    priority: int = 1,
    alias: Optional[str] = None,
    allow_broadcast: bool = False
):
    """
    Initialize event.
    
    Args:
        name (str): Event name (unique within topic)
        topic (BaseTopic): Parent topic
        priority (int): Default priority for event (default: 1)
        alias (Optional[str]): Alternative name
        allow_broadcast (bool): If True, can broadcast to all subscribers
        
    Attributes:
        name (str): Event identifier
        topic (BaseTopic): Owning topic
        priority (int): Execution priority
        alias (Optional[str]): Alternative identifier
        allow_broadcast (bool): Broadcasting flag
        _handlers (List): Registered handlers
    """
```

### Abstract Methods

#### trigger()

**Signature**:
```python
@abstractmethod
def trigger(self, message: Dict[str, Any]) -> None:
    """
    Trigger the event with data.
    
    Args:
        message: Event message data
        
    Raises:
        NotImplementedError: Must be implemented by subclass
    """
```

**Purpose**: Subclasses implement specific triggering logic.

---

## BaseTopic

**Location**: `core/logic/topic.py`

### Purpose

`BaseTopic` implements a publish-subscribe topic with priority-based handler execution, security controls, error strategies, and performance monitoring.

### Class Definition

```python
class BaseTopic:
    """
    Topic implementation for event-driven architecture.
    
    Features:
    - Decorator-based handler registration
    - Priority-based execution
    - Error strategies (RAISE, WARN, IGNORE, CUSTOM)
    - Blacklist/whitelist security
    - Dead Letter Queue for debugging
    - Performance metrics tracking
    - Async/await support
    """
```

### Error Strategies

```python
class ErrorStrategy(Enum):
    """Error handling strategies."""
    
    RAISE = "raise"      # Raise exception immediately
    WARN = "warn"        # Log warning and continue
    IGNORE = "ignore"    # Silently ignore errors
    CUSTOM = "custom"    # Use custom error handler
```

### Constructor

```python
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
    Initialize topic.
    
    Args:
        _id (str): Unique topic identifier
        version (str): Semantic version (default: "1.0.0")
        error_strategy (ErrorStrategy): Error handling approach
        error_handler (Optional[Callable]): Custom error handler
        blacklist (Optional[List[str]]): Blocked sender IDs
        whitelist (Optional[List[str]]): Allowed sender IDs (None = all allowed)
        max_dead_letters (int): Max failed events to retain
        broker (Optional[BaseBroker]): Parent broker
        debug (bool): Enable debug logging
        
    Attributes:
        _id (str): Topic identifier
        version (str): Version string
        _full_id (str): "<_id>@<version>"
        error_strategy (ErrorStrategy): Error handling mode
        error_handler (Optional[Callable]): Custom handler
        _debug (bool): Debug flag
        _blacklist (Set[str]): Blocked senders (O(1) lookup)
        _whitelist (Optional[Set[str]]): Allowed senders
        _handlers (List[BaseTopicHandler]): Registered handlers
        _metrics (Dict): Performance metrics
        _dead_letters (Queue): Failed event queue
        _broker (Optional[BaseBroker]): Parent broker
    """
```

**Initialization**:
```python
self._id = _id
self.version = version
self._full_id = f"{_id}@{version}"
self.error_strategy = error_strategy
self.error_handler = error_handler
self._debug = debug

# Security (O(1) set lookups)
self._blacklist: Set[str] = set(blacklist or [])
self._whitelist: Optional[Set[str]] = set(whitelist) if whitelist else None

# Handlers (priority-ordered list)
self._handlers: List = []

# Metrics
self._metrics = {
    "events_processed": 0,
    "errors": 0,
    "last_processed": None,
    "latency_avg": 0.0,  # Exponential moving average
}

# Dead letter queue
self._dead_letters = queue.Queue(maxsize=max_dead_letters)

self._broker = broker
```

### Handler Registration

#### register() (Decorator)

**Signatures**:
```python
# Overload 1: Direct decoration
@overload
def register(self, handler: HandlerType) -> HandlerType:
    """Usage: @topic.register"""
    ...

# Overload 2: Parametrized decoration
@overload
def register(
    self,
    *,
    aliases: Optional[List[str]] = None,
    priority: int = 0,
    transactional: bool = False,
    generic: bool = False,
) -> Callable[[HandlerType], HandlerType]:
    """Usage: @topic.register(priority=100)"""
    ...
```

**Implementation**:
```python
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
    
    Args:
        handler: Handler function (for direct decoration)
        aliases: Alternative names for the handler
        priority: Execution priority (higher = earlier)
        transactional: Whether to execute in transaction
        generic: Whether handler accepts any event type
        
    Returns:
        Decorated handler or decorator function
        
    Behavior:
        - Creates wrapper with error handling
        - Adds to handlers list (priority-ordered)
        - Creates sender closure for handler
        - Adds metadata to handler function
    """
    
    # Case 1: Direct decoration (@topic.register)
    if handler is not None:
        return self._register_handler(
            handler, aliases, priority, transactional, generic
        )

    # Case 2: Parametrized (@topic.register(priority=100))
    def decorator(func: HandlerType) -> HandlerType:
        return self._register_handler(
            func, aliases, priority, transactional, generic
        )

    return decorator
```

**Usage Examples**:
```python
# Direct decoration
@topic.register
def simple_handler(data):
    st.write(data)

# With priority
@topic.register(priority=100)
def high_priority_handler(data):
    validate(data)

# With aliases
@topic.register(aliases=["alt_name"], priority=50)
def named_handler(data):
    process(data)

# Generic handler (receives all events)
@topic.register(generic=True)
def catch_all_handler(data):
    log(data)

# Async handler
@topic.register(priority=75)
async def async_handler(data):
    await async_process(data)
```

#### _register_handler() (Internal)

**Signature**:
```python
def _register_handler(
    self,
    handler: HandlerType,
    aliases: Optional[List[str]] = None,
    priority: int = 0,
    transactional: bool = False,
    generic: bool = False,
) -> HandlerType:
    """
    Internal handler registration logic.
    
    Process:
        1. Create error-wrapped handler
        2. Build handler metadata dict
        3. Insert by priority (maintains order)
        4. Create sender closure
        5. Add metadata to function
        
    Returns:
        Original handler with metadata
    """
```

**Handler Metadata**:
```python
topic_handler = {
    "handler": wrapped_function,
    "name": handler.__name__,
    "aliases": aliases or [],
    "priority": priority,
    "generic": generic,
    "is_async": asyncio.iscoroutinefunction(handler)
}
```

**Function Metadata**:
```python
handler._topic_registered = True
handler._topic_id = self._full_id
handler._topic_priority = priority
```

### Message Publishing

#### publish_event()

**Signature**:
```python
def publish_event(self, event: TopicMessage) -> None:
    """
    Publish event to topic.
    
    Args:
        event: Message to publish
        
    Process:
        1. Validate sender (security check)
        2. Log if debug enabled
        3. Delegate to handle_event()
        
    Security:
        Checks blacklist/whitelist before processing
    """
```

**Implementation**:
```python
def publish_event(self, event: TopicMessage) -> None:
    # Security check
    if not self.is_sender_allowed(event["sender"]):
        error_msg = (
            f"Sender '{event['sender']}' blocked by security policy "
            f"in topic '{self._full_id}'"
        )
        self._handle_error(PermissionError(error_msg), event)
        return

    # Debug logging
    if self._debug:
        logger.debug(f"Event published to {self._full_id}: {event}")

    # Process event
    self.handle_event(event)
```

#### handle_event()

**Signature**:
```python
def handle_event(self, event: TopicMessage) -> None:
    """
    Process event by executing handlers.
    
    Args:
        event: Message to process
        
    Process:
        For each handler (in priority order):
        1. Check if handler should process (destination/generic)
        2. Execute handler (sync or async)
        3. Handle errors per strategy
        4. Stop if critical error and RAISE strategy
    """
```

**Implementation**:
```python
def handle_event(self, event: TopicMessage) -> None:
    for handler in self._handlers:
        # Filter handlers
        destination = event.get("destination")
        if (destination != handler["name"] and 
            destination not in handler["aliases"] and 
            not handler["generic"]):
            continue  # Skip this handler
        
        try:
            # Execute based on type
            if handler["is_async"]:
                asyncio.create_task(handler["handler"](event["data"]))
            else:
                handler["handler"](event["data"])
        except Exception as e:
            self._handle_error(e, event["data"])
            if self.error_strategy == ErrorStrategy.RAISE:
                break  # Stop on critical errors
```

### Security Controls

#### is_sender_allowed()

**Signature**:
```python
def is_sender_allowed(self, sender_id: str) -> bool:
    """
    Check if sender can publish to topic.
    
    Args:
        sender_id: Sender identifier
        
    Returns:
        bool: True if allowed, False if blocked
        
    Logic:
        1. If in blacklist → False
        2. If whitelist exists and not in whitelist → False
        3. Otherwise → True
        
    Performance:
        O(1) via set lookups
    """
```

**Implementation**:
```python
def is_sender_allowed(self, sender_id: str) -> bool:
    if sender_id in self._blacklist:
        return False
    if self._whitelist is not None:
        return sender_id in self._whitelist
    return True  # No whitelist = all allowed
```

#### add_to_blacklist() / remove_from_blacklist()

**Signatures**:
```python
def add_to_blacklist(self, sender_id: str) -> None:
    """Block a sender."""
    if sender_id not in self._blacklist:
        self._blacklist.add(sender_id)

def remove_from_blacklist(self, sender_id: str) -> None:
    """Unblock a sender."""
    if sender_id in self._blacklist:
        self._blacklist.remove(sender_id)
```

#### add_to_whitelist() / remove_from_whitelist()

**Signatures**:
```python
def add_to_whitelist(self, sender_id: str) -> None:
    """Add sender to whitelist."""
    if self._whitelist is None:
        self._whitelist = set()
    if sender_id not in self._whitelist:
        self._whitelist.add(sender_id)

def remove_from_whitelist(self, sender_id: str) -> None:
    """Remove sender from whitelist."""
    if self._whitelist and sender_id in self._whitelist:
        self._whitelist.remove(sender_id)
```

### Error Handling

#### _handle_error()

**Signature**:
```python
def _handle_error(self, exc: Exception, event_data: Any) -> None:
    """
    Handle errors per configured strategy.
    
    Args:
        exc: Exception that occurred
        event_data: Data being processed when error occurred
        
    Process:
        1. Add to dead letter queue
        2. Execute strategy:
           - CUSTOM: Call custom handler
           - RAISE/WARN/IGNORE: Default handler
    """
```

**Implementation**:
```python
def _handle_error(self, exc: Exception, event_data: Any) -> None:
    # Add to dead letters
    try:
        self._dead_letters.put_nowait((exc, event_data))
    except queue.Full:
        pass  # Queue full, discard

    # Execute strategy
    if self.error_strategy == ErrorStrategy.CUSTOM and self.error_handler:
        try:
            self.error_handler(exc, event_data)
        except Exception as e:
            logger.critical(
                f"Error in custom handler for '{self._full_id}': {e}"
            )
    else:
        self._default_error_handler(exc, event_data)
```

#### _default_error_handler()

**Signature**:
```python
def _default_error_handler(self, exc: Exception, event_data: Any) -> None:
    """
    Default error handling.
    
    Strategies:
        - RAISE: Raise TopicProcessingError
        - WARN: Log warning
        - IGNORE: Do nothing
    """
```

### Metrics

#### _update_metrics()

**Signature**:
```python
def _update_metrics(self, success: bool, latency: float = 0.0) -> None:
    """
    Update performance metrics.
    
    Args:
        success: Whether processing succeeded
        latency: Processing time in seconds
        
    Updates:
        - events_processed: Total count
        - errors: Error count (if not success)
        - last_processed: Timestamp
        - latency_avg: Exponential moving average
    """
```

**Implementation**:
```python
def _update_metrics(self, success: bool, latency: float = 0.0) -> None:
    self._metrics["events_processed"] += 1
    self._metrics["last_processed"] = time.time()

    if not success:
        self._metrics["errors"] += 1
    else:
        # Exponential moving average
        alpha = 0.2
        self._metrics["latency_avg"] = (
            alpha * latency
            + (1 - alpha) * self._metrics["latency_avg"]
        )
```

#### get_metrics()

**Signature**:
```python
def get_metrics(self) -> Dict[str, Any]:
    """
    Get performance metrics.
    
    Returns:
        dict: {
            "id": str,
            "events_processed": int,
            "errors": int,
            "last_processed": float (timestamp),
            "latency_avg": float (seconds),
            "handler_count": int,
            "error_rate": float (0-1)
        }
    """
```

#### get_dead_letters()

**Signature**:
```python
def get_dead_letters(self) -> List[Tuple[Exception, Any]]:
    """
    Get failed events for debugging.
    
    Returns:
        List of (exception, event_data) tuples
    """
```

### Properties

#### full_id

**Signature**:
```python
@property
def full_id(self) -> str:
    """Get full topic ID with version (e.g., 'filters@1.0.0')"""
    return self._full_id
```

#### active_handlers

**Signature**:
```python
@property
def active_handlers(self) -> List[Dict[str, Any]]:
    """
    Get handler metadata (without actual functions).
    
    Returns:
        List of dicts with: name, priority, aliases, generic
    """
```

#### get_handler()

**Signature**:
```python
def get_handler(self, name: str) -> Optional[Dict[str, Any]]:
    """
    Get handler metadata by name or alias.
    
    Args:
        name: Handler name or alias
        
    Returns:
        Handler metadata dict or None
    """
```

---

## BaseBroker

**Location**: `core/logic/broker.py`

### Purpose

`BaseBroker` acts as the central message router, managing multiple topics and routing messages between publishers and subscribers.

### Class Definition

```python
class BaseBroker:
    """
    Message broker for topic management.
    
    Manages:
    - Topic registration
    - Message routing
    - Topic lifecycle
    """
```

### Constructor

```python
def __init__(self, name: str = "broker", debug: bool = False) -> None:
    """
    Initialize broker.
    
    Args:
        name (str): Broker identifier
        debug (bool): Enable debug logging
        
    Attributes:
        _name (str): Broker name
        _debug (bool): Debug flag
        _topics (Dict[str, BaseTopic]): Topic registry
    """
```

### Topic Management

#### create_topic()

**Signature**:
```python
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
) -> BaseTopic:
    """
    Create and register new topic.
    
    Args:
        _id: Topic identifier
        version: Semantic version
        error_strategy: Error handling strategy
        error_handler: Custom error handler
        blacklist: Blocked sender IDs
        whitelist: Allowed sender IDs
        max_dead_letters: Dead letter queue size
        debug: Debug logging
        
    Returns:
        BaseTopic: Created topic instance
        
    Side Effects:
        - Topic added to _topics dict
        - Topic set as broker attribute
    """
```

**Implementation**:
```python
def create_topic(self, _id, version="1.0.0", **kwargs) -> BaseTopic:
    topic = BaseTopic(
        _id,
        version=version,
        broker=self,
        **kwargs
    )
    self._register_topic(topic)
    return topic
```

#### subscribe()

**Signature**:
```python
def subscribe(self, topic: BaseTopic) -> None:
    """
    Subscribe existing topic to broker.
    
    Args:
        topic: Topic instance to register
        
    Side Effects:
        - Sets topic._broker = self
        - Registers topic
    """
```

#### _register_topic()

**Signature**:
```python
def _register_topic(self, topic: BaseTopic) -> None:
    """
    Internal topic registration.
    
    Args:
        topic: Topic to register
        
    Side Effects:
        - Adds to _topics dict
        - Sets as broker attribute
    """
```

**Implementation**:
```python
def _register_topic(self, topic: BaseTopic) -> None:
    self._topics[topic._id] = topic
    setattr(self, topic._id, topic)
```

**Usage**:
```python
broker = BaseBroker()
broker.create_topic("filters")

# Now accessible as attribute
broker.filters.register(handler)
```

### Message Routing

#### publish()

**Signature**:
```python
def publish(self, topic_id: str, message: TopicMessage) -> None:
    """
    Publish message to topic.
    
    Args:
        topic_id: Target topic identifier
        message: Message to publish
        
    Raises:
        ValueError: If topic not found
        
    Process:
        1. Lookup topic by ID
        2. Delegate to topic.publish_event()
    """
```

**Implementation**:
```python
def publish(self, topic_id: str, message: TopicMessage) -> None:
    topic = self._get_topic(topic_id)
    if topic:
        topic.publish_event(message)
    else:
        raise ValueError(f"Topic '{topic_id}' not found")
```

#### _get_topic()

**Signature**:
```python
def _get_topic(self, topic_id: str) -> Optional[BaseTopic]:
    """
    Retrieve topic by ID.
    
    Args:
        topic_id: Topic identifier
        
    Returns:
        BaseTopic or None
    """
```

---

## Usage Examples

### Example 1: Basic Pub/Sub

```python
from declarative_streamlit.core.logic import BaseBroker, TopicMessage

# Create broker
broker = BaseBroker(debug=True)

# Create topic
filters_topic = broker.create_topic("filters")

# Register handler
@filters_topic.register
def update_chart(data):
    st.write(f"Updating chart with: {data}")

# Publish message
message: TopicMessage = {
    "sender": "filter_ui",
    "data": {"months": ["Jan", "Feb"]}
}
broker.publish("filters", message)
```

### Example 2: Priority Handlers

```python
topic = broker.create_topic("data_processing")

# High priority - validation
@topic.register(priority=100)
def validate_data(data):
    if not data:
        raise ValueError("Empty data")
    st.success("Data validated")

# Medium priority - transformation
@topic.register(priority=50)
def transform_data(data):
    transformed = [x * 2 for x in data]
    st.write(f"Transformed: {transformed}")

# Low priority - logging
@topic.register(priority=1)
def log_data(data):
    logger.info(f"Processed: {data}")

# Handlers execute: validate → transform → log
message: TopicMessage = {
    "sender": "processor",
    "data": [1, 2, 3]
}
broker.publish("data_processing", message)
```

### Example 3: Error Strategies

```python
# Strategy 1: RAISE (default)
strict_topic = broker.create_topic(
    "strict",
    error_strategy=ErrorStrategy.RAISE
)

@strict_topic.register
def strict_handler(data):
    raise ValueError("Critical error")
    # Raises TopicProcessingError, stops execution

# Strategy 2: WARN
lenient_topic = broker.create_topic(
    "lenient",
    error_strategy=ErrorStrategy.WARN
)

@lenient_topic.register
def lenient_handler(data):
    raise ValueError("Non-critical error")
    # Logs warning, continues

# Strategy 3: CUSTOM
def custom_error_handler(exc, data):
    st.error(f"Error: {exc}")
    st.write(f"Failed data: {data}")

custom_topic = broker.create_topic(
    "custom",
    error_strategy=ErrorStrategy.CUSTOM,
    error_handler=custom_error_handler
)

@custom_topic.register
def custom_handler(data):
    raise ValueError("Custom handling")
    # Calls custom_error_handler
```

### Example 4: Security Controls

```python
topic = broker.create_topic("secure")

# Blacklist specific sender
topic.add_to_blacklist("malicious_sender")

# Or use whitelist (only allowed senders)
topic.add_to_whitelist("trusted_sender_1")
topic.add_to_whitelist("trusted_sender_2")

@topic.register
def secure_handler(data):
    st.write(f"Processing: {data}")

# This will be blocked
blocked_msg: TopicMessage = {
    "sender": "malicious_sender",
    "data": "bad data"
}
topic.publish_event(blocked_msg)  # Blocked, handler not called

# This will work
allowed_msg: TopicMessage = {
    "sender": "trusted_sender_1",
    "data": "good data"
}
topic.publish_event(allowed_msg)  # Handler called
```

### Example 5: Async Handlers

```python
topic = broker.create_topic("async_topic")

@topic.register(priority=100)
async def async_handler(data):
    await asyncio.sleep(1)
    st.write(f"Async processed: {data}")

@topic.register(priority=50)
def sync_handler(data):
    st.write(f"Sync processed: {data}")

# Both execute, async runs concurrently
message: TopicMessage = {
    "sender": "async_publisher",
    "data": {"value": 42}
}
broker.publish("async_topic", message)
```

### Example 6: Generic Handlers

```python
topic = broker.create_topic("events")

# Specific handlers
@topic.register(aliases=["user_login"])
def handle_login(data):
    st.write(f"User logged in: {data['username']}")

@topic.register(aliases=["user_logout"])
def handle_logout(data):
    st.write(f"User logged out: {data['username']}")

# Generic handler (catches all)
@topic.register(generic=True, priority=1)
def log_all_events(data):
    logger.info(f"Event occurred: {data}")

# Targeted message
login_msg: TopicMessage = {
    "sender": "auth_system",
    "data": {"username": "john"},
    "destination": "user_login"
}
broker.publish("events", login_msg)
# Calls: handle_login, log_all_events

# Generic message
other_msg: TopicMessage = {
    "sender": "system",
    "data": {"action": "something"}
}
broker.publish("events", other_msg)
# Calls: log_all_events only
```

### Example 7: Performance Monitoring

```python
topic = broker.create_topic("monitored")

@topic.register
def slow_handler(data):
    import time
    time.sleep(0.5)
    return data

# Process messages
for i in range(10):
    message: TopicMessage = {
        "sender": "test",
        "data": i
    }
    broker.publish("monitored", message)

# Check metrics
metrics = topic.get_metrics()
print(f"Events processed: {metrics['events_processed']}")
print(f"Average latency: {metrics['latency_avg']:.4f}s")
print(f"Error rate: {metrics['error_rate']:.2%}")
print(f"Handler count: {metrics['handler_count']}")
```

### Example 8: Dead Letter Queue

```python
topic = broker.create_topic(
    "dlq_topic",
    error_strategy=ErrorStrategy.WARN,
    max_dead_letters=50
)

@topic.register
def failing_handler(data):
    if data % 2 == 0:
        raise ValueError(f"Even number not allowed: {data}")
    st.write(f"Processed: {data}")

# Process mixed data
for i in range(10):
    message: TopicMessage = {
        "sender": "test",
        "data": i
    }
    broker.publish("dlq_topic", message)

# Check dead letters
dead = topic.get_dead_letters()
print(f"Failed events: {len(dead)}")
for exc, data in dead:
    print(f"Error: {exc}, Data: {data}")
```

---

## Best Practices

### 1. Use Descriptive Topic Names

```python
# ❌ Bad
topic = broker.create_topic("t1")

# ✅ Good
topic = broker.create_topic("user_authentication")
```

### 2. Set Appropriate Priorities

```python
# ✅ Good - logical priority order
@topic.register(priority=100)  # Validation first
def validate(data): ...

@topic.register(priority=50)   # Processing second
def process(data): ...

@topic.register(priority=1)    # Logging last
def log(data): ...
```

### 3. Choose Right Error Strategy

```python
# Critical operations - RAISE
payment_topic = broker.create_topic(
    "payments",
    error_strategy=ErrorStrategy.RAISE
)

# Analytics - WARN or IGNORE
analytics_topic = broker.create_topic(
    "analytics",
    error_strategy=ErrorStrategy.WARN
)
```

### 4. Use Whitelists for Security

```python
# Sensitive topics - whitelist
sensitive = broker.create_topic("admin_actions")
sensitive.add_to_whitelist("admin_user")
sensitive.add_to_whitelist("super_admin")
# Only these can publish
```

### 5. Monitor Performance

```python
# Check metrics regularly
metrics = topic.get_metrics()
if metrics["error_rate"] > 0.1:  # More than 10% errors
    st.warning("High error rate detected!")
```

---

## Performance Considerations

### Handler Lookup

Priority-ordered list means O(n) iteration:
```python
# Minimize handlers per topic for best performance
# 10-20 handlers per topic is reasonable
```

### Security Checks

Set-based security provides O(1) lookups:
```python
topic.is_sender_allowed("user_id")  # O(1)
```

### Dead Letter Queue

Fixed-size queue prevents memory growth:
```python
broker.create_topic("topic", max_dead_letters=100)
# Oldest entries discarded when full
```

---

## Common Pitfalls

### 1. Forgetting to Set Destination

```python
# ❌ Wrong - no destination for specific handler
message: TopicMessage = {
    "sender": "app",
    "data": 123
}
# Only generic handlers will receive

# ✅ Correct
message: TopicMessage = {
    "sender": "app",
    "data": 123,
    "destination": "specific_handler"
}
```

### 2. Not Handling Async Properly

```python
# ❌ Wrong - missing await in async context
@topic.register
async def handler(data):
    result = async_function(data)  # Missing await
    
# ✅ Correct
@topic.register
async def handler(data):
    result = await async_function(data)
```

### 3. Circular Dependencies

```python
# ❌ Bad - circular message publishing
@topic1.register
def handler1(data):
    broker.publish("topic2", {"sender": "t1", "data": data})

@topic2.register
def handler2(data):
    broker.publish("topic1", {"sender": "t2", "data": data})
# Creates infinite loop!
```

---

## Type Annotations

```python
from typing import Dict, Any, List, Callable, Optional, Union, NoReturn, Tuple
from enum import Enum

# Message type
TopicMessage = Dict[str, Any]

# Error handler
ErrorHandler = Callable[[Exception, Any], None]

# Event handler
EventHandler = Callable[[Any], Any]

# Handler metadata
BaseTopicHandler = Dict[str, Any]
```

---

## Revision History

| Version | Date       | Changes                          |
|---------|------------|----------------------------------|
| 1.0.0   | 2025-12-14 | Initial documentation            |

---

## See Also

- [Base Classes Documentation](./base-classes.md)
- [Components Documentation](./components.md)
- [Parsers Documentation](./parsers.md)
- [Handlers Documentation](./handlers.md)
- [API Reference](./api-reference.md)
