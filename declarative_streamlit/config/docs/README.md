# Configuration Module Documentation

## Overview

The `config` module is a critical component of the declarative Streamlit library that provides a **representation-based configuration system** for managing Streamlit components. This module implements a sophisticated pattern that separates component definitions from their runtime behavior, enabling declarative UI construction with standardized configurations.

## Purpose and Architecture

The configuration module serves three primary purposes:

1. **Component Abstraction**: Provides a unified interface for defining and managing Streamlit components through representations
2. **Behavior Standardization**: Enables consistent component behavior across applications through the Standard pattern
3. **Type Safety and Serialization**: Ensures type-safe component definitions with built-in serialization/deserialization capabilities

## Module Structure

```
config/
├── base/                          # Core abstractions
│   ├── representation.py          # BaseRepresentation abstract class
│   └── standard.py                # BaseStandard collection manager
│
├── common/                        # Streamlit-specific implementations
│   ├── representation.py          # CommonRepresentation base class
│   ├── stdstreamlit.py           # StreamlitCommonStandard singleton
│   │
│   ├── widgets/                   # Interactive input components
│   │   ├── buttons.py            # Button-based widgets
│   │   ├── inputs.py             # Text and number inputs
│   │   ├── selections.py         # Selection widgets (selectbox, radio, etc.)
│   │   └── media.py              # Media input widgets
│   │
│   ├── elements/                  # Display-only components
│   │   ├── text.py               # Text display elements
│   │   ├── data.py               # Data display elements
│   │   ├── media.py              # Media display elements
│   │   └── status.py             # Status message elements
│   │
│   └── containers/                # Layout and organizational components
│       ├── rowbased.py           # Vertical layout containers
│       ├── columbased.py         # Horizontal layout containers
│       └── status.py             # Status context containers
│
└── docs/                          # This documentation
```

## Core Concepts

### Representations

**Representations** are configuration objects that define the default behavior, arguments, and metadata for Streamlit components. Each representation encapsulates:

- **Type Information**: The actual Streamlit component type (e.g., `st.button`, `st.selectbox`)
- **Default Arguments**: Predefined positional arguments
- **Default Keyword Arguments**: Predefined keyword arguments with default values
- **Behavioral Flags**: Configuration flags controlling component behavior:
  - `stateful`: Whether the component maintains state across reruns
  - `fatal`: Whether parsing errors should terminate execution
  - `strict`: Whether to enforce strict type checking
  - `column_based`: Whether the component supports column-based layout

### Standards

**Standards** are collections of representations that define a consistent set of component configurations. The `StreamlitCommonStandard` class provides a pre-configured collection of all common Streamlit components with sensible defaults.

Standards enable:
- **Unified Configuration**: Apply consistent settings across all components in an application
- **Component Discovery**: Look up representations by component type or name
- **Binding Management**: Override default representations through custom bindings
- **Serialization**: Export and import configuration sets

## Key Features

### 1. Singleton Pattern Implementation

Both `BaseRepresentation` and `BaseStandard` implement the singleton pattern to ensure consistent configuration across the application:

```python
def __new__(cls, *args: Any, **kwargs: Any) -> T:
    if not hasattr(cls, "_instance"):
        cls._instance = super(BaseRepresentation, cls).__new__(cls)
    return cls._instance
```

### 2. Generic Factory Pattern

Representations provide a `generic_factory()` method that creates parser instances configured with the representation's default settings:

```python
def generic_factory(self) -> Callable[..., Any]:
    p = StreamlitComponentParser(
        self._type,
        *self.default_args,
        **self.default_kwargs,
    ).set_stateful(self.stateful).set_fatal(self.fatal).set_strict(self.strict)
    return p
```

### 3. Flexible Binding System

Representations can be bound by either:
- **Type binding**: Match components by their Python type object
- **Name binding**: Match components by their string name

The binding mode is controlled by the `bind` parameter (default: `"name"`).

### 4. Graceful Degradation

All component implementations include import fallbacks that provide user-friendly warnings when components are unavailable:

```python
try:
    from streamlit import button
except ImportError:
    def button(*args: Any, **kwargs: Any) -> Any:
        st.warning("Button component not available in this Streamlit version")
        return None
```

## Component Categories

### Widgets (Interactive Components)

Widgets are **stateful** components that capture user input and maintain state across reruns. They typically include:
- Unique keys for state management (using `uuid4()`)
- Event handlers and callbacks
- Input validation

