# Standards System

## Overview

The **Standards System** provides a centralized mechanism for managing collections of component representations. It implements a registry pattern that enables component lookup, binding management, and configuration consistency across applications.

**Location**: `declarative_streamlit/config/base/standard.py`

## Class Definition

```python
class BaseStandard:
    """
    Base class for a collection of standard representations.
    It helps to manage the standard representations and their configurations.
    """
```

## Purpose and Architecture

The Standards System serves as a **component registry** that:

1. **Centralizes Configuration**: Maintains a single source of truth for component representations
2. **Enables Discovery**: Provides lookup mechanisms for finding representations by type or name
3. **Supports Overrides**: Allows custom bindings to replace default representations
4. **Enforces Consistency**: Ensures all components use standardized configurations

## Design Patterns

### 1. Singleton Pattern

`BaseStandard` implements singleton behavior to ensure consistent configuration:

```python
def __new__(cls, *args: Any, **kwargs: Any) -> T:
    if not hasattr(cls, "_instance"):
        cls._instance = super(BaseStandard, cls).__new__(cls)
    return cls._instance
```

**Rationale**:
- Guarantees a single global standard instance
- Prevents configuration drift
- Simplifies dependency management

### 2. Registry Pattern

The standard acts as a registry for representations:

```python
self.representations: List[BaseRepresentation] = []
```

**Operations**:
- **Register**: Add representations to the registry
- **Lookup**: Find representations by type or name
- **Iterate**: Access all registered representations

### 3. Strategy Pattern

The binding system implements the strategy pattern for lookup:

- **Type Binding Strategy**: Match by Python type object
- **Name Binding Strategy**: Match by string name

## Constructor Parameters

```python
def __init__(
    self,
    bindings: Dict[Any, Union[BaseRepresentation, Tuple[str, ...]]],
    defaultbinding: Literal["type", "name"] = "type",
)
```

### Parameters

#### `bindings: Dict[Any, Union[BaseRepresentation, Tuple[str, ...]]]`

A dictionary that maps component types to custom representations, enabling override functionality.

**Structure**:
```python
bindings = {
    st.button: CustomButtonRepresentation(),
    st.selectbox: (SelectboxRepresentation(), CustomSelectboxRepresentation()),
}
```

**Key Types**: Any (typically component types like `st.button`)

**Value Types**:
- `BaseRepresentation`: Single custom representation override
- `Tuple[BaseRepresentation, ...]`: Multiple representation options

**Purpose**: 
- Override default representations for specific components
- Provide alternative representations for the same component
- Support cross-standard compatibility

**Example Usage**:
```python
from declarative_streamlit.config.base import BaseStandard
from declarative_streamlit.config.common.widgets import ButtonRepresentation

# Create standard with custom button representation
custom_standard = BaseStandard(
    bindings={
        st.button: CustomButtonRepresentation(),
    },
    defaultbinding="type"
)
```

#### `defaultbinding: Literal["type", "name"] = "type"`

Determines the default lookup strategy for component discovery.

**Options**:

##### `"type"` (default for BaseStandard)
Match components by their Python type object:

```python
standard = BaseStandard(bindings={}, defaultbinding="type")
rep = standard.get_similar(st.button)  # Matches by type object
```

**Use Cases**:
- Type-safe lookups
- Static analysis support
- IDE autocomplete integration

**Advantages**:
- Strong typing
- Compile-time validation
- Refactoring safety

**Disadvantages**:
- Requires import of actual types
- Less flexible for dynamic scenarios

##### `"name"` (default for StreamlitCommonStandard)
Match components by their string name:

```python
standard = StreamlitCommonStandard()  # Uses defaultbinding="name"
rep = standard.get_similar("button")  # Matches by name string
```

**Use Cases**:
- String-based configuration (YAML, JSON)
- Dynamic component loading
- API-driven component selection

**Advantages**:
- Dynamic lookup without imports
- Serialization-friendly
- Flexible configuration

