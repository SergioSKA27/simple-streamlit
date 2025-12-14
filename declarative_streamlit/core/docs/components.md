# Components Documentation

## Overview

The `components` submodule provides concrete implementations of visual and interactive elements. These classes extend the base abstractions (`Renderable`, `Stateful`, `Composable`) to create fully functional Streamlit components with enhanced capabilities.

## Module Structure

```
components/
├── __init__.py
├── container.py       # Layout container component
├── ielement.py        # Interactive element component
├── velement.py        # Visual element component
└── models/            # Pydantic validation models
    ├── ielement.py
    └── __pycache__/
```

---

## IElement (Interactive Element)

**Location**: `core/components/ielement.py`

### Purpose

`IElement` represents interactive Streamlit components that maintain state through session storage. These are components that users can interact with and whose values need to be tracked across reruns (buttons, text inputs, select boxes, sliders, etc.).

### Class Definition

```python
class IElement(Renderable, Stateful):
    """
    Base class for all interactive elements.
    
    Combines rendering capabilities with state management for
    components that require user interaction tracking.
    
    Examples: Button, Checkbox, TextInput, Selectbox, Slider
    
    Attributes:
        key (str): Unique identifier for session state tracking
        strict (bool): Whether to enforce key requirement
        _base_component (Callable): The underlying Streamlit component
        _internal_state (Dict[str, Any]): Internal state storage
    """
```

### Inheritance Hierarchy

```
Renderable + Stateful
    └── IElement
```

**Multiple Inheritance**: IElement inherits from both `Renderable` and `Stateful`, combining rendering lifecycle with state management.

### Constructor

```python
def __init__(self, *args, **kwargs):
    """
    Initialize interactive element.
    
    Args:
        *args: Positional arguments for the Streamlit component
        **kwargs: Keyword arguments for the component
            key (str, optional): Session state identifier
            
    Attributes:
        _internal_state (Dict[str, Any]): Internal state storage
        
    Validation:
        Uses IElementConfig Pydantic model
        
    Notes:
        - If 'key' not provided, behavior depends on strict mode
        - Calls both Renderable.__init__ and Stateful.__init__
    """
```

**Initialization Order**:
```python
# 1. Validate inputs
config = IElementConfig(args=args, kwargs=kwargs)

# 2. Initialize Renderable
Renderable.__init__(self, *config.args, **config.kwargs)

# 3. Initialize Stateful
Stateful.__init__(self, *config.args, **config.kwargs)

# 4. Initialize internal state
self._internal_state: Dict[str, Any] = {}
```

### Rendering

#### render()

**Signature**:
```python
def render(self, *args, **kwargs) -> Any:
    """
    Render the interactive component.
    
    Args:
        *args: Runtime positional arguments (override constructor args)
        **kwargs: Runtime keyword arguments (override constructor kwargs)
        
    Returns:
        Any: The component's current value (from session state)
        
    Raises:
        ValueError: If base_component not set
        ValueError: If strict mode enabled and no key provided
        
    Behavior:
        1. Validates base_component is set
        2. Uses runtime args/kwargs or falls back to constructor values
        3. Extracts and validates 'key' from kwargs
        4. Calls the Streamlit component
        5. Returns the component's value
    """
```

**Implementation**:
```python
def render(self, *args, **kwargs) -> Any:
    if not self._base_component:
        raise ValueError("Base component must be set before rendering")
        
    args = args or self.args
    kwargs = kwargs or self.kwargs

    # Extract and validate key
    if "key" in kwargs:
        self.set_key(kwargs["key"])
    else:
        if self.is_strict():
            raise ValueError("Key must be provided in strict mode")
    
    # Render component
    return self._base_component(*args, **kwargs)
```

**Key Handling Logic**:
- If `key` in kwargs → extract and set via `set_key()`
- If `key` not in kwargs + strict mode → raise ValueError
- If `key` not in kwargs + non-strict → proceed (state not tracked)

### State Management

#### track_state()

**Signature**:
```python
def track_state(self) -> Any:
    """
    Track and retrieve current state from session.
    
    Returns:
        Any: Current state value, or None if key doesn't exist
        
    Raises:
        ValueError: If key is invalid or not set
        
    Validation:
        Uses StateKeyConfig Pydantic model
    """
```

