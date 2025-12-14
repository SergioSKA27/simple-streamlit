# AppFragment

## Overview

`AppFragment` is an application-level class that extends the `Fragment` canvas to provide isolated, independently rerunnable sections of a Streamlit application. Fragments enable performance optimization by allowing specific UI sections to update without triggering a full page rerun.

## Class Signature

```python
class AppFragment(Fragment):
    """
    Represents a fragment in the application with component management capabilities.
    
    This class provides methods to add components and containers to a fragment,
    manage the fragment schema, and start fragment rendering with isolated reruns.
    """
    
    def __init__(
        self,
        name: str = None,
        failsafe: bool = False,
        failhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
        run_every: Union[int, float, timedelta, str, None] = None,
        standard: BaseStandard = None,
    ) -> None
```

## Description

`AppFragment` wraps Streamlit's `@st.fragment` decorator in a declarative, object-oriented interface. It provides:

- **Isolated Reruns**: Only the fragment content reruns, not the entire page
- **Auto-refresh**: Optional automatic rerun on intervals
- **Component Management**: Same interface as `AppPage` for adding components
- **Standard Integration**: Apply configuration standards to fragment components
- **Nesting Support**: Can be embedded in pages or other fragments

### Key Benefits

1. **Performance**: Avoid full page reruns for dynamic sections
2. **Modularity**: Encapsulate related UI logic
3. **Reusability**: Use the same fragment across multiple pages
4. **Isolation**: Fragment state and behavior independent from main page

## Constructor Parameters

### `name: str = None`
**Type**: `Optional[str]`  
**Default**: `None`  
**Description**: Optional name identifier for the fragment.

Used for debugging and serialization. If not provided, class name is used.

**Example**:
```python
fragment = AppFragment(name="user_stats")
```

### `failsafe: bool = False`
**Type**: `bool`  
**Default**: `False`  
**Inherited from**: `Canvas`  
**Description**: Enable failsafe mode for error resilience.

**Example**:
```python
fragment = AppFragment(failsafe=True)
```

### `failhandler: Callable[[Exception], Union[NoReturn, bool]] = None`
**Type**: `Optional[Callable]`  
**Default**: `None`  
**Inherited from**: `Canvas`  
**Description**: Custom error handler for fragment errors.

**Example**:
```python
def fragment_error_handler(e: Exception) -> bool:
    st.warning(f"Fragment error: {e}")
    return True

fragment = AppFragment(failhandler=fragment_error_handler)
```

### `strict: bool = True`
**Type**: `bool`  
**Default**: `True`  
**Inherited from**: `Canvas`  
**Description**: Enable strict type checking and validation.

### `run_every: Union[int, float, timedelta, str, None] = None`
**Type**: `Union[int, float, timedelta, str, None]`  
**Default**: `None`  
**Description**: Auto-rerun interval for the fragment.

Accepts:
- `int` or `float`: Seconds between reruns
- `timedelta`: Time interval object
- `str`: Time string (e.g., "1s", "5m", "1h")
- `None`: No automatic rerun

**Example**:
```python
from datetime import timedelta

# Rerun every 5 seconds
fragment = AppFragment(run_every=5)

# Rerun every minute
fragment = AppFragment(run_every=timedelta(minutes=1))

# Rerun every 30 seconds (string format)
fragment = AppFragment(run_every="30s")
```

**Use Cases**:
- Live data dashboards
- Real-time metrics
- Polling for updates
- Auto-refreshing charts

### `standard: BaseStandard = None`
**Type**: `Optional[BaseStandard]`  
**Default**: `None`  
**Description**: Configuration standard to apply to components.

**Example**:
```python
from declarative_streamlit.config.common.stdstreamlit import StreamlitCommonStandard

fragment = AppFragment(standard=StreamlitCommonStandard())
```

## Attributes

### Public Attributes

Inherited from `Canvas`:
- `failsafe: bool`
- `failhandler: Optional[Callable]`
- `strict: bool`
- `run_every: Union[int, float, timedelta, str, None]` (from `Fragment`)

### Protected Attributes

#### `_name: Optional[str]`
**Type**: `Optional[str]`  
**Description**: The fragment's name identifier.

#### `_standard: Optional[BaseStandard]`
**Type**: `Optional[BaseStandard]`  
**Description**: Configuration standard applied to components.

#### `_body: Schema`
**Type**: `Schema`  
**Inherited from**: `Canvas`  
**Description**: Internal schema managing component hierarchy.

## Methods

### Component Management

