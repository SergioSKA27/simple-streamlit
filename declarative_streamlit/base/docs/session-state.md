# SessionState

## Overview

`SessionState` is a type-safe, feature-rich wrapper around Streamlit's session state that provides enhanced functionality for managing application state with optional strict type checking, functional programming patterns, and comprehensive error handling.

## Class Signature

```python
class SessionState:
    """A type-safe, feature-rich wrapper for Streamlit session state management."""
    
    __slots__ = ("key", "session_type", "strict", "_deserialize", "engine")
    
    def __init__(
        self,
        key: str,
        initial_value: Any = None,
        session_type: Optional[Type[T]] = None,
        strict: bool = True,
        deserialize: bool = False,
        engine: Union[Callable[[Any], Any], Literal['json']] = 'pickle',
    ) -> None
```

## Description

`SessionState` enhances Streamlit's built-in session state with:

- **Type Safety**: Optional strict type checking for stored values
- **Property Access**: Pythonic getter/setter properties
- **Functional Patterns**: Factory methods for functional programming
- **Validation**: Runtime type validation with clear error messages
- **Deserialization**: Support for custom value deserialization
- **Class Methods**: Utility methods for direct state access
- **Rich Debugging**: Comprehensive string representations

### Design Philosophy

The class wraps `st.session_state` to provide:
1. **Type Safety**: Prevent type-related bugs
2. **Better APIs**: Property-based access vs dictionary syntax
3. **Functional Support**: Getters/setters for callbacks
4. **Validation**: Early error detection
5. **Consistency**: Unified interface across application

## Constructor Parameters

### `key: str`
**Type**: `str`  
**Required**: Yes  
**Description**: Unique identifier for the session state entry.

**Validation**: Must be non-empty string.

**Example**:
```python
state = SessionState("user_name")
state2 = SessionState("counter")
```

**Raises**: `ValueError` if empty or not a string.

### `initial_value: Any = None`
**Type**: `Any`  
**Default**: `None`  
**Description**: Initial value for the session state entry.

Only set if the key doesn't exist in session state (preserves existing values across reruns).

**Example**:
```python
# Initialize with value
counter = SessionState("counter", initial_value=0)

# Initialize with complex value
user_data = SessionState("user", initial_value={"name": "Alice", "age": 30})
```

**Type Checking**: If `session_type` is provided and `strict=True`, initial value is type-checked.

### `session_type: Optional[Type[T]] = None`
**Type**: `Optional[Type[T]]`  
**Default**: `None`  
**Description**: Expected type for stored values.

When set, enables type checking:
- `None`: No type checking (any type allowed)
- `Type`: Values must be instances of this type

**Example**:
```python
# Type-safe integer counter
counter = SessionState("counter", initial_value=0, session_type=int)
counter.value = 5  # OK
counter.value = "text"  # TypeError if strict=True

# Type-safe list
items = SessionState("items", initial_value=[], session_type=list)

# Type-safe custom class
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

user_state = SessionState("user", initial_value=User("Alice", 30), session_type=User)
```

### `strict: bool = True`
**Type**: `bool`  
**Default**: `True`  
**Description**: Whether to enforce type checking on value assignment.

- `True`: Type violations raise `TypeError`
- `False`: Type mismatches allowed (silent)

**Example**:
```python
# Strict mode (default)
strict_counter = SessionState("strict", initial_value=0, session_type=int, strict=True)
strict_counter.value = "text"  # Raises TypeError

# Non-strict mode
lenient_counter = SessionState("lenient", initial_value=0, session_type=int, strict=False)
lenient_counter.value = "text"  # Allowed, no error
```

### `deserialize: bool = False`
**Type**: `bool`  
**Default**: `False`  
**Description**: Whether to deserialize the initial value using specified engine.

**Example**:
```python
import json

# Store JSON string, deserialize on init
json_data = '{"name": "Alice", "age": 30}'
state = SessionState(
    "user_data",
    initial_value=json_data,
    deserialize=True,
    engine='json'
)
# state.value is now dict, not string
```

### `engine: Union[Callable[[Any], Any], Literal['json']] = 'pickle'`
**Type**: `Union[Callable, Literal['json']]`  
**Default**: `'pickle'`  
**Description**: Deserialization engine to use when `deserialize=True`.

Options:
- `'json'`: Use `json.loads()` for deserialization
- `Callable`: Custom deserialization function

**Example**:
```python
# JSON deserialization
state = SessionState(
    "config",
    initial_value='{"setting": "value"}',
    deserialize=True,
    engine='json'
)

# Custom deserializer
def custom_deserializer(data: str) -> dict:
    # Custom logic
    return process_data(data)

state = SessionState(
    "data",
    initial_value=raw_data,
    deserialize=True,
    engine=custom_deserializer
)
```