**Examples**: `ButtonRepresentation`, `TextInputRepresentation`, `SelectboxRepresentation`

### Elements (Display Components)

Elements are **non-stateful** components used for displaying information. They do not maintain state and are re-rendered on each rerun.

**Examples**: `MarkdownRepresentation`, `DataFrameRepresentation`, `ImageRepresentation`

### Containers (Layout Components)

Containers organize other components and manage layout structure. They can be:
- **Row-based**: Stack children vertically (`ContainerRepresentation`, `ExpanderRepresentation`)
- **Column-based**: Arrange children horizontally (`ColumnsRepresentation`, `TabsRepresentation`)

## Usage Patterns

### Basic Usage with Standards

```python
from declarative_streamlit import AppPage, StreamlitCommonStandard
import streamlit as st

# Create application with standard configuration
app = AppPage(standard=StreamlitCommonStandard())

# Add components - they inherit standard configuration
app.add_component(st.button, "Click me")

# Container components also use standard configuration
with app.add_container(st.columns, 2) as columns:
    columns.add_component(st.write, "Column 1")
    columns.add_component(st.write, "Column 2")

app.start()
```

### Inspecting Component Configuration

```python
# Get representation for a specific component
standard = StreamlitCommonStandard()
button_rep = standard.get_similar(st.button)

# Serialize to inspect configuration
config = button_rep.serialize()
# Returns: {
#     "type": "button",
#     "args": [],
#     "kwargs": {"label": "Button", "key": "...", "help": "..."},
#     "stateful": True,
#     "fatal": True,
#     "strict": True,
#     "column_based": False
# }
```

### Custom Bindings

```python
from declarative_streamlit.config.base import BaseStandard
from declarative_streamlit.config.common.widgets.buttons import ButtonRepresentation

# Create custom standard with bindings
custom_standard = BaseStandard(
    bindings={
        st.button: CustomButtonRepresentation(),
    },
    defaultbinding="type"
)
```

## Design Principles

### 1. Separation of Concerns
Configuration is completely separated from component rendering logic, allowing independent evolution of both systems.

### 2. Convention over Configuration
Sensible defaults are provided for all components, reducing boilerplate while maintaining flexibility.

### 3. Type Safety
Generic type parameters ensure type safety throughout the representation hierarchy.

### 4. Extensibility
The abstract base classes (`BaseRepresentation`, `BaseStandard`) enable custom representations and standards.

### 5. Backward Compatibility
Import fallbacks ensure graceful degradation with older Streamlit versions.

## Related Documentation

- [Base Representations](./base-representations.md) - Detailed documentation of the base abstraction layer
- [Standards System](./standards.md) - In-depth guide to the Standards pattern and implementation
- [Common Representations](./common-representations.md) - Overview of the CommonRepresentation class
- [Widgets Reference](./widgets-reference.md) - Complete widget representations catalog
- [Containers Reference](./containers-reference.md) - Container components documentation
- [Elements Reference](./elements-reference.md) - Display elements documentation

## Version Compatibility

This configuration system is designed to work across multiple Streamlit versions. Components are imported with try-except blocks to ensure graceful degradation when features are unavailable in older versions.

**Minimum Requirements:**
- Python 3.7+
- Streamlit 1.0+ (recommended: latest stable version)

## Best Practices

1. **Use Standards**: Always leverage `StreamlitCommonStandard` for consistent component behavior
2. **Avoid Direct Instantiation**: Let the standard manage representation instances through the singleton pattern
3. **Inspect Before Customizing**: Use `serialize()` to understand default configurations before creating custom representations
4. **Maintain Immutability**: Treat representations as immutable configuration objects
5. **Document Custom Representations**: When creating custom representations, document behavioral flags clearly

## Contributing

When adding new component representations:

1. Follow the established naming convention: `{ComponentName}Representation`
2. Implement all abstract methods from `BaseRepresentation`
3. Add import fallbacks for version compatibility
4. Include comprehensive default configurations
5. Set appropriate behavioral flags (`stateful`, `fatal`, `strict`, `column_based`)
6. Register the representation in `StreamlitCommonStandard`
7. Update the appropriate reference documentation

## Conclusion

The configuration module provides a robust, type-safe, and extensible foundation for declarative Streamlit applications. By separating component configuration from rendering logic and providing standardized defaults, it enables developers to build consistent, maintainable, and scalable Streamlit applications with minimal boilerplate.
