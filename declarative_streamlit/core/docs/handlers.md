# Handlers Documentation

## Overview

The `handlers` submodule provides the organizational infrastructure for managing component layouts through a schema-based system. It implements a two-tier hierarchy: **Schema** (top-level organization) and **Layer** (component grouping), enabling complex multi-layer layouts with flexible rendering strategies.

## Module Structure

```
handlers/
├── __init__.py
├── schema.py          # Top-level layout schema
└── layer.py           # Layer-based component organization
```

---

## Schema

**Location**: `core/handlers/schema.py`

### Purpose

`Schema` is the top-level layout manager that organizes components into a hierarchical structure. It maintains a main body (primary layer) and optional named/indexed layers for complex layouts.

### Class Definition

```python
class Schema:
    """
    Top-level layout schema manager.
    
    Organizes components into a hierarchical structure with:
    - Main body layer (primary container)
    - Named/indexed layers (sub-organization)
    - Dynamic layer access via properties
    - Serialization support
    """
```

### Constructor

```python
def __init__(
    self,
    body_name: Optional[str] = None,
):
    """
    Initialize schema with optional body name.
    
    Args:
        body_name (Optional[str]): Name for main body layer
                                   Default: "__body__"
                                   
    Attributes:
        _body (Layer): Main body layer containing all content
        _schema (Dict[Union[int, str], Layer]): Map of layer IDs to layers
    """
```

**Initialization**:
```python
self._body = Layer("__body__" if not body_name else body_name)
self._schema = {}  # Empty dict for additional layers
```

**Default Structure**:
```
Schema
└── _body (Layer: "__body__")
    └── elements: []
```

### Properties

#### main_body

**Signature**:
```python
@property
def main_body(self) -> Layer:
    """
    Get the main body layer.
    
    Returns:
        Layer: The primary layer containing all top-level components
        
    Usage:
        schema.main_body.add_component(component)
    """
```

**Purpose**: Provides access to the primary layer where components are added by default.

### Layer Management

#### add_layer()

**Signature**:
```python
def add_layer(self, idlayer: Optional[Union[int, str]]) -> Layer:
    """
    Add a new layer to the schema.
    
    Args:
        idlayer: Unique identifier for the layer (int or str)
        
    Returns:
        Layer: The newly created layer
        
    Behavior:
        1. Creates Layer with idlayer
        2. Stores in _schema dictionary
        3. Adds layer to main body as a component
        4. Sets layer as dynamic property on schema
        
    Side Effects:
        - Layer becomes accessible as schema.<idlayer>
        - Layer added to main body's element list
    """
```

**Implementation**:
```python
def add_layer(self, idlayer):
    self._schema[idlayer] = Layer(idlayer)
    self._body.add_component(self._schema[idlayer])
    self._set_layer_prop(self._schema[idlayer])
    return self._schema[idlayer]
```

**Example**:
```python
schema = Schema()
header = schema.add_layer("header")
sidebar = schema.add_layer(1)

# Now accessible as properties
schema.header  # Returns header layer
schema[1]      # Returns sidebar layer
```

#### _set_layer_prop()

**Signature**:
```python
def _set_layer_prop(self, layer: Layer) -> None:
    """
    Set layer as dynamic property.
    
    Args:
        layer: Layer to set as property
        
    Side Effects:
        Sets attribute with layer's ID as name
    """
```

**Implementation**:
```python
def _set_layer_prop(self, layer: Layer):
    setattr(self, layer.idlayer, layer)
```

### Component Management

#### add_component()

**Signature**:
```python
def add_component(
    self,
    component: Callable[..., Any],
) -> Callable[..., Any]:
    """
    Add component to main body layer.
    
    Args:
        component: Callable component (parser or direct callable)
        
    Returns:
        Callable: The added component
        
    Behavior:
        Delegates to main body layer's add_component()
    """
```

**Implementation**:
```python
def add_component(self, component):
    self._body.add_component(component)
    return component
```

**Usage**:
```python
from declarative_streamlit.core.build import StreamlitComponentParser

parser = StreamlitComponentParser(st.button, "Click")
schema.add_component(parser)
```