## Attributes

### Public Attributes (Slots)

#### `key: str`
Session state key identifier.

#### `session_type: Optional[Type]`
Expected type for values (None allows any type).

#### `strict: bool`
Whether strict type checking is enabled.

#### `_deserialize: bool`
Internal flag for deserialization.

#### `engine: Union[Callable, str]`
Deserialization engine.

## Properties

### `value: Any`
**Type**: `Any`  
**Read/Write**  
**Description**: Current value stored in session state.

**Getter**:
```python
counter = SessionState("counter", initial_value=0)
current = counter.value  # Get current value
print(current)  # 0
```

**Setter** (with type checking):
```python
counter = SessionState("counter", initial_value=0, session_type=int, strict=True)
counter.value = 10  # OK
counter.value = "text"  # TypeError
```

**Example**:
```python
# Property-based access
state = SessionState("count", initial_value=0)

# Read
print(state.value)  # 0

# Write
state.value = 5
print(state.value)  # 5

# Increment
state.value += 1
print(state.value)  # 6
```

## Methods

### Instance Methods

#### `set_value()`
```python
def set_value(self, value: Any) -> None:
    """
    Set a new session state value.
    
    Args:
        value: The new value to store
        
    Raises:
        TypeError: If strict=True and value doesn't match session_type
    """
```

**Description**: Alternative to property setter for explicit method calls.

**Example**:
```python
state = SessionState("data", initial_value=[])

# Using property
state.value = [1, 2, 3]

# Using method (equivalent)
state.set_value([1, 2, 3])
```

#### `get_setter()`
```python
def get_setter(self) -> Callable[[Any], Any]:
    """
    Create a functional setter for this session state.
    
    Returns:
        Callable that accepts a value, updates state, and returns the value
        
    Raises:
        TypeError: If strict=True and provided value doesn't match type
    """
```

**Description**: Factory method that creates a closure for functional programming patterns.

**Use Cases**:
- Button callbacks
- Event handlers
- Functional composition

**Example**:
```python
counter = SessionState("counter", initial_value=0)
setter = counter.get_setter()

# Use in callback
import streamlit as st
st.button("Increment", on_click=lambda: setter(counter.value + 1))

# Use in effects
app.add_component(st.button, "Reset", key="reset").add_effect(
    lambda val: setter(0) if val else None
)
```

#### `get_tracker()`
```python
def get_tracker(self) -> Callable[[], Any]:
    """
    Create a functional tracker for this session state.
    
    Returns:
        Callable that returns the current session state value
    """
```

**Description**: Factory method for creating value tracking closures.

**Example**:
```python
state = SessionState("status", initial_value="idle")
tracker = state.get_tracker()

# Use tracker
current_status = tracker()  # Returns current value
print(tracker())  # "idle"

# In monitoring
def monitor_status():
    if tracker() == "error":
        st.error("System error!")
```

### Class Methods

#### `get()`
```python
@classmethod
def get(cls, key: str) -> Any:
    """
    Retrieve a session state value by key.
    
    Args:
        key: The session state key to retrieve
        
    Returns:
        The current value stored under the key
        
    Raises:
        ValueError: If key is empty or invalid
        KeyError: If key doesn't exist in session state
    """
```

**Description**: Direct access to session state without creating SessionState instance.

**Example**:
```python
# Set value via instance
counter = SessionState("counter", initial_value=0)
counter.value = 10

# Get value via class method (from anywhere)
value = SessionState.get("counter")  # 10
```

#### `exists()`
```python
@classmethod
def exists(cls, key: str) -> bool:
    """
    Check if a session state key exists.
    
    Args:
        key: The session state key to check
        
    Returns:
        True if key exists, False otherwise
    """
```

**Example**:
```python
# Check before accessing
if SessionState.exists("user_data"):
    data = SessionState.get("user_data")
else:
    data = default_data
```

#### `delete()`
```python
@classmethod
def delete(cls, key: str) -> None:
    """
    Remove a session state entry by key.
    
    Args:
        key: The session state key to remove
        
    Raises:
        KeyError: If key doesn't exist
    """
```

**Example**:
```python
# Create state
temp = SessionState("temp_data", initial_value="value")

# Delete when done
SessionState.delete("temp_data")

# Check
print(SessionState.exists("temp_data"))  # False
```

### Special Methods

#### `__eq__()`
```python
def __eq__(self, other: object) -> bool:
    """
    Compare SessionState instances for equality.
    
    Two instances are equal if they have the same key, session_type, and strict settings.
    """
```

