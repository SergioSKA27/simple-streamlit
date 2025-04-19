from st_simple import AppPage
from st_simple.core.build.cstparser import StreamlitComponentParser
from st_simple.core.build.lstparser import StreamlitLayoutParser
from st_simple.core.handlers.layer import Layer


import streamlit as st
import random

AppPage.set_page_config(
    layout="wide",
)
app = AppPage()


imgs = [
    "https://static.streamlit.io/examples/cat.jpg",
    "https://static.streamlit.io/examples/dog.jpg",
    "https://static.streamlit.io/examples/owl.jpg",
]


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
).set_errhandler(lambda e: st.write(f"Error! {e}")).set_stateful(
    True
).set_fatal(
    False
)



# You can also use the add_effect method to add an effect to the component
# The effect is a function that will be called when the component is rendered
# The effect will be called with the value of the rendered component as an argument
# You can also use the add_effects method to add multiple effects to the component
# The effects will be called in the order they are added

app.main_body["selectbox"].add_effect(
    lambda val: st.write(val) # This will be called when the selectbox is rendered
).add_effect(
    lambda val: st.write("New effect!") # You can add many 
)


# You can also use the add_container method to add a container to the app page
# The container can be a column based(columns,tabs) or a general container(container,expander,etc)
# The container will be added to the main body of the app page
app.add_container(
    st.container, border=True
).set_fatal(
    False # You can also use set some of the methods to control the container behavior
).set_errhandler(
    lambda e: st.write(f"Error! {e}")
).add_component(
    st.image, imgs[0], width=100, caption="Image 1" # You can add only one component to the when you use the add_container method
)

# If you want to add more components or containers to the container you can use the add_component/add_container method 
# But in  some cases if the component not support key argument you will need to use the index of the component in the main body
# Note if you're adding the components inmediately after you add to the main body of the app page you can use the last index of the main body
app.main_body[-1].add_component(
    st.button, "Click me!",key="button2"
).add_effect(
    lambda *_: st.write("Button pressed!")
).add_effect(
    lambda *_: st.write("New effect!")
)


# Based column containers will require you to use the set_column_based method to allow the container rendering each element in the main body in a column based layout
app.add_container(
    st.columns,3
).set_column_based(
    True
).set_errhandler(
    lambda val: st.write(val) # Error handler in containers will take care of the components inside the container if they are not fatal or have an error handler defined
)

# You can also use the set_order method to control the order of the components in the container
# The order is a list of integers that represent the index of the components in the main body of the app page
app.main_body[-1].schema.main_body.set_order([1, 2, 0])

app.main_body[-1].add_component(
    st.image, imgs[0], width=100, caption="Image 1"
)
app.main_body[-1].add_component(
    st.image, imgs[1], width=100, caption="Image 2"
)
app.main_body[-1].add_component(
    st.image, imgs[2], width=100, caption="Image 3"
)

with app.add_container(
    st.expander, "Expander", expanded=True
) as expander:
    # You can also use the with statement to add components to the container
    expander.add_component(
        st.image, imgs[0], width=100, caption="Image 1"
    )


with app.add_container(st.columns, 2).set_column_based(
    True
) as columns:
    # You can also use the with statement to add components to the container
    columns.add_component(
        st.image, imgs[0], width=100, caption="Image 1"
    )
    columns.add_component(
        st.image, imgs[1], width=100, caption="Image 2"
    )




# Once you have added all the components and containers to the app page you can use the start method to start the app
# The start method will render all the components and containers in the main body of the app page
app.start()

# If you want to see the schema of the app page and the configuration of the components and containers you can use the serialize method
# The serialize method will return a dictionary that contains the schema and the configuration of the app page
st.write(app.serialize())