#### `add_component()`
```python
def add_component(
    self,
    component: Union[Callable[..., Any], StreamlitComponentParser],
    *args: Any,
    **kwargs: Any,
) -> StreamlitComponentParser:
    """
    Add a component to the fragment.
    
    Args:
        component: The Streamlit component function or parser
        *args: Positional arguments for the component
        **kwargs: Keyword arguments for the component
        
    Returns:
        StreamlitComponentParser: Parser wrapping the component
        
    Raises:
        TypeError: If component is not callable
    """
```

**Description**: Add Streamlit components to the fragment with automatic standard application.

**Example**:
```python
fragment = AppFragment(name="metrics")

# Add components
fragment.add_component(st.metric, "Users", "1000")
fragment.add_component(st.metric, "Revenue", "$50K")

# With configuration
fragment.add_component(
    st.button, "Refresh", key="refresh_btn"
).set_stateful(True).add_effect(
    lambda val: refresh_data() if val else None
)
```

#### `add_container()`
```python
def add_container(
    self,
    container: Union[Callable[..., Any], StreamlitLayoutParser],
    *args: Any,
    **kwargs: Any,
) -> StreamlitLayoutParser:
    """
    Add a container to the fragment.
    
    Args:
        container: The Streamlit container function or parser
        *args: Positional arguments for the container
        **kwargs: Keyword arguments for the container
        
    Returns:
        StreamlitLayoutParser: Parser wrapping the container
        
    Raises:
        TypeError: If container is not callable
    """
```

**Description**: Add layout containers to organize fragment components.

**Example**:
```python
fragment = AppFragment(name="dashboard")

# Add columns
with fragment.add_container(st.columns, 2).set_column_based(True) as cols:
    cols.add_component(st.metric, "Left Metric", "100")
    cols.add_component(st.metric, "Right Metric", "200")

# Add expander
with fragment.add_container(st.expander, "Details") as exp:
    exp.add_component(st.dataframe, data)
```

#### `add_function()`
```python
def add_function(
    self,
    function: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> StreamlitComponentParser:
    """
    Add a custom function to the fragment.
    
    Args:
        function: The function to execute
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        StreamlitComponentParser: Parser wrapping the function
    """
```

**Description**: Add custom functions that execute during fragment rendering.

**Example**:
```python
fragment = AppFragment(name="custom")

def display_data():
    data = fetch_live_data()
    st.dataframe(data)
    st.line_chart(data)

fragment.add_function(display_data)
```

### Rendering

#### `start()`
```python
def start(self) -> None:
    """
    Start the fragment rendering process.
    
    This wraps the fragment body in Streamlit's @fragment decorator
    and initiates rendering.
    """
```

**Description**: Initiate fragment rendering. This is called automatically when the fragment is embedded in a page or manually to render standalone.

**Behavior**:
1. Wraps body in `@st.fragment(run_every=self.run_every)`
2. Executes all components in order
3. Applies error handling per configuration
4. Returns immediately (non-blocking)

**Example**:
```python
fragment = AppFragment(name="stats", run_every=5)
fragment.add_component(st.metric, "Live Users", get_user_count())

# When added to page, starts automatically
app.add_fragment(fragment)

# Or start manually
fragment.start()
```

### Serialization

