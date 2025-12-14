# Canvas

## Overview

`Canvas` is the abstract base class that defines the core interface for all renderable components in the declarative Streamlit framework. It provides a unified abstraction for managing components, containers, error handling, and configuration options.

## Class Signature

```python
class Canvas(metaclass=ABCMeta):
    """
    Represents a canvas in the application with component management capabilities.
    """
    
    def __init__(
        self,
        failsafe: bool = False,
        failhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
    ) -> None
```

## Description

The `Canvas` class serves as the foundation for all canvas-like components in the system. It implements:

- **Component Management**: Abstract methods for adding components and containers
- **Error Handling**: Configurable error handling through failsafe mode and custom handlers
- **Type Safety**: Strict mode for enforcing type checking
- **Schema-based Rendering**: Internal schema system using `Layer` objects
- **Property Access**: Dictionary-like access to components by key or index

### Design Philosophy

The Canvas follows the **Abstract Base Class (ABC)** pattern, requiring subclasses to implement:
- `add_component()` - Component addition logic
- `add_container()` - Container addition logic  
- `start()` - Rendering initiation logic
- `serialize()` - Serialization logic

This ensures all canvas implementations provide a consistent interface while allowing custom behavior.

## Constructor Parameters

### `failsafe: bool = False`
**Type**: `bool`  
**Default**: `False`  
**Description**: Controls whether the canvas continues execution when errors occur.

- When `True`: Errors are caught and handled gracefully without stopping execution
- When `False`: Errors propagate normally and may halt execution
- Works in conjunction with `failhandler`

**Example**:
```python
# Graceful error handling
app = Canvas(failsafe=True)  # Errors won't crash the app
```

### `failhandler: Callable[[Exception], Union[NoReturn, bool]] = None`
**Type**: `Optional[Callable[[Exception], Union[NoReturn, bool]]]`  
**Default**: `None`  
**Description**: Custom error handler function called when exceptions occur.

- Receives the exception as its argument
- Can return `bool` to indicate if execution should continue
- Can raise the exception or handle it silently
- Only invoked when `failsafe=True` or component-level error handling is enabled

**Example**:
```python
def custom_handler(error: Exception) -> bool:
    st.error(f"Error occurred: {error}")
    return True  # Continue execution

app = Canvas(failsafe=True, failhandler=custom_handler)
```

### `strict: bool = True`
**Type**: `bool`  
**Default**: `True`  
**Description**: Enforces strict type checking and validation.

- When `True`: Type checking is enforced
- When `False`: More permissive behavior
- Affects component validation and configuration

**Example**:
```python
# Strict mode enabled
app = Canvas(strict=True)
```

## Attributes

### Public Attributes

#### `failsafe: bool`
Current failsafe mode setting. Can be modified via `set_failsafe()`.

#### `failhandler: Optional[Callable]`
Current error handler function. Can be modified via `set_failhandler()`.

#### `strict: bool`
Current strict mode setting. Can be modified via `set_strict()`.

### Protected Attributes

#### `_body: Schema`
**Type**: `Schema`  
**Description**: Internal schema object managing the component hierarchy. The schema contains a main body `Layer` that holds all components and containers.

**Access**: Use `main_body` property instead of direct access.

## Properties

### `main_body: Layer`
**Type**: `Layer`  
**Read-only**  
**Description**: Returns the main body layer containing all components and containers.

**Example**:
```python
app = AppPage()
app.add_component(st.button, "Click", key="btn")

# Access component by key
button_component = app.main_body["btn"]

# Access component by index
first_component = app.main_body[0]
```

## Methods

### Abstract Methods

These methods **must** be implemented by subclasses.

#### `add_component()`
```python
@abstractmethod
def add_component(
    self,
    component: Union[Callable[..., Any], StreamlitComponentParser],
    *args: Any,
    **kwargs: Any,
) -> StreamlitComponentParser:
    """
    Add a component to the canvas.
    
    Args:
        component: The component to add (callable or parser)
        *args: Positional arguments for the component
        **kwargs: Keyword arguments for the component
        
    Returns:
        StreamlitComponentParser: The parser wrapping the component
        
    Raises:
        NotImplementedError: If not implemented in subclass
    """
```

**Purpose**: Add individual Streamlit components (widgets, elements) to the canvas.

