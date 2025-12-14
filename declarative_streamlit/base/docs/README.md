# Base Module Documentation

## Overview

The **base** module provides high-level abstractions for building declarative Streamlit applications. It consists of three main areas that work together to create a flexible, composable architecture for Streamlit application development.

## Module Structure

```
base/
├── app/              # Application-level implementations
├── components/       # Core canvas components
├── logic/           # State management utilities
└── docs/            # Documentation (this directory)
```

## Architecture Components

### 1. Application Layer (`app/`)
High-level application components that extend base canvas functionality with Streamlit-specific features.

- **[AppPage](./app-page.md)** - Main application page implementation
- **[AppFragment](./app-fragment.md)** - Fragment-based component for isolated reruns
- **[AppDialog](./app-dialog.md)** - Modal dialog implementation

### 2. Component Layer (`components/`)
Base abstractions that define the core canvas interface and specialized canvas types.

- **[Canvas](./canvas.md)** - Abstract base class for all canvases
- **[Fragment](./fragment.md)** - Fragment canvas abstraction
- **[Dialog](./dialog.md)** - Dialog canvas abstraction

### 3. Logic Layer (`logic/`)
State management and business logic utilities.

- **[SessionState](./session-state.md)** - Type-safe session state wrapper

## Design Patterns

### Canvas Pattern
The module follows a **Canvas Pattern** where all renderable components extend from a base `Canvas` class. Each canvas type provides:

- Component management through `add_component()` and `add_container()` methods
- Error handling with `failsafe` and `failhandler` mechanisms
- Strict type checking capabilities
- Schema-based rendering through internal `Layer` system

### Composition over Inheritance
The architecture favors composition, allowing developers to:

- Nest canvases within canvases (e.g., fragments in pages)
- Build complex UIs from simple, reusable components
- Maintain separation of concerns between layout and logic

### Type Safety
All components are designed with type safety in mind:

- Pydantic models for configuration validation
- Generic type support with `TypeVar`
- Strict type checking in session state management

## Quick Start

```python
from declarative_streamlit.base import AppPage, SessionState
import streamlit as st

# Configure page
AppPage.set_page_config(layout="wide", title="My App")

# Create application
app = AppPage()

# Add components
app.add_component(st.title, "Hello World")
app.add_component(st.button, "Click Me", key="btn1")

# Add container with nested components
with app.add_container(st.container, border=True) as container:
    container.add_component(st.text_input, "Name:", key="name")
    
# Render application
app.start()
```

## Documentation Standards

Each documentation file in this directory follows these standards:

### Structure
1. **Overview** - Brief description and purpose
2. **Class/Module Signature** - Full signature with type hints
3. **Description** - Detailed explanation of functionality
4. **Parameters** - Complete parameter documentation
5. **Attributes** - Public attributes and properties
6. **Methods** - Detailed method documentation
7. **Usage Examples** - Practical code examples
8. **Error Handling** - Exception documentation
9. **Best Practices** - Recommended usage patterns
10. **Related Components** - Links to related documentation

### Code Examples
All code examples are:
- **Complete** - Can be run as-is
- **Tested** - Verified to work with current implementation
- **Documented** - Include inline comments explaining key concepts

## Reading Guide

### For Beginners
1. Start with [Canvas](./canvas.md) to understand the base abstraction
2. Read [AppPage](./app-page.md) for application-level concepts
3. Explore [SessionState](./session-state.md) for state management
4. Review usage examples in each document

### For Advanced Users
1. [Canvas](./canvas.md) - Understand the abstract interface
2. [Fragment](./fragment.md) and [AppFragment](./app-fragment.md) - Performance optimization
3. [Dialog](./dialog.md) and [AppDialog](./app-dialog.md) - Modal interactions
4. Integration patterns across all components

## API Stability

The base module is considered **stable** for the following components:
- `Canvas` abstract interface
- `AppPage`, `AppFragment`, `AppDialog` public APIs
- `SessionState` core functionality

## Version Information

- **Module Version**: 0.0.1
- **Documentation Version**: 1.0.0
- **Last Updated**: December 2025

## Contributing

When extending base components:
1. Maintain compatibility with the `Canvas` abstract interface
2. Follow type safety guidelines
3. Document all public APIs following these standards
4. Include usage examples in documentation

## See Also

- [Core Module Documentation](../../core/docs/README.md) - Lower-level parser and handler implementation
- [Config Module Documentation](../../config/docs/README.md) - Configuration standards and representations
- [Examples](../../examples/) - Full application examples

---

**Navigation**: [Home](#) | [Canvas](./canvas.md) | [AppPage](./app-page.md) | [AppFragment](./app-fragment.md) | [AppDialog](./app-dialog.md) | [SessionState](./session-state.md)