#### `serialize()`
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize the fragment to a dictionary.
    
    Returns:
        Dict[str, Any]: Dictionary representation including:
            - __fragment__: Fragment schema
            - __config__: Configuration settings
    """
```

**Description**: Convert fragment structure to JSON-compatible format.

**Return Structure**:
```python
{
    "__fragment__": {
        # Schema with all components
    },
    "__config__": {
        "strict": bool,
        "failsafe": bool
    }
}
```

**Example**:
```python
fragment = AppFragment(name="metrics")
fragment.add_component(st.metric, "Users", "100")

data = fragment.serialize()
st.json(data)
```

### Utility Methods

#### `__name__()`
```python
def __name__(self) -> str:
    """
    Get the fragment's name.
    
    Returns:
        str: Fragment name or class name if name not set
    """
```

**Example**:
```python
fragment = AppFragment(name="my_fragment")
print(fragment.__name__())  # "my_fragment"

fragment2 = AppFragment()
print(fragment2.__name__())  # "AppFragment"
```

#### `__repr__()`
```python
def __repr__(self) -> str:
    """String representation for debugging."""
    return f"Fragment({self.__str__()})"
```

## Usage Examples

### Basic Fragment

```python
from declarative_streamlit.base import AppPage, AppFragment
import streamlit as st

AppPage.set_page_config(layout="wide")
app = AppPage()

# Create fragment
fragment = AppFragment(name="user_stats")
fragment.add_component(st.metric, "Active Users", "1,234")
fragment.add_component(st.metric, "New Today", "45")

# Add to page
app.add_component(st.title, "Dashboard")
app.add_fragment(fragment)

app.start()
```

### Auto-Refreshing Fragment

```python
from declarative_streamlit.base import AppPage, AppFragment
import streamlit as st
from datetime import datetime

app = AppPage()

# Fragment refreshes every 2 seconds
live_fragment = AppFragment(name="live_stats", run_every=2)

def show_live_time():
    st.metric("Current Time", datetime.now().strftime("%H:%M:%S"))

live_fragment.add_function(show_live_time)
live_fragment.add_component(st.caption, "Updates every 2 seconds")

# Add to page
app.add_component(st.title, "Live Dashboard")
app.add_fragment(live_fragment)
app.add_component(st.write, "This content doesn't rerun")

app.start()
```

### Fragment with Interactive Components

```python
from declarative_streamlit.base import AppPage, AppFragment, SessionState
import streamlit as st

app = AppPage()
AppPage.set_page_config(layout="wide")

# Fragment-specific state
fragment_counter = SessionState("fragment_counter", initial_value=0)

# Create interactive fragment
interactive_fragment = AppFragment(name="interactive")

interactive_fragment.add_component(st.subheader, "Fragment Counter")
interactive_fragment.add_component(
    st.button, "Increment", key="frag_increment"
).add_effect(
    lambda val: fragment_counter.set_value(
        fragment_counter.value + 1
    ) if val else None
)

interactive_fragment.add_component(
    st.metric, "Count", fragment_counter.value
)

# Main page
app.add_component(st.title, "Fragment Isolation Demo")
app.add_component(st.write, "Click button below - only fragment reruns!")
app.add_fragment(interactive_fragment)
app.add_component(st.info("This text doesn't rerender on button click"))

app.start()
```

### Nested Fragments

```python
from declarative_streamlit.base import AppPage, AppFragment
import streamlit as st

app = AppPage()

# Inner fragment
inner_fragment = AppFragment(name="inner", run_every=3)
inner_fragment.add_component(st.caption, "Inner fragment (refreshes every 3s)")
inner_fragment.add_component(
    st.metric, "Random Value", str(random.randint(0, 100))
)

# Outer fragment
outer_fragment = AppFragment(name="outer")
outer_fragment.add_component(st.subheader, "Outer Fragment")
outer_fragment.add_fragment(inner_fragment)  # Nest fragments
outer_fragment.add_component(st.write, "Outer fragment content")

# Main page
app.add_component(st.title, "Nested Fragments")
app.add_fragment(outer_fragment)

app.start()
```

### Fragment with Standard

```python
from declarative_streamlit.base import AppPage, AppFragment
from declarative_streamlit.config.common.stdstreamlit import StreamlitCommonStandard
import streamlit as st

app = AppPage(standard=StreamlitCommonStandard())

# Fragment inherits or has own standard
fragment = AppFragment(
    name="configured",
    standard=StreamlitCommonStandard()
)

# Components auto-configured per standard
fragment.add_component(st.text_input, "Name", key="frag_name")
fragment.add_component(st.selectbox, "Option", ["A", "B"], key="frag_opt")

app.add_fragment(fragment)
app.start()
```

### Error Handling in Fragments

```python
from declarative_streamlit.base import AppPage, AppFragment
import streamlit as st

app = AppPage()

# Fragment with error handling
safe_fragment = AppFragment(
    name="safe",
    failsafe=True,
    failhandler=lambda e: st.error(f"Fragment error: {e}")
)

safe_fragment.add_component(st.subheader, "Safe Fragment")

# This will fail but won't crash the fragment
safe_fragment.add_component(lambda: 1/0)  # Division by zero

safe_fragment.add_component(st.success, "Fragment continues after error")

app.add_fragment(safe_fragment)
app.start()
```

### Reusable Fragment Component

```python
from declarative_streamlit.base import AppPage, AppFragment
import streamlit as st

def create_stats_fragment(title: str, metrics: dict) -> AppFragment:
    """Factory function for reusable stats fragments."""
    fragment = AppFragment(name=f"stats_{title}")
    
    fragment.add_component(st.subheader, title)
    
    # Add columns with metrics
    with fragment.add_container(st.columns, len(metrics)).set_column_based(True) as cols:
        for label, value in metrics.items():
            cols.add_component(st.metric, label, value)
    
    return fragment

# Create multiple fragments from template
app = AppPage()
app.add_component(st.title, "Multiple Stats")

sales_fragment = create_stats_fragment("Sales", {
    "Revenue": "$100K",
    "Orders": "500",
    "AOV": "$200"
})

user_fragment = create_stats_fragment("Users", {
    "Active": "1,234",
    "New": "45",
    "Churn": "2.3%"
})

app.add_fragment(sales_fragment)
app.add_fragment(user_fragment)

app.start()
```

## Best Practices

### 1. Use Fragments for Independent Sections
```python
# Good - chart updates independently
chart_fragment = AppFragment(name="chart", run_every=5)
chart_fragment.add_component(st.line_chart, get_live_data())
app.add_fragment(chart_fragment)

# Bad - entire page reruns
app.add_component(st.line_chart, get_live_data())
```

### 2. Name Your Fragments
```python
# Good - easy to debug
fragment = AppFragment(name="user_metrics")

# Less useful
fragment = AppFragment()  # Name will be "AppFragment"
```

### 3. Choose Appropriate Refresh Intervals
```python
# Too frequent - may cause performance issues
fragment = AppFragment(run_every=0.1)  # 100ms

# Reasonable intervals
live_data = AppFragment(run_every=5)  # 5 seconds
metrics = AppFragment(run_every=60)  # 1 minute
```

### 4. Keep Fragment State Isolated
```python
# Good - fragment has its own state
fragment_state = SessionState("fragment_value", 0)

# Avoid - sharing state can cause unexpected reruns
global_state = SessionState("global_value", 0)
```

### 5. Use Fragments for Performance
```python
# Fragment only reruns on button click inside it
button_fragment = AppFragment(name="button_section")
button_fragment.add_component(st.button, "Click", key="btn")
button_fragment.add_component(expensive_computation)

app.add_fragment(button_fragment)

# This doesn't rerun when button is clicked
app.add_component(st.write, "Static content")
```

### 6. Limit Nesting Depth
```python
# Good - 1-2 levels
app.add_fragment(outer_fragment)
outer_fragment.add_fragment(inner_fragment)

# Avoid - deep nesting can be confusing
# app -> frag1 -> frag2 -> frag3 -> frag4  # Too deep
```

## Error Handling

### Common Exceptions

#### `TypeError: fragment is not callable`
**Cause**: Passing non-Fragment to add_fragment  
**Solution**: Ensure you pass Fragment instances

```python
# Wrong
app.add_fragment("not a fragment")

# Correct
fragment = AppFragment()
app.add_fragment(fragment)
```

#### Fragment doesn't rerun independently
**Cause**: Fragment not properly isolated or state shared with page  
**Solution**: Check state isolation and fragment configuration

```python
# Ensure fragment has isolated state
fragment_state = SessionState("fragment_only", 0)

# Don't mix with page state in fragment
# page_state = SessionState("page_level", 0)  # Avoid in fragments
```

## Performance Considerations

### When to Use Fragments

**Use fragments when**:
- Section updates independently (e.g., live charts, metrics)
- Section has interactive elements that trigger reruns
- Want to avoid full page reruns
- Need auto-refresh functionality

**Don't use fragments when**:
- Section rarely updates
- Component is simple and fast
- Adding unnecessary complexity

### Refresh Intervals

Choose appropriate intervals:
```python
# Real-time data
live_fragment = AppFragment(run_every=1)  # 1 second

# Periodic updates
metrics_fragment = AppFragment(run_every=30)  # 30 seconds

# Infrequent updates
daily_stats = AppFragment(run_every=3600)  # 1 hour
```

## Streamlit Fragment Compatibility

`AppFragment` wraps Streamlit's `@st.fragment` decorator. Key compatibility notes:

1. **Isolation**: Fragment runs in isolated context
2. **State Access**: Can access session state
3. **Sidebar**: Cannot modify sidebar from within fragment
4. **Callbacks**: Work within fragment scope
5. **Nesting**: Supports nested fragments

**Limitations** (from Streamlit):
- Cannot use `st.sidebar` inside fragment
- Some advanced features may have limited support

## Related Components

- **[Fragment](./fragment.md)** - Base Fragment canvas class
- **[AppPage](./app-page.md)** - Main page that can contain fragments
- **[Canvas](./canvas.md)** - Base canvas abstraction
- **[SessionState](./session-state.md)** - State management for fragments

## See Also

- [Streamlit Fragments Documentation](https://docs.streamlit.io/library/api-reference/execution-flow/st.fragment)
- [Examples](../../examples/) - Fragment usage examples
- [Performance Optimization](../../docs/performance.md) - Fragment best practices

---

**Navigation**: [README](./README.md) | [Canvas](./canvas.md) | [AppPage](./app-page.md) | [AppDialog](./app-dialog.md) | [SessionState](./session-state.md)
