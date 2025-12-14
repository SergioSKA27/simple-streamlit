# Common Representations

## Overview

The `CommonRepresentation` class is a concrete implementation of `BaseRepresentation` designed specifically for Streamlit components. It provides a standardized interface for creating component representations with integrated parser generation and serialization capabilities.

**Location**: `declarative_streamlit/config/common/representation.py`

## Class Definition

```python
class CommonRepresentation(BaseRepresentation[T], metaclass=ABCMeta):
    """
    A class that represents a common representation in the system.
    It is a subclass of BaseRepresentation and provides additional functionality.
    """
```

### Type Parameters

- **`T`**: Generic type variable representing the Streamlit component type (e.g., `button`, `selectbox`, `text_input`)

## Purpose and Design

`CommonRepresentation` serves as the **bridge** between abstract representation concepts and concrete Streamlit component implementations. It:

1. **Simplifies Parser Integration**: Automatically creates `StreamlitComponentParser` instances
2. **Provides Default Implementations**: Implements all abstract methods from `BaseRepresentation`
3. **Standardizes Serialization**: Defines consistent serialization format for all Streamlit components
4. **Enables AST Generation**: Supports metaprogramming and code generation use cases

## Constructor

```python
def __init__(
    self,
    default_args: List[Any] = None,
    default_kwargs: Dict[str, Any] = None,
    stateful: bool = False,
    fatal: bool = False,
    strict: bool = True,
    column_based: bool = False,
    **kwargs: Dict[str, Any],
) -> None
```

### Parameters

All parameters are identical to `BaseRepresentation.__init__()`, with the following enhancements:

#### Default Value Handling

- `default_args`: Defaults to `[]` if `None` provided
- `default_kwargs`: Defaults to `{}` if `None` provided

This simplification allows subclasses to omit these parameters when not needed:

```python
class SimpleRepresentation(CommonRepresentation[some_type]):
    def __init__(self) -> None:
        # No need to pass empty lists/dicts
        super().__init__(stateful=True, fatal=True)
        self.set_type(some_type)
```

### Initialization Behavior

```python
def __init__(self, default_args=None, default_kwargs=None, ..., **kwargs) -> None:
    super().__init__(
        default_args or [],      # Convert None to []
        default_kwargs or {},    # Convert None to {}
        stateful,
        fatal,
        strict,
        column_based,
        **kwargs,
    )
```

**Rationale**: Reduces boilerplate in subclass constructors.

## Implemented Abstract Methods

### `generic_factory() -> Callable[..., Any]`

Creates a `StreamlitComponentParser` instance configured with the representation's settings.

**Implementation**:
```python
def generic_factory(self) -> Callable[..., Any]:
    p = (
        StreamlitComponentParser(
            self._type,
            *self.default_args,
            **self.default_kwargs,
        )
        .set_stateful(self.stateful)
        .set_fatal(self.fatal)
        .set_strict(self.strict)
    )
    return p
```

**Returns**: Configured `StreamlitComponentParser` instance

**Usage**:
```python
rep = ButtonRepresentation()
parser = rep.generic_factory()
# parser is now a StreamlitComponentParser configured for buttons
```

**Parser Configuration**:
- **Type**: Set to `self._type` (the Streamlit component function)
- **Default Args**: Unpacked from `self.default_args`
- **Default Kwargs**: Unpacked from `self.default_kwargs`
- **Stateful**: Set to `self.stateful`
- **Fatal**: Set to `self.fatal`
- **Strict**: Set to `self.strict`