### Configuration

#### set_body_name()

**Signature**:
```python
def set_body_name(self, name: str) -> "Schema":
    """
    Change the main body layer's name.
    
    Args:
        name (str): New name for body layer
        
    Returns:
        self: For method chaining
        
    Purpose:
        Used for serialization identification
        (e.g., "__container__" vs "__children__")
    """
```

**Implementation**:
```python
def set_body_name(self, name: str) -> "Schema":
    self._body.set_idlayer(name)
    return self
```

### Access Methods

#### \_\_getitem\_\_()

**Signature**:
```python
def __getitem__(self, index: Union[int, str]) -> Union[Layer, Callable[..., Any]]:
    """
    Access layers by index/key.
    
    Args:
        index: Layer identifier
        
    Returns:
        Layer: The layer with given identifier
        
    Raises:
        KeyError: If layer doesn't exist
    """
```

**Usage**:
```python
schema.add_layer("header")
schema.add_layer(1)

header_layer = schema["header"]
first_layer = schema[1]
```

#### \_\_call\_\_()

**Signature**:
```python
def __call__(self, key: Optional[str] = None) -> Union[Layer, Callable[..., Any]]:
    """
    Call schema to render layers.
    
    Args:
        key (Optional[str]): Specific component key to render
                            If None, renders entire body
                            
    Returns:
        Result of layer/component rendering
        
    Behavior:
        - key=None: Calls main_body() → renders all layers
        - key=str: Calls main_body[key]() → renders specific component
    """
```

**Implementation**:
```python
def __call__(self, key=None):
    if key:
        return self.main_body[key].__call__()
    return self._body()
```

**Usage**:
```python
# Render all
schema()

# Render specific component
schema("button_key")
```

### Utility Methods

#### \_\_len\_\_()

**Signature**:
```python
def __len__(self) -> int:
    """
    Get number of layers (excluding main body).
    
    Returns:
        int: Count of layers in _schema dictionary
    """
```

#### \_\_repr\_\_() and \_\_str\_\_()

**Signature**:
```python
def __repr__(self) -> str:
    """String representation of schema structure."""
    return f"Schema: {self._schema}\nBody: {self._body}"

def __str__(self) -> str:
    """Alias for __repr__."""
    return self.__repr__()
```

### Serialization

#### serialize()

**Signature**:
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize schema to dictionary.
    
    Returns:
        dict: Main body layer's serialization
        
    Format:
        {
            "<body_name>": [
                {component1 serialization},
                {component2 serialization},
                ...
            ]
        }
    """
```

**Implementation**:
```python
def serialize(self) -> Dict[str, Any]:
    return self.main_body.serialize()
```

**Example Output**:
```python
{
    "__body__": [
        {
            "__base__": {...},
            "__parser__": {...},
            "__engine__": "StreamlitComponentParser"
        },
        {
            "__base__": {...},
            "__parser__": {...},
            "__engine__": "StreamlitComponentParser"
        }
    ]
}
```

#### ast_serialize()

**Signature**:
```python
def ast_serialize(self) -> Dict[str, Any]:
    """
    Serialize to AST format.
    
    Returns:
        dict: AST-compatible serialization
    """
```

#### deserialize()

**Signature**:
```python
@classmethod
def deserialize(
    cls,
    data: List[dict[str, Any]],
    componentmap: dict[str, Any],
    component_parser: type = None,
    layout_parser: type = None,
    strict: bool = False,
) -> "Schema":
    """
    Deserialize schema from data.
    
    Args:
        data: Serialized schema data
        componentmap: Map of component names to callables
        component_parser: Parser class for components
        layout_parser: Parser class for layouts
        strict: Strict validation mode
        
    Returns:
        Schema: Reconstructed schema instance
        
    Process:
        1. Extract schema name from data
        2. Deserialize main body layer
        3. Create Schema with deserialized layer
        4. Return configured instance
    """
```

**Implementation**:
```python
@classmethod
def deserialize(cls, data, componentmap, component_parser=None, 
                layout_parser=None, strict=False):
    # Get schema name (first key or "__body__")
    schema = list(data.keys())[0] if data else "__body__"
    
    # Deserialize layer
    layer = Layer.deserialize(
        schema,
        data[schema],
        componentmap,
        component_parser,
        layout_parser,
        strict
    )
    
    # Create schema instance
    schema_instance = cls(schema)
    schema_instance._body = layer
    schema_instance._schema = {schema: layer}
    
    return schema_instance
```

---

## Layer

**Location**: `core/handlers/layer.py`

### Purpose

`Layer` is the component container that holds and organizes a collection of components. It provides ordering, indexing, rendering, and serialization capabilities.

### Class Definition

```python
class Layer:
    """
    Component organization layer.
    
    Provides:
    - Component storage and ordering
    - Key-based and index-based access
    - Batch rendering
    - Serialization support
    """
```

### Constructor

```python
def __init__(
    self,
    _id: Union[int, str],
    elements: Sequence[Callable[..., Any]] = None,
    order: Sequence[Union[int, str]] = None,
):
    """
    Initialize layer.
    
    Args:
        _id: Layer identifier (name or index)
        elements: Initial components (default: [])
        order: Rendering order for elements (default: [])
               Can reference by index or key
               
    Attributes:
        _id (Union[int, str]): Layer identifier
        elements (List[Callable]): Component list
        _order (List[Union[int, str]]): Rendering order
    """
```

**Initialization**:
```python
self._id = _id or uuid4().hex  # Auto-generate if None
self.elements = elements or []
self._order = order or []
```

### Properties

#### idlayer

**Signature**:
```python
@property
def idlayer(self) -> Union[int, str]:
    """
    Get layer identifier.
    
    Returns:
        Union[int, str]: Layer ID
    """
```

#### order

**Signature**:
```python
@property
def order(self) -> Sequence[Union[int, str]]:
    """
    Get rendering order.
    
    Returns:
        Sequence: List of indices/keys defining render order
    """
```

### Configuration

#### set_idlayer()

**Signature**:
```python
def set_idlayer(self, idlayer: Union[int, str]) -> "Layer":
    """
    Change layer identifier.
    
    Args:
        idlayer: New identifier
        
    Returns:
        self: For method chaining
    """
```

#### set_order()

**Signature**:
```python
def set_order(self, order: Sequence[Union[int, str]]) -> "Layer":
    """
    Set rendering order.
    
    Args:
        order: Sequence of indices/keys
        
    Returns:
        self: For method chaining
        
    Purpose:
        Control the order components render,
        independent of addition order
    """
```

**Example**:
```python
layer = Layer("header")
layer.add_component(title)    # Index 0
layer.add_component(subtitle) # Index 1
layer.add_component(logo)     # Index 2

# Render logo first, then title, then subtitle
layer.set_order([2, 0, 1])
```

### Component Management

#### add_component()

**Signature**:
```python
def add_component(self, component: Callable[..., Any]) -> Callable[..., Any]:
    """
    Add component to layer.
    
    Args:
        component: Callable component
        
    Returns:
        Callable: The added component (last element)
        
    Behavior:
        Appends to elements list
    """
```

**Implementation**:
```python
def add_component(self, component):
    self.elements.append(component)
    return self.elements[-1]
```

### Access Methods

#### \_\_getitem\_\_()

**Signature**:
```python
def __getitem__(self, index: Union[int, str]) -> Union[Callable[..., Any], "Layer"]:
    """
    Access components by index or key.
    
    Args:
        index: Integer index or string key
        
    Returns:
        Component at index or with matching key
        
    Behavior:
        - int: Direct indexing into elements list
        - str: Search for component with matching "key" in kwargs
        
    Raises:
        IndexError: If integer index out of range
        KeyError: If string key not found
    """
```

**Implementation**:
```python
def __getitem__(self, index):
    if isinstance(index, str):
        # Search by key
        for el in self.elements:
            if "key" in el.kwargs and el.kwargs["key"] == index:
                return el
        raise KeyError(f"Component with key '{index}' not found")
    # Index access
    return self.elements[index]
```

**Usage**:
```python
# By index
first = layer[0]
last = layer[-1]

# By key
button = layer["my_button"]  # Component with key="my_button"
```

#### \_\_setitem\_\_()

**Signature**:
```python
def __setitem__(self, key: Union[int, str], value: Callable[..., Any]) -> "Layer":
    """
    Set component at index.
    
    Args:
        key: Index
        value: New component
        
    Returns:
        self: For method chaining
    """
```

### Iteration

#### \_\_iter\_\_()

**Signature**:
```python
def __iter__(self):
    """
    Iterate over elements.
    
    Yields:
        Components in order
    """
```

**Usage**:
```python
for component in layer:
    print(component)
```

#### \_\_len\_\_()

**Signature**:
```python
def __len__(self) -> int:
    """
    Get component count.
    
    Returns:
        int: Number of components in layer
    """
```

### Rendering

#### \_\_call\_\_()

**Signature**:
```python
def __call__(self, key: Optional[str] = None) -> Union[Callable[..., Any], List[Callable[..., Any]]]:
    """
    Render layer components.
    
    Args:
        key (Optional[str]): Specific component key to render
                            If None, renders all components
                            
    Returns:
        Single component result or list of results
        
    Behavior:
        - key=None: Calls __call_all() → renders all
        - key=str: Renders specific component by key
    """
```

**Implementation**:
```python
def __call__(self, key=None):
    if key:
        # Render specific component
        return self.__getitem__(key).parse().__call__()
    # Render all
    return self.__call_all()
```

#### \_\_call_all()

**Signature**:
```python
def __call_all(self) -> List[Callable[..., Any]]:
    """
    Render all components in order.
    
    Returns:
        List: Render results
        
    Behavior:
        1. Uses self.order if set, else renders in list order
        2. For each element:
           a. If has parse() method → call parse().call()
           b. Else → call directly
        3. Collect results
    """
```

**Implementation**:
```python
def __call_all(self) -> List[Callable[..., Any]]:
    res = []
    # Determine order
    elements_to_render = (
        [self[i] if isinstance(i, int) else i for i in self.order]
        if self.order
        else self.elements
    )
    
    for element in elements_to_render:
        if hasattr(element, "parse"):
            # Parser object
            parsed = element.parse()
            res.append(parsed())
        else:
            # Direct callable
            res.append(element())
    
    return res
```

### Utility Methods

#### \_\_repr\_\_() and \_\_str\_\_()

**Signature**:
```python
def __repr__(self) -> str:
    """String representation."""
    return f"Layer: {self.idlayer}"

def __str__(self) -> str:
    """Alias for __repr__."""
    return self.__repr__()
```

### Serialization

#### serialize()

**Signature**:
```python
def serialize(self) -> dict[str, Any]:
    """
    Serialize layer to dictionary.
    
    Returns:
        dict: {
            <layer_id>: [
                {component1 serialization},
                {component2 serialization},
                ...
            ]
        }
        
    Behavior:
        Only serializes components with serialize() method
    """
```

**Implementation**:
```python
def serialize(self) -> dict[str, Any]:
    data = []
    for el in self.elements:
        if hasattr(el, "serialize"):
            data.append(el.serialize())
    return {self.idlayer: data}
```

#### ast_serialize()

**Signature**:
```python
def ast_serialize(self) -> dict[str, Any]:
    """
    Serialize to AST format.
    
    Returns:
        dict: AST-compatible data
    """
```

#### deserialize()

**Signature**:
```python
@classmethod
def deserialize(
    cls,
    layerid: str,
    data: List[dict[str, Any]],
    componentmap: dict[str, Any],
    component_parser: type = None,
    layout_parser: type = None,
    strict: bool = False,
) -> "Layer":
    """
    Deserialize layer from data.
    
    Args:
        layerid: Layer identifier
        data: List of serialized components
        componentmap: Component name to callable map
        component_parser: Parser class for components
        layout_parser: Parser class for layouts
        strict: Strict validation mode
        
    Returns:
        Layer: Reconstructed layer
        
    Behavior:
        1. Create empty layer with layerid
        2. For each serialized component:
           a. Check __type__ field
           b. Route to appropriate parser deserialize()
           c. Add to layer
        3. Return populated layer
        
    Error Handling:
        - strict=True: Raise ValueError on unknown types
        - strict=False: Log warning and skip
    """
```

**Implementation Logic**:
```python
@classmethod
def deserialize(cls, layerid, data, componentmap, 
                component_parser=None, layout_parser=None, strict=False):
    layer = cls(layerid)
    
    if not data:
        logger.warning(f"Layer {layerid} is empty.")
        return layer

    for el in data:
        if not isinstance(el, dict):
            if strict:
                raise ValueError(f"Expected dict, got {type(el)}")
            logger.warning(f"Skipping non-dict element")
            continue
            
        if "__type__" not in el:
            if strict:
                raise ValueError("Missing '__type__' key")
            logger.warning("Skipping element without '__type__'")
            continue
        
        # Route based on type
        if el["__type__"] == "StreamlitComponentParser":
            component = component_parser.deserialize(el, componentmap, strict)
            layer.add_component(component)
        elif el["__type__"] == "StreamlitLayoutParser":
            layout = layout_parser.deserialize(el, componentmap)
            layer.add_component(layout)
        else:
            if strict:
                raise ValueError(f"Unknown type: {el['__type__']}")
            logger.warning(f"Skipping unknown type: {el['__type__']}")
    
    return layer
```

---

## Usage Examples

### Example 1: Basic Schema Usage

```python
from declarative_streamlit.core.handlers import Schema

# Create schema
schema = Schema()

# Add to main body
schema.add_component(parser1)
schema.add_component(parser2)

# Render all
schema()
```

### Example 2: Multi-Layer Schema

```python
schema = Schema()

# Add layers
header = schema.add_layer("header")
content = schema.add_layer("content")
footer = schema.add_layer("footer")

# Access layers
schema.header.add_component(title_parser)
schema.content.add_component(body_parser)
schema.footer.add_component(copyright_parser)

# Also accessible via indexing
schema["header"].add_component(logo_parser)
```

### Example 3: Layer with Ordering

```python
layer = Layer("dashboard")

# Add components
layer.add_component(metric1)  # 0
layer.add_component(metric2)  # 1
layer.add_component(metric3)  # 2

# Set custom render order
layer.set_order([2, 0, 1])  # Renders: metric3, metric1, metric2

# Render
layer()
```

### Example 4: Key-Based Access

```python
layer = Layer("controls")

# Add with keys
btn1 = StreamlitComponentParser(st.button, "Submit", key="submit")
btn2 = StreamlitComponentParser(st.button, "Cancel", key="cancel")

layer.add_component(btn1)
layer.add_component(btn2)

# Access by key
submit_btn = layer["submit"]
cancel_btn = layer["cancel"]

# Render specific component
layer("submit")  # Only renders submit button
```

### Example 5: Nested Schema Structure

```python
# Main schema
main = Schema()

# Add header layer
header = main.add_layer("header")
header.add_component(title_parser)

# Add content layer with sub-layers
content = main.add_layer("content")
content_schema = Schema("content_body")
content_schema.add_component(text_parser)
content_schema.add_component(image_parser)

# Add as component
content.add_component(content_schema)

# Render entire structure
main()
```

### Example 6: Serialization Round-Trip

```python
# Create and populate
schema = Schema()
schema.add_component(parser1)
schema.add_component(parser2)

# Serialize
data = schema.serialize()

# Deserialize
from declarative_streamlit.core.build import (
    StreamlitComponentParser,
    StreamlitLayoutParser
)

restored = Schema.deserialize(
    data,
    componentmap={"button": st.button, "text": st.text},
    component_parser=StreamlitComponentParser,
    layout_parser=StreamlitLayoutParser
)

# Restored schema has same structure
restored()
```

### Example 7: Dynamic Layer Properties

```python
schema = Schema()

# Add layers - become properties
schema.add_layer("sidebar")
schema.add_layer("main")

# Access as properties
schema.sidebar.add_component(filter_parser)
schema.main.add_component(chart_parser)

# Or via indexing
schema["sidebar"].add_component(another_parser)
```

---

## Best Practices

### 1. Use Descriptive Layer Names

```python
# ❌ Bad
schema.add_layer(1)
schema.add_layer(2)

# ✅ Good
schema.add_layer("header")
schema.add_layer("content")
schema.add_layer("footer")
```

### 2. Set Order for Non-Sequential Rendering

```python
# When render order differs from addition order
layer.add_component(a)  # Add first
layer.add_component(b)  # Add second
layer.add_component(c)  # Add third

layer.set_order([2, 0, 1])  # Render: c, a, b
```

### 3. Use Keys for Important Components

```python
# Makes components accessible by name
parser = StreamlitComponentParser(st.button, "Submit", key="submit_btn")
layer.add_component(parser)

# Later access
submit = layer["submit_btn"]
```

### 4. Handle Empty Layers

```python
# Check before rendering
if len(layer) > 0:
    layer()
```

---

## Architecture Patterns

### Pattern 1: Header-Content-Footer

```python
schema = Schema()
schema.add_layer("header")
schema.add_layer("content")
schema.add_layer("footer")

# Populate
schema.header.add_component(title)
schema.content.add_component(main_content)
schema.footer.add_component(copyright)
```

### Pattern 2: Sidebar-Main

```python
schema = Schema()
schema.add_layer("sidebar")
schema.add_layer("main")

# Filters in sidebar
schema.sidebar.add_component(date_filter)
schema.sidebar.add_component(category_filter)

# Content in main
schema.main.add_component(dashboard)
```

### Pattern 3: Tab-Based Layout

```python
schema = Schema()
schema.add_layer("overview")
schema.add_layer("details")
schema.add_layer("settings")

# Each layer corresponds to a tab
```

---

## Performance Considerations

### Layer Lookup

Dictionary-based layer storage provides O(1) access:
```python
layer = schema["layer_id"]  # O(1)
```

### Component Iteration

Rendering all components is O(n):
```python
layer()  # Iterates through all elements
```

### Order Processing

Custom ordering adds minimal overhead:
```python
layer.set_order([2, 0, 1])  # O(1) assignment
layer()  # O(n) iteration with order lookup
```

---

## Common Pitfalls

### 1. Forgetting to Add Layers Before Use

```python
# ❌ Wrong
schema["header"].add_component(parser)  # KeyError

# ✅ Correct
schema.add_layer("header")
schema["header"].add_component(parser)
```

### 2. Accessing Non-Existent Keys

```python
# ❌ Wrong
component = layer["nonexistent"]  # KeyError

# ✅ Correct - check first
if "my_key" in [el.kwargs.get("key") for el in layer.elements]:
    component = layer["my_key"]
```

### 3. Modifying Order Without Validation

```python
# ❌ Risky
layer.set_order([5, 10, 15])  # Indices might not exist

# ✅ Better - validate indices
valid_order = [i for i in [5, 10, 15] if i < len(layer)]
layer.set_order(valid_order)
```

---

## Type Annotations

```python
from typing import Union, List, Dict, Any, Callable, Sequence, Optional

# Layer identifier
LayerID = Union[int, str]

# Component type
Component = Callable[..., Any]

# Layer collection
LayerDict = Dict[LayerID, Layer]

# Serialized data
SerializedSchema = Dict[str, Any]
SerializedLayer = Dict[str, List[Dict[str, Any]]]
```

---

## Revision History

| Version | Date       | Changes                    |
|---------|------------|----------------------------|
| 1.0.0   | 2025-12-14 | Initial documentation      |

---

## See Also

- [Base Classes Documentation](./base-classes.md)
- [Components Documentation](./components.md)
- [Parsers Documentation](./parsers.md)
- [Event System Documentation](./event-system.md)
- [API Reference](./api-reference.md)