**Implementation**:
```python
def track_state(self) -> Any:
    # Validate key
    try:
        config = StateKeyConfig(key=self.key)
    except ValueError:
        raise ValueError("Invalid key: must be a non-empty string") from None
        
    # Check session state
    if config.key not in session_state:
        return None

    return session_state[config.key]
```

**Usage Pattern**:
```python
# Get current state
current_value = element.track_state()

# Or use the public API
current_value = element.get_state()
```

#### _set_state()

**Signature**:
```python
def _set_state(self, state: Any) -> Any:
    """
    Set internal state (private implementation).
    
    Args:
        state (Any): New state value
        
    Returns:
        Any: The state that was set
        
    Notes:
        This updates _internal_state, not session_state
        Use the public set_state() method for session state
    """
```

**Implementation**:
```python
def _set_state(self, state):
    self._internal_state = state
    return self._internal_state
```

### Configuration

#### set_key()

**Signature**:
```python
def set_key(self, key: str) -> T:
    """
    Set the session state key with validation.
    
    Args:
        key (str): Unique identifier (non-empty string)
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If key is invalid
        
    Validation:
        Uses StateKeyConfig Pydantic model
    """
```

**Enhanced Validation**:
```python
def set_key(self, key: str) -> T:
    # Validate using Pydantic model
    config = StateKeyConfig(key=key)
    
    # Call parent implementation
    return super().set_key(config.key)
```

#### _set_base_component()

**Signature**:
```python
def _set_base_component(self, base_component: Callable[..., Any]) -> T:
    """
    Set the Streamlit component with validation.
    
    Args:
        base_component: The Streamlit function (st.button, st.text_input, etc.)
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If base_component is not callable
        
    Validation:
        Uses BaseComponentConfig Pydantic model
    """
```

### Serialization

#### serialize()

**Signature**:
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize to dictionary format.
    
    Returns:
        dict: {
            "__component__": str (component function name),
            "__args__": {
                "args": List[Any],
                "kwargs": Dict[str, Any]
            },
            "__type__": "IElement"
        }
        
    Raises:
        ValueError: If base_component not set
    """
```

**Example Output**:
```python
{
    "__component__": "button",
    "__args__": {
        "args": [],
        "kwargs": {
            "label": "Click me",
            "key": "my_button"
        }
    },
    "__type__": "IElement"
}
```

#### deserialize()

**Signature**:
```python
@classmethod
def deserialize(
    cls,
    data: Dict[str, Any],
    component_map: Dict[str, Callable[..., Any]]
) -> 'IElement':
    """
    Deserialize from dictionary.
    
    Args:
        data: Serialized element data
        component_map: Mapping of component names to callables
            Example: {"button": st.button, "text_input": st.text_input}
            
    Returns:
        IElement: Reconstructed instance
        
    Raises:
        ValueError: If required fields missing or invalid
        KeyError: If component not in component_map
    """
```

**Validation Logic**:
```python
# Required fields
required_fields = ["__component__", "__args__", "__type__"]
for field in required_fields:
    if field not in data:
        raise ValueError(f"Missing required field '{field}'")
        
# Type validation
if data["__type__"] != "IElement":
    raise ValueError(f"Expected type 'IElement', got '{data['__type__']}'")
    
# Component lookup
if data["__component__"] not in component_map:
    raise KeyError(f"Component '{data['__component__']}' not found")
```

---

## VElement (Visual Element)

**Location**: `core/components/velement.py`

### Purpose

`VElement` represents stateless visual components that don't require user interaction tracking. These are purely presentational elements (text, images, charts, dataframes, etc.).

### Class Definition

```python
class VElement(Renderable):
    """
    Base class for all stateless visual elements.
    
    Provides simplified rendering for components that don't
    need state tracking.
    
    Examples: Text, Markdown, Image, Chart, DataFrame, HTML
    """
```

### Inheritance Hierarchy

```
Renderable
    └── VElement
```

**Single Inheritance**: VElement only inherits from `Renderable` since it doesn't need state management.

### Constructor

```python
def __init__(self, *args, **kwargs):
    """
    Initialize visual element.
    
    Args:
        *args: Positional arguments for the Streamlit component
        **kwargs: Keyword arguments for the component
        
    Notes:
        Simply delegates to Renderable.__init__
        No state-related attributes needed
    """
```

**Simplicity**: Much simpler than IElement since no state management required.

### Rendering

#### render()

**Signature**:
```python
def render(self, *args, **kwargs) -> Any:
    """
    Render the visual component.
    
    Args:
        *args: Runtime positional arguments (override constructor args)
        **kwargs: Runtime keyword arguments (override constructor kwargs)
        
    Returns:
        Any: The rendered component object
        
    Notes:
        - No key validation needed
        - No state tracking
        - Simple pass-through to base component
    """
```

**Implementation**:
```python
def render(self, *args, **kwargs):
    args = args or self.args
    kwargs = kwargs or self.kwargs
    return self._base_component(*args, **kwargs)
```

**Simplicity**: Just calls the base component with arguments - no complexity.

### Serialization

#### serialize()

**Signature**:
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize to dictionary format.
    
    Returns:
        dict: {
            "__component__": str (component function name),
            "__args__": {
                "args": List[Any],
                "kwargs": Dict[str, Any]
            },
            "__type__": "VElement"
        }
    """