**Note**: `column_based` is **not** passed to the parser (it's used elsewhere in layout logic).

### `deserialize() -> Callable[..., Any]`

Returns the underlying component type for deserialization.

**Implementation**:
```python
def deserialize(self) -> Callable[..., Any]:
    return self._type
```

**Returns**: The Streamlit component callable (e.g., `st.button`)

**Usage**:
```python
rep = ButtonRepresentation()
component = rep.deserialize()
# component is now the st.button function
```

**Purpose**: Enable reconstruction of component references from serialized data.

### `serialize() -> Dict[str, Union[str, List[Any], Dict[str, Any]]]`

Serializes the representation to a dictionary format.

**Implementation**:
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

**Returns**: Dictionary with the following structure:

```python
{
    "type": str,                    # Component name (e.g., "button")
    "args": List[Any],              # Default positional arguments
    "kwargs": Dict[str, Any],       # Default keyword arguments
    "stateful": bool,               # Statefulness flag
    "fatal": bool,                  # Error handling flag
    "strict": bool,                 # Validation strictness flag
    "column_based": bool,           # Layout support flag
}
```

**Example Output**:
```python
rep = ButtonRepresentation()
config = rep.serialize()
# {
#     "type": "button",
#     "args": [],
#     "kwargs": {
#         "label": "Button",
#         "key": "abc-123-def",
#         "help": "This a generic button"
#     },
#     "stateful": True,
#     "fatal": True,
#     "strict": True,
#     "column_based": False
# }
```

**Use Cases**:
- Configuration export (JSON, YAML)
- Debugging and introspection
- Documentation generation
- Configuration validation

### `ast_definition(*args, **kwargs) -> Dict[str, Any]`

Generates an Abstract Syntax Tree (AST) definition for the component.

**Implementation**:
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

**Returns**: Dictionary with AST metadata:

```python
{
    "name": str,                           # Component name
    "ctype": Callable,                     # Component type object
    "attributes": Dict[str, type],         # Argument type definitions
    "reserved_names": Dict[str, type],     # Parser configuration types
}
```

**Helper Methods**:

#### `get_default_args_definition() -> Dict[str, Any]`

Generates type definitions for all component arguments.

**Implementation**:
```python
def get_default_args_definition(self) -> Dict[str, Any]:
    _args_def = {"args": list}
    
    for kw in self.default_kwargs.keys():
        _args_def[kw] = type(self.default_kwargs[kw])
    
    return _args_def
```

**Returns**: Dictionary mapping argument names to their types:

```python
{
    "args": list,
    "label": str,
    "key": str,
    "help": str,
}
```

#### `get_default_parser_definition() -> Dict[str, Any]`

Generates type definitions for parser configuration.

**Implementation**:
```python
def get_default_parser_definition(self) -> Dict[str, Any]:
    return dict(map(
        lambda k: (k[0], type(k[1])),
        self.get_parser_defaults().items()
    ))
```

**Returns**: Dictionary mapping parser flags to their types:

```python
{
    "stateful": bool,
    "fatal": bool,
    "strict": bool,
    "column_based": bool,
}
```

**Use Cases**:
- Code generation and metaprogramming
- Type inference systems
- Schema validation
- Documentation generation

## Additional Methods

### `__str__() -> str`

Returns a human-readable string representation.

**Implementation**:
```python
def __str__(self) -> str:
    return f"{self._type.__name__}: {self.default_args}, {self.default_kwargs}, {self.get_parser_defaults()}"
```

**Example Output**:
```
button: [], {'label': 'Button', 'key': '...', 'help': '...'}, {'stateful': True, 'fatal': True, 'strict': True, 'column_based': False}
```

**Use Cases**:
- Debugging
- Logging
- Quick configuration inspection

### `__repr__() -> str`

Returns a developer-friendly representation.

**Implementation**:
```python
def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self._type.__name__})"
```

**Example Output**:
```
ButtonRepresentation(button)
```

**Use Cases**:
- Interactive Python sessions
- Debugging
- Logging

## Inheritance Hierarchy

```
BaseRepresentation[V]
    └── CommonRepresentation[T]
            ├── Widgets
            │   ├── ButtonRepresentation
            │   ├── TextInputRepresentation
            │   ├── SelectboxRepresentation
            │   └── ... (23 more widgets)
            │
            ├── Elements
            │   ├── MarkdownRepresentation
            │   ├── DataFrameRepresentation
            │   ├── ImageRepresentation
            │   └── ... (16 more elements)
            │
            └── Containers
                ├── ContainerRepresentation
                ├── ColumnsRepresentation
                ├── TabsRepresentation
                └── ... (5 more containers)
```

## Complete Example Implementation

### Simple Widget Representation

```python
from declarative_streamlit.config.common.representation import CommonRepresentation
from streamlit import checkbox
from uuid import uuid4

class CheckboxRepresentation(CommonRepresentation[checkbox]):
    """Representation for Streamlit checkbox widget."""
    
    def __init__(self) -> None:
        super().__init__(
            # No default_args needed
            default_kwargs={
                "label": "Checkbox",
                "key": str(uuid4()),
                "help": "This a generic checkbox",
            },
            stateful=True,      # Maintains state
            fatal=True,         # Errors are critical
            strict=True,        # Enforce validation
            column_based=False, # Not a layout container
        )
        
        # Critical: Set the component type
        self.set_type(checkbox)

# Usage
rep = CheckboxRepresentation()

# Get parser
parser = rep.generic_factory()

# Serialize configuration
config = rep.serialize()
print(config)

# Get AST definition
ast = rep.ast_definition()
print(ast)
```

### Complex Container Representation

```python
from declarative_streamlit.config.common.representation import CommonRepresentation
from streamlit import columns

class ColumnsRepresentation(CommonRepresentation[columns]):
    """Representation for Streamlit columns container."""
    
    def __init__(self) -> None:
        super().__init__(
            # Columns don't have default kwargs typically
            stateful=False,      # No state maintenance
            fatal=True,          # Layout errors are critical
            strict=True,         # Enforce validation
            column_based=True,   # THIS IS A COLUMN CONTAINER
        )
        
        self.set_type(columns)

# Usage
rep = ColumnsRepresentation()

# Check layout support
assert rep.is_column_based() == True

# Serialize
config = rep.serialize()
assert config["column_based"] == True
```

## Integration with StreamlitComponentParser

The `generic_factory()` method creates `StreamlitComponentParser` instances that integrate with the broader library ecosystem:

```python
from declarative_streamlit.core.build.cstparser import StreamlitComponentParser

# CommonRepresentation creates parser instances like this:
parser = StreamlitComponentParser(
    component_type,        # From self._type
    *default_args,         # From self.default_args
    **default_kwargs,      # From self.default_kwargs
).set_stateful(stateful).set_fatal(fatal).set_strict(strict)

# The parser can then be used to:
# - Validate component arguments
# - Generate component instances
# - Handle errors and state management
```

## Component Import Pattern

All concrete implementations follow a consistent import pattern with graceful degradation:

```python
import streamlit as st
from typing import Any

# Try to import component, fallback to warning function
try:
    from streamlit import button
except ImportError:
    def button(*args: Any, **kwargs: Any) -> Any:
        st.warning("Button component not available in this Streamlit version")
        return None

class ButtonRepresentation(CommonRepresentation[button]):
    def __init__(self) -> None:
        super().__init__(...)
        self.set_type(button)  # May be the fallback function
```

**Benefits**:
- **Version Compatibility**: Works across Streamlit versions
- **Graceful Degradation**: Provides user-friendly warnings
- **Type Safety**: Maintains type hints even with fallbacks

## Best Practices

### 1. Always Provide Meaningful Defaults

```python
# Good: Comprehensive defaults
default_kwargs = {
    "label": "Descriptive Label",
    "key": str(uuid4()),
    "help": "Clear help text",
}

# Avoid: Empty or minimal defaults
default_kwargs = {"label": ""}
```

### 2. Set Behavioral Flags Appropriately

```python
# Widget: Maintains state, critical errors, strict validation
super().__init__(stateful=True, fatal=True, strict=True, column_based=False)

# Display Element: No state, critical rendering, strict validation
super().__init__(stateful=False, fatal=True, strict=True, column_based=False)

# Container: No state, critical layout, supports columns
super().__init__(stateful=False, fatal=True, strict=True, column_based=True)
```

### 3. Use Unique Keys for Stateful Widgets

```python
from uuid import uuid4

default_kwargs = {
    "key": str(uuid4()),  # Ensures unique state key
}
```

### 4. Implement Import Fallbacks

```python
try:
    from streamlit import new_component
except ImportError:
    def new_component(*args: Any, **kwargs: Any) -> Any:
        st.warning("Component not available")
        return None
```

### 5. Document Custom Behaviors

```python
class CustomRepresentation(CommonRepresentation[component]):
    """
    Custom representation with special behavior.
    
    Attributes:
        custom_flag: Enables special rendering mode
    """
    
    def __init__(self, custom_flag: bool = False) -> None:
        super().__init__(..., custom_flag=custom_flag)
        self.set_type(component)
```

## Advanced Topics

### Custom Serialization

Override `serialize()` for custom serialization logic:

```python
class CustomRepresentation(CommonRepresentation[component]):
    def serialize(self) -> Dict[str, Any]:
        base_config = super().serialize()
        base_config["custom_field"] = self.custom_value
        return base_config
```

### Dynamic Default Generation

Use lambda functions for dynamic defaults:

```python
from datetime import datetime

default_kwargs = {
    "timestamp": datetime.now(),  # Evaluated once at init
}

# For dynamic evaluation, override generic_factory()
def generic_factory(self) -> Callable[..., Any]:
    # Update timestamp on each factory call
    self.default_kwargs["timestamp"] = datetime.now()
    return super().generic_factory()
```

### Type-Safe Subclassing

Leverage generic type parameters for type safety:

```python
from typing import TypeVar
from streamlit import button

ButtonType = TypeVar("ButtonType", bound=button)

class TypeSafeButtonRep(CommonRepresentation[ButtonType]):
    def deserialize(self) -> ButtonType:
        return super().deserialize()
```

## Testing Common Representations

```python
import unittest
from streamlit import button

class TestButtonRepresentation(unittest.TestCase):
    def setUp(self):
        self.rep = ButtonRepresentation()
    
    def test_initialization(self):
        self.assertEqual(self.rep.get_type(), button)
        self.assertTrue(self.rep.is_stateful())
        self.assertTrue(self.rep.is_fatal())
    
    def test_serialization(self):
        config = self.rep.serialize()
        self.assertEqual(config["type"], "button")
        self.assertTrue(config["stateful"])
    
    def test_factory(self):
        parser = self.rep.generic_factory()
        self.assertIsInstance(parser, StreamlitComponentParser)
    
    def test_ast_definition(self):
        ast = self.rep.ast_definition()
        self.assertEqual(ast["name"], "button")
        self.assertIn("attributes", ast)
```

## Related Documentation

- [Base Representations](./base-representations.md) - Abstract foundation
- [Standards System](./standards.md) - Collection management
- [Widgets Reference](./widgets-reference.md) - Concrete widget implementations
- [Containers Reference](./containers-reference.md) - Container implementations
- [Elements Reference](./elements-reference.md) - Element implementations

## Conclusion

`CommonRepresentation` provides a robust, well-structured foundation for Streamlit component representations. By implementing all abstract methods with sensible defaults and integrating seamlessly with the `StreamlitComponentParser`, it enables developers to create consistent, type-safe, and well-documented component configurations with minimal boilerplate. The class balances flexibility with convention, making it easy to create new representations while maintaining consistency across the library.