**Disadvantages**:
- No compile-time checking
- Potential naming collisions
- Case sensitivity considerations

## Instance Attributes

### `bindings: Dict[Any, Union[BaseRepresentation, Tuple[str, ...]]]`
Stores custom representation overrides.

### `defaultbinding: Literal["type", "name"]`
Stores the default binding strategy.

### `representations: List[BaseRepresentation]`
Maintains the registry of all representations in the standard.

**Initialization**: Empty list `[]`

**Population**: Via `add_representation()` method

## Public Methods

### Registration Methods

#### `add_representation(representation: BaseRepresentation) -> T`

Adds a representation to the standard's registry.

**Parameters**:
- `representation`: The representation instance to register

**Returns**: `self` (enables method chaining)

**Behavior**:
```python
def add_representation(self, representation: BaseRepresentation) -> T:
    self.representations.append(representation)
    return cast(T, self)
```

**Example**:
```python
standard = BaseStandard(bindings={})
standard.add_representation(ButtonRepresentation()) \
        .add_representation(TextInputRepresentation()) \
        .add_representation(SelectboxRepresentation())
```

**Method Chaining**: Supports fluent interface pattern for multiple additions.

### Lookup Methods

#### `get_similar(value: Any) -> Optional[BaseRepresentation]`

Finds a representation matching the given value using the default binding strategy.

**Parameters**:
- `value`: Component type or name to search for

**Returns**: 
- `BaseRepresentation` if match found
- `None` if no match found

**Behavior**:
```python
def get_similar(self, value: Any) -> Optional[BaseRepresentation]:
    if isinstance(value, str):
        return self.__search_by_name(value)
    return self._search_by_type(value)
```

**Logic**:
1. If `value` is a string → search by name
2. Otherwise → search by type

**Example**:
```python
standard = StreamlitCommonStandard()

# Name-based lookup
button_rep = standard.get_similar("button")

# Type-based lookup  
button_rep = standard.get_similar(st.button)
```

**Note**: Automatically checks bindings for overrides before returning default representation.

#### `_search_by_type(typ: Any) -> Optional[BaseRepresentation]`

Searches for a representation by component type (internal method).

**Parameters**:
- `typ`: The component type to search for

**Returns**: Matching representation or `None`

**Algorithm**:
```python
def _search_by_type(self, typ: Any) -> Optional[BaseRepresentation]:
    for rep in self.representations:
        if rep == typ:
            if bind := self._find_binding(rep):
                return bind
            return rep
    return None
```

**Steps**:
1. Iterate through all representations
2. Use representation's `__eq__` method for comparison
3. Check for binding override via `_find_binding()`
4. Return binding override if exists, otherwise return representation
5. Return `None` if no match found

**Complexity**: O(n) where n is number of representations

#### `_search_by_name(name: str) -> Optional[BaseRepresentation]`

Searches for a representation by component name (internal method).

**Parameters**:
- `name`: String name of the component (e.g., `"button"`)

**Returns**: Matching representation or `None`

**Algorithm**:
```python
def _search_by_name(self, name: str) -> Optional[BaseRepresentation]:
    for rep in self.representations:
        if name == rep:
            if bind := self._find_binding(rep):
                return bind
            return rep
    return None
```

**Note**: Uses representation's `__eq__` method which compares against `_type.__name__`.

#### `_find_binding(typ: Any) -> Optional[BaseRepresentation]`

Finds a custom binding override for a given type (internal method).

**Parameters**:
- `typ`: The type to find a binding for

**Returns**: Bound representation or `None`

**Algorithm**:
```python
def _find_binding(self, typ: Any) -> Optional[BaseRepresentation]:
    if len(self.bindings) == 0:
        return None
    
    for key, value in self.bindings.items():
        if typ == key:
            if isinstance(value, BaseRepresentation):
                return value
            elif isinstance(value, tuple):
                for rep in value:
                    if rep == typ:
                        return rep
    
    return None
```

