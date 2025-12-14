# Parsers Documentation

## Overview

The `build` submodule provides a sophisticated parser system that transforms declarative component definitions into executable, feature-rich components. The parser architecture acts as a bridge between raw Streamlit components and the enhanced component wrappers (IElement, VElement, Container).

## Module Structure

```
build/
├── __init__.py
├── base.py              # Abstract Parser base class
├── cstparser.py         # Component parser (StreamlitComponentParser)
├── lstparser.py         # Layout parser (StreamlitLayoutParser)
└── models/              # Pydantic validation models
    ├── base.py
    └── __pycache__/
```

---

## Parser (Abstract Base)

**Location**: `core/build/base.py`

### Purpose

`Parser` is the abstract base class that defines the contract for all parsers in the system. It establishes configuration patterns, validation strategies, and method chaining capabilities.

### Class Definition

```python
class Parser(ABC):
    """
    Abstract base class for parsers.
    
    Defines the interface for transforming raw components into
    enhanced, feature-rich component wrappers.
    """
```

### Inheritance Hierarchy

```
ABC (Python stdlib)
    └── Parser
        ├── StreamlitComponentParser
        └── StreamlitLayoutParser
```

### Constructor

```python
def __init__(
    self,
    component: Callable[..., Any],
    *args: Any,
    **kwargs: Any
) -> None:
    """
    Initialize parser with component and arguments.
    
    Args:
        component: The callable to wrap (st.button, st.text, etc.)
        *args: Positional arguments for the component
        **kwargs: Keyword arguments for the component
        
    Attributes:
        component (Callable): The wrapped callable
        args (List[Any]): Positional arguments
        kwargs (Dict[str, Any]): Keyword arguments
        _stateful (bool): Whether to create stateful components
        _fatal (bool): Error handling strategy
        _strict (bool): Strict validation mode
        autoconfig (bool): Auto-apply configuration on parse
        _effects (List[Callable]): Post-render effects
        _errhandler (Optional[Callable]): Error handler function
        
    Validation:
        Uses ParserConfig Pydantic model
    """
```

**Initialization Process**:
```python
# Validate inputs
config = ParserConfig(
    component=component,
    args=list(args),
    kwargs=kwargs,
)

# Set validated attributes
self.component = config.component
self.args = config.args
self.kwargs = config.kwargs
self._stateful = config.stateful
self._fatal = config.fatal
self._strict = config.strict
self.autoconfig = config.autoconfig
self._effects: List[Callable[..., Any]] = []
self._errhandler: Optional[Callable[..., Any]] = None
```

### Abstract Methods

#### parse()

**Signature**:
```python
@abstractmethod
def parse(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
    """
    Parse and transform the component.
    
    This method MUST be implemented by subclasses.
    
    Args:
        *args: Override arguments
        **kwargs: Override keyword arguments
        
    Returns:
        Callable: Enhanced component (IElement, VElement, or Container)
        
    Raises:
        NotImplementedError: If not implemented
    """
```

### Configuration Property

#### parserconfig

**Signature**:
```python
@property
def parserconfig(self) -> ParserConfig:
    """
    Get current parser configuration.
    
    Returns:
        ParserConfig: Pydantic model with current settings
    """
```

**Returns**:
```python
ParserConfig(
    component=self.component,
    args=self.args,
    kwargs=self.kwargs,
    stateful=self._stateful,
    fatal=self._fatal,
    strict=self._strict,
    autoconfig=self.autoconfig,
    errhandler=self._errhandler,
    effects=self._effects,
)
```

### Configuration Methods

All methods support method chaining (return `self`).

#### set_stateful()

**Signature**:
```python
def set_stateful(self, stateful: bool) -> T:
    """
    Configure state tracking behavior.
    
    Args:
        stateful (bool): True for IElement, False for VElement
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If not a boolean
    """
```

**Usage**:
```python
# Create stateful component (button, input)
parser.set_stateful(True)

# Create stateless component (text, image)
parser.set_stateful(False)
```

#### set_fatal()

**Signature**:
```python
def set_fatal(self, fatal: bool) -> T:
    """
    Configure error handling strategy.
    
    Args:
        fatal (bool): True to raise exceptions, False for graceful handling
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If not a boolean
    """
```

#### set_strict()

**Signature**:
```python
def set_strict(self, strict: bool) -> T:
    """
    Configure strict validation mode.
    
    Args:
        strict (bool): True to enforce key requirement for stateful components
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If not a boolean
    """
```

#### set_autoconfig()

**Signature**:
```python
def set_autoconfig(self, autoconfig: bool) -> T:
    """
    Configure automatic config application.
    
    Args:
        autoconfig (bool): If True, parse() uses parser's config
                          If False, parse() accepts runtime config
                          
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If not a boolean
    """
```

**Autoconfig Behavior**:
```python
# With autoconfig=True
parser.set_stateful(True).set_fatal(False)
element = parser.parse()  # Uses stateful=True, fatal=False

# With autoconfig=False
parser.set_stateful(True)
element = parser.parse(stateful=False)  # Overrides to stateful=False
```

#### set_errhandler()

**Signature**:
```python
def set_errhandler(self, errhandler: Callable[..., Any]) -> T:
    """
    Set error handler for parsed components.
    
    Args:
        errhandler: Error handler function
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If not callable
    """
```

#### add_effect()

**Signature**:
```python
def add_effect(self, effect: Callable[..., Any]) -> T:
    """
    Add post-render effect.
    
    Args:
        effect: Effect function
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If not callable
    """
```

#### add_effects()

**Signature**:
```python
def add_effects(self, effects: List[Callable[..., Any]]) -> T:
    """
    Add multiple effects.
    
    Args:
        effects: List of effect functions
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If any effect is not callable
    """
```

### Magic Method

#### \_\_call\_\_()

**Signature**:
```python
def __call__(self, *args: Any, **kwargs: Any) -> Any:
    """
    Make parser callable - parse and execute.
    
    Args:
        *args: Override arguments
        **kwargs: Override keyword arguments
        
    Returns:
        Any: Result of parsed component execution
        
    Behavior:
        1. Parse component (with override args if provided)
        2. Call parsed component
        3. Return result
    """
```

**Usage**:
```python
# Parse and execute in one step
result = parser()

# Parse with overrides and execute
result = parser("new arg", key="new_key")
```

---

## StreamlitComponentParser

**Location**: `core/build/cstparser.py`

### Purpose

`StreamlitComponentParser` wraps individual Streamlit components (buttons, inputs, text, images, etc.) and transforms them into enhanced IElement or VElement instances based on configuration.

### Class Definition

```python
class StreamlitComponentParser(Parser):
    """
    Parser for individual Streamlit components.
    
    Transforms raw Streamlit functions into feature-rich
    IElement (stateful) or VElement (stateless) wrappers.
    """
```

### Constructor

```python
def __init__(self, component: Callable[..., Any], *args, **kwargs):
    """
    Initialize component parser.
    
    Args:
        component: Streamlit component function
        *args: Positional arguments for component
        **kwargs: Keyword arguments for component
        
    Inherits:
        All attributes from Parser base class
    """
```

**Example**:
```python
# Parse a button
btn_parser = StreamlitComponentParser(
    st.button,
    "Click me",
    key="my_button"
)

# Parse text
txt_parser = StreamlitComponentParser(
    st.text,
    "Hello, World!"
)
```

### Parsing

#### parse()

**Signature**:
```python
def parse(
    self,
    stateful: bool = False,
    fatal: bool = True,
    errhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
    strict: bool = True,
) -> Union[IElement, VElement]:
    """
    Parse component into IElement or VElement.
    
    Args:
        stateful: Create IElement if True, VElement if False
        fatal: Error handling strategy
        errhandler: Custom error handler
        strict: Strict validation mode
        
    Returns:
        IElement: If stateful=True
        VElement: If stateful=False
        
    Notes:
        - If autoconfig=True, uses parser's config
        - If autoconfig=False, uses provided arguments
    """
```

**Implementation Logic**:
```python
def parse(self, stateful=False, fatal=True, errhandler=None, strict=True):
    # Check autoconfig
    if self.parserconfig.autoconfig:
        stateful = self.parserconfig.stateful
        fatal = self.parserconfig.fatal
        errhandler = self.parserconfig.errhandler
        strict = self.parserconfig.strict

    # Create appropriate component type
    if stateful:
        comp = IElement(*self.args, **self.kwargs)
        comp._set_base_component(self.component)
        comp.set_errhandler(errhandler)
        comp.set_fatal(fatal)
        comp.set_strict(strict)
    else:
        comp = VElement(*self.args, **self.kwargs)
        comp._set_base_component(self.component)
        comp.set_errhandler(errhandler)
        comp.set_fatal(fatal)

    # Add effects
    comp.add_effects(self._effects)

    return comp
```

**Decision Tree**:
```
stateful? 
├─ Yes → Create IElement
│         └─ Set: base_component, errhandler, fatal, strict
│         └─ Add: effects
│         └─ Return: IElement
│
└─ No  → Create VElement
          └─ Set: base_component, errhandler, fatal
          └─ Add: effects
          └─ Return: VElement
```

### Serialization

#### serialize()

**Signature**:
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize parser to dictionary.
    
    Returns:
        dict: {
            "__base__": dict (parsed component serialization),
            "__parser__": {
                "stateful": bool,
                "fatal": bool,
                "strict": bool,
                "autoconfig": bool
            },
            "__engine__": "StreamlitComponentParser"
        }
    """
```

**Example Output**:
```python
{
    "__base__": {
        "__component__": "button",
        "__args__": {
            "args": [],
            "kwargs": {"label": "Click", "key": "btn"}
        },
        "__type__": "IElement"
    },
    "__parser__": {
        "stateful": True,
        "fatal": True,
        "strict": True,
        "autoconfig": True
    },
    "__engine__": "StreamlitComponentParser"
}
```

#### ast_serialize()

**Signature**:
```python
def ast_serialize(self) -> Dict[str, Any]:
    """
    Serialize to AST-compatible format.
    
    Returns:
        dict: {
            "base_component": str,
            "args": List[Any],
            "kwargs": Dict[str, Any],
            "parserconfig": dict,
            "unique_id": str (8-char UUID)
        }
    """
```

**Purpose**: Used for abstract syntax tree representations and code generation.

#### deserialize()

**Signature**:
```python
@classmethod
def deserialize(
    cls,
    data: Dict[str, Any],
    componentmap: Union[Dict[str, Any], BaseStandard],
    strict: bool = False
) -> "StreamlitComponentParser":
    """
    Deserialize from dictionary.
    
    Args:
        data: Serialized parser data
        componentmap: Map of component names to callables OR
                     BaseStandard instance with get_similar() method
        strict: If True, raise errors for missing components
        
    Returns:
        StreamlitComponentParser: Reconstructed instance
        
    Raises:
        ValueError: If component not found (strict=True)
    """
```

**Component Resolution**:
```python
# Two resolution strategies:

# 1. Using BaseStandard (fuzzy matching)
if hasattr(componentmap, "get_similar"):
    component = componentmap.get_similar("button")

# 2. Using dictionary (exact match)
else:
    component = componentmap.get("button")
```

### String Representation

```python
def __str__(self) -> str:
    """String format: StreamlitComponentParser(<component>): <config>"""
    return f"StreamlitComponentParser({self.component.__name__}): {self.parserconfig}"
```

---

## StreamlitLayoutParser

**Location**: `core/build/lstparser.py`

### Purpose

`StreamlitLayoutParser` handles container components (columns, tabs, expanders, etc.) and manages hierarchical layouts with multiple layers of nested components.

### Class Definition

```python
class StreamlitLayoutParser(Parser):
    """
    Parser for layout/container components.
    
    Manages complex hierarchical layouts with:
    - Multiple layers
    - Nested containers
    - Component organization
    - Schema-based structure
    """
```

### Constructor

```python
def __init__(self, container: Callable[..., Any], *args, **kwargs):
    """
    Initialize layout parser.
    
    Args:
        container: Container component (st.columns, st.container, etc.)
        *args: Positional arguments for container
        **kwargs: Keyword arguments for container
        
    Attributes:
        _colum_based (bool): Column rendering flag (default: False)
        schema (Schema): Layout organization with "__children__" body
    """
```

**Initialization**:
```python
super().__init__(container, *args, **kwargs)
self._colum_based = False
self.schema = Schema("__children__")
```

### Properties

#### body

**Signature**:
```python
@property
def body(self) -> Layer:
    """
    Get the main body layer.
    
    Returns:
        Layer: The schema's main body layer
    """
```

### Component Management

#### add_component()

**Signature**:
```python
def add_component(
    self,
    component: Callable[..., Any],
    *args,
    **kwargs
) -> StreamlitComponentParser:
    """
    Add a component to the layout.
    
    Args:
        component: Streamlit component function
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        StreamlitComponentParser: Parser wrapper for the component
        
    Behavior:
        - Automatically wraps in StreamlitComponentParser
        - Adds to main schema body
    """
```

**Implementation**:
```python
def add_component(self, component, *args, **kwargs):
    return self.schema.add_component(
        StreamlitComponentParser(component, *args, **kwargs)
    )
```

#### add_function()

**Signature**:
```python
def add_function(
    self,
    function: Callable[..., Any],
    *args,
    **kwargs
) -> StreamlitComponentParser:
    """
    Add a custom function to the layout.
    
    Args:
        function: Any callable
        *args: Arguments to partially apply
        **kwargs: Keyword arguments to partially apply
        
    Returns:
        StreamlitComponentParser: Parser wrapper
        
    Behavior:
        Uses functools.partial for argument binding
    """
```

**Implementation**:
```python
def add_function(self, function, *args, **kwargs):
    return self.schema.add_component(
        partial(function, *args, **kwargs)
    )
```

### Container Management

#### add_container()

**Signature**:
```python
def add_container(
    self,
    container: Callable[..., Any],
    *args,
    **kwargs
) -> "StreamlitLayoutParser":
    """
    Add a nested container.
    
    Args:
        container: Container component
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        StreamlitLayoutParser: Parser for the nested container
        
    Behavior:
        Creates nested layout structure
    """
```

#### add_fragment()

**Signature**:
```python
def add_fragment(
    self,
    fragment: Callable[..., Any]
) -> "StreamlitLayoutParser":
    """
    Add a fragment (self-contained component group).
    
    Args:
        fragment: Fragment component
        
    Returns:
        StreamlitLayoutParser: Parser wrapper
    """
```

### Layer Management

#### add_layer()

**Signature**:
```python
def add_layer(self, idlayer: Union[int, str] = None) -> Layer:
    """
    Add a layer to the layout.
    
    Args:
        idlayer: Layer identifier (auto-generated if None)
        
    Returns:
        Layer: The created layer
    """
```

#### add_component_to_layer()

**Signature**:
```python
def add_component_to_layer(
    self,
    idlayer: Union[int, str],
    component: Callable[..., Any],
    *args,
    **kwargs
) -> StreamlitComponentParser:
    """
    Add component to specific layer.
    
    Args:
        idlayer: Layer identifier
        component: Component function
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        StreamlitComponentParser: Parser wrapper
        
    Raises:
        KeyError: If layer doesn't exist
    """
```

#### add_container_to_layer()

**Signature**:
```python
def add_container_to_layer(
    self,
    idlayer: Union[int, str],
    container: Callable[..., Any],
    *args,
    **kwargs
) -> "StreamlitLayoutParser":
    """
    Add container to specific layer.
    
    Args:
        idlayer: Layer identifier
        container: Container component
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        StreamlitLayoutParser: Parser for nested container
    """
```

### Configuration

#### set_column_based()

**Signature**:
```python
def set_column_based(self, column_based: bool) -> "StreamlitLayoutParser":
    """
    Configure rendering strategy.
    
    Args:
        column_based (bool): True for column-based, False for row-based
        
    Returns:
        self: For method chaining
        
    Raises:
        ValueError: If not a boolean
    """
```

**Critical for**:
- `st.columns()`
- `st.tabs()`
- Any container where each layer needs its own space

### Parsing

#### parse()

**Signature**:
```python
def parse(
    self,
    fatal: bool = True,
    errhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
    column_based: bool = False,
) -> Container:
    """
    Parse into Container instance.
    
    Args:
        fatal: Error handling strategy
        errhandler: Custom error handler
        column_based: Rendering strategy
        
    Returns:
        Container: Configured container instance
        
    Behavior:
        - Creates Container instance
        - Transfers schema
        - Applies configuration
        - Sets StreamlitComponentParser as component parser
    """
```

**Implementation**:
```python
def parse(self, fatal=True, errhandler=None, column_based=False):
    comp = Container(*self.args, **self.kwargs)
    
    # Check autoconfig
    if self.parserconfig.autoconfig:
        fatal = self.parserconfig.fatal
        errhandler = self.parserconfig.errhandler
        column_based = self._colum_based

    # Configure container
    comp._set_base_component(self.component)
    comp.set_errhandler(errhandler)
    comp.set_fatal(fatal)
    comp.set_column_based(column_based)
    comp.set_component_parser(StreamlitComponentParser)
    
    # Transfer schema
    comp.schema = self.schema

    return comp
```

### Context Manager

#### \_\_enter\_\_() and \_\_exit\_\_()

**Signatures**:
```python
def __enter__(self) -> "StreamlitLayoutParser":
    """Enter context - returns self for adding components."""
    return self

def __exit__(self, exc_type, exc_value, traceback) -> None:
    """Exit context - propagates exceptions."""
    pass
```

**Usage**:
```python
with StreamlitLayoutParser(st.container) as layout:
    layout.add_component(st.text, "Hello")
    layout.add_component(st.button, "Click", key="btn")
```

### Indexing

#### \_\_getitem\_\_()

**Signature**:
```python
def __getitem__(
    self,
    index: Union[int, str]
) -> Union[Layer, StreamlitComponentParser]:
    """
    Access layers by index.
    
    Args:
        index: Layer identifier
        
    Returns:
        Layer or StreamlitComponentParser
    """
```

**Usage**:
```python
# Access layer
layer = parser["header"]

# Access component by index
component = parser[0]
```

### Serialization

#### serialize()

**Signature**:
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize layout parser.
    
    Returns:
        dict: {
            "__base__": dict (container serialization),
            "__schema__": dict (schema serialization),
            "__parser__": {
                "stateful": bool,
                "fatal": bool,
                "strict": bool,
                "column_based": bool
            },
            "__engine__": "StreamlitLayoutParser"
        }
    """
```

#### ast_serialize()

**Signature**:
```python
def ast_serialize(self) -> Dict[str, Any]:
    """
    Serialize to AST format.
    
    Returns:
        dict: {
            "component": str,
            "args": List[Any],
            "kwargs": Dict[str, Any],
            "parserconfig": dict,
            "schema": List[dict] (AST-serialized schema)
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
    componentmap: Union[Dict[str, Any], BaseStandard],
    strict: bool = False,
) -> "StreamlitLayoutParser":
    """
    Deserialize layout parser.
    
    Args:
        data: Serialized data
        componentmap: Component map
        strict: Strict validation mode
        
    Returns:
        StreamlitLayoutParser: Reconstructed instance
        
    Notes:
        Recursively deserializes schema with nested components
    """
```

---

## Usage Examples

### Example 1: Basic Component Parsing

```python
from declarative_streamlit.core.build import StreamlitComponentParser
import streamlit as st

# Create parser
parser = StreamlitComponentParser(
    st.button,
    "Click me!",
    key="my_button"
)

# Configure
parser.set_stateful(True).set_fatal(False)

# Parse to IElement
button = parser.parse()

# Render
button()
```

### Example 2: Parser with Effects

```python
parser = StreamlitComponentParser(st.selectbox, "Choose", ["A", "B", "C"])

# Add effects before parsing
parser.add_effect(lambda val: st.write(f"Selected: {val}"))
parser.add_effect(lambda val: analytics.track("selection", val))

# Parse with autoconfig
parser.set_autoconfig(True).set_stateful(True)
select = parser.parse()

# Render with effects
select()
```

### Example 3: Layout Parser - Simple Container

```python
from declarative_streamlit.core.build import StreamlitLayoutParser
import streamlit as st

# Create layout parser
layout = StreamlitLayoutParser(st.container, border=True)

# Add components
layout.add_component(st.title, "My App")
layout.add_component(st.write, "Welcome!")
layout.add_component(st.button, "Start", key="start")

# Parse to Container
container = layout.parse()

# Render
container.render()
```

### Example 4: Layout Parser - Columns

```python
# Create columns layout
cols = StreamlitLayoutParser(st.columns)
cols.set_column_based(True)  # Important!

# Add layers (one per column)
cols.add_layer(0)
cols.add_layer(1)
cols.add_layer(2)

# Add to each layer
cols.add_component_to_layer(0, st.metric, "Users", 1234)
cols.add_component_to_layer(1, st.metric, "Sales", 5678)
cols.add_component_to_layer(2, st.metric, "Orders", 910)

# Parse and render
container = cols.parse()
container.lrender(st.columns, 3)
```

### Example 5: Nested Layouts

```python
# Main layout
main = StreamlitLayoutParser(st.container)

# Add header
main.add_component(st.title, "Dashboard")

# Create nested columns
cols = StreamlitLayoutParser(st.columns)
cols.set_column_based(True)
cols.add_layer("left")
cols.add_layer("right")
cols.add_component_to_layer("left", st.write, "Left panel")
cols.add_component_to_layer("right", st.write, "Right panel")

# Add columns to main
main.add_container(st.columns)

# Parse both
main_container = main.parse()
cols_container = cols.parse()

# Render
main_container.render()
cols_container.lrender(st.columns, 2)
```

### Example 6: Context Manager Usage

```python
with StreamlitLayoutParser(st.container) as layout:
    layout.add_component(st.header, "Section 1")
    layout.add_component(st.write, "Content here")
    
    # Nested container
    with StreamlitLayoutParser(st.expander, "Details") as expander:
        expander.add_component(st.write, "Hidden content")

# Parse after context
container = layout.parse()
container.render()
```

### Example 7: Configuration Patterns

```python
# Pattern 1: Autoconfig (parser config applied)
parser = (
    StreamlitComponentParser(st.button, "Click")
    .set_stateful(True)
    .set_fatal(False)
    .set_autoconfig(True)
)
element = parser.parse()  # Uses parser config

# Pattern 2: Runtime config (override at parse time)
parser = StreamlitComponentParser(st.button, "Click")
parser.set_autoconfig(False)
element = parser.parse(stateful=True, fatal=False)  # Runtime config
```

### Example 8: Serialization Round-Trip

```python
# Create and configure
parser = StreamlitComponentParser(st.button, "Click", key="btn")
parser.set_stateful(True).set_fatal(False)

# Serialize
data = parser.serialize()

# Deserialize
component_map = {"button": st.button}
restored = StreamlitComponentParser.deserialize(data, component_map)

# Restored parser has same config
element = restored.parse()
```

---

## Best Practices

### 1. Always Set Component Parser for Containers

```python
# ❌ Bad
container = Container()
container.add_component(st.button, "Click")  # Fails

# ✅ Good
container = Container()
container.set_component_parser(StreamlitComponentParser)
container.add_component(st.button, "Click")
```

### 2. Set column_based for Column Layouts

```python
# ❌ Bad
cols = StreamlitLayoutParser(st.columns)
cols.parse()  # Renders incorrectly

# ✅ Good
cols = StreamlitLayoutParser(st.columns)
cols.set_column_based(True)
cols.parse()
```

### 3. Use Autoconfig for Consistency

```python
# ✅ Good - consistent configuration
parser = (
    StreamlitComponentParser(st.button, "Click")
    .set_stateful(True)
    .set_fatal(False)
    .set_strict(True)
    .set_autoconfig(True)
)

# All parsed elements have same config
btn1 = parser.parse()
btn2 = parser.parse()
```

### 4. Add Effects Before Parsing

```python
# ✅ Good - effects included in parsed element
parser.add_effect(effect1).add_effect(effect2)
element = parser.parse()

# ❌ Less ideal - manual effect addition
element = parser.parse()
element.add_effect(effect1).add_effect(effect2)
```

### 5. Use Context Managers for Readability

```python
# ✅ Good - clear structure
with StreamlitLayoutParser(st.container) as layout:
    layout.add_component(st.title, "Header")
    layout.add_component(st.write, "Body")
```

---

## Performance Considerations

### Parser Overhead

Parsers add minimal overhead - configuration is O(1):
```python
parser = StreamlitComponentParser(st.button, "Click")  # Fast
element = parser.parse()  # Fast - just wrapping
```

### Schema Management

Layouts use dictionaries for O(1) layer access:
```python
layer = layout.schema[layer_id]  # O(1) lookup
```

### Lazy Parsing

Parsers don't execute components until parsed and called:
```python
parser = StreamlitComponentParser(st.button, "Click")  # No execution
element = parser.parse()  # Still no execution
element()  # Now executes
```

---

## Common Pitfalls

### 1. Forgetting Column-Based Flag

```python
# ❌ Wrong
cols = StreamlitLayoutParser(st.columns)
container = cols.parse()  # Missing column_based=True

# ✅ Correct
cols = StreamlitLayoutParser(st.columns)
cols.set_column_based(True)
container = cols.parse(column_based=True)
```

### 2. Not Setting Autoconfig

```python
# ❌ Confusing - config ignored
parser.set_stateful(True)
element = parser.parse()  # Uses default stateful=False

# ✅ Clear
parser.set_stateful(True).set_autoconfig(True)
element = parser.parse()  # Uses stateful=True
```

### 3. Adding Components Without Parser

```python
# ❌ Wrong
layout = StreamlitLayoutParser(st.container)
# Forgot to set up before adding
layout.add_component(st.button, "Click")

# ✅ Correct  
layout = StreamlitLayoutParser(st.container)
layout.add_component(st.button, "Click")  # Works - automatic wrapping
```

---

## Type Annotations

```python
from typing import Any, Callable, Dict, List, Union, Optional, NoReturn

# Parser types
Parser = Union[StreamlitComponentParser, StreamlitLayoutParser]

# Component types
Component = Callable[..., Any]

# Error handler
ErrorHandler = Callable[[Exception], Union[NoReturn, bool]]

# Component map for deserialization
ComponentMap = Union[Dict[str, Component], BaseStandard]
```

---

## Revision History

| Version | Date       | Changes                       |
|---------|------------|-------------------------------|
| 1.0.0   | 2025-12-14 | Initial documentation         |

---

## See Also

- [Base Classes Documentation](./base-classes.md)
- [Components Documentation](./components.md)
- [Handlers Documentation](./handlers.md)
- [API Reference](./api-reference.md)
