# AppPage

## Overview

`AppPage` is the primary application-level class for building full Streamlit applications using a declarative approach. It extends the `Canvas` abstract class and provides concrete implementations for managing Streamlit components, containers, and fragments in a structured, composable manner.

## Class Signature

```python
class AppPage(Canvas):
    """
    Represents a page in the application with component management capabilities.
    
    This class provides methods to add components and containers to the page,
    manage the page schema, and start the page rendering.
    """
    
    def __init__(
        self,
        failsafe: bool = False,
        failhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
        standard: BaseStandard = None,
    ) -> None
```

## Description

`AppPage` serves as the main entry point for declarative Streamlit applications. It provides:

- **Component Management**: Add and configure Streamlit widgets and elements
- **Container Support**: Manage layout containers (columns, expanders, etc.)
- **Fragment Integration**: Embed reusable fragment components
- **Standards Support**: Apply configuration standards via `BaseStandard`
- **Error Handling**: Built-in error handling with failsafe mechanisms
- **Serialization**: Convert application structure to JSON-compatible formats
- **Page Configuration**: Static methods for Streamlit page settings

### Key Features

1. **Declarative API**: Build UIs by chaining method calls
2. **Type Safety**: Full type hints and runtime validation
3. **Component Reuse**: Support for fragments and custom components
4. **Error Resilience**: Configurable error handling per component
5. **Schema-based Rendering**: Internal representation allows serialization and inspection

## Constructor Parameters

### `failsafe: bool = False`
**Type**: `bool`  
**Default**: `False`  
**Description**: Global failsafe mode for the entire page.

When enabled, errors in components won't crash the entire application. Instead, they're handled according to the `failhandler` or silently ignored.

**Example**:
```python
# Production app with error resilience
app = AppPage(failsafe=True)
```

### `failhandler: Callable[[Exception], Union[NoReturn, bool]] = None`
**Type**: `Optional[Callable[[Exception], Union[NoReturn, bool]]]`  
**Default**: `None`  
**Description**: Global error handler for the page.

Called when exceptions occur in components that don't have their own error handlers.

**Example**:
```python
def global_error_handler(error: Exception) -> bool:
    st.error(f"Application error: {error}")
    logging.error(error, exc_info=True)
    return True  # Continue execution

app = AppPage(failsafe=True, failhandler=global_error_handler)
```

### `strict: bool = True`
**Type**: `bool`  
**Default**: `True`  
**Description**: Enable strict mode for type checking and validation.

**Example**:
```python
app = AppPage(strict=True)  # Strict validation
```

### `standard: BaseStandard = None`
**Type**: `Optional[BaseStandard]`  
**Default**: `None`  
**Description**: Configuration standard to apply to components automatically.

Standards allow you to pre-configure components with default behaviors (stateful, error handling, etc.) based on component type.

**Example**:
```python
from declarative_streamlit.config.common.stdstreamlit import StreamlitCommonStandard

app = AppPage(standard=StreamlitCommonStandard())
```

## Attributes

### Public Attributes

Inherited from `Canvas`:
- `failsafe: bool` - Current failsafe setting
- `failhandler: Optional[Callable]` - Current error handler
- `strict: bool` - Current strict mode setting

### Protected Attributes

#### `_body: Schema`
**Type**: `Schema`  
**Description**: Internal schema managing the component hierarchy.

#### `_standard: Optional[BaseStandard]`
**Type**: `Optional[BaseStandard]`  
**Description**: Configuration standard applied to components.

When set, the standard automatically configures components based on their type (e.g., making certain widgets stateful by default).

## Properties

### `main_body: Layer`
**Type**: `Layer`  
**Inherited from**: `Canvas`  
**Description**: Access the main body layer containing all components.

**Example**:
```python
app = AppPage()
app.add_component(st.button, "Click", key="btn")

# Access component
button = app.main_body["btn"]
print(len(app.main_body))  # Number of components
```

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
    Add a component to the page.
    
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

