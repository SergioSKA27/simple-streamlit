from simplest.core.build.cstparser import StreamlitComponentParser
from simplest.core.build.lstparser import StreamlitLayoutParser

import streamlit as st





# Create a StreamlitComponentParser instance
parser = StreamlitComponentParser(st.checkbox, "Click me!")
writeparser = StreamlitComponentParser(st.write, "Hello World!")

container = StreamlitLayoutParser(st.tabs,['Tab1','Tab2'])


# Parse the component

button = parser.parse(stateful=True,strict=False,fatal=False,errhandler=lambda e: st.write("An error occured"))
text = writeparser.parse()
layout ={
    0:[button,],
    1:[text,]
}

# Render the layout with the container
containerp = container.parse(layers=layout,column_based=True,order=[1,0])

containerp()

# Render the component alone
#if ev := button():
#    st.write("Clicked :O")
#
#text()

