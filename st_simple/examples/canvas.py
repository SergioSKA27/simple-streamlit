from st_simple import AppPage, AppFragment, AppDialog
import streamlit as st

AppPage.set_page_config(
    layout="wide",
)

# Working with the different canvases

# We understand a canvas as a space where we can insert components,containers and even other canvases or functions.
# This canvas are the top level containers of the app. They consist of a sequence of components, containers or functions.
# This elements are called sequentialy in the order they were added to the canvas.

# Let's start with the primary canvas, the AppPage canvas.
# This canvas is the main one, and it is the one that will be displayed when the app is run.
# It is the one that will be used to display the main content of the app.

# To create a new AppPage canvas, we can use the AppPage class.

app = AppPage(
    failsafe=False, # If True, the app will ignore any errors that occur in the app and will continue running.
    failhandler=None, # If failsafe is True, this function will be called when an error occurs and only will be attached to the component that caused the error.
    strict=True, # If True, this will make the app strict, meaning that it will not allow any components to be added to the app without a key.
)


# Let's add a title to the app.
# To add a title to the app, we can use the add_component method of the AppPage class.
# This method takes the component to be added as the first argument, and any additional arguments.
app.add_component(st.title, "Hello World!")


# Now let's add a button to the app.
# To add a button to the app, we can use the add_component method of the AppPage class.
# Note that we can pass multiple arguments and keyword arguments to the component.
app.add_component(st.button, "Click me!", key="button1")


# Now let's add containers to the app.
# To add a container to the app, we can use the add_container method of the AppPage class.
# This method works the same way as the add_component method, but it will create a container for the component.
# In this case, we will use the with syntax to create the container and manage the components inside it.
with app.add_container(st.container,border=True) as container:
    container.add_component(st.text_input, "Enter your name:", key="name")
    container.add_component(st.button, "Submit", key="submit")


# We can also add functions directly to the app.
# To add a function to the app, we can use the add_function method of the AppPage class.
# This method takes the function to be added as the first argument, and any additional arguments.

def greet(name):
    st.write(f"Hello, {name}!")

app.add_function(greet, "John Doe")

# All this components are added to the main body of the app.
# And are rendered from top to bottom as in regular streamlit apps.
# This also means each time the app is rerun, the components are rendered again.

# If we want to avoid this, we can use the second canvas, the AppFragment canvas.
# This canvas is a fragment of the app, and it could be used to create separate sections of the app.
# That runs independently of the main app. Except when the app is rerun from a global scope.

# To create a new AppFragment canvas, we can use the AppFragment class.
# This class works the same way as the AppPage class, but it will create a fragment of the app.

# This fragment can be used to create separate sections of the app. and avoid many reruns of the full app.

fragment = AppFragment(
    name="Fragment 1", # We can give a name to the fragment,
    failsafe=False, 
    failhandler=None,
    strict=True, # This will make the app strict, meaning that it will not allow any components to be added to the app without a key.
)

# Let's add a title to the fragment.
fragment.add_component(st.title, "Fragment 1")

# Let's add a button to the fragment.
fragment.add_component(st.button, "Fragment Click me!", key="button2")


# Now let's add a container to the fragment.
with fragment.add_container(st.container,border=True) as container:
    container.add_component(st.text_input, "Enter your name:", key="name2")
    container.add_component(st.button, "Submit", key="submit2")


# We can also add functions directly to the fragment.

fragment.add_function(greet, "Mary Jane")

# Once we have created the fragment, we can add it to the app.
# To add a fragment to the app, we can use the add_fragment method of the AppPage class.

app.add_fragment(fragment)


# We can also add fragments into containers or other fragments.
# This will allow us to create nested fragments and containers.
# We recommend see the streamlit documentation to check the limitations of nested containers and fragments.

# Finally, we can also create dialogs.
# This dialogs are used to create popups or modals in the app.
# And they are only usable if they are product of some action in the app.
# If we ignore this, the dialog will be shown every time the app is rerun.
# To create a new AppDialog canvas, we can use the AppDialog class.
# This class works the same way as the AppPage class, but it will create a dialog of the app.

dialog = AppDialog(
    title="Dialog 1", # Dialog requires a title that will be shown in the header of the dialog.
    width="large", # We can set the width of the dialog to small or large.
    failsafe=False,
    failhandler=None,
    strict=True,
)

# Let's create a confirmation dialog that will be shown when the user clicks a button in the app.

dialog.add_component(st.button, "Confirm", key="confirm",type="primary")
dialog.add_component(st.button, "Cancel", key="cancel")

# Now let's create the button that triggers the dialog.
# To create the button, we can use the add_component method of the AppPage or AppFragment class.
# And we can use the add_effect method to show the dialog when the button is clicked.
app.add_component(st.button, "Show Dialog", key="show_dialog").add_effect(
    dialog
)



# Now we can run the app and see the result.
# To run the app, we can use the start method of the AppPage class.

# This method will start the app and render all components in the main body schema.
app.start()

# We can also use the serialize method to get the app schema as a dictionary.
st.write(app.serialize())