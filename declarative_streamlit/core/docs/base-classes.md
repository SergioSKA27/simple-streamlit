# Base Classes Documentation

## Overview

The `base` submodule provides the foundational abstract base classes (ABCs) that define the core contracts and behaviors for all components in the declarative-streamlit framework. These classes implement essential patterns such as rendering lifecycle, state management, and component composition.

## Module Structure

```
base/
├── __init__.py
├── composable.py      # Layout composition base class
├── renderable.py      # Rendering lifecycle base class
├── stateful.py        # State management interface
└── models/            # Pydantic validation models
    ├── composable.py
    └── renderable.py
```

---

## Renderable

**Location**: `core/base/renderable.py`

### Purpose

`Renderable` is the abstract base class for all visual components in the framework. It establishes the rendering lifecycle, error handling strategies, and effect execution patterns that all visual elements must follow.

### Class Definition

```python
class Renderable(metaclass=ABCMeta):
    """
    Base class for all renderable components.
    
    Establishes the contract for component rendering, error handling,
    and post-render effects.
    """
```

### Inheritance Hierarchy

```
ABCMeta (Python stdlib)
    └── Renderable
        ├── IElement (interactive elements)
        ├── VElement (visual elements)
        └── Container (via multiple inheritance with Composable)
```

### Constructor

```python
def __init__(self, *args, **kwargs) -> None:
    """
    Initialize the renderable object.
    
    Args:
        *args: Variable positional arguments for the base component
        **kwargs: Keyword arguments for the base component
        
    Attributes:
        args (tuple): Positional arguments
        kwargs (dict): Keyword arguments
        _base_component (Optional[Callable]): The wrapped Streamlit component
        fatal (bool): Whether errors should halt execution (default: False)
        _errhandler (Optional[Callable]): Custom error handler
        _top_render (bool): Whether this is a top-level render (default: False)
        _effects (List[Callable]): Post-render effect functions
    """
```

**Validation**: Uses `RenderableConfig` Pydantic model to validate inputs.

### Abstract Methods

#### render()

**Signature**:
```python
@abstractmethod
def render(self, *args, **kwargs) -> Any:
    """
    Render the content.
    
    This method MUST be implemented by all subclasses.
    
    Args:
        *args: Runtime positional arguments (override constructor args)
        **kwargs: Runtime keyword arguments (override constructor kwargs)
        
    Returns:
        Any: The rendered component (typically a Streamlit object)
        
    Raises:
        NotImplementedError: If not implemented by subclass
    """
```

**Implementation Requirements**:
1. Must call the `_base_component` with appropriate arguments
2. Must handle both constructor-time and render-time arguments
3. Should support being called multiple times (idempotent when possible)

**Example Implementation** (from VElement):
```python
def render(self, *args, **kwargs):
    args = args or self.args
    kwargs = kwargs or self.kwargs
    return self._base_component(*args, **kwargs)
```

### Configuration Methods

All configuration methods use method chaining pattern (return `self`).

#### set_fatal()

**Signature**:
```python
def set_fatal(self, fatal: bool) -> T:
    """
    Set whether errors should be fatal.
    
    Args:
        fatal (bool): True = raise exceptions, False = handle gracefully
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If fatal is not a boolean
    """
```

**Usage**:
```python
# Fatal errors (default behavior)
component.set_fatal(True)  # Raises exceptions

# Non-fatal errors
component.set_fatal(False)  # Returns NonRenderError object
```

**Best Practices**:
- Use `fatal=True` for critical components (data loaders, authentication)
- Use `fatal=False` for optional UI elements (badges, tooltips)
- Always pair `fatal=False` with an error handler

#### set_errhandler()

**Signature**:
```python
def set_errhandler(self, handler: Callable[[Exception], Union[NoReturn, bool]]) -> T:
    """
    Set a custom error handler.
    
    Args:
        handler: Function that takes an Exception and returns:
                 - True: Error was handled, continue execution
                 - False: Error not handled, propagate
                 - NoReturn: Redirects/stops execution (st.switch_page, st.stop)
                 
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If handler is not callable
    """
```

**Validation**: Uses `ErrorHandlerConfig` Pydantic model.

**Usage**:
```python
# Simple error display
component.set_errhandler(lambda e: st.error(f"Error: {e}"))

# Conditional handling
def smart_handler(e: Exception) -> bool:
    if isinstance(e, ValueError):
        st.warning(str(e))
        return True
    return False  # Re-raise other errors

component.set_errhandler(smart_handler)

# Redirect on error
component.set_errhandler(lambda e: st.switch_page("error_page"))
```