**Description**: Add individual Streamlit components (widgets, text elements, media, etc.) to the page.

**Behavior**:
1. Validates component is callable
2. Wraps in `StreamlitComponentParser`
3. Applies standard configuration if available
4. Adds to main body schema
5. Returns parser for further configuration

**Example**:
```python
app = AppPage()

# Simple component
app.add_component(st.title, "My Application")

# Component with configuration
app.add_component(
    st.button, 
    "Submit", 
    key="submit_btn",
    type="primary"
).set_stateful(True).add_effect(
    lambda val: st.success("Clicked!") if val else None
)

# Component from parser
from declarative_streamlit.core.build.cstparser import StreamlitComponentParser

parser = StreamlitComponentParser(st.text_input, "Name:", key="name")
app.add_component(parser)
```

**Standard Integration**:
When a standard is set, components are automatically configured:
```python
app = AppPage(standard=StreamlitCommonStandard())

# This button automatically gets standard configurations
btn = app.add_component(st.button, "Click", key="btn")
# - Stateful behavior based on standard
# - Error handling based on standard
# - Strict mode based on standard
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
    Add a container to the page.
    
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

**Description**: Add layout containers (columns, expanders, containers, tabs, etc.) to organize components.

**Behavior**:
1. Validates container is callable
2. Wraps in `StreamlitLayoutParser`
3. Applies standard configuration including column-based settings
4. Adds to main body schema
5. Returns parser for nested component addition

**Example**:
```python
app = AppPage()

# Simple container
app.add_container(st.container, border=True)

# Container with nested components using 'with' syntax
with app.add_container(st.expander, "Details") as expander:
    expander.add_component(st.text, "Hidden content")
    expander.add_component(st.button, "Action", key="action_btn")

# Column-based container
cols = app.add_container(st.columns, 3).set_column_based(True)
cols.add_component(st.metric, "Metric 1", "100")
cols.add_component(st.metric, "Metric 2", "200")
cols.add_component(st.metric, "Metric 3", "300")
```

**Column-Based Containers**:
Some containers distribute components across columns:
```python
# Must set column_based for st.columns, st.tabs
cols = app.add_container(st.columns, 2).set_column_based(True)

# Each component goes to next column
cols.add_component(st.button, "Left", key="left")
cols.add_component(st.button, "Right", key="right")
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
    Add a function to the page.
    
    Args:
        function: The function to execute
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        StreamlitComponentParser: Parser wrapping the function
        
    Raises:
        TypeError: If function is not callable
    """
```

**Description**: Add custom Python functions that will be executed during rendering.

**Example**:
```python
app = AppPage()

def display_greeting(name: str):
    st.write(f"Hello, {name}!")
    st.balloons()

# Add function with arguments
app.add_function(display_greeting, "Alice")

# Add lambda function
app.add_function(lambda: st.info("This is a custom function"))
```

**Use Cases**:
- Custom logic that doesn't fit standard components
- Complex rendering that combines multiple Streamlit calls
- Conditional rendering based on state

#### `add_fragment()`
```python
def add_fragment(
    self,
    fragment: Union[Callable[..., Any], Fragment],
) -> Fragment:
    """
    Add a fragment to the page.
    
    Args:
        fragment: Fragment instance or callable
        
    Returns:
        Fragment: The added fragment
        
    Raises:
        TypeError: If fragment is not callable
    """
```

**Description**: Embed reusable fragment components that can rerun independently of the main page.

**Example**:
```python
from declarative_streamlit.base import AppPage, AppFragment

app = AppPage()

# Create a fragment
fragment = AppFragment(name="stats_fragment")
fragment.add_component(st.metric, "Users", "1000")
fragment.add_component(st.button, "Refresh", key="refresh_stats")

# Add fragment to page
app.add_fragment(fragment)
```

**Benefits**:
- Isolated reruns improve performance
- Reusable across multiple pages
- Independent state management

### Rendering and Execution

#### `start()`
```python
def start(self) -> AppPage:
    """
    Start the app page by rendering all components in the main body.
    
    Returns:
        self: The AppPage instance for method chaining
    """
```

**Description**: Initiates the rendering process, executing all components in order.

**Behavior**:
1. Calls `_body()` which triggers the schema rendering
2. Components execute in the order they were added
3. Error handling applied according to failsafe settings
4. Returns self for method chaining

**Example**:
```python
app = AppPage()
app.add_component(st.title, "Hello World")
app.add_component(st.button, "Click Me", key="btn")

# Render the page
app.start()

# Or use call syntax
app()  # Equivalent to app.start()
```

### Serialization

#### `serialize()`
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize the app page to a dictionary.
    
    Returns:
        Dict[str, Any]: Dictionary representation of the page
    """
