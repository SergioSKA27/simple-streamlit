from declarative_streamlit.core.build.cstparser import StreamlitComponentParser
from declarative_streamlit.core.build.lstparser import StreamlitLayoutParser
import streamlit as st


# Basic example of using the StreamlitComponentParser and StreamlitLayoutParser

# Streamlit elements are commonly defined in the main file of the app.
# This means that the Streamlit component is called inmediately in the main file.
# And returns its value to the main file. It's a common pattern to use the Streamlit component in a function and return its value.
# For example, the following code defines a text input component and returns its value to the main file.

val = st.text_input("Enter your name")

# This works, but it is not the best way to do it, because as the app grows, it becomes difficult to manage the components.
# And its behavior under different conditions. for example, imagine that the element recieives its arguments from a function
# and the function could return invalid values such as None, if we want to use the component under this premise, 
# we need to check if the value is None or use a try/except block to handle the error.
def get_value():
    # This function returns a value that is used in the Streamlit component as label.
    # But it could return None or an invalid value
    return None

try:
    val = st.text_input(get_value())
except Exception as e:
    # Handle the error here
    st.error(f"An error occurred: {e}")

# This is not the best way to do it, because it makes the code difficult to read and understand.
# This exact same pattern could be used in error handling in general.

# Now, imagine that we want define the component in a more declarative way.
# We want to define the component and its arguments and save that declaration in a variable.
# And call it later when we need it. And also wrap it with additional logic to handle errors and other conditions.
# This is where the StreamlitComponentParser comes in.

# The StreamlitComponentParser is a class that parses the Streamlit component and its arguments.
# And wraps it with additional logic to handle errors and other conditions.
# It also provides a way to define the component in a more declarative way.

# Let's see an example of how to use the StreamlitComponentParser to define button

button_declaration = StreamlitComponentParser(st.button, "button", key="my_button") # This is not rendered yet, just a declaration


# If we want to use the button, we need to parse it first.


# If we want to run a specific function when the button is clicked, we can use the `add_effect` method to add a callable effect to the button.
# This method takes a callable that will be called when the button is clicked. We can add multiple effects to the button.
button_declaration.add_effect(lambda _: st.success("Effect Button was clicked!")) # This will be called when the button is clicked.
# Note that we are using a lambda with the underscore to indicate that we are not using the first argument  which is the value returned by the button.
# If we want to use the value returned by the button, we just receive it as an argument in the lambda function.

usable_button = button_declaration.parse() # This will return a callable object that can be used to render the button as normal.


val_button = usable_button() # This will render the button and return its value.
if val_button:  
    # This is the usual way to use the button, we just check if the button was clicked
    st.success("Parsed button was clicked!") # This will be shown if the button was clicked.

# Now, let's see the previous example with a possible error and how to handle it with the StreamlitComponentParser.

# Let's say we want to define a text that may produce an Exception.

def zero_division():
    # This function returns a value that is used in the Streamlit component as label.
    # But it could return None or an invalid value
    return 1 / 0

text_declaration = StreamlitComponentParser(lambda: st.write(zero_division())) # This is not rendered yet, just a declaration

# Note that we are using a lambda function to wrap the st.write function if we use the st.write without the zero_division function it will raise an exception.
# Cause the zero_division function is called when declared, not when parsed.
# So we need to wrap it in a lambda function to delay the execution of the zero_division function until the write function is called.

# Add the error handling logic to the declaration
# We can use the `set_errhandler` method to set the error handler for the component.
# This method takes a callable that will be called when an error occurs receiving the exception as an argument.
# You need to return true value if the error was handled, or use a non-returning function to handle the error.

def error_handler(e):
    # This function handles the error and returns true if the error was handled.
    # If the error was not handled, it will raise the exception.
    st.error(f"An error occurred: {e}")
    return True # This indicates that the error was handled.
text_declaration.set_errhandler(error_handler)

# If the error handler fails to handle the error, we can add a second barrier to handle the error trough the fatal property.
# This property allows the component to fail silently and not raise an exception, even if the error handler fails to handle the error.
# We can use the `set_fatal` method to set the fatal property for the component.

text_declaration.set_fatal(False) # This will make the component fail silently and not raise an exception, even if the error handler fails to handle the error.


# Now, we can parse the component and use it as normal.
usable_text = text_declaration.parse() # This will return a callable object that can be used to render the text as normal.
usable_text() # This will render the text and return its value.

# This also works with the effects system, so if someone error occurs in the effects system, it will be handled by the error handler.
# And if the error handler fails to handle the error, it will be handled by the fatal property.