#### set_top_render()

**Signature**:
```python
def set_top_render(self, top_render: bool) -> T:
    """
    Mark as top-level render component.
    
    Args:
        top_render (bool): True for container-level components
        
    Returns:
        self: For method chaining
    """
```

**Purpose**: Identifies components that act as render boundaries (containers, columns, tabs).

#### add_effect()

**Signature**:
```python
def add_effect(self, effect: Callable[..., Any]) -> T:
    """
    Add a post-render effect.
    
    Args:
        effect: Callable that receives the render result as first argument
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If effect is not callable
    """
```

**Validation**: Uses `EffectConfig` Pydantic model.

**Usage**:
```python
# Log render result
component.add_effect(lambda result: print(f"Rendered: {result}"))

# Conditional side effect
def update_analytics(result):
    if result:
        analytics.track("component_rendered", value=result)

component.add_effect(update_analytics)

# Chain multiple effects
component.add_effect(log_effect).add_effect(analytics_effect)
```

**Effect Execution**:
1. Effects execute AFTER successful rendering
2. Effects execute in order of addition
3. Errors in effects are caught and handled via `_safe_effect_execution`
4. Effect errors don't prevent subsequent effects from running

#### add_effects()

**Signature**:
```python
def add_effects(self, effects: List[Callable[..., Any]]) -> T:
    """
    Add multiple effects at once.
    
    Args:
        effects: List of callable effects
        
    Returns:
        self: For method chaining
    """
```

### Internal Methods

#### _set_base_component()

**Signature**:
```python
def _set_base_component(self, base_component: Callable[..., Any]) -> T:
    """
    Set the underlying Streamlit component.
    
    Args:
        base_component: The Streamlit function to wrap (st.button, st.text, etc.)
        
    Returns:
        self: For method chaining
        
    Validation:
        Uses BaseComponentConfig Pydantic model
    """
```

**Usage**: Called by parsers, not typically used directly by users.

#### _safe_render()

**Signature**:
```python
def _safe_render(self, *args, **kwargs) -> Union[NoReturn, Any]:
    """
    Safely render with error handling and effects.
    
    Execution Flow:
        1. Call render(*args, **kwargs)
        2. If successful and result exists:
           a. Execute all effects with result
        3. If error occurs:
           a. Call error handler if defined
           b. Return NonRenderError if not fatal
           c. Re-raise if fatal
           
    Returns:
        Render result or NonRenderError object
    """
```

**Error Handling Logic**:
```python
try:
    if res := self.render(*args, **kwargs):
        for eff in self._effects:
            self._safe_effect_execution(eff, res)
        return res
except Exception as e:
    status = False
    if self._errhandler:
        status = self._errhandler(e)
    if not status:
        return NonRenderError(e, self.fatal, self)
```

#### _safe_effect_execution()

**Signature**:
```python
def _safe_effect_execution(self, effect: Callable[..., Any], *args, **kwargs) -> None:
    """
    Execute an effect with error handling.
    
    Args:
        effect: The effect function to execute
        *args: Arguments to pass to effect
        **kwargs: Keyword arguments to pass to effect
        
    Raises:
        Exception: If error handler doesn't handle the error
    """
```

### Magic Methods

#### \_\_call\_\_()

**Signature**:
```python
def __call__(self, *args, **kwargs) -> Union[NoReturn, Any]:
    """
    Make the component callable.
    
    Args:
        *args: Override constructor args
        **kwargs: Override constructor kwargs
        
    Returns:
        Result of _safe_render()
        
    Usage:
        component()  # Use constructor args
        component("new", key="different")  # Use runtime args
    """
```

#### \_\_enter\_\_() and \_\_exit\_\_()

**Signatures**:
```python
def __enter__(self) -> Any:
    """Enter context manager - returns render() result."""
    return self.render()

def __exit__(self, exc_type, exc_value, traceback) -> None:
    """Exit context manager - propagates exceptions."""
    if exc_type:
        raise exc_type(exc_value).with_traceback(traceback)
```

**Usage**:
```python
with container.render() as c:
    st.write("Inside container")
    # c is the rendered container object
```

### Serialization

#### serialize()