```

**Description**: Convert the page structure to a JSON-compatible dictionary.

**Return Structure**:
```python
{
    "__page__": {
        # Schema serialization with all components
    },
    "__config__": {
        "strict": bool,
        "failsafe": bool
    }
}
```

**Example**:
```python
app = AppPage()
app.add_component(st.title, "My App")
app.add_component(st.button, "Click", key="btn")

# Serialize
data = app.serialize()

# Save to file
import json
with open("app_structure.json", "w") as f:
    json.dump(data, f, indent=2)

# Display in Streamlit
st.json(data)
```

**Use Cases**:
- Debugging application structure
- Saving application configurations
- Exporting to other formats
- Introspection and analysis

### Page Configuration

#### `set_page_config()` (Static Method)
```python
@staticmethod
def set_page_config(
    title: str = "Streamlit App",
    layout: Literal["centered", "wide"] = "centered",
    initial_sidebar_state: Literal["auto", "expanded", "collapsed"] = "auto",
    page_icon: Optional[str] = None,
    **kwargs: Any,
) -> None:
    """
    Set the configuration for the Streamlit page.
    
    Args:
        title: The title of the app
        layout: Layout mode ("centered" or "wide")
        initial_sidebar_state: Initial sidebar state
        page_icon: Emoji or image for page icon
        **kwargs: Additional arguments passed to st.set_page_config
    """