**Steps**:
1. Return `None` if no bindings defined
2. Iterate through bindings dictionary
3. If key matches `typ`:
   - If value is single representation → return it
   - If value is tuple → search tuple for matching representation
4. Return `None` if no binding found

**Use Case**: Enable representation overrides without modifying the registry.

### Utility Methods

#### `__getitem__(key: Any) -> Optional[BaseRepresentation]`

Enables dictionary-style access to representations.

**Parameters**:
- `key`: Component type or name

**Returns**: Matching representation or `None`

**Implementation**:
```python
def __getitem__(self, key: Any) -> Optional[BaseRepresentation]:
    if self.defaultbinding == "type":
        return self._search_by_type(key)
    elif self.defaultbinding == "name":
        return self._search_by_name(key)
    else:
        raise ValueError("Invalid default binding type. Use 'type' or 'name'.")
```

**Usage**:
```python
standard = StreamlitCommonStandard()

# Dictionary-style access
button_rep = standard["button"]
selectbox_rep = standard["selectbox"]

# Equivalent to get_similar()
assert standard["button"] == standard.get_similar("button")
```

**Error Handling**: Raises `ValueError` if `defaultbinding` is invalid.

#### `get_representations(stringfy: bool = False) -> List[Union[BaseRepresentation, str]]`

Returns all representations in the standard.

**Parameters**:
- `stringfy`: If `True`, return string names; if `False`, return representation objects

**Returns**: 
- List of `BaseRepresentation` objects (if `stringfy=False`)
- List of string names (if `stringfy=True`)

**Implementation**:
```python
def get_representations(self, stringfy: bool = False) -> List[Union[BaseRepresentation, str]]:
    if stringfy:
        return [rep.get_str_representation() for rep in self.representations]
    return self.representations
```

**Example**:
```python
standard = StreamlitCommonStandard()

# Get representation objects
reps = standard.get_representations()
# Returns: [ButtonRepresentation(), TextInputRepresentation(), ...]

# Get string names
names = standard.get_representations(stringfy=True)
# Returns: ["button", "text_input", "selectbox", ...]
```

**Use Cases**:
- Introspection and debugging
- Documentation generation
- Configuration validation

## StreamlitCommonStandard Implementation

### Class Definition

```python
class StreamlitCommonStandard(BaseStandard):
    """
    A standard representation for common elements in Streamlit.
    It helps to manage the standard representations and their configurations.
    """
```

**Location**: `declarative_streamlit/config/common/stdstreamlit.py`

### Initialization

```python
def __init__(self) -> None:
    super().__init__(
        bindings={},
        defaultbinding="name",  # Uses name-based lookup by default
    )
    
    # Register all widget representations
    self.add_representation(ButtonRepresentation())
    self.add_representation(TextInputRepresentation())
    # ... (57 total representations)
```

### Registered Component Categories

#### Widgets (26 representations)
Interactive components that maintain state:

- **Buttons**: `button`, `download_button`, `form_submit_button`, `link_button`, `page_link`
- **Selections**: `selectbox`, `multiselect`, `radio`, `checkbox`, `select_slider`, `color_picker`, `toggle`, `feedback`, `pills`, `segmented_control`
- **Inputs**: `text_input`, `text_area`, `number_input`, `date_input`, `time_input`, `chat_input`, `slider`
- **Media**: `file_uploader`, `data_editor`, `camera_input`, `audio_input`

#### Elements (19 representations)
Display-only components:

- **Data**: `dataframe`, `table`, `json`, `metric`
- **Status**: `success`, `error`, `warning`, `info`
- **Text**: `markdown`, `code`, `text`, `header`, `subheader`, `title`, `caption`, `latex`, `badge`, `html`
- **Media**: `image`, `video`, `audio`

#### Containers (8 representations)
Layout and organizational components:

