# Core Module Documentation

## Overview

The `core` module is the foundational layer of the declarative-streamlit library, providing a comprehensive framework for building declarative, event-driven Streamlit applications. This module implements a sophisticated architecture that enables component composition, state management, layout parsing, and event-driven communication patterns.

## Purpose

The core module serves as the backbone for:

1. **Component Abstraction**: Wrapping Streamlit components with enhanced functionality
2. **State Management**: Tracking and managing interactive element states
3. **Layout Composition**: Building complex hierarchical layouts declaratively
4. **Error Handling**: Providing robust error handling strategies
5. **Event-Driven Architecture**: Enabling pub/sub communication patterns
6. **Parser System**: Converting declarative definitions into executable components

## Architecture

The core module is organized into five main subsystems:

```
core/
├── base/           # Abstract base classes
├── components/     # Concrete component implementations
├── build/          # Parser system for components and layouts
├── handlers/       # Schema and layer management
└── logic/          # Event-driven messaging system
```

### Module Dependencies

```
┌─────────────────────────────────────────────┐
│             Application Layer               │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          Build Layer (Parsers)              │
│   - StreamlitComponentParser                │
│   - StreamlitLayoutParser                   │
└──────┬─────────────────────────┬────────────┘
       │                         │
┌──────▼──────────┐    ┌────────▼────────────┐
│   Components    │    │     Handlers        │
│  - IElement     │    │    - Schema         │
│  - VElement     │◄───┤    - Layer          │
│  - Container    │    └─────────────────────┘
└──────┬──────────┘
       │
┌──────▼──────────────────────────────────────┐
│          Base Layer (Abstractions)          │
│   - Renderable                              │
│   - Stateful                                │
│   - Composable                              │
└─────────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────┐
│      Logic Layer (Event System)             │
│   - BaseBroker                              │
│   - BaseTopic                               │
│   - BaseEvent                               │
└─────────────────────────────────────────────┘
```

## Key Concepts

### 1. Renderable Pattern

All visual components implement the `Renderable` base class, which provides:
- **Lazy Rendering**: Components are rendered on-demand via the `render()` method
- **Error Handling**: Built-in error handling with fatal/non-fatal strategies
- **Effect System**: Post-render effects for side effects and callbacks
- **Context Management**: Support for Python's `with` statement

### 2. Stateful Components

Interactive elements (buttons, inputs, selects) implement the `Stateful` interface:
- **Key-based State**: Automatic session state tracking via unique keys
- **State Validation**: Strict mode for enforcing key presence
- **State Mutation**: Controlled state modification with editable flag

### 3. Composable Layouts

Containers implement the `Composable` base class for hierarchical composition:
- **Schema-based Organization**: Multi-layer structure for complex layouts
- **Column vs Row Rendering**: Support for both rendering strategies
- **Component Parser Integration**: Automatic component wrapping and parsing

### 4. Parser Architecture

The build system uses a two-tier parser architecture:
- **Component Parser**: Wraps individual Streamlit components
- **Layout Parser**: Manages containers and nested structures
- **Configuration Propagation**: Automatic config inheritance

### 5. Event-Driven Communication

The logic subsystem implements a robust pub/sub pattern:
- **Topic-based Messaging**: Decoupled component communication
- **Priority Handlers**: Execution order control
- **Error Strategies**: Configurable error handling (RAISE, WARN, IGNORE, CUSTOM)
- **Dead Letter Queue**: Debugging failed events

## Module Structure

### Base Classes (`base/`)

**Purpose**: Define core abstractions and contracts