```

**Description**: Configure Streamlit page settings. Must be called before creating any components.

**Example**:
```python
# Configure page before creating app
AppPage.set_page_config(
    title="My Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

app = AppPage()
# ... add components
app.start()
```

**Important**: This wraps `streamlit.set_page_config()` and has the same restrictions:
- Must be called only once per app
- Must be called before any other Streamlit command
- Usually called at the top of your script

**Validation**: Uses `StreamlitPageConfig` Pydantic model for validation:
```python
class StreamlitPageConfig(BaseModel):
    title: str = "Streamlit App"
    layout: Literal["centered", "wide"] = "centered"
    initial_sidebar_state: Literal["auto", "expanded", "collapsed"] = "auto"
    page_icon: Optional[str] = None
```

### Special Methods

#### `__repr__()`
```python
def __repr__(self) -> str:
    """String representation for debugging."""
    return f"AppPage({self.__str__()})"
```

#### `__call__()`
Inherited from `Canvas`. Allows calling the page instance to start rendering:
```python
app = AppPage()
app.add_component(st.title, "Hello")
app()  # Calls app.start()
```

## Usage Examples

### Basic Application

```python
from declarative_streamlit.base import AppPage
import streamlit as st

# Configure page
AppPage.set_page_config(
    title="Basic App",
    layout="centered"
)

# Create application
app = AppPage()

# Add components
app.add_component(st.title, "Welcome")
app.add_component(st.write, "This is a basic application")
app.add_component(st.button, "Click Me", key="click_btn")

# Render
app.start()
```

### Application with Containers

```python
from declarative_streamlit.base import AppPage
import streamlit as st

AppPage.set_page_config(layout="wide")
app = AppPage()

app.add_component(st.title, "Dashboard")

# Sidebar filters
with app.add_container(st.sidebar) as sidebar:
    sidebar.add_component(st.selectbox, "Category", ["A", "B", "C"], key="cat")
    sidebar.add_component(st.slider, "Range", 0, 100, (25, 75), key="range")

# Main content in columns
with app.add_container(st.columns, 3).set_column_based(True) as cols:
    cols.add_component(st.metric, "Metric 1", "100", "+10%")
    cols.add_component(st.metric, "Metric 2", "200", "-5%")
    cols.add_component(st.metric, "Metric 3", "300", "+15%")

# Expandable details
with app.add_container(st.expander, "View Details") as exp:
    exp.add_component(st.write, "Detailed information here")
    exp.add_component(st.dataframe, data)

app.start()
```

### Error Handling

```python
from declarative_streamlit.base import AppPage
import streamlit as st
import logging

# Global error handler
def handle_error(error: Exception) -> bool:
    st.error(f"Error: {error}")
    logging.error(error, exc_info=True)
    return True  # Continue

app = AppPage(failsafe=True, failhandler=handle_error)

# Component with custom error handler
app.add_component(
    st.button, "Test", key="test"
).set_errhandler(
    lambda e: st.warning(f"Button error: {e}")
).set_fatal(False)

# This will fail but won't crash the app
app.add_component(lambda: 1/0)  # Handled by global handler

app.start()
```

### Using Standards

```python
from declarative_streamlit.base import AppPage
from declarative_streamlit.config.common.stdstreamlit import StreamlitCommonStandard
import streamlit as st

# Create app with standard
app = AppPage(standard=StreamlitCommonStandard())

# Components automatically configured per standard
app.add_component(st.text_input, "Name", key="name")
# ^ Automatically stateful if standard defines it

app.add_component(st.selectbox, "Option", ["A", "B"], key="opt")
# ^ Automatically configured per standard

app.start()
```

### Component Access and Effects

```python
from declarative_streamlit.base import AppPage, SessionState
import streamlit as st

app = AppPage()

# Create session state
counter = SessionState("counter", initial_value=0)

# Add button with effects
app.add_component(
    st.button, "Increment", key="inc_btn"
).add_effect(
    lambda val: counter.set_value(counter.value + 1) if val else None
).add_effect(
    lambda val: st.success(f"Count: {counter.value}") if val else None
)

# Access component by key
button_parser = app["inc_btn"]
print(button_parser)

# Access by index
first_component = app[0]

app.start()
```

### Fragments Integration

```python
from declarative_streamlit.base import AppPage, AppFragment
import streamlit as st

app = AppPage()
AppPage.set_page_config(layout="wide")

# Create reusable fragment
stats_fragment = AppFragment(name="stats", run_every=5)
stats_fragment.add_component(st.metric, "Live Users", "1,234")
stats_fragment.add_component(st.metric, "Revenue", "$12,345")

# Main page
app.add_component(st.title, "Dashboard")

# Embed fragment
app.add_fragment(stats_fragment)

# More page content
app.add_component(st.write, "Other content that doesn't rerun")

app.start()
```

### Serialization Example

```python
from declarative_streamlit.base import AppPage
import streamlit as st
import json

app = AppPage()
app.add_component(st.title, "Serialization Demo")
app.add_component(st.button, "Click", key="btn")

# Serialize the app structure
app_structure = app.serialize()

# Display serialized structure
st.json(app_structure)

# Download as JSON
st.download_button(
    label="Download App Structure",
    data=json.dumps(app_structure, indent=2),
    file_name="app_structure.json",
    mime="application/json"
)

app.start()
```

## Best Practices

### 1. Configure Page First
Always call `set_page_config()` before creating the AppPage:
```python
# Correct
AppPage.set_page_config(layout="wide")
app = AppPage()

# Wrong - may cause errors
app = AppPage()
AppPage.set_page_config(layout="wide")  # Too late
```

### 2. Use Keys for Interactive Components
Always provide keys for widgets that maintain state:
```python
# Good
app.add_component(st.text_input, "Name", key="user_name")

# Bad - state won't persist correctly
app.add_component(st.text_input, "Name")
```

### 3. Use 'with' for Containers
Use context manager syntax for containers:
```python
# Readable and clear
with app.add_container(st.expander, "Details") as exp:
    exp.add_component(st.write, "Content")

# Less clear
exp = app.add_container(st.expander, "Details")
exp.add_component(st.write, "Content")
```

### 4. Set column_based for Column Containers
```python
# Required for st.columns, st.tabs
cols = app.add_container(st.columns, 3).set_column_based(True)

# Not required for st.container, st.expander
container = app.add_container(st.container, border=True)
```

### 5. Use Standards for Consistency
```python
# Define once, apply everywhere
standard = StreamlitCommonStandard()
app = AppPage(standard=standard)

# All components automatically configured
app.add_component(st.button, "Submit", key="submit")
# ^ Automatically gets standard configurations
```

### 6. Enable Failsafe in Production
```python
# Development
app = AppPage(failsafe=False)  # Fail fast

# Production
app = AppPage(
    failsafe=True,
    failhandler=production_error_handler
)
```

### 7. Organize with Functions
```python
def build_sidebar(app: AppPage):
    with app.add_container(st.sidebar) as sidebar:
        sidebar.add_component(st.selectbox, "Filter", [...], key="filter")

def build_main_content(app: AppPage):
    app.add_component(st.title, "Main Content")
    # ...

app = AppPage()
build_sidebar(app)
build_main_content(app)
app.start()
```

## Error Handling

### Common Exceptions

#### `TypeError: Expected a callable`
**Cause**: Passing non-callable to `add_component` or `add_container`  
**Solution**: Ensure you pass function references, not results

```python
# Wrong
app.add_component(st.button("Click", key="btn"))  # Returns bool

# Correct
app.add_component(st.button, "Click", key="btn")  # Function reference
```

#### `KeyError: Key not found`
**Cause**: Accessing component with invalid key  
**Solution**: Verify key exists

```python
# Check before accessing
if "my_key" in app.main_body:
    component = app["my_key"]
```

#### `ValueError: failhandler must be callable`
**Cause**: Setting non-callable failhandler  
**Solution**: Use callable

```python
# Wrong
app.set_failhandler("not callable")

# Correct
app.set_failhandler(lambda e: print(e))
```

#### `StreamlitAPIException: set_page_config() can only be called once`
**Cause**: Calling `set_page_config()` multiple times  
**Solution**: Call only once at the start

```python
# Call once at top of script
AppPage.set_page_config(layout="wide")
```

## Performance Considerations

### Fragment Usage
Use fragments for components that update independently:
```python
# Bad - entire page reruns on button click
app.add_component(st.button, "Refresh Data", key="refresh")
app.add_component(expensive_data_component)

# Good - only fragment reruns
fragment = AppFragment(name="data")
fragment.add_component(st.button, "Refresh", key="refresh")
fragment.add_component(expensive_data_component)
app.add_fragment(fragment)
```

### Component Organization
Group related components in containers for better organization and performance:
```python
# Organized and efficient
with app.add_container(st.expander, "Settings") as settings:
    # 10 setting components
    settings.add_component(...)
```

## Related Components

- **[Canvas](./canvas.md)** - Base class that AppPage extends
- **[AppFragment](./app-fragment.md)** - Fragment implementation for isolated reruns
- **[AppDialog](./app-dialog.md)** - Dialog implementation for modals
- **[SessionState](./session-state.md)** - State management

## See Also

- [Examples](../../examples/) - Complete application examples
- [Core Parsers](../../core/docs/parsers.md) - Component and layout parser details
- [Standards](../../config/docs/standards.md) - Configuration standards documentation

---

**Navigation**: [README](./README.md) | [Canvas](./canvas.md) | [AppFragment](./app-fragment.md) | [AppDialog](./app-dialog.md) | [SessionState](./session-state.md)