#### `add_container()`
```python
@abstractmethod
def add_container(
    self,
    container: Union[Callable[..., Any], StreamlitLayoutParser],
    *args: Any,
    **kwargs: Any,
) -> StreamlitLayoutParser:
    """
    Add a container to the canvas.
    
    Args:
        container: The container to add (callable or parser)
        *args: Positional arguments for the container
        **kwargs: Keyword arguments for the container
        
    Returns:
        StreamlitLayoutParser: The parser wrapping the container
        
    Raises:
        NotImplementedError: If not implemented in subclass
    """
```

**Purpose**: Add layout containers (columns, expanders, etc.) to the canvas.

#### `start()`
```python
@abstractmethod
def start(self) -> T:
    """
    Initiate the rendering process for the canvas.
    
    Raises:
        NotImplementedError: If not implemented in subclass
    """
```

**Purpose**: Begin rendering all components in the canvas.

#### `serialize()`
```python
@abstractmethod
def serialize(self) -> Dict[str, Any]:
    """
    Serialize the canvas to a dictionary representation.
    
    Returns:
        Dict[str, Any]: Dictionary representation of the canvas
    """
```

**Purpose**: Convert the canvas structure to a serializable format.

### Configuration Methods

#### `set_failsafe()`
```python
def set_failsafe(self, failsafe: bool) -> T:
    """
    Set the failsafe mode for the canvas.
    
    Args:
        failsafe: Whether to enable failsafe mode
        
    Returns:
        Self for method chaining
    """
```

**Example**:
```python
app = AppPage()
app.set_failsafe(True).set_strict(False)  # Method chaining
```

#### `set_failhandler()`
```python
def set_failhandler(
    self, 
    failhandler: Callable[[Exception], Union[NoReturn, bool]]
) -> T:
    """
    Set the failhandler for the canvas.
    
    Args:
        failhandler: Callable to handle exceptions
        
    Returns:
        Self for method chaining
        
    Raises:
        ValueError: If failhandler is not callable
    """
```

**Example**:
```python
app = AppPage()
app.set_failhandler(lambda e: st.warning(str(e)))
```

#### `set_strict()`
```python
def set_strict(self, strict: bool) -> T:
    """
    Set the strict mode for the canvas.
    
    Args:
        strict: Whether to enable strict mode
        
    Returns:
        Self for method chaining
    """
```

### Special Methods

#### `__getitem__()`
```python
def __getitem__(
    self, 
    key: Union[int, str]
) -> Union[StreamlitComponentParser, StreamlitLayoutParser]:
    """
    Get a component from the canvas by key or index.
    
    Args:
        key: String key or integer index
        
    Returns:
        The component parser at the specified key/index
        
    Raises:
        KeyError: If key is not found
    """
```

**Example**:
```python
app = AppPage()
app.add_component(st.button, "Click", key="my_button")

# Access by key
btn = app["my_button"]

# Access by index
first = app[0]
```

#### `__call__()`
```python
def __call__(self):
    """Call the start method to execute the canvas."""
    return self.start()
```

**Example**:
```python
app = AppPage()
app.add_component(st.title, "Hello")
app()  # Equivalent to app.start()
```

#### `__str__()` and `__repr__()`
```python
def __str__(self) -> str:
    """String representation of the canvas."""
    
def __repr__(self) -> str:
    """Developer-friendly representation."""
```

## Configuration Validation

The Canvas uses a Pydantic model (`CanvasConfig`) to validate constructor parameters:

```python
class CanvasConfig(BaseModel):
    failsafe: bool = False
    failhandler: Optional[Callable[[Exception], Union[NoReturn, bool]]] = None
    strict: bool = True
    
    @field_validator("failhandler")
    def validate_failhandler(cls, value):
        if value is not None and not callable(value):
            raise ValueError("failhandler must be callable")
        return value
```

This ensures:
- Type safety at initialization
- Validation of callable objects
- Clear error messages for invalid configurations

## Usage Examples

### Basic Usage (Subclass Implementation)

Since `Canvas` is abstract, you'll typically use concrete implementations like `AppPage`:

```python
from declarative_streamlit.base import AppPage
import streamlit as st

# Create a canvas instance
app = AppPage()

# Add components
app.add_component(st.title, "My Application")
app.add_component(st.text, "Welcome to the app!")

# Start rendering
app.start()
```

### Error Handling

```python
import streamlit as st
from declarative_streamlit.base import AppPage

def error_handler(e: Exception) -> bool:
    st.error(f"An error occurred: {e}")
    logging.error(e, exc_info=True)
    return True  # Continue execution

app = AppPage(
    failsafe=True,
    failhandler=error_handler
)

# This component will fail gracefully
app.add_component(st.button, "Test", key="btn")
app.add_component(lambda: 1/0)  # Error handled by error_handler

app.start()
```