- [`Renderable`](./base-classes.md#renderable) - Base class for all renderable components
- [`Stateful`](./base-classes.md#stateful) - Abstract interface for state-tracked components
- [`Composable`](./base-classes.md#composable) - Base class for layout composition

### Components (`components/`)

**Purpose**: Concrete implementations of visual elements

- [`IElement`](./components.md#ielement) - Interactive elements (buttons, inputs, selects)
- [`VElement`](./components.md#velement) - Visual elements (text, images, media)
- [`Container`](./components.md#container) - Layout containers (columns, tabs, expanders)

### Build System (`build/`)

**Purpose**: Parse and construct component trees

- [`Parser`](./parsers.md#parser) - Abstract parser base class
- [`StreamlitComponentParser`](./parsers.md#streamlitcomponentparser) - Component wrapper and parser
- [`StreamlitLayoutParser`](./parsers.md#streamlitlayoutparser) - Container and layout parser

### Handlers (`handlers/`)

**Purpose**: Manage component organization and execution

- [`Schema`](./handlers.md#schema) - Top-level layout schema management
- [`Layer`](./handlers.md#layer) - Layer-based component organization

### Logic System (`logic/`)

**Purpose**: Event-driven communication infrastructure

- [`BaseBroker`](./event-system.md#basebroker) - Message broker for topic management
- [`BaseTopic`](./event-system.md#basetopic) - Pub/sub topic implementation
- [`BaseEvent`](./event-system.md#baseevent) - Event abstraction
- [`TopicMessage`](./event-system.md#topicmessage) - Message type definition

## Design Principles

### 1. Separation of Concerns

Each subsystem has a clear, single responsibility:
- **Base**: Define contracts and behavior
- **Components**: Implement visual elements
- **Build**: Parse and transform
- **Handlers**: Organize and execute
- **Logic**: Enable communication

### 2. Open/Closed Principle

Classes are open for extension but closed for modification:
- Abstract base classes define interfaces
- Concrete implementations extend functionality
- Method chaining enables flexible configuration

### 3. Dependency Inversion

High-level modules depend on abstractions, not concretions:
- Parsers depend on abstract `Renderable`, not concrete types
- Handlers work with callables, not specific components
- Logic system uses type-agnostic messages

### 4. Liskov Substitution

Subtypes can replace their base types:
- `IElement` and `VElement` are both valid `Renderable` instances
- Any `Parser` subclass can be used interchangeably
- Topic handlers accept any callable

## Common Patterns

### Method Chaining

All configuration methods return `self` for fluent APIs:

```python
component = (
    app.add_component(st.button, "Click me", key="btn")
    .set_fatal(False)
    .set_errhandler(lambda e: st.error(str(e)))
    .add_effect(lambda val: st.write(f"Clicked: {val}"))
)
```

### Lazy Evaluation

Components are configured but not executed until explicitly called:

```python
# Configuration phase - no rendering
parser = StreamlitComponentParser(st.text, "Hello")
element = parser.parse()

# Execution phase - renders to Streamlit
element()  # or element.render()
```

### Context Management

Components support the `with` statement for scoped rendering:

```python
with container.render():
    st.write("Inside container")
```

## Type System

The core module uses comprehensive type hints:

```python
from typing import Any, Callable, Dict, List, Union, Optional, TypeVar

T = TypeVar('T', bound='BaseClass')  # For method chaining
HandlerType = Callable[[Exception], Union[NoReturn, bool]]  # Error handlers
TopicMessage = Dict[str, Any]  # Event messages
```

## Error Handling

The module implements a three-tier error handling strategy:

### 1. Fatal Errors

Errors that halt execution and raise exceptions:

```python
component.set_fatal(True)  # Default for most components
```

### 2. Non-Fatal Errors

Errors handled gracefully with fallback behavior:

```python
component.set_fatal(False).set_errhandler(lambda e: st.warning(str(e)))
```

### 3. Silent Errors

Errors that are suppressed (use cautiously):

```python
component.set_fatal(False)  # No handler - returns NonRenderError
```

## Performance Considerations

### Lazy Rendering

Components are only rendered when called, reducing unnecessary work:

```python
# Configured but not rendered
button = parser.parse()

# Only renders if condition is true
if show_button:
    button()
```

### Effect Execution

Effects are executed post-render with error isolation:

```python
component.add_effect(heavy_computation)  # Errors won't break render
```

### Priority-based Handlers

Event handlers execute in priority order for predictable behavior:

```python
@topic.register(priority=100)  # Higher priority = earlier execution
def critical_handler(data): ...
```

## Validation and Type Safety

The module uses Pydantic for runtime validation:

```python
from pydantic import BaseModel, validator

class ComponentConfig(BaseModel):
    component: Callable
    args: List[Any]
    kwargs: Dict[str, Any]
    
    @validator('component')
    def must_be_callable(cls, v):
        if not callable(v):
            raise ValueError('component must be callable')
        return v
```

## Documentation Navigation

- **[Base Classes](./base-classes.md)** - Renderable, Stateful, Composable
- **[Components](./components.md)** - IElement, VElement, Container
- **[Parsers](./parsers.md)** - Component and Layout parsing
- **[Handlers](./handlers.md)** - Schema and Layer management
- **[Event System](./event-system.md)** - Broker, Topic, Event
- **[API Reference](./api-reference.md)** - Complete API documentation
- **[Usage Examples](./usage-examples.md)** - Practical examples
- **[Migration Guide](./migration-guide.md)** - Upgrading from previous versions

## Version Information

- **Module Version**: 1.0.0
- **Python Compatibility**: 3.8+
- **Streamlit Compatibility**: 1.0.0+
- **Documentation Version**: 1.0.0
- **Last Updated**: 2025-12-14

## Contributing

When extending the core module:

1. Inherit from appropriate base classes
2. Follow type hint conventions
3. Implement abstract methods completely
4. Add docstrings in Google style
5. Include validation using Pydantic
6. Write comprehensive tests
7. Update documentation

## License

This module is part of the declarative-streamlit library. Refer to the main LICENSE file for terms and conditions.
