# Simplest: A Structured Component-Based Framework for Streamlit

[![PyPI version](https://badge.fury.io/py/simplest.svg)](https://badge.fury.io/py/simplest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Simplest** transforms Streamlit development with a structured, component-driven approach that improves organization, error handling, and reactivity. Build maintainable Streamlit applications that scale gracefully as complexity increases.

## Key Features

- **Component-Based Architecture**: Organize UI elements in a modular, hierarchical structure
- **Reactive Effects System**: Add side effects that respond to component value changes
- **Robust Error Handling**: Component-level error management that prevents app crashes
- **Simplified Layout Management**: Easily create complex layouts with organized container objects
- **Stateful Components**: Explicit state management for interactive applications
- **Fragments & Partial Updates**: Optimize performance with fine-grained updates of specific UI sections

## Installation

```bash
pip install simplest
```

## Quick Start

```python
from simplest.base.app.singleapp import AppPage
import streamlit as st

# Initialize the app
app = AppPage()

# Add components
app.add_component(st.title, "Hello Simplest!")

app.add_component(
    st.selectbox, "Choose an option:", ["Option 1", "Option 2", "Option 3"], key="selector"
).add_effect(
    lambda val: st.write(f"You selected: {val}")
)

# Start the app
app.start()
```

## Core Concepts

### AppPage

The central container for your application that manages all components and their rendering:

```python
from simplest.base.app.singleapp import AppPage
import streamlit as st

# Configure the app
AppPage.set_page_config(layout="wide")

# Initialize the app
app = AppPage()

# Add components and start the app
app.add_component(st.write, "Hello World!")
app.start()
```

### Component Management

Add UI elements as distinct components with fine-grained control:

```python
# Add a component with error handling
app.add_component(
    st.selectbox, "Select me!", ["Option 1", "Option 2", "Option 3"], key="selectbox"
).set_errhandler(
    lambda e: st.write(f"Error! {e}")
).set_stateful(
    True
).set_fatal(
    False
)
```

### Effects System

Attach functions that run in response to component value changes:

```python
# Add multiple effects to a component
app.add_component(
    st.selectbox, "Select an option:", ["Option 1", "Option 2", "Option 3"], key="selectbox"
).add_effect(
    lambda val: st.write(f"You selected: {val}")
).add_effect(
    lambda _: st.write("This effect runs on any selection")
)
```

### Container Management

Organize components in a hierarchical structure with simplified layout control:

```python
# Create a column-based container
with app.add_container(st.columns, 3).set_column_based(True) as columns:
    columns.add_component(st.image, "image1.jpg", width=100, caption="Image 1")
    columns.add_component(st.image, "image2.jpg", width=100, caption="Image 2")
    columns.add_component(st.image, "image3.jpg", width=100, caption="Image 3")

# Create an expander container
with app.add_container(st.expander, "Expander", expanded=True) as expander:
    expander.add_component(st.write, "Content inside expander")
```

### State Management

Maintain component state across app reruns:

```python
from simplest.base.logic import SessionState

# Create a session state object
counter = SessionState("counter", initial_value=0)

# Add a button with an effect that updates state
app.add_component(
    st.button, "Increment", key="increment"
).add_effect(
    lambda *_: counter.set_value(counter.value + 1)
).add_effect(
    st.rerun  # Rerun the app to display the updated state
)

# Display the current state value
app.add_component(st.write, "Counter value:", counter.value)

# Using the state setter and tracker
double_counter = SessionState("double_counter", initial_value=1)
counter_setter = double_counter.get_setter()
counter_tracker = double_counter.get_tracker()

app.add_component(
    st.button, "Double", key="double"
).add_effect(
    lambda *_: counter_setter(double_counter.value * 2)
).add_effect(
    st.rerun
)

app.add_component(st.write, "Double counter:", counter_tracker())
```

### Fragments for Partial Updates

Create sections of your UI that can be updated independently:

```python
from simplest.base.app.fragment import AppFragment

# Create a fragment with its own state
fragment_counter = SessionState("fragment_counter", initial_value=0)
fragment = AppFragment()

fragment.add_component(
    st.button, "Increment Fragment", key="increment_fragment"
).add_effect(
    lambda *_: fragment_counter.set_value(fragment_counter.value + 1)
).add_effect(
    lambda *_: st.rerun(scope="fragment")  # Only rerun the fragment
)

fragment.add_component(
    st.write, "Fragment counter:", fragment_counter.value
)

# Add the fragment to the app
app.add_fragment(fragment)
```

### Timed Fragments

Create fragments that automatically update on a schedule:

```python
# Create a fragment that runs every 30 seconds
interval_state = SessionState("interval_state", initial_value=0)
interval_fragment = AppFragment(run_every="30s")

def update_interval_state():
    interval_state.set_value(interval_state.value + 1)
    if interval_state.value % 5 == 0:
        st.toast("App has been running for 5 intervals")

interval_fragment.add_component(
    st.write, "This section updates every 30 seconds"
)
interval_fragment.add_function(update_interval_state)
interval_fragment.add_component(
    st.write, "Interval counter:", interval_state.value
)

app.add_fragment(interval_fragment)
```

### Dialogs

Create modal dialogs for confirmations or user input:

```python
from simplest.base.app.dialog import AppDialog

# Create a dialog
dialog = AppDialog(title="Confirm Selection", width="small")

dialog.add_component(
    st.button, "Confirm", key="confirm"
).add_effect(
    lambda *_: st.success("Confirmed!")
).add_effect(
    st.rerun
)

dialog.add_component(
    st.button, "Cancel", key="cancel"
).add_effect(
    lambda *_: st.warning("Cancelled!")
)

# Add a button that shows the dialog when clicked
app.add_component(
    st.button, "Show Dialog", key="show_dialog"
).add_effect(
    dialog  # The dialog is shown as an effect
).set_stateful(True)
```

## Real-World Example: Dashboard Application

Here's how to build a simple dashboard application with Simplest:

```python
from simplest.base.app.singleapp import AppPage
from simplest.base.logic import SessionState
import streamlit as st
import pandas as pd
import numpy as np

# Initialize the app
app = AppPage.set_page_config(layout="wide")
app = AppPage()

# Add a title
app.add_component(st.title, "Sales Dashboard")

# Create sample data
data = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Sales': np.random.randint(100, 1000, 5),
    'Expenses': np.random.randint(100, 500, 5)
})

# Create a state for filtered months
filtered_months = SessionState("filtered_months", initial_value=data['Month'].tolist())

# Add a sidebar with filters
with app.add_container(st.sidebar) as sidebar:
    sidebar.add_component(
        st.multiselect,
        "Select Months",
        options=data['Month'].tolist(),
        default=filtered_months.value,
        key="month_filter"
    ).add_effect(
        lambda val: filtered_months.set_value(val)
    ).add_effect(
        st.rerun
    )

# Create a function to filter data
def get_filtered_data():
    return data[data['Month'].isin(filtered_months.value)]

# Add main content in two columns
with app.add_container(st.columns, 2).set_column_based(True) as columns:
    # Column 1: Bar chart
    columns.add_component(
        lambda: st.bar_chart(get_filtered_data().set_index('Month'))
    ).set_errhandler(
        lambda e: st.error(f"Chart error: {e}")
    )
    
    # Column 2: Data table
    columns.add_component(
        lambda: st.dataframe(get_filtered_data())
    )

# Start the app
app.start()
```

## Comparison with Pure Streamlit

| Feature | Pure Streamlit | Simplest |
|---------|----------------|----------|
| **Code Organization** | Linear, monolithic script | Hierarchical, component-based architecture |
| **Error Handling** | Global try/except blocks | Component-level error handlers |
| **Reactivity** | Automatic reruns of entire script | Fine-grained effects and targeted updates |
| **Layout Management** | Manual use of context managers | Structured container objects |
| **Component Reusability** | Limited by session state | Direct component references |
| **Complex Layouts** | Requires extensive planning | Simplified through container management |

## Best Practices

1. **Organize by Feature**
   - Group related components into dedicated containers
   - Structure your application based on functional modules

2. **Implement Component-Level Error Handling**
   - Attach error handlers to components that may fail
   - Use non-fatal error configurations to keep the app responsive

3. **Leverage the Effects System**
   - Use effects for side effects such as logging or UI updates
   - Keep effect functions focused on a single responsibility

4. **Manage State Explicitly**
   - Mark components as stateful where necessary
   - Use clear, consistent keys for component state

5. **Plan Your Layout**
   - Use containers to design responsive, scalable layouts
   - Consider using context managers for complex layouts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.