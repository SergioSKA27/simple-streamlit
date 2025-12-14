# Base Representation System

## Overview

The `BaseRepresentation` class is the foundational abstract base class that defines the interface and core functionality for all component representations in the declarative Streamlit library. It provides a contract for component configuration, serialization, and factory pattern implementation.

**Location**: `declarative_streamlit/config/base/representation.py`

## Class Definition

```python
class BaseRepresentation(Generic[V], metaclass=ABCMeta):
    """
    Base class for all representations.

    A representation is a class that can be used to represent the default
    representation of a given type, including the default arguments to create
    a generic representation of that type. and also can be used to enforce an
    specific behavior through the use of the different parsers.
    """
```

### Type Parameters

- **`V`**: Generic type variable representing the underlying component type (e.g., `st.button`, `st.selectbox`)

## Design Patterns

### 1. Singleton Pattern

`BaseRepresentation` implements the singleton pattern to ensure only one instance of each representation class exists:

```python
def __new__(cls, *args: Any, **kwargs: Any) -> T:
    if not hasattr(cls, "_instance"):
        cls._instance = super(BaseRepresentation, cls).__new__(cls)
    return cls._instance
```

**Rationale**: 
- Ensures consistent configuration across the application
- Prevents duplicate representation instances
- Reduces memory overhead
- Guarantees predictable behavior

### 2. Abstract Factory Pattern

The `generic_factory()` abstract method implements the factory pattern for creating parser instances:

```python
@abstractmethod
def generic_factory(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
    """
    Abstract method to create a generic representation of the type.
    
    Returns:
        Callable[..., Any]: A callable that represents the generic factory.
    """
```

**Purpose**: Decouple representation configuration from parser instantiation.

## Constructor Parameters

```python
def __init__(
    self,
    default_args: List[Any],
    default_kwargs: Dict[str, Any],
    stateful: bool = False,
    fatal: bool = False,
    strict: bool = True,
    column_based: bool = False,
    bind: Optional[Literal["type", "name"]] = "name",
    **kwargs: Dict[str, Any]
)
```

### Parameters

#### `default_args: List[Any]`
List of default positional arguments passed to the component when instantiated.

**Example**: 
```python
default_args = ["Default Label"]
```

#### `default_kwargs: Dict[str, Any]`
Dictionary of default keyword arguments with their default values.

**Example**:
```python
default_kwargs = {
    "label": "Button",
    "key": str(uuid4()),
    "help": "This is a generic button"
}
```

#### `stateful: bool = False`
Indicates whether the component maintains state across Streamlit reruns.

**Usage**:
- `True`: Widgets that capture user input (buttons, text inputs, sliders)
- `False`: Display elements that don't maintain state (markdown, images, charts)

**Impact**:
- Affects session state management
- Determines callback behavior
- Influences re-rendering logic

#### `fatal: bool = False`
Determines whether parsing or rendering errors should terminate execution.

**Usage**:
- `True`: Critical components where failure is unacceptable
- `False`: Optional components where graceful degradation is acceptable

**Impact**:
- Error handling strategy
- Application robustness
- Debugging behavior

#### `strict: bool = True`
Enforces strict type checking and validation of component arguments.

**Usage**:
- `True`: Enforce type safety and argument validation
- `False`: Allow flexible argument passing

**Impact**:
- Type safety level
- Validation strictness
- Development vs. production behavior

#### `column_based: bool = False`
Indicates whether the component supports column-based layout arrangement.

**Usage**:
- `True`: Containers that arrange children horizontally (`st.columns`, `st.tabs`)
- `False`: Containers that arrange children vertically or non-containers

**Impact**:
- Layout algorithm selection
- Child component rendering order
- Nesting behavior

#### `bind: Optional[Literal["type", "name"]] = "name"`
Determines the binding strategy for component lookup in standards.

**Options**:
- `"type"`: Match by Python type object (e.g., `st.button`)
- `"name"`: Match by string name (e.g., `"button"`)
- `None`: No automatic binding

**Default**: `"name"` (more flexible for string-based lookups)

#### `**kwargs: Dict[str, Any]`
Additional custom configuration parameters stored in `self.kwargs`.

## Instance Attributes

### Private Attributes

#### `_type: Optional[TypeVar]`
Stores the actual component type after being set via `set_type()`.

**Initialization**: `None` (set during subclass initialization)

**Usage**: 
```python
self.set_type(st.button)  # Sets _type to the button function
```

### Public Attributes

All constructor parameters are stored as instance attributes:
- `self.default_args`
- `self.default_kwargs`
- `self.stateful`
- `self.fatal`
- `self.strict`
- `self.column_based`
- `self.bind`
- `self.kwargs`

## Abstract Methods

Subclasses **must** implement these methods:

### `generic_factory(*args, **kwargs) -> Callable[..., Any]`
Creates and returns a factory function or parser for the component.

**Purpose**: Generate component instances with configured defaults.

**Return**: A callable that produces component instances.

**Example Implementation**:
```python
def generic_factory(self) -> Callable[..., Any]:
    p = StreamlitComponentParser(
        self._type,
        *self.default_args,
        **self.default_kwargs,
    ).set_stateful(self.stateful).set_fatal(self.fatal)
    return p
```

### `serialize(*args, **kwargs) -> Dict[str, Any]`
Serializes the representation into a dictionary format.

**Purpose**: Enable configuration export, inspection, and storage.

**Return**: Dictionary containing representation configuration.

**Example Implementation**:
```python
def serialize(self) -> Dict[str, Union[str, List[Any], Dict[str, Any]]]:
    return {
        "type": self._type.__name__,
        "args": self.default_args,
        "kwargs": self.default_kwargs,
        "stateful": self.stateful,
        "fatal": self.fatal,
        "strict": self.strict,
        "column_based": self.column_based,
    }
```

### `deserialize(*args, **kwargs) -> Callable[..., Any]`
Deserializes configuration and returns the component type.

**Purpose**: Reconstruct component references from serialized data.

**Return**: The original component callable.

**Example Implementation**:
```python
def deserialize(self) -> Callable[..., Any]:
    return self._type
```

### `ast_definition(*args, **kwargs) -> Dict[str, Any]`
Generates an Abstract Syntax Tree (AST) definition of the representation.

**Purpose**: Support code generation and metaprogramming.

**Return**: Dictionary containing AST metadata.

**Example Implementation**:
```python
def ast_definition(self, *args, **kwargs):
    _type = self.get_type()
    return {
        "name": _type.__name__,
        "ctype": _type,
        "attributes": self.get_default_args_definition(),
        "reserved_names": self.get_default_parser_definition(),
    }
```

## Public Methods

### Configuration Methods

#### `set_type(typ: TypeVar) -> None`
Sets the component type and automatically fills missing keyword arguments.

**Parameters**:
- `typ`: The component type (e.g., `st.button`)

**Behavior**:
1. Sets `self._type = typ`
2. Extracts initialization parameters from type signature
3. Fills `default_kwargs` with `None` for missing parameters

**Example**:
```python
class ButtonRepresentation(CommonRepresentation[button]):
    def __init__(self) -> None:
        super().__init__(default_kwargs={"label": "Button"})
        self.set_type(button)  # Auto-fills missing kwargs
```

### Query Methods

#### `is_stateful() -> bool`
Returns whether the representation is stateful.

#### `is_fatal() -> bool`
Returns whether the representation uses fatal error handling.

#### `is_strict() -> bool`
Returns whether the representation enforces strict validation.

#### `is_column_based() -> bool`
Returns whether the representation supports column-based layout.

#### `get_type() -> V`
Returns the underlying component type.

#### `get_str_representation() -> str`
Returns the string representation of the component type.

**Return**: Component name as string (e.g., `"button"`)

#### `get_default_args() -> List[Any]`
Returns the list of default positional arguments.

#### `get_default_kwargs() -> Dict[str, Any]`
Returns the dictionary of default keyword arguments.

#### `get_parser_defaults() -> Dict[str, Any]`
Returns behavioral configuration as a dictionary.

**Return**:
```python
{
    "stateful": self.stateful,
    "fatal": self.fatal,
    "strict": self.strict,
    "column_based": self.column_based,
}
```

#### `get_tdeserializer() -> Tuple[TypeVar, Callable[..., Any]]`
Returns a tuple of the type and its deserializer.

**Return**: `(self._type, self.deserialize)`

### Utility Methods

#### `_get_type_init_args() -> List[str]`
Extracts initialization parameter names from the component type's signature.

**Return**: List of parameter names.

**Implementation**:
```python
from inspect import signature

def _get_type_init_args(self) -> List[str]:
    _type = self.get_type()
    if _type is None:
        return []
    return list(signature(_type).parameters.keys())
```

#### `_fill_missing_kwargs(missing: List[str]) -> Dict[str, Any]`
Creates a dictionary with `None` values for missing keyword arguments.

**Parameters**:
- `missing`: List of parameter names not in `default_kwargs`

**Return**: Dictionary mapping missing parameters to `None`

## Magic Methods

### `__eq__(value) -> bool`
Compares representation to another value by type name.

**Comparison Logic**:
```python
return value == self._type.__name__ or value.__name__ == self._type.__name__
```

