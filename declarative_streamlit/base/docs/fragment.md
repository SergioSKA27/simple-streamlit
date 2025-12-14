# Fragment (Component)

## Overview

`Fragment` is an abstract base class that extends `Canvas` to provide the foundational interface for fragment-based rendering in Streamlit. It defines the core contract for fragments that can rerun independently from the main application.

## Class Signature

```python
class Fragment(Canvas, metaclass=ABCMeta):
    """
    Fragment class that extends the Canvas class.
    
    This class is used to create a fragment of a canvas, allowing for more granular 
    control over the layout and components with isolated rerun capability.
    """
    
    def __init__(
        self,
        failsafe: bool = False,
        failhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
        run_every: Union[int, float, timedelta, str, None] = None,
    ) -> None
```

## Description

`Fragment` serves as the abstract base for all fragment implementations. It extends `Canvas` with fragment-specific functionality:

- **Isolated Reruns**: Fragments can rerun independently of parent context
- **Auto-refresh**: Optional automatic rerun intervals via `run_every`
- **Decorator Wrapping**: Internally wraps content with `@st.fragment` decorator
- **Component Inheritance**: Inherits all `Canvas` component management capabilities

### Position in Architecture

```
Canvas (Abstract Base)
    └── Fragment (Abstract Fragment Base)
        └── AppFragment (Concrete Implementation)
```

The `Fragment` class is an intermediate abstraction that:
1. Extends `Canvas` with fragment-specific behavior
2. Defines fragment rendering contract
3. Is subclassed by `AppFragment` for actual usage

## Constructor Parameters

### `failsafe: bool = False`
**Type**: `bool`  
**Default**: `False`  
**Inherited from**: `Canvas`  
**Description**: Enable failsafe error handling mode.

### `failhandler: Callable[[Exception], Union[NoReturn, bool]] = None`
**Type**: `Optional[Callable]`  
**Default**: `None`  
**Inherited from**: `Canvas`  
**Description**: Custom error handler for fragment errors.

### `strict: bool = True`
**Type**: `bool`  
**Default**: `True`  
**Inherited from**: `Canvas`  
**Description**: Enable strict type checking and validation.

### `run_every: Union[int, float, timedelta, str, None] = None`
**Type**: `Union[int, float, timedelta, str, None]`  
**Default**: `None`  
**Description**: Automatic rerun interval for the fragment.

**Values**:
- `int` or `float`: Seconds between reruns
- `timedelta`: Time interval object
- `str`: Time string format ("1s", "5m", "1h")
- `None`: No automatic rerun

**Example**:
```python
from datetime import timedelta

# Rerun every 5 seconds
fragment = Fragment(run_every=5)

# Rerun every minute
fragment = Fragment(run_every=timedelta(minutes=1))

# No auto-rerun
fragment = Fragment(run_every=None)
```

## Attributes

### Public Attributes

Inherited from `Canvas`:
- `failsafe: bool` - Failsafe mode setting
- `failhandler: Optional[Callable]` - Error handler function
- `strict: bool` - Strict mode setting

### Fragment-Specific Attributes

#### `run_every: Union[int, float, timedelta, str, None]`
**Type**: `Union[int, float, timedelta, str, None]`  
**Description**: Auto-rerun interval configuration.

### Protected Attributes

#### `_body: Schema`
**Type**: `Schema`  
**Inherited from**: `Canvas`  
**Description**: Internal schema managing component hierarchy.

## Methods

### Abstract Methods

Fragment inherits all abstract methods from `Canvas`:

- `add_component()` - Must be implemented by subclass
- `add_container()` - Must be implemented by subclass
- `serialize()` - Must be implemented by subclass

### Fragment-Specific Methods

#### `start()`
```python
def start(self) -> None:
    """
    Start the fragment rendering process.
    
    This method initiates the rendering of the fragment, wrapping the content
    in Streamlit's @fragment decorator with the configured run_every interval.
    """
```

**Description**: Initiates fragment rendering with isolated rerun behavior.

**Behavior**:
1. Wraps `_body` in `@st.fragment(run_every=self.run_every)` decorator
2. Executes all components in the fragment
3. Fragment reruns independently when interactions occur
4. Auto-reruns if `run_every` is configured

**Implementation Details**:
```python
def start(self):
    """Start the fragment rendering process."""
    self.__render_on_fragment()

def __render_on_fragment(self):
    """Internal method to wrap body in @st.fragment decorator."""
    @fragment(run_every=self.run_every)
    def render():
        self._body()
    
    return render()
```

**Example**:
```python
# Concrete implementation (AppFragment)
frag = AppFragment(run_every=5)
frag.add_component(st.metric, "Value", "100")
frag.start()  # Renders and auto-refreshes every 5 seconds
```

### Inherited Methods

From `Canvas`:
- `set_failsafe()` - Configure failsafe mode
- `set_failhandler()` - Set error handler
- `set_strict()` - Configure strict mode
- `__getitem__()` - Access components by key/index
- `main_body` property - Access component layer

## Implementation Notes

### Internal Rendering Mechanism

The `Fragment` class uses a private method to wrap rendering:

```python
def __render_on_fragment(self):
    """
    Render the fragment on the canvas.
    
    This method is responsible for rendering the fragment on the canvas.
    It should be called when the fragment is ready to be displayed.
    """
    @fragment(run_every=self.run_every)
    def render():
        self._body()
    
    return render()
```

