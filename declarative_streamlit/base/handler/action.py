from typing import List, Tuple, Any, Callable, Union, Sequence,Optional

from declarative_streamlit.core.logic.broker import BaseBroker

from ...core.logic.topic import Topic
from ...core.logic.message import TopicMessage
from ...core.logic.broker import BaseBroker



class SimpleAction(Topic):

    def __init__(self, _id: Union[int, str],
                  fatal: Optional[bool] = True,
                  allow_global_events: Optional[bool] = False,
                  subscribers: Optional[List[Union[int, str]]] = None,
                  blacklist: Optional[List[Union[int, str]]] = None,
                  multi_handler: Optional[bool] = False,
                  broker: Optional[BaseBroker] = None,
                  debug: Optional[bool] = False):
        super().__init__(_id, fatal, allow_global_events, subscribers, blacklist, multi_handler, broker, debug)
        self._global_handlers: List[Callable[[TopicMessage], None]] = []

    def set_global_handler(self, handler: Callable[[TopicMessage], None]) -> None:
        self._global_handlers.append(handler)