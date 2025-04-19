from st_simple.base.app.singleapp import AppPage
from st_simple.base.app.fragment import AppFragment
from st_simple.base.app.dialog import AppDialog
from st_simple.base.logic import SessionState
from st_simple.config.common.stdstreamlit import StreamlitCommonStandard

# You can also import directly the classes you need
# from st_simple import AppPage, AppFragment, AppDialog, SessionState, ...

import streamlit as st
import random
from datetime import datetime

AppPage.set_page_config(
    layout="wide",
)
app = AppPage(standard=StreamlitCommonStandard())


imgs = [
    "https://static.streamlit.io/examples/cat.jpg",
    "https://static.streamlit.io/examples/dog.jpg",
    "https://static.streamlit.io/examples/owl.jpg",
]

# You can use the SessionState class to create a session state object
# The SessionState class is a wrapper around the Streamlit session state object
# It allows you to create a session state object with a key and an initial value
# That will be consistent throughout reruns of the app

state = SessionState("my_state", initial_value=0)
state2 = SessionState("my_state2", initial_value=1)
# The session state object will be created with the key "my_state" and an initial value of 0
# You can use the value property to get and set the value of the session state object
# The value property will return the current value of the session state object
# if you need to set a new value many times you can use the get_setter method to get a setter for the session state object
# The setter will be a callable that takes a new value as an argument and sets the value of the session state object
# You can also use the get_tracker method to get a tracker for the session state object
# The tracker will be a callable that takes a new value as an argument and sets the value of the session state object
# The tracker will also return the current value of the session state object
state_setter = state2.get_setter()
state_tracker = state2.get_tracker()


# Working with the streamlit components and adding actions to them


# The app page is a container that holds the components and containers of the app
# using a schema that is a list of layers, by default the schema only contains
# one layer that we call the main body of the app page, it consists of a list of components and containers
# so each time you add a component or a container to the app page you append it to the main body of the app page
# and they will be rendered in the order they were added to the main body of the app page


# You can use the add_component method to add a component to the app page.
# The component can be a function or a StreamlitComponentParser object
# You need to pass the function and its arguments to the add_component method
# The component will be added to the main body of the app page
app.add_component(st.write, "Hello World!")

# The api also allows you to control how the component behaves
# You can control the error handling of the component by using the set_errhandler method
# The set_errhandler method takes a function as an argument and will be called when an error occurs
# This is useful for debugging or for handling errors in a specific that does not crash app and show simple error messages
# You can also use the set_fatal method to make the component fatal and stop the app when an error occurs
# Or ignore the error if there is no error handler defined for the component
# You can also use the set_stateful method to make the component stateful and keep track of its state
# Throughout the key of the component,
app.add_component(
    st.selectbox, "Select me!", ["Option 1", "Option 2", "Option 3"], key="selectbox"
).set_errhandler(lambda e: st.write(f"Error! {e}")).set_stateful(True).set_fatal(False)


# You can also use the add_effect method to add an effect to the component
# The effect is a function that will be called when the component is rendered
# The effect will be called with the value of the rendered component as an argument
# You can also use the add_effects method to add multiple effects to the component
# The effects will be called in the order they are added

app.main_body["selectbox"].add_effect(
    lambda val: st.write(val)  # This will be called when the selectbox is rendered
).add_effect(
    lambda _: st.write("New effect!")  # You can add many
)


# You can also use the add_container method to add a container to the app page
# The container can be a column based(columns,tabs) or a general container(container,expander,etc)
# The container will be added to the main body of the app page
app.add_container(st.container, border=True).set_fatal(
    False  # You can also use set some of the methods to control the container behavior
).set_errhandler(lambda e: st.write(f"Error! {e}")).add_component(
    st.image,
    imgs[0],
    width=100,
    caption="Image 1",  # You can add only one component to the when you use the add_container method
)

# If you want to add more components or containers to the container you can use the add_component/add_container method
# But in  some cases if the component not support key argument you will need to use the index of the component in the main body
# Note if you're adding the components inmediately after you add to the main body of the app page you can use the last index of the main body
app.main_body[-1].add_component(st.button, "Click me!", key="button2").add_effect(
    lambda *_: st.write("Button pressed!")
).add_effect(lambda *_: st.write("New effect!"))


# Based column containers will require you to use the set_column_based method to allow the container rendering each element in the main body in a column based layout
app.add_container(st.columns, 3).set_errhandler(
    lambda val: st.write(
        val
    )  # Error handler in containers will take care of the components inside the container if they are not fatal or have an error handler defined
)

# You can also use the set_order method to control the order of the components in the container
# The order is a list of integers that represent the index of the components in the main body of the app page
app.main_body[-1].schema.main_body.set_order([1, 2, 0])

app.main_body[-1].add_component(st.image, imgs[0], width=100, caption="Image 1")
app.main_body[-1].add_component(st.image, imgs[1], width=100, caption="Image 2")
app.main_body[-1].add_component(st.image, imgs[2], width=100, caption="Image 3")

with app.add_container(st.expander, "Expander", expanded=True) as expander:
    # You can also use the with statement to add components to the container
    expander.add_component(st.image, imgs[0], width=100, caption="Image 1")

