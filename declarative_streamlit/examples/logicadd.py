
import streamlit as st
### Example of Adding Custom Logic

from declarative_streamlit.core.logic.topic import BaseTopic
from declarative_streamlit.core.logic.broker import BaseBroker



from declarative_streamlit.base.app.singleapp import AppPage
from declarative_streamlit.config.common.stdstreamlit import StreamlitCommonStandard


# First we create a custom topic class that inherits from the BaseTopic class

class MyAppLogicTopic(BaseTopic):
    ...



# Then we create an instance of the topic class

my_topic = MyAppLogicTopic("my_topic",debug=True)


# Now you can use the topic instance to register handlers and send messages

@my_topic.register(priority=1, transactional=True)
def echo_handler(message):
    st.write(f"Echo handler received message: {message}")

# Let's register another handler with different priority
@my_topic.register(priority=2,)
def another_handler(message):
    st.write(f"Another handler received message: {message}")


# Now we can publish events to the corresponding handlers  by specifying the destination in the event data
# For example, to send a message to the echo_handler, we set destination to "echo_handler"
my_topic.publish_event({
                "sender": "user",
                "data": "Hello, World0!",
                "destination": "echo_handler",
                "message_type": "echo_request",
            }
)


# We can define another type of handler that listens to all messages regardless of destination
@my_topic.register(priority=0, generic=True)
def generic_handler(message):
    st.write(f"Generic handler received message: {message}")


# Now we can publish another event that will be picked up by the generic handler
my_topic.publish_event({
                "sender": "user",
                "data": "Hello, World from generic!",
                "destination": "some_other_handler",
                "message_type": "generic",
            }
)



# Once the topic is set up with handlers, we can create a broker and register the topic with it


broker = BaseBroker(name="my_broker", debug=True)

broker.subscribe(my_topic)

# Now we can publish messages to the topic via the broker

broker.publish("my_topic", {
                "sender": "broker",
                "data": "Hello from broker to echo handler!",
                "destination": "echo_handler",
                "message_type": "broker_echo",
            }
)

# We can also create topics directly via the broker

another_topic = broker.create_topic(
    _id="another_topic",
    version="1.0.0",
    error_handler=None,
    debug=True,
)


@another_topic.register(priority=1)
def another_topic_handler(message):
    st.write(f"Another topic handler received message: {message}")
# Publish an event to the another_topic via the broker
broker.publish("another_topic", {
                "sender": "broker",
                "data": "Hello from broker to another topic handler!",
                "destination": "another_topic_handler",
                "message_type": "broker_another",
            }
)

# Triggering events directly on the topic
# Often we might want to trigger events directly on the topic instance
# For example, when we want to use a espefic topic's functionality directly
# This can be achieved via the topic's sender closure, that is accessible via topic instance
# And the way it works is that it creates a closure around the topic's publish_event method
# to automatically publish events to that topic via the defined broker as universal entry point

# First we can get the sender closure from the topic instance
my_topic._broker  = broker # Ensure the topic has a reference to the broker
echo_handler_publisher = my_topic.echo_handler
st.write(echo_handler_publisher)

# Now we can use the sender closure to publish events directly to the echo_handler
echo_handler_publisher("Hello directly to echo handler via sender closure!")


# Similarly, we can get the sender closure directly from the broker
# This is way more expressive as we can get the sender closure for any topic registered with the broker

another_topic_handler_publisher = broker.another_topic.another_topic_handler
st.write(another_topic_handler_publisher)

# Now we can use the sender closure to publish events directly to the another_topic_handler
another_topic_handler_publisher("Hello directly to another topic handler via broker's topic sender closure!")


# Now you have seen how to create custom topics, register handlers, publish events, and use a broker to manage topics and route messages between them.

# This example demonstrates the flexibility and power of the topic-broker pattern for building event-driven applications in Declarative Streamlit.

# First we create an instance of the AppPage class
app = AppPage(standard=StreamlitCommonStandard())

# As we have seen before we can declare components directly on the app instance

app.add_component(st.title, "Declarative Streamlit App with Custom Logic")

# And we also see how to add effects to the components via the app instance
app.add_component(st.text_input, "Enter your name:", key="name_input").add_effect(
    lambda name: st.write(f"Hello, {name}!")
)

# We can combine this pattern with the sender closures from the topics and broker to create interactive applications


app.add_component(st.number_input, "Enter a number to send to echo handler:", key="number_input").add_effect(
    echo_handler_publisher
)
app.start()
