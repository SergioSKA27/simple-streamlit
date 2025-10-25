from typing import TYPE_CHECKING, Dict, Any, Optional
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .topic import BaseTopic

class BaseEvent(ABC):
    """
    Abstract base class for events.

    An event represents a significant occurrence within a topic that can trigger handlers.
    """

    

    def __init__(self, name: str, topic: "BaseTopic", priority: int = 1,alias: Optional[str] = None,allow_broadcast: bool = False):
        """
        Initialize the event.

        Args:
            name: Name of the event
            topic: The topic this event belongs to
            priority: Priority of the event (higher means more important)
            alias: Optional alias for the event
            allow_broadcast: If True, the event can be broadcasted to all subscribers
        """
        self.name = name
        self.topic = topic
        self.priority = priority
        self.alias = alias
        self.allow_broadcast = allow_broadcast
        self._handlers = []
        
        