- **Row-based**: `container`, `expander`, `form`, `popover`, `chat_message`
- **Column-based**: `columns`, `tabs`
- **Status**: `status`, `spinner`

### Total: 53 Representations

## Usage Patterns

### Basic Standard Usage

```python
from declarative_streamlit import AppPage, StreamlitCommonStandard
import streamlit as st

# Create application with standard
app = AppPage(standard=StreamlitCommonStandard())

# Components automatically use standard configuration
app.add_component(st.button, "Click Me")  # Uses ButtonRepresentation defaults
```

### Inspecting Standard Components

```python
standard = StreamlitCommonStandard()

# Get all available components
component_names = standard.get_representations(stringfy=True)
print(component_names)  # ["button", "text_input", "selectbox", ...]

# Inspect specific component configuration
button_config = standard["button"].serialize()
print(button_config)
# {
#     "type": "button",
#     "args": [],
#     "kwargs": {"label": "Button", "key": "...", "help": "..."},
#     "stateful": True,
#     "fatal": True,
#     "strict": True,
#     "column_based": False
# }
```

### Custom Standard with Bindings

```python
from declarative_streamlit.config.base import BaseStandard
from declarative_streamlit.config.common.widgets import ButtonRepresentation

class CustomButtonRepresentation(ButtonRepresentation):
    def __init__(self) -> None:
        super().__init__()
        self.default_kwargs["label"] = "Custom Button"
        self.stateful = False  # Override: make non-stateful

# Create standard with custom binding
custom_standard = BaseStandard(
    bindings={
        st.button: CustomButtonRepresentation(),
    },
    defaultbinding="type"
)

# Add other standard representations
custom_standard.add_representation(TextInputRepresentation())
custom_standard.add_representation(SelectboxRepresentation())

# Now st.button will use CustomButtonRepresentation
app = AppPage(standard=custom_standard)
app.add_component(st.button, "Test")  # Uses CustomButtonRepresentation
```

### Multiple Binding Options

```python
# Provide multiple representation options for same component
multi_binding_standard = BaseStandard(
    bindings={
        st.button: (
            ButtonRepresentation(),
            CustomButtonRepresentation(),
            MinimalButtonRepresentation(),
        ),
    },
    defaultbinding="type"
)

# The first matching representation in the tuple will be used
rep = multi_binding_standard.get_similar(st.button)
# Returns first match from the tuple
```

## Advanced Topics

### Dynamic Standard Creation

```python
def create_dynamic_standard(component_list: List[str]) -> BaseStandard:
    """Create a standard with only specified components."""
    standard = BaseStandard(bindings={}, defaultbinding="name")
    
    # Mapping of names to representation classes
    rep_map = {
        "button": ButtonRepresentation,
        "text_input": TextInputRepresentation,
        "selectbox": SelectboxRepresentation,
    }
    
    for component_name in component_list:
        if rep_class := rep_map.get(component_name):
            standard.add_representation(rep_class())
    
    return standard

# Usage
minimal_standard = create_dynamic_standard(["button", "text_input"])
```

### Standard Introspection

```python
def analyze_standard(standard: BaseStandard) -> Dict[str, Any]:
    """Analyze a standard's configuration."""
    analysis = {
        "total_components": len(standard.representations),
        "binding_mode": standard.defaultbinding,
        "custom_bindings": len(standard.bindings),
        "stateful_components": [],
        "fatal_components": [],
    }
    
    for rep in standard.representations:
        name = rep.get_str_representation()
        if rep.is_stateful():
            analysis["stateful_components"].append(name)
        if rep.is_fatal():
            analysis["fatal_components"].append(name)
    
    return analysis

# Usage
standard = StreamlitCommonStandard()
report = analyze_standard(standard)
print(f"Total components: {report['total_components']}")
print(f"Stateful components: {len(report['stateful_components'])}")
```

### Cross-Standard Compatibility