```

**Example Output**:
```python
{
    "__component__": "text",
    "__args__": {
        "args": ["Hello, World!"],
        "kwargs": {}
    },
    "__type__": "VElement"
}
```

**Note**: Nearly identical to IElement serialization, just different `__type__`.

---

## Container

**Location**: `core/components/container.py`

### Purpose

`Container` represents layout components that can hold other components and containers. It combines rendering capabilities with composition to create hierarchical layouts.

### Class Definition

```python
class Container(Renderable, Composable):
    """
    Layout container for organizing components.
    
    Combines rendering with composition to create complex
    hierarchical layouts with multiple layers.
    
    Examples: st.container, st.columns, st.tabs, st.expander
    """
```

### Inheritance Hierarchy

```
Renderable + Composable
    └── Container
```

**Multiple Inheritance**: Container inherits from both `Renderable` and `Composable`.

### Constructor

```python
def __init__(self, *args, **kwargs):
    """
    Initialize container.
    
    Args:
        *args: Positional arguments for the container component
        **kwargs: Keyword arguments for the container component
        
    Attributes:
        _base_component (Callable): The Streamlit container function
        _top_render (bool): Initialized to False
        
    Notes:
        - Calls both Renderable and Composable __init__
        - Sets schema body name to "__container__"
    """
```

**Initialization**:
```python
# Initialize both parent classes
Renderable.__init__(self, *args, **kwargs)
Composable.__init__(self)

# Container-specific setup
self._base_component: Callable[..., Any] = None
self._top_render: bool = False
self.schema.set_body_name("__container__")
```

### Rendering

#### render()

**Signature**:
```python
def render(self, *args, **kwargs) -> Any:
    """
    Render the container and its contents.
    
    Args:
        *args: Runtime arguments for the container
        **kwargs: Runtime keyword arguments
        
    Returns:
        Any: The rendered container
        
    Process:
        1. Creates the container component
        2. Renders based on column_based setting
        3. Renders all layers and their components
    """
```

**Implementation**:
```python
def render(self, *args, **kwargs) -> Any:
    self.lrender(self._base_component, *args, **kwargs)
```

**Note**: Delegates to `lrender()` from Composable mixin.

### Serialization

#### serialize()

**Signature**:
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize container to dictionary.
    
    Returns:
        dict: {
            "__component__": str (component name),
            "__args__": {
                "args": List[Any],
                "kwargs": Dict[str, Any]
            },
            "__type__": "Container"
        }
        
    Notes:
        - Sets schema body name to "__children__" before serialization
        - Only serializes if base_component is set
    """
```

**Implementation**:
```python
def serialize(self):
    if self._base_component is not None:
        self.schema.set_body_name("__children__")
    return {
        "__component__": self._base_component.__name__,
        "__args__": {
            "args": self.args,
            "kwargs": self.kwargs,
        },
        "__type__": "Container",
    }
```

### String Representation

#### \_\_str\_\_()

**Signature**:
```python
def __str__(self) -> str:
    """
    String representation of container.
    
    Returns:
        str: "Container(<component_name>): <schema>"
    """
```

