from typing import List, Any, Callable, Union, Sequence

import logging
from ...core.logic.message import TopicMessage
from ...core.logic.broker import BaseBroker
from ...core.logic.topic import Topic




logger = logging.getLogger(__name__)

class SimpleBroker(BaseBroker):


    def publish(self, topic_id: Union[int, str], message: TopicMessage) -> None:
        topic = self.get_topic(topic_id)
        if topic:
            topic.event_listener(message)
        else:
            logger.warning(f"Topic {topic_id} not found for publishing.")

    def add_topic(self, topic: Topic) -> Topic:
        self._topics.append(topic)
        return topic

    def remove_topic(self, topic_id: Union[int, str]) -> None:
        topic = self.get_topic(topic_id)
        if topic:
            self._topics.remove(topic)
        else:
            logger.warning(f"Topic {topic_id} not found for removal.")