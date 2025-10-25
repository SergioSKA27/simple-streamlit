from declarative_streamlit import AppPage, StreamlitCommonStandard
import streamlit as st


# Basic example of using standards in a Streamlit app 

app = AppPage()

# As we see in other examples, we can add components to the app page
# And then we can set the basic behavior for the components through
# ´set_fatal´, ´set_stateful´ and ´set_column_based´ methods.
# These methods are used to set the behavior of the components in the app page.

app.add_component(
    st.button,
    "Click me",
    key="button"
).set_stateful(
    True
).set_fatal(
    False
)

with app.add_container(st.columns, 2).set_column_based(
    True
).set_stateful(False) as columns:
    columns.add_component(
        st.write,
        "Column 1",
    )

    columns.add_component(
        st.write,
        "Column 2",
    )

app.start()


# This is tedious, you need to set any of this properties for each component and we need to know the behavior of the component
# before hand. So we can use a ´Standard´  which is a class that contains the representation of the component and
# the behavior of the component. So each component we add to the app page will have the same behavior as the standard.
# The standard is a class that contains the representation of each component and the behavior of the component.

# First we need to create a canvas(AppPage,AppFragment,AppDialog) and then we can define the standard that the canvas will use.

app_standard = AppPage(standard=StreamlitCommonStandard())

# The standard is a class that contains the representation of each component and the behavior of the component.
# So we can add components to the app page and they will have the same behavior as their representation in the standard.

# For example, we can add a button to the app page and it will have the same behavior as the button in the standard.
# in this case, the button will be stateful and fatal by default.
app_standard.add_component(
    st.button,
    "Click me",
) 

# We can also add a container to the app page and it will have the same behavior as the container in the standard.
# in this case, the columns will be not stateful, fatal and column based by default.
with app_standard.add_container(st.columns, 2) as columns:
    columns.add_component(
        st.write,
        "Column 1 Standard",
    )

    columns.add_component(
        st.write,
        "Column 2 Standard",
    )

app_standard.start()

# we can also check the configuration of each component in the app page by serializing the app page.
st.write(app_standard.serialize())

# we can also check the configuration of each component in the standard by using the ´get_similar´ method.
standard = StreamlitCommonStandard()
st.write(standard.get_similar(st.button).serialize()) # This will return  representation of the button in the standard.
# Note: if the component is not in the standard, it will return None, so be careful using the serializer.