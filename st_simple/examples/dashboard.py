from st_simple import AppPage
import streamlit as st
import pandas as pd
import numpy as np

# Initialize the application and configure the layout for a wide screen
app = AppPage()
app.set_page_config(layout="wide")

# Set the title of the dashboard
app.add_component(st.title, "Sales Dashboard")

# Simulated data (in a real application, this would be replaced with actual data)
data = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Sales': np.random.randint(100, 1000, 5),
    'Expenses': np.random.randint(100, 500, 5)
})

# Sidebar: Add filters for data selection
with app.add_container(st.popover,"Filters") as popover:
    popover.add_component(
        st.multiselect, 
        "Select Months", 
        options=data['Month'].tolist(),
        default=data['Month'].tolist(),
        key="month_filter"
    ).add_effect(
        lambda val: app.set_state("filtered_months", val)
    )

# Main content: Divide into two columns for visualization and data presentation
with app.add_container(st.columns, 2).set_column_based(True) as columns:
    # Column 1: Bar chart for sales data visualization
    columns.add_component(
        lambda: st.bar_chart(
            data[data['Month'].isin(st.session_state.get("filtered_months", data['Month'].tolist()))].set_index('Month')
        )
    ).set_errhandler(lambda e: st.error(f"Chart error: {e}"))
    
    # Column 2: Data table for detailed data display
    columns.add_component(
        lambda: st.dataframe(
            data[data['Month'].isin(st.session_state.get("filtered_months", data['Month'].tolist()))].set_index('Month')
        )
    )

# Start the application (trigger the rendering process)
app.start()