**Usage**:
```python
rep = ButtonRepresentation()
rep == "button"  # True
rep == st.button  # True
```

### `__repr__() -> str`
Returns a string representation based on binding mode.

**Return**:
- If `bind == "name"`: Component name (e.g., `"button"`)
- Otherwise: Type representation (e.g., `"<class 'ButtonRepresentation'>"`)

### `__str__() -> str`
Returns a string representation (same logic as `__repr__`).

## Complete Lifecycle Example

```python
from declarative_streamlit.config.base import BaseRepresentation
from streamlit import button
from uuid import uuid4

class ButtonRepresentation(CommonRepresentation[button]):
    def __init__(self) -> None:
        # Step 1: Initialize with default configuration
        super().__init__(
            default_args=[],
            default_kwargs={
                "label": "Button",
                "key": str(uuid4()),
                "help": "This a generic button",                
            },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )
        
        # Step 2: Set the component type (auto-fills missing kwargs)
        self.set_type(button)
    
    def generic_factory(self) -> Callable[..., Any]:
        # Step 3: Create parser with configuration
        return StreamlitComponentParser(
            self._type,
            *self.default_args,
            **self.default_kwargs,
        ).set_stateful(self.stateful).set_fatal(self.fatal)
    
    def serialize(self) -> Dict[str, Any]:
        # Step 4: Export configuration
        return {
            "type": self._type.__name__,
            "args": self.default_args,
            "kwargs": self.default_kwargs,
            "stateful": self.stateful,
            "fatal": self.fatal,
            "strict": self.strict,
            "column_based": self.column_based,
        }
    
    def deserialize(self) -> Callable[..., Any]:
        # Step 5: Return original type
        return self._type
    
    def ast_definition(self) -> Dict[str, Any]:
        # Step 6: Generate AST metadata
        return {
            "name": self._type.__name__,
            "ctype": self._type,
            "attributes": self.get_default_args_definition(),
            "reserved_names": self.get_default_parser_definition(),
        }
```

## Best Practices

### 1. Always Call `set_type()`
Ensure `set_type()` is called during initialization to populate missing kwargs:

```python
def __init__(self) -> None:
    super().__init__(default_kwargs={...})
    self.set_type(st.button)  # Critical!
```

### 2. Provide Comprehensive Defaults
Include sensible defaults for all common parameters:

```python
default_kwargs = {
    "label": "Descriptive Label",
    "key": str(uuid4()),  # Unique key for stateful widgets
    "help": "Helpful description",
}
```

### 3. Set Behavioral Flags Appropriately
Choose flags based on component characteristics:

- **Widgets**: `stateful=True, fatal=True, strict=True`
- **Display Elements**: `stateful=False, fatal=True, strict=True`
- **Containers**: `fatal=True, strict=True, column_based=<True/False>`

### 4. Document Custom Attributes
If using `**kwargs`, document custom attributes clearly:

```python
def __init__(self, custom_flag: bool = False) -> None:
    super().__init__(..., custom_flag=custom_flag)
    # Document: custom_flag controls XYZ behavior
```

### 5. Maintain Immutability
Treat representations as immutable after initialization:

```python
# Good: Create new instance for different config
config_a = ButtonRepresentation()
config_b = CustomButtonRepresentation()

# Avoid: Modifying existing instance
# config_a.stateful = False  # Don't do this
```

## Advanced Topics

### Custom Binding Strategies

Override `__eq__` for custom matching logic:

```python
def __eq__(self, value):
    # Custom matching: case-insensitive name comparison
    if isinstance(value, str):
        return value.lower() == self._type.__name__.lower()
    return super().__eq__(value)
```

### Dynamic Default Generation

Use callables for dynamic default values:

```python
def __init__(self) -> None:
    super().__init__(
        default_kwargs={
            "timestamp": lambda: datetime.now(),  # Dynamic default
        }
    )
```

### Type-Safe Generic Usage

Leverage generic type parameters for type safety:

```python
from typing import TypeVar
from streamlit import button

ButtonType = TypeVar("ButtonType", bound=button)

class TypedButtonRep(BaseRepresentation[ButtonType]):
    def get_type(self) -> ButtonType:
        return super().get_type()
```

## Related Documentation

- [Standards System](./standards.md) - How representations are organized into standards
- [Common Representations](./common-representations.md) - Streamlit-specific implementation
- [Widgets Reference](./widgets-reference.md) - Concrete widget representations

## Conclusion

The `BaseRepresentation` class provides a robust, extensible foundation for component configuration in the declarative Streamlit library. By implementing the abstract methods and following best practices, developers can create type-safe, well-configured component representations that integrate seamlessly with the broader library architecture.