**Signature**:
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize to dictionary.
    
    Returns:
        dict: {
            "base_component": str (component name),
            "args": tuple,
            "kwargs": dict,
            "fatal": bool,
            "top_render": bool
        }
    """
```

#### deserialize()

**Signature**:
```python
@classmethod
def deserialize(
    cls,
    data: Dict[str, Any],
    components: Dict[str, Callable[..., Any]]
) -> "Renderable":
    """
    Deserialize from dictionary.
    
    Args:
        data: Serialized component data
        components: Map of component names to callables
        
    Returns:
        Renderable: Reconstructed instance
    """
```

### Properties and Helpers

```python
def is_top_render(self) -> bool:
    """Check if this is a top-level render."""
    return self._top_render

def _get_base_component(self) -> Callable[..., Any]:
    """Get the wrapped component."""
    return self._base_component
```

---

## Stateful

**Location**: `core/base/stateful.py`

### Purpose

`Stateful` is an abstract base class that defines the interface for components that need to track and manage state through Streamlit's session state mechanism.

### Class Definition

```python
class Stateful(ABC):
    """
    Abstract base class for stateful components.
    
    Provides state tracking and mutation capabilities for
    interactive elements.
    """
```

### Inheritance Hierarchy

```
ABC (Python stdlib)
    └── Stateful
        └── IElement (interactive elements)
```

### Constructor

```python
def __init__(self, *_, **kwargs):
    """
    Initialize stateful object.
    
    Args:
        **kwargs: Arbitrary keyword arguments
            key (str, optional): Unique identifier for session state
            
    Attributes:
        key (str | None): Session state identifier
        editable (bool): Whether state can be modified (default: False)
        strict (bool): Whether key is required (default: True)
    """
```

### Abstract Methods

#### track_state()

**Signature**:
```python
@abstractmethod
def track_state(self) -> Any:
    """
    Retrieve the current state value.
    
    Returns:
        Any: The current state value from session_state
        
    Raises:
        NotImplementedError: If not implemented by subclass
    """
```

**Implementation Requirements**:
1. Must query Streamlit's `session_state` using `self.key`
2. Should return `None` if key doesn't exist
3. Should validate key before access

**Example Implementation** (from IElement):
```python
def track_state(self) -> Any:
    config = StateKeyConfig(key=self.key)  # Validate
    if config.key not in session_state:
        return None
    return session_state[config.key]
```

#### _set_state()

**Signature**:
```python
@abstractmethod
def _set_state(self, state: Any) -> Any:
    """
    Set the state value.
    
    Args:
        state (Any): New state value
        
    Returns:
        Any: The set state value
        
    Raises:
        NotImplementedError: If not implemented by subclass
    """
```

**Note**: This is an internal method. Use `set_state()` for public API.

### Public Methods

#### set_key()

**Signature**:
```python
def set_key(self, key: str) -> Self:
    """
    Set the session state key.
    
    Args:
        key (str): Unique identifier for this component's state
        
    Returns:
        self: For method chaining
    """
```

**Usage**:
```python
element.set_key("my_button")
```

#### get_key()

**Signature**:
```python
def get_key(self) -> str | None:
    """
    Get the session state key.
    
    Returns:
        str | None: The current key, or None if not set
    """
```

#### set_editable()

**Signature**:
```python
def set_editable(self, editable: bool) -> Self:
    """
    Set whether state can be modified programmatically.
    
    Args:
        editable (bool): True to allow set_state() calls
        
    Returns:
        self: For method chaining
    """
```

**Usage**:
```python
# Allow programmatic state changes
element.set_editable(True)
element.set_state("new_value")

# Prevent programmatic changes (default)
element.set_editable(False)
element.set_state("new_value")  # Raises Exception
```

#### set_strict()

**Signature**:
```python
def set_strict(self, strict: bool) -> Self:
    """
    Set strict mode for key validation.
    
    Args:
        strict (bool): True to require key, False to allow keyless components
        
    Returns:
        self: For method chaining
    """
```

**Usage**:
```python
# Strict mode (default) - key required
element.set_strict(True)
element.render()  # Raises ValueError if no key

# Non-strict mode - key optional
element.set_strict(False)
element.render()  # Works without key (state not tracked)
```

#### is_strict()

**Signature**:
```python
def is_strict(self) -> bool:
    """
    Check if component is in strict mode.
    
    Returns:
        bool: True if strict mode enabled
    """
```

#### set_state()

**Signature**:
```python
def set_state(self, state: Any) -> Any:
    """
    Set the state value (public API).
    
    Args:
        state (Any): New state value
        
    Returns:
        Any: The set state value
        
    Raises:
        Exception: If not editable
    """
```

**Implementation**:
```python
def set_state(self, state: Any):
    if not self.editable:
        raise Exception("The state is not editable")
    return self._set_state(state)
```

#### get_state()

**Signature**:
```python
def get_state(self) -> Any:
    """
    Get the current state value.
    
    Returns:
        Any: Current state from track_state()
    """
```

#### get_state_tracker()

**Signature**:
```python
def get_state_tracker(self) -> Callable[[], Any]:
    """
    Get a callable that tracks state.
    
    Returns:
        Callable: Function that returns current state when called
        
    Usage:
        tracker = element.get_state_tracker()
        current_value = tracker()  # Gets state each time called
    """
```

---

## Composable

**Location**: `core/base/composable.py`

### Purpose

`Composable` provides the foundation for building hierarchical layouts with multiple layers and components. It manages a `Schema` object that organizes components into layers and handles rendering strategies.

### Class Definition

```python
class Composable:
    """
    Base class for composable components that organize content in layers.
    
    Enables building complex layouts with:
    - Multi-layer organization
    - Column-based or row-based rendering
    - Component parser integration
    - Schema-based structure
    """
```

### Inheritance Hierarchy

```
Composable
    └── Container (via multiple inheritance with Renderable)
```

### Constructor

```python
def __init__(self):
    """
    Initialize composable instance.
    
    Attributes:
        schema (Schema): Layout organization structure
        _column_based (bool): Rendering strategy flag (default: False)
        _component_parser (Optional[Callable]): Parser for components
    """
```

### Configuration Methods

#### set_component_parser()

**Signature**:
```python
def set_component_parser(self, component_parser: Callable[..., Any]) -> T:
    """
    Set the parser for wrapping components.
    
    Args:
        component_parser: Parser class (typically StreamlitComponentParser)
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If parser is not callable
        
    Validation:
        Uses ComponentParserValidator Pydantic model
    """
```

**Usage**:
```python
container.set_component_parser(StreamlitComponentParser)
```

#### set_column_based()

**Signature**:
```python
def set_column_based(self, column_based: bool) -> "Composable":
    """
    Set rendering strategy.
    
    Args:
        column_based (bool): 
            - True: Render each layer in separate columns
            - False: Render all layers sequentially (row-based)
            
    Returns:
        self: For method chaining
    """
```

**Usage**:
```python
# Column-based (for st.columns, st.tabs)
container.set_column_based(True)

# Row-based (for st.container, st.expander)
container.set_column_based(False)
```

#### is_column_based()

**Signature**:
```python
def is_column_based(self) -> bool:
    """
    Check rendering strategy.
    
    Returns:
        bool: True if column-based, False if row-based
    """
```

### Layer Management

#### add_layer()

**Signature**:
```python
def add_layer(self, idlayer: Union[int, str]) -> Layer:
    """
    Add a new layer to the schema.
    
    Args:
        idlayer: Unique identifier for the layer (int or str)
        
    Returns:
        Layer: The created layer object
        
    Validation:
        Uses LayerIDValidator Pydantic model
    """
```

**Usage**:
```python
# Numeric layers
layer1 = container.add_layer(1)
layer2 = container.add_layer(2)

# Named layers
header = container.add_layer("header")
footer = container.add_layer("footer")
```

### Component Management

#### add_component()

**Signature**:
```python
def add_component(self, component: Callable[..., Any], *args, **kwargs) -> Any:
    """
    Add a component to the main body layer.
    
    Args:
        component: Streamlit component function
        *args: Positional arguments for component
        **kwargs: Keyword arguments for component
        
    Returns:
        Any: Parsed component object
        
    Raises:
        ValueError: If component_parser not set
    """
```

**Usage**:
```python
# Add to main body
container.add_component(st.text, "Hello")
container.add_component(st.button, "Click", key="btn1")
```

#### add_to_layer()

**Signature**:
```python
def add_to_layer(
    self,
    idlayer: Union[int, str],
    component: Callable[..., Any],
    *args,
    **kwargs
) -> Any:
    """
    Add a component to a specific layer.
    
    Args:
        idlayer: Layer identifier
        component: Streamlit component function
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Any: Parsed component
        
    Raises:
        ValueError: If component_parser not set
        KeyError: If layer doesn't exist
    """
```

**Usage**:
```python
# First create the layer
container.add_layer("sidebar")

# Then add components to it
container.add_to_layer("sidebar", st.selectbox, "Choose", options=["A", "B"])
container.add_to_layer("sidebar", st.button, "Submit", key="submit")
```

### Rendering

#### lrender()

**Signature**:
```python
def lrender(self, based_component: Callable[..., Any], *args, **kwargs) -> Any:
    """
    Render the layout based on strategy.
    
    Args:
        based_component: The container component (st.columns, st.container, etc.)
        *args: Arguments for based_component
        **kwargs: Keyword arguments for based_component
        
    Returns:
        Any: Rendered component
        
    Raises:
        ValueError: If component_parser not set
    """
```

**Internal Rendering Methods**:

##### __render_column_based()
```python
def __render_column_based(
    self,
    based_component: Callable[..., Any],
    *args,
    **kwargs
) -> Any:
    """
    Render in column-based layout.
    
    Each layer gets its own column.
    Respects layer order if specified.
    """
```

**Algorithm**:
```python
# Create base component (e.g., st.columns(3))
c = based_component(*args, **kwargs)

# Get layer render order
layers_to_render = (
    self.schema.main_body.order
    if self.schema.main_body.order
    else range(len(self.schema.main_body))
)

# Render each layer in its column
for k, layer_id in enumerate(layers_to_render):
    with c[k]:
        self.schema.main_body[layer_id]()
```

##### __render_row_based()
```python
def __render_row_based(
    self,
    based_component: Callable[..., Any],
    *args,
    **kwargs
) -> Any:
    """
    Render in row-based layout.
    
    All layers render sequentially in the same container.
    """
```

**Algorithm**:
```python
# Create base component (e.g., st.container())
c = based_component(*args, **kwargs)

# Render all layers in sequence
with c:
    self.schema()  # Calls all layers
```

### Schema Access

#### get_schema()

**Signature**:
```python
def get_schema(self) -> Schema:
    """
    Get the layout schema.
    
    Returns:
        Schema: The schema object managing layers
    """
```

#### clear()

**Signature**:
```python
def clear(self) -> "Composable":
    """
    Clear all layers and components.
    
    Returns:
        self: For method chaining
    """
```

### Serialization

#### serialize()

**Signature**:
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize to dictionary.
    
    Returns:
        dict: {
            "schema": dict (serialized schema),
            "column_based": bool
        }
    """