```python
class ExtendedStandard(BaseStandard):
    """Extend StreamlitCommonStandard with custom components."""
    
    def __init__(self, base_standard: StreamlitCommonStandard) -> None:
        super().__init__(bindings={}, defaultbinding="name")
        
        # Import all base representations
        for rep in base_standard.representations:
            self.add_representation(rep)
        
        # Add custom representations
        self.add_representation(CustomComponentRepresentation())

# Usage
base = StreamlitCommonStandard()
extended = ExtendedStandard(base)
```

## Best Practices

### 1. Use Appropriate Binding Mode

- **Type binding (`"type"`)**: For type-safe, statically-defined applications
- **Name binding (`"name"`)**: For dynamic, configuration-driven applications

```python
# Type-safe application
app = AppPage(standard=BaseStandard(bindings={}, defaultbinding="type"))

# Configuration-driven application
app = AppPage(standard=StreamlitCommonStandard())  # Uses "name" binding
```

### 2. Prefer Standard Over Manual Configuration

```python
# Good: Use standard for consistent configuration
app = AppPage(standard=StreamlitCommonStandard())
app.add_component(st.button, "Click")  # Inherits standard config

# Avoid: Manual configuration for each component
app = AppPage()
app.add_component(st.button, "Click").set_stateful(True).set_fatal(True)
```

### 3. Document Custom Bindings

```python
custom_standard = BaseStandard(
    bindings={
        # Override button with custom representation
        # Reason: Project requires non-stateful buttons
        st.button: CustomButtonRepresentation(),
    },
    defaultbinding="type"
)
```

### 4. Validate Component Existence

```python
def safe_get_representation(standard: BaseStandard, component: Any) -> Optional[BaseRepresentation]:
    """Safely get representation with validation."""
    rep = standard.get_similar(component)
    if rep is None:
        print(f"Warning: No representation found for {component}")
    return rep
```

### 5. Use Singleton Appropriately

```python
# Good: Let singleton pattern work
standard1 = StreamlitCommonStandard()
standard2 = StreamlitCommonStandard()
assert standard1 is standard2  # Same instance

# Note: If you need different configurations, use different classes
class CustomStandard(BaseStandard):
    pass  # Different singleton instance
```

## Error Handling

### Invalid Binding Type

```python
try:
    standard = BaseStandard(bindings={}, defaultbinding="invalid")
    rep = standard["button"]
except ValueError as e:
    print(f"Error: {e}")  # "Invalid default binding type. Use 'type' or 'name'."
```

### Component Not Found

```python
standard = StreamlitCommonStandard()
rep = standard.get_similar("nonexistent_component")
if rep is None:
    print("Component not found in standard")
```

## Performance Considerations

### Lookup Complexity

- **Time Complexity**: O(n) for component lookup (linear search)
- **Space Complexity**: O(n) for storing representations

### Optimization Strategies

```python
# For frequently accessed standards, cache lookups
class CachedStandard(BaseStandard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache: Dict[Any, BaseRepresentation] = {}
    
    def get_similar(self, value: Any) -> Optional[BaseRepresentation]:
        if value in self._cache:
            return self._cache[value]
        
        rep = super().get_similar(value)
        if rep:
            self._cache[value] = rep
        return rep
```

## Related Documentation

- [Base Representations](./base-representations.md) - Foundation of the representation system
- [Common Representations](./common-representations.md) - Streamlit-specific implementations
- [Widgets Reference](./widgets-reference.md) - Complete widget catalog
- [Containers Reference](./containers-reference.md) - Container components
- [Elements Reference](./elements-reference.md) - Display elements

## Conclusion

The Standards System provides a robust, flexible mechanism for managing component configurations at scale. By centralizing representation management and providing multiple lookup strategies, it enables consistent, maintainable, and extensible declarative Streamlit applications. The combination of singleton pattern, registry pattern, and binding overrides creates a powerful configuration management system that balances ease of use with advanced customization capabilities.