with app.add_container(st.columns, 2) as columns:
    # You can also use the with statement to add components to the container
    columns.add_component(st.image, imgs[0], width=100, caption="Image 1")
    columns.add_component(st.image, imgs[1], width=100, caption="Image 2")


app.add_component(st.button, "Increment", key="increment").add_effect(
    lambda *_: state.set_value(
        state.value + 1
    )  # This will be called when the button is clicked
).add_effect(
    # ¡¡¡you can only trigger the rerun method using effect, callbacks doesn't support it!!!
    st.rerun  # This will be called when the button is clicked be sure to not add effect after this one because it will not be called
)

app.add_component(
    st.write,
    "Counter Increment",
    state.value,  # This will be called when the button is clicked
)


app.add_component(st.button, "Double", key="double").add_effect(
    lambda *_: state_setter(
        state2.value * 2
    )  # This will be called when the button is clicked
).add_effect(
    st.rerun  # This will be called when the button is clicked be sure to not add effect after this one because it will not be called
)


app.add_component(
    st.write,
    "Counter Double",
    state_tracker(),  # This will be called when the button is clicked
)

# Once you have added all the components and containers to the app page you can use the start method to start the app
# The start method will render all the components and containers in the main body of the app page

# If you want to see the schema of the app page and the configuration of the components and containers you can use the serialize method
# The serialize method will return a dictionary that contains the schema and the configuration of the app page

# You can also create a fragment of the app page using the AppFragment class
# The AppFragment allows you to create a fragment that allows you to rerun only the fragment and not the whole app page

s = SessionState("fragment_state", initial_value=0)

fragment = AppFragment()

fragment.add_component(
    st.button, "Increment Fragment", key="increment_fragment"
).add_effect(
    lambda *_: s.set_value(
        s.value + 1
    )  # This will be called when the button is clicked
).add_effect(
    lambda *_: st.rerun(
        scope="fragment"
    )  # This will be called when the button is clicked be sure to not add effect after this one because it will not be called
)

fragment.add_component(
    st.write,
    "Counter Fragment",
    s.value,  # This will be called when the button is clicked
)

app.add_fragment(fragment)  # This will add the fragment to the app page

app.add_component(
    st.button, "see how many times the fragment was rerun", key="fragment_rerun"
).add_effect(
    lambda *_: st.toast(
        f"Fragment incremented to {s.value}"
    )  # This will be called when the button is clicked
)


# You can also use fragments that reruns on determined time intervals
# You can use the run_every argument to set the time interval of the fragment
# The time interval can be a timedelta object or a string that represents the time interval

interval_state = SessionState("interval_state", initial_value=0)

intervalfragment = AppFragment(run_every="30s")


def update_interval_state():
    interval_state.set_value(interval_state.value + 1)
    if interval_state.value % 5 == 0:
        st.toast("App has been running for 5 intervals")


intervalfragment.add_component(
    st.write,
    "Interval Fragment Update the time every 30 seconds",  # This will be called when the fragment is rerun
)
intervalfragment.add_function(
    update_interval_state
)  # you can add a function to the fragment that will be called when the fragment is rendered
intervalfragment.add_component(
    st.write,
    "Interval Fragment Counter",
    interval_state.value,  # This will be called when the button is clicked
)

app.add_fragment(intervalfragment)  # This will add the fragment to the app page


# You can also use the AppDialog class to create a canvas that allows you to show a dialog in the app page
# Be sure to use the dialog only if it's used as an effect, otherwise it will be rendered in the app page every time

dialogcanvas = AppDialog(title="Confirm Selection", width="small")
dialogcanvas.add_component(st.button, "Confirm", key="confirm").add_effect(
    lambda *_: st.success(
        "Confirmed!"
    )  # This will be called when the button is clicked
).add_effect(
    st.rerun  # This will be called when the button is clicked be sure to not add effect after this one because it will not be called
)

dialogcanvas.add_component(st.button, "Cancel", key="cancel").add_effect(
    lambda *_: st.warning(
        "Cancelled!"
    )  # This will be called when the button is clicked
)


app.add_component(st.button, "Show Dialog", key="dialog").add_effect(
    dialogcanvas  # This will be called when the button is clicked
).set_stateful(
    True  # This will be called when the button is clicked
)


app.add_component(st.button, "Generic Button", key="generic")


app.start()  # This will start the app page and render all the components and containers in the main body of the app page
st.write(app.serialize())



# This is the default way to use the adding components and containers logic
# As you can see each time you add a component or a container you need to set
# the especific behavior of the component or container using the set methods
# such as set_errhandler, set_fatal, set_stateful, etc. 
# This is not the best way to use the logic because it can be a bit verbose and hard to read
# So we created the StreamlitCommonStandard class that allows you to use default values for the components and containers

# For example if you want to add a column based container you need to do the following:
# app.add_container(st.columns, 3).set_column_based(True)
# But if you use the StreamlitCommonStandard class you can do the following:
# app.add_container(st.columns, 3)
# The StreamlitCommonStandard class will set the default values for the components and containers
# Also you can still use the set methods to override the default values if you want to add a more specific behavior to the component or container
std = StreamlitCommonStandard()

st.write(std.get_similar(st.columns)) # This will return the StreamlitCommonStandard class that is similar to the st.columns class