### Component Access

```python
app = AppPage()

# Add components with keys
app.add_component(st.text_input, "Name:", key="name_input")
app.add_component(st.slider, "Age:", 0, 100, key="age_slider")

# Access by key
name_component = app["name_input"]
age_component = app["age_slider"]

# Access by index
first_component = app[0]  # name_input
second_component = app[1]  # age_slider

# Access main body layer
layer = app.main_body
print(len(layer))  # 2
```

### Method Chaining

```python
app = AppPage()

# Chain configuration methods
app.set_failsafe(True)\
   .set_strict(False)\
   .set_failhandler(lambda e: print(e))

# Add components
app.add_component(st.title, "Configured App")
app.start()
```

## Error Handling

### Exceptions Raised

#### `NotImplementedError`
**When**: Calling abstract methods on `Canvas` directly
**Solution**: Use concrete implementations (AppPage, AppFragment, AppDialog)

```python
# Wrong - Canvas is abstract
canvas = Canvas()  # TypeError: Can't instantiate abstract class

# Correct - Use concrete implementation
app = AppPage()
```

#### `ValueError`
**When**: Setting invalid failhandler
**Solution**: Ensure failhandler is callable

```python
# Wrong
app.set_failhandler("not callable")  # ValueError

# Correct
app.set_failhandler(lambda e: print(e))  # OK
```

#### `KeyError`
**When**: Accessing non-existent component by key
**Solution**: Check if key exists or use try-except

```python
app = AppPage()
app.add_component(st.button, "Click", key="btn")

# Wrong
component = app["nonexistent"]  # KeyError

# Correct
try:
    component = app["nonexistent"]
except KeyError:
    print("Component not found")
```

#### `TypeError`
**When**: Invalid component types passed to add_component/add_container
**Solution**: Ensure components are callables or appropriate parser objects

## Best Practices

### 1. Use Concrete Implementations
Never instantiate `Canvas` directly. Always use concrete implementations:
- `AppPage` for main applications
- `AppFragment` for isolated rerun sections
- `AppDialog` for modal dialogs

### 2. Enable Failsafe for Production
```python
# Development
app = AppPage(failsafe=False)  # Fail fast for debugging

# Production
app = AppPage(
    failsafe=True,
    failhandler=log_and_notify_error
)
```

### 3. Use Keys for Important Components
```python
# Good - easy to reference
app.add_component(st.button, "Submit", key="submit_btn")
result = app["submit_btn"]

# Avoid - brittle index-based access
result = app[5]  # What is at index 5?
```

### 4. Leverage Method Chaining
```python
app = AppPage()\
    .set_failsafe(True)\
    .set_strict(False)
```

### 5. Validate Configuration Early
```python
# Validate at creation time
try:
    app = AppPage(
        failsafe=True,
        failhandler=invalid_handler  # Not callable
    )
except ValueError as e:
    print(f"Invalid configuration: {e}")
```

## Implementation Notes

### Internal Schema Structure

The Canvas maintains components in a `Schema` object which contains `Layer` instances:

```
Canvas
└── _body (Schema)
    └── main_body (Layer)
        ├── Component 1 (StreamlitComponentParser)
        ├── Component 2 (StreamlitLayoutParser)
        └── Component N
```

### Type Safety with TypeVar

The class uses `TypeVar` for type-safe method chaining:

```python
T = TypeVar("T", bound="Canvas")

def set_failsafe(self, failsafe: bool) -> T:
    # Returns the same type as the instance
    return cast(T, self)
```

This allows:
```python
app: AppPage = AppPage()
same_app: AppPage = app.set_failsafe(True)  # Type preserved
```

## Related Components

- **[AppPage](./app-page.md)** - Main application implementation
- **[AppFragment](./app-fragment.md)** - Fragment implementation  
- **[AppDialog](./app-dialog.md)** - Dialog implementation
- **[Fragment](./fragment.md)** - Fragment canvas base class
- **[Dialog](./dialog.md)** - Dialog canvas base class

## See Also

- [Core Layer Documentation](../../core/docs/README.md) - Parser and handler details
- [Schema and Layer](../../core/docs/handlers.md) - Schema system architecture
- [StreamlitComponentParser](../../core/docs/parsers.md) - Component parser documentation

---

**Navigation**: [README](./README.md) | [AppPage](./app-page.md) | [AppFragment](./app-fragment.md) | [AppDialog](./app-dialog.md)