**Key Points**:
1. Uses `@st.fragment` decorator from Streamlit
2. Wraps the `_body()` schema execution
3. Passes `run_every` parameter to decorator
4. Returns immediately (non-blocking)

### Rerun Isolation

Fragments created from this class:
- Rerun independently when components inside them interact
- Don't trigger parent page reruns
- Can access and modify session state
- Maintain isolation from parent rendering context

### Auto-Refresh Behavior

When `run_every` is set:
- Fragment automatically reruns at specified interval
- Useful for live data, metrics, monitoring
- Interval starts after fragment initialization
- Can be combined with manual triggers

## Usage Patterns

### Basic Fragment Pattern

Since `Fragment` is abstract, it's typically used through `AppFragment`:

```python
from declarative_streamlit.base import AppFragment
import streamlit as st

# Create fragment instance
fragment = AppFragment(name="metrics", run_every=10)

# Add components
fragment.add_component(st.metric, "Users", "1000")
fragment.add_component(st.metric, "Revenue", "$50K")

# Fragment reruns every 10 seconds and on internal interactions
```

### Isolated Rerun Pattern

```python
# Fragment with button - only fragment reruns on click
fragment = AppFragment(name="counter")
fragment.add_component(st.button, "Click Me", key="frag_btn")
fragment.add_component(st.write, "Fragment content")

# Main page content doesn't rerun when fragment button is clicked
```

### Auto-Refresh Pattern

```python
from datetime import datetime

# Live clock fragment
clock_fragment = AppFragment(name="clock", run_every=1)
clock_fragment.add_component(
    st.metric,
    "Current Time",
    datetime.now().strftime("%H:%M:%S")
)
```

## Design Considerations

### Why Fragment is Abstract

`Fragment` is kept abstract to:
1. **Separation of Concerns**: Core fragment logic separated from application-specific features
2. **Extensibility**: Allows different fragment implementations (e.g., AppFragment)
3. **Interface Definition**: Defines contract without prescribing implementation
4. **Consistency**: Maintains architecture pattern with Canvas

### Relationship to AppFragment

```python
# Fragment - Abstract base defining interface
class Fragment(Canvas, metaclass=ABCMeta):
    # Core fragment functionality
    pass

# AppFragment - Concrete implementation
class AppFragment(Fragment):
    # Implements abstract methods
    # Adds application-specific features (name, standard support)
    pass
```

Users interact with `AppFragment`, which provides:
- Concrete implementations of abstract methods
- Additional features (naming, standards)
- Full component management
- Ready-to-use fragment functionality

## Best Practices

### 1. Use AppFragment for Actual Fragments

```python
# Don't instantiate Fragment directly
# fragment = Fragment()  # Abstract, won't work

# Use AppFragment
fragment = AppFragment(name="my_fragment")
```

### 2. Choose Appropriate Refresh Intervals

```python
# Too frequent
fragment = AppFragment(run_every=0.1)  # 100ms - may cause issues

# Reasonable intervals
live_data = AppFragment(run_every=5)  # 5 seconds
periodic = AppFragment(run_every=60)  # 1 minute
```

### 3. Understand Rerun Isolation

```python
# Fragment interactions don't trigger page rerun
fragment = AppFragment(name="isolated")
fragment.add_component(st.button, "Fragment Button", key="frag_btn")
# ^ Clicking this only reruns the fragment

# Page-level button
app.add_component(st.button, "Page Button", key="page_btn")
# ^ Clicking this reruns entire page
```

## Error Handling

### Abstract Method Errors

```python
# Wrong - Fragment is abstract
try:
    fragment = Fragment()  # Can't instantiate
except TypeError as e:
    print("Fragment is abstract")

# Correct - Use concrete implementation
fragment = AppFragment()  # OK
```

### Refresh Interval Validation

```python
# Invalid intervals may cause Streamlit errors
# Ensure run_every values are reasonable

# Valid
fragment = AppFragment(run_every=5)  # 5 seconds
fragment = AppFragment(run_every="10s")  # 10 seconds string

# Invalid (handled by Streamlit)
# fragment = AppFragment(run_every="invalid")  # Error
```

## Performance Considerations

### When to Use Fragments

**Use fragments when**:
- Section needs isolated reruns
- Implementing live/auto-updating content
- Optimizing page performance
- Creating reusable UI components

**Don't use when**:
- Content is static
- Full page rerun is acceptable
- Adding unnecessary complexity

### Refresh Interval Impact

```python
# High frequency - higher CPU/network usage
high_freq = AppFragment(run_every=1)  # Every second

# Moderate frequency - balanced
moderate = AppFragment(run_every=30)  # Every 30 seconds

# Low frequency - minimal impact
low_freq = AppFragment(run_every=300)  # Every 5 minutes
```

## Related Components

- **[Canvas](./canvas.md)** - Base class that Fragment extends
- **[AppFragment](./app-fragment.md)** - Concrete implementation for use in applications
- **[Dialog](./dialog.md)** - Sister class for dialog functionality
- **[AppPage](./app-page.md)** - Can contain fragments

## See Also

- [Streamlit Fragments](https://docs.streamlit.io/library/api-reference/execution-flow/st.fragment)
- [Canvas Documentation](./canvas.md) - Base class details
- [AppFragment Documentation](./app-fragment.md) - Concrete usage

---

**Navigation**: [README](./README.md) | [Canvas](./canvas.md) | [AppFragment](./app-fragment.md) | [Dialog](./dialog.md)