```

#### deserialize()

**Signature**:
```python
@classmethod
def deserialize(
    cls,
    data: Dict[str, Any],
    content_map: Optional[Dict[str, Any]] = None
) -> 'Composable':
    """
    Deserialize from dictionary.
    
    Args:
        data: Serialized composable data
        content_map: Map of content names to callables
        
    Returns:
        Composable: Reconstructed instance
    """
```

---

## Usage Examples

### Example 1: Basic Renderable

```python
from declarative_streamlit.core import VElement
import streamlit as st

# Create a visual element
text = VElement("Hello, World!")
text._set_base_component(st.text)

# Configure
text.set_fatal(False).add_effect(lambda _: print("Rendered!"))

# Render
text()  # Displays "Hello, World!" in Streamlit
```

### Example 2: Stateful Interactive Element

```python
from declarative_streamlit.core import IElement
import streamlit as st

# Create interactive element
button = IElement("Click me", key="my_button")
button._set_base_component(st.button)
button.set_strict(True)  # Require key

# Add state tracking
def on_click(clicked):
    if clicked:
        st.success("Button was clicked!")

button.add_effect(on_click)

# Render
button()

# Check state later
if button.track_state():
    st.write("Button is currently pressed")
```

### Example 3: Composable Container

```python
from declarative_streamlit.core import Container
from declarative_streamlit.core.build import StreamlitComponentParser
import streamlit as st

# Create container
container = Container(border=True)
container._set_base_component(st.container)
container.set_component_parser(StreamlitComponentParser)

# Add layers
container.add_layer("header")
container.add_layer("content")
container.add_layer("footer")

# Add components to layers
container.add_to_layer("header", st.title, "My App")
container.add_to_layer("content", st.write, "Main content")
container.add_to_layer("footer", st.caption, "Footer text")

# Render (row-based)
container.render()
```

### Example 4: Column-based Layout

```python
# Create columns container
cols = Container()
cols._set_base_component(st.columns)
cols.set_column_based(True)  # Important!
cols.set_component_parser(StreamlitComponentParser)

# Add layers (one per column)
cols.add_layer(0)
cols.add_layer(1)
cols.add_layer(2)

# Add components to each column
cols.add_to_layer(0, st.metric, "Metric 1", 100)
cols.add_to_layer(1, st.metric, "Metric 2", 200)
cols.add_to_layer(2, st.metric, "Metric 3", 300)

# Render with 3 columns
cols.lrender(st.columns, 3)
```

### Example 5: Error Handling

```python
def safe_error_handler(e: Exception) -> bool:
    if isinstance(e, ValueError):
        st.warning(f"Validation error: {e}")
        return True  # Handled
    elif isinstance(e, KeyError):
        st.error(f"Missing key: {e}")
        return True  # Handled
    return False  # Not handled, will re-raise

component = VElement("data")
component._set_base_component(st.text)
component.set_fatal(False)
component.set_errhandler(safe_error_handler)

# Even if render fails, error is handled gracefully
component()
```

---

## Best Practices

### 1. Always Validate Inputs

Use Pydantic models for validation:
```python
from pydantic import BaseModel, validator

class MyComponentConfig(BaseModel):
    component: Callable
    
    @validator('component')
    def must_be_callable(cls, v):
        if not callable(v):
            raise ValueError('Must be callable')
        return v
```

### 2. Use Method Chaining

Configure components in a fluent manner:
```python
component = (
    parser.parse()
    .set_fatal(False)
    .set_errhandler(error_handler)
    .add_effect(effect1)
    .add_effect(effect2)
)
```

### 3. Separate Configuration from Execution

```python
# Configuration phase
component = setup_component()

# Execution phase (can be conditional)
if should_render:
    component()
```

### 4. Handle Errors Appropriately

```python
# Critical components - fail fast
auth_component.set_fatal(True)

# Optional components - fail gracefully
badge.set_fatal(False).set_errhandler(lambda e: None)
```

### 5. Use Context Managers for Containers

```python
with container.render() as c:
    st.write("Content inside container")
```

---

## Type Annotations Reference

```python
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Union,
    Optional,
    NoReturn,
    TypeVar,
)

# Method chaining
T = TypeVar('T', bound='BaseClass')

# Error handlers
ErrorHandler = Callable[[Exception], Union[NoReturn, bool]]

# Effect functions
Effect = Callable[..., Any]

# Component parsers
ComponentParser = Callable[..., Any]

# Layer identifiers
LayerID = Union[int, str]
```

---

## Common Pitfalls

### 1. Forgetting to Set Base Component

```python
# ❌ Wrong
element = VElement("text")
element()  # ValueError: base component not set

# ✅ Correct
element = VElement("text")
element._set_base_component(st.text)
element()
```

### 2. Mixing Rendering Strategies

```python
# ❌ Wrong - column container without column_based flag
container.set_column_based(False)  # Default
container.lrender(st.columns, 3)  # Renders incorrectly

# ✅ Correct
container.set_column_based(True)
container.lrender(st.columns, 3)
```

### 3. Not Setting Component Parser

```python
# ❌ Wrong
container.add_component(st.button, "Click")  # ValueError

# ✅ Correct
container.set_component_parser(StreamlitComponentParser)
container.add_component(st.button, "Click")
```

### 4. Strict Mode Without Key

```python
# ❌ Wrong
element = IElement("Click")
element.set_strict(True)
element.render()  # ValueError: key required

# ✅ Correct
element = IElement("Click", key="my_key")
element.set_strict(True)
element.render()
```

---

## Performance Considerations

### Lazy Evaluation

Components are not rendered until explicitly called:
```python
# No rendering happens here
component = parser.parse()
component.set_fatal(False)

# Rendering happens here
component()
```

### Effect Overhead

Each effect adds overhead - use judiciously:
```python
# ❌ Avoid excessive effects
for i in range(100):
    component.add_effect(lambda x: print(f"Effect {i}"))

# ✅ Better - single combined effect
def combined_effect(result):
    for i in range(100):
        print(f"Effect {i}: {result}")

component.add_effect(combined_effect)
```

---

## Revision History

| Version | Date       | Changes                          |
|---------|------------|----------------------------------|
| 1.0.0   | 2025-12-14 | Initial documentation            |

---

## See Also

- [Components Documentation](./components.md)
- [Parsers Documentation](./parsers.md)
- [API Reference](./api-reference.md)
- [Usage Examples](./usage-examples.md)