**Example Output**:
```
Container(columns): Schema: {...}
```

---

## Component Comparison

### Feature Matrix

| Feature              | IElement | VElement | Container |
|----------------------|----------|----------|-----------|
| Inherits Renderable  | ✅       | ✅       | ✅        |
| Inherits Stateful    | ✅       | ❌       | ❌        |
| Inherits Composable  | ❌       | ❌       | ✅        |
| Session State        | ✅       | ❌       | ❌        |
| Key Required         | ✅*      | ❌       | ❌        |
| Can Hold Components  | ❌       | ❌       | ✅        |
| Error Handling       | ✅       | ✅       | ✅        |
| Effect System        | ✅       | ✅       | ✅        |
| Serializable         | ✅       | ✅       | ✅        |

*In strict mode (default)

### When to Use Each

#### Use IElement when:
- Component requires user interaction
- Need to track value across reruns
- Need to respond to state changes
- Examples: buttons, inputs, selects, sliders, checkboxes

#### Use VElement when:
- Component is purely visual
- No interaction needed
- No state tracking required
- Examples: text, images, charts, dataframes, markdown

#### Use Container when:
- Need to organize multiple components
- Building complex layouts
- Need layer-based organization
- Examples: columns, tabs, expanders, containers

---

## Usage Examples

### Example 1: Interactive Button with State Tracking

```python
from declarative_streamlit.core import IElement
import streamlit as st

# Create button
button = IElement("Submit Form", key="submit_btn")
button._set_base_component(st.button)

# Configure
button.set_strict(True)  # Require key
button.set_fatal(False)  # Non-fatal errors

# Add effects
def on_submit(clicked):
    if clicked:
        st.session_state.form_submitted = True
        st.success("Form submitted!")

button.add_effect(on_submit)

# Render
was_clicked = button()

# Check state anywhere in the app
if button.track_state():
    st.write("Button was clicked this session")
```

### Example 2: Simple Text Display

```python
from declarative_streamlit.core import VElement
import streamlit as st

# Create text element
title = VElement("# My Application")
title._set_base_component(st.markdown)

# Add analytics effect
title.add_effect(lambda _: analytics.track("title_rendered"))

# Render
title()

# Can re-render with different content
title.render("# Different Title")
```

### Example 3: Text Input with Validation

```python
from declarative_streamlit.core import IElement
import streamlit as st

# Create input
email_input = IElement(
    "Email Address",
    placeholder="user@example.com",
    key="email"
)
email_input._set_base_component(st.text_input)

# Validation effect
def validate_email(email):
    if email and "@" not in email:
        st.error("Invalid email address")
    elif email:
        st.success("Valid email")

email_input.add_effect(validate_email)

# Render
email = email_input()

# Access state
current_email = email_input.track_state()
```

### Example 4: Column-Based Container

```python
from declarative_streamlit.core import Container
from declarative_streamlit.core.build import StreamlitComponentParser
import streamlit as st

# Create columns container
cols = Container()
cols._set_base_component(st.columns)
cols.set_column_based(True)  # Essential for columns!
cols.set_component_parser(StreamlitComponentParser)

# Add 3 layers (one per column)
for i in range(3):
    cols.add_layer(i)

# Populate columns
cols.add_to_layer(0, st.metric, "Users", "1,234", "+12%")
cols.add_to_layer(1, st.metric, "Revenue", "$56K", "+8%")
cols.add_to_layer(2, st.metric, "Orders", "789", "+23%")

# Render with 3 columns
cols.lrender(st.columns, 3)
```

### Example 5: Nested Containers

```python
from declarative_streamlit.core import Container
from declarative_streamlit.core.build import StreamlitComponentParser
import streamlit as st

# Main container
main = Container(border=True)
main._set_base_component(st.container)
main.set_component_parser(StreamlitComponentParser)

# Add header
main.add_component(st.title, "Dashboard")

# Add nested columns
cols = Container()
cols._set_base_component(st.columns)
cols.set_column_based(True)
cols.set_component_parser(StreamlitComponentParser)

cols.add_layer("left")
cols.add_layer("right")
cols.add_to_layer("left", st.write, "Left column")
cols.add_to_layer("right", st.write, "Right column")

# Add columns to main
main.schema.add_component(cols)

# Render
main.render()
cols.lrender(st.columns, 2)
```