button_failure = StreamlitComponentParser(st.button, "Click me", key="failure_button") # This is not rendered yet, just a declaration

# add a problematic effect to the button

button_failure.add_effect(lambda _: 1 / 0) # This will raise an exception when the button is clicked.
# add the error handler to the button

button_failure.set_errhandler(error_handler) # This will handle the error and return true if the error was handled.

# add the fatal property to the button
button_failure.set_fatal(False) # This will make the component fail silently and not raise an exception, even if the error handler fails to handle the error.

# Now, we can parse the component and use it as normal.
usable_button_failure = button_failure.parse() # This will return a callable object that can be used to render the button as normal.

val_button_failure = usable_button_failure() # This will render the button and return its value.
if val_button_failure:  
    st.success("Parsed button was clicked!") # This will be shown if the button was clicked.

# Other properties of the StreamlitComponentParser are the `statefull` and `strict`,
# which are used to define if the component is statefull(like a button) or not (like a text).
# And if the component is strict, which means that it will raise an exception if the component is not used correctly
# for example, if the component not has a key or if the component is not used in the main file.
# To set this properties, we can use the `set_stateful` and `set_strict` methods.
# These methods take a boolean value that indicates if the component is statefull or strict.

# By default, the component is non-statefull and strict, so we don't need to set these properties if we want to use the default values.

# StreamlitComponentParser only works with Streamlit components, such as st.button, st.text_input, st.write, etc.
# And callable objects in general, such as functions and classes.
# But if you want to use it with other streamlit elements, such as st.container, st.expander, st.columns, etc.
# Maybe you want to use the StreamlitLayoutParser, which is a class that parses the Streamlit layout elements and their arguments.
# And also allows to add elements that would be rendered inside the layout element.

# For example, we can use the StreamlitLayoutParser to define a container and add elements to it.
# The functionality is the same as the StreamlitComponentParser, but it is used for layout elements.

container_declaration = StreamlitLayoutParser(st.container, border=True) # This is not rendered yet, just a declaration

# We can also set fatal and errhandler properties to the container, but it is not recommended.
# Because the container will handle any error that occurs inside it, that could be a problem when localizing the error.
# So it is recommended to use the error handler and fatal properties only for components that are not layout elements.

# Now, let's add a button to the container and set the error handler and fatal properties to the button.
# To this, we can use the `add_component` method to add a component to the container, it automatically creates a ComponentParser instance for the component.
# And returns it, so we can use it as we did with the button and text examples.
button_in_container = container_declaration.add_component(st.button, "Click me", key="button_in_container") # This is not rendered yet, just a declaration
button_in_container.set_errhandler(error_handler) # This will handle the error and return true if the error was handled.
button_in_container.set_fatal(False) # This will make the component fail silently and not raise an exception, even if the error handler fails to handle the error.

# We can also add components using the with statement, which is a understandable way to add components to the container.
with container_declaration as container:
    container.add_component(st.write, "Hello from the container!") # This will add a text to the container.


# Now, we can parse the container and use it as normal.
usable_container = container_declaration.parse() # This will return a callable object that can be used to render the container as normal.

usable_container() # This will render the container and return its value.

# This works with any layout element, such as st.expander, st.container, etc.
#  We call this layout elements "row based elements" because their elements are rendered such as rows.
# But if you want to use a "column based element", such as st.columns or st.tabs
# You need to use the property `column_based` to set the element as column based.
# This will make the element to be rendered as columns instead of rows.
# To set this property, we can use the `set_column_based` method.

cols_declaration = StreamlitLayoutParser(st.columns, 2) # This is not rendered yet, just a declaration

cols_declaration.set_column_based(True) # This will make the element to be rendered as columns instead of rows.

# Now, we can add components to the columns

with cols_declaration as cols:
    cols.add_component(st.write, "Hello from the first column!") # This will add a text to the first column.
    # if you want to add more than one element to the column, you need to wrap around another container or layout element.
    with cols.add_container(st.container) as col:
        col.add_component(st.write, "Hello from the second column!")
        col.add_component(st.button, "Click me", key="button_in_column")


# Now, we can parse the columns and use it as normal.
usable_cols = cols_declaration.parse() # This will return a callable object that can be used to render the columns as normal.

# This will render the columns and return its value.
usable_cols()

# This process of parsing the components and layout elements and calling it, could be a bit tedious.
# So we can use the `__call__` method to call the component or layout element directly.
# just by calling the parser directly, this is the same as calling the parse method
# and then calling the component or layout element.

component_declaration = StreamlitComponentParser(st.button, "Click me Directly", key="button_direct") # This is not rendered yet, just a declaration

component_declaration() # This will render the button and return its value.