**Example**:
```python
s1 = SessionState("key", initial_value=0)
s2 = SessionState("key", initial_value=0)
s3 = SessionState("other", initial_value=0)

print(s1 == s2)  # True (same key)
print(s1 == s3)  # False (different key)
```

#### `__hash__()`
```python
def __hash__(self) -> int:
    """Generate hash based on key (for use in sets/dicts)."""
```

**Example**:
```python
state_set = {
    SessionState("key1", initial_value=0),
    SessionState("key2", initial_value=0)
}
```

#### `__repr__()`
```python
def __repr__(self) -> str:
    """Developer-friendly string representation."""
    # SessionState(key='counter', value=0, type=<class 'int'>, strict=True)
```

#### `__str__()`
```python
def __str__(self) -> str:
    """User-friendly string representation."""
    # SessionState['counter']: 0
```

## Usage Examples

### Basic Usage

```python
from declarative_streamlit.base import SessionState
import streamlit as st

# Create counter
counter = SessionState("counter", initial_value=0)

# Display current value
st.write(f"Count: {counter.value}")

# Increment on button click
if st.button("Increment"):
    counter.value += 1
    st.rerun()
```

### Type-Safe State

```python
from declarative_streamlit.base import SessionState
import streamlit as st

# Strict integer counter
counter = SessionState("count", initial_value=0, session_type=int, strict=True)

# This works
counter.value = 10

# This raises TypeError
try:
    counter.value = "invalid"
except TypeError as e:
    st.error(f"Type error: {e}")
```

### Functional Setters

```python
from declarative_streamlit.base import AppPage, SessionState
import streamlit as st

app = AppPage()

counter = SessionState("counter", initial_value=0)
setter = counter.get_setter()

# Use setter in effects
app.add_component(
    st.button, "Increment", key="inc"
).add_effect(
    lambda val: setter(counter.value + 1) if val else None
)

app.add_component(
    st.button, "Reset", key="reset"
).add_effect(
    lambda val: setter(0) if val else None
)

app.add_component(st.metric, "Counter", counter.value)
app.start()
```

### Complex State Management

```python
from declarative_streamlit.base import SessionState
from dataclasses import dataclass
from typing import List
import streamlit as st

@dataclass
class TodoItem:
    text: str
    completed: bool = False

# Type-safe list of todos
todos = SessionState(
    "todos",
    initial_value=[],
    session_type=list,
    strict=True
)

# Add todo
def add_todo(text: str):
    current = todos.value
    current.append(TodoItem(text=text, completed=False))
    todos.value = current

# Display todos
st.write("### Todo List")
new_todo = st.text_input("New todo")
if st.button("Add") and new_todo:
    add_todo(new_todo)
    st.rerun()

for i, todo in enumerate(todos.value):
    st.checkbox(todo.text, value=todo.completed, key=f"todo_{i}")
```

### JSON Deserialization

```python
from declarative_streamlit.base import SessionState
import streamlit as st

# Load JSON config
json_config = '{"theme": "dark", "language": "en", "notifications": true}'

config = SessionState(
    "app_config",
    initial_value=json_config,
    deserialize=True,
    engine='json'
)

# config.value is now a dict
st.write("Theme:", config.value["theme"])
st.write("Language:", config.value["language"])

# Update config
config.value["theme"] = "light"
st.write("Updated config:", config.value)
```

### Class Method Usage

```python
from declarative_streamlit.base import SessionState
import streamlit as st

# Initialize in one module
user_state = SessionState("current_user", initial_value=None)
user_state.value = {"name": "Alice", "role": "admin"}

# Access from another module/function without instance
def display_user():
    if SessionState.exists("current_user"):
        user = SessionState.get("current_user")
        st.write(f"Welcome, {user['name']}!")
    else:
        st.write("No user logged in")

display_user()
```

### Tracker Pattern

```python
from declarative_streamlit.base import SessionState
import streamlit as st

# Create state and tracker
status = SessionState("app_status", initial_value="idle")
status_tracker = status.get_tracker()

# Use tracker in monitoring function
def check_status():
    current = status_tracker()
    if current == "error":
        st.error("Application error!")
    elif current == "processing":
        st.info("Processing...")
    else:
        st.success("Ready")

# Update status
if st.button("Process"):
    status.value = "processing"
    # ... do processing ...
    status.value = "idle"

check_status()
```

### Multi-State Coordination

```python
from declarative_streamlit.base import SessionState, AppPage
import streamlit as st

app = AppPage()

# Multiple coordinated states
name = SessionState("user_name", initial_value="")
email = SessionState("user_email", initial_value="")
is_valid = SessionState("form_valid", initial_value=False)

# Validation function
def validate_form():
    valid = len(name.value) > 0 and "@" in email.value
    is_valid.value = valid
    return valid

# Form components
app.add_component(st.title, "User Form")

app.add_component(
    st.text_input, "Name", key="name_input", value=name.value
).add_effect(
    lambda val: name.set_value(val) if val else None
).add_effect(
    lambda _: validate_form()
)

app.add_component(
    st.text_input, "Email", key="email_input", value=email.value
).add_effect(
    lambda val: email.set_value(val) if val else None
).add_effect(
    lambda _: validate_form()
)

if is_valid.value:
    app.add_component(
        st.button, "Submit", key="submit", type="primary"
    ).add_effect(
        lambda val: st.success(f"Submitted: {name.value}, {email.value}") if val else None
    )

app.start()
```

## Best Practices

### 1. Use Type Safety in Production
```python
# Development - lenient
dev_state = SessionState("temp", strict=False)

# Production - strict
prod_state = SessionState("user_data", session_type=dict, strict=True)
```

### 2. Initialize with Sensible Defaults
```python
# Good - clear initial state
counter = SessionState("counter", initial_value=0)
items = SessionState("items", initial_value=[])

# Avoid - None without clear reason
unclear = SessionState("data", initial_value=None)
```

### 3. Use Descriptive Keys
```python
# Good - clear purpose
user_name = SessionState("user_name", initial_value="")
shopping_cart = SessionState("shopping_cart", initial_value=[])

# Avoid - cryptic keys
x = SessionState("x", initial_value=0)
data = SessionState("d", initial_value=[])
```

### 4. Prefer Properties Over Direct Access
```python
state = SessionState("counter", initial_value=0)

# Good - use properties
state.value = 10
current = state.value

# Avoid - direct session_state access
st.session_state["counter"] = 10  # Bypasses type checking
```

### 5. Use Functional Patterns for Callbacks
```python
counter = SessionState("counter", initial_value=0)
setter = counter.get_setter()

# Good - functional setter in callback
st.button("Inc", on_click=lambda: setter(counter.value + 1))

# Avoid - direct manipulation in callback
# st.button("Inc", on_click=lambda: counter.value + 1)  # Doesn't update
```

### 6. Check Existence Before Access
```python
# Good - safe access
if SessionState.exists("optional_data"):
    data = SessionState.get("optional_data")
else:
    data = default_value

# Risky - may raise KeyError
# data = SessionState.get("optional_data")
```

## Error Handling

### Common Exceptions

#### `ValueError: Key must be a non-empty string`
**Cause**: Empty or non-string key  
**Solution**: Provide valid string key

```python
# Wrong
SessionState("", initial_value=0)
SessionState(None, initial_value=0)

# Correct
SessionState("counter", initial_value=0)
```

#### `TypeError: Type mismatch`
**Cause**: Value doesn't match `session_type` when `strict=True`  
**Solution**: Use correct type or disable strict mode

```python
# Wrong
state = SessionState("count", initial_value=0, session_type=int, strict=True)
state.value = "text"  # TypeError

# Correct
state.value = 10  # OK

# Or disable strict
state = SessionState("count", initial_value=0, session_type=int, strict=False)
state.value = "text"  # Allowed
```

#### `KeyError: Session state key not found`
**Cause**: Accessing non-existent key via class methods  
**Solution**: Check existence first

```python
# Wrong
value = SessionState.get("nonexistent")  # KeyError

# Correct
if SessionState.exists("nonexistent"):
    value = SessionState.get("nonexistent")
else:
    value = default
```

## Performance Considerations

### Memory Usage
SessionState stores values in Streamlit's session state, which persists across reruns:
- Be mindful of large data structures
- Clean up unused state with `SessionState.delete()`

### Type Checking Overhead
Type checking has minimal overhead, but can be disabled if needed:
```python
# Strict type checking (minimal overhead)
state = SessionState("data", session_type=list, strict=True)

# No type checking (slightly faster, less safe)
state = SessionState("data", strict=False)
```

## Related Components

- **[AppPage](./app-page.md)** - Use SessionState for page-level state
- **[AppFragment](./app-fragment.md)** - Fragment-specific state management
- **[AppDialog](./app-dialog.md)** - Dialog state management

## See Also

- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)
- [Examples](../../examples/) - SessionState usage examples
- [State Management Patterns](../../docs/patterns.md) - Advanced patterns

---

**Navigation**: [README](./README.md) | [Canvas](./canvas.md) | [AppPage](./app-page.md) | [AppFragment](./app-fragment.md) | [AppDialog](./app-dialog.md)