### Example 6: Error Handling Patterns

```python
# Pattern 1: Fatal errors (default)
critical = IElement("Submit", key="submit")
critical._set_base_component(st.button)
critical.set_fatal(True)
# Errors will raise and halt app

# Pattern 2: Non-fatal with handler
optional = VElement("Optional content")
optional._set_base_component(st.text)
optional.set_fatal(False)
optional.set_errhandler(lambda e: st.warning("Content unavailable"))
# Errors handled gracefully

# Pattern 3: Silent failure
badge = VElement("New!")
badge._set_base_component(st.text)
badge.set_fatal(False)
# Errors suppressed completely
```

---

## Best Practices

### 1. Always Set Keys for Interactive Elements

```python
# ❌ Bad - no key
button = IElement("Click")
button.render()  # ValueError in strict mode

# ✅ Good - explicit key
button = IElement("Click", key="my_button")
button.render()
```

### 2. Use Appropriate Component Types

```python
# ❌ Bad - IElement for static text
text = IElement("Hello")  # Unnecessary complexity

# ✅ Good - VElement for static content
text = VElement("Hello")

# ✅ Good - IElement for interaction
button = IElement("Click", key="btn")
```

### 3. Set Column-Based Flag for Column Containers

```python
# ❌ Bad - forget column_based
cols = Container()
cols.lrender(st.columns, 3)  # Wrong rendering

# ✅ Good - set column_based
cols = Container()
cols.set_column_based(True)
cols.lrender(st.columns, 3)
```

### 4. Validate Serialization/Deserialization

```python
# Always provide complete component_map
component_map = {
    "button": st.button,
    "text_input": st.text_input,
    "selectbox": st.selectbox,
}

element = IElement.deserialize(data, component_map)
```

### 5. Use Effects for Side Effects

```python
# ❌ Bad - side effects in render
def render_with_side_effects():
    result = component.render()
    analytics.track("rendered")  # Tight coupling
    return result

# ✅ Good - effects for side effects
component.add_effect(lambda _: analytics.track("rendered"))
result = component.render()
```

---

## Type Annotations

```python
from typing import Any, Callable, Dict, List, Union, Optional
from streamlit import session_state

# Component types
Component = Callable[..., Any]

# Component map for deserialization
ComponentMap = Dict[str, Component]

# Serialized data
SerializedComponent = Dict[str, Any]

# Session state key
StateKey = str
```

---

## Common Pitfalls

### 1. Forgetting to Import session_state

```python
# ❌ Wrong
from declarative_streamlit.core import IElement

# ✅ Correct
from declarative_streamlit.core import IElement
from streamlit import session_state  # Needed for state tracking
```

### 2. Not Setting Base Component

```python
# ❌ Wrong
element = IElement("Click", key="btn")
element()  # ValueError

# ✅ Correct
element = IElement("Click", key="btn")
element._set_base_component(st.button)
element()
```

### 3. Using IElement for Non-Interactive Components

```python
# ❌ Wrong - unnecessary complexity
text = IElement("Hello", key="text")
text._set_base_component(st.text)

# ✅ Correct - simpler and appropriate
text = VElement("Hello")
text._set_base_component(st.text)
```

### 4. Incorrect Container Rendering

```python
# ❌ Wrong - render before lrender
container.render()
container.lrender(st.container)  # Renders twice

# ✅ Correct - only lrender
container.lrender(st.container)
```

---

## Performance Considerations

### IElement State Tracking

State tracking has minimal overhead:
```python
# O(1) session state lookup
value = element.track_state()
```

### VElement Simplicity

VElement has the lowest overhead (no state management).

### Container Layer Management

Layers are stored in a dictionary (O(1) access):
```python
layer = container.schema[layer_id]  # Fast lookup
```

---

## Revision History

| Version | Date       | Changes                     |
|---------|------------|-----------------------------|
| 1.0.0   | 2025-12-14 | Initial documentation       |

---

## See Also

- [Base Classes Documentation](./base-classes.md)
- [Parsers Documentation](./parsers.md)
- [Handlers Documentation](./handlers.md)
- [API Reference](./api-reference.md)
