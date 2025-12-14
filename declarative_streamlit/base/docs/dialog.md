# Dialog (Component)

## Overview

`Dialog` is an abstract base class that extends `Canvas` to provide the foundational interface for modal dialog functionality in Streamlit applications. It defines the core contract for dialogs that overlay the main application and require user interaction.

## Class Signature

```python
class Dialog(Canvas, metaclass=ABCMeta):
    """
    Dialog class that extends the Canvas class.
    
    This class is used to create modal dialogs, allowing for focused user interactions
    that overlay the main application content.
    """
    
    def __init__(
        self,
        title: str,
        width: Literal["large", "small"] = "small",
        failsafe: bool = False,
        failhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
    ) -> None
```

## Description

`Dialog` serves as the abstract base for all dialog implementations. It extends `Canvas` with dialog-specific functionality:

- **Modal Behavior**: Dialogs overlay main UI and block interaction
- **Title Display**: Required title shown in dialog header
- **Configurable Width**: Choose between small and large dialog sizes
- **Decorator Wrapping**: Internally wraps content with `@st.dialog` decorator
- **Event-Driven**: Designed to be triggered by user actions

### Position in Architecture

```
Canvas (Abstract Base)
    └── Dialog (Abstract Dialog Base)
        └── AppDialog (Concrete Implementation)
```

The `Dialog` class is an intermediate abstraction that:
1. Extends `Canvas` with dialog-specific behavior
2. Defines dialog rendering contract
3. Is subclassed by `AppDialog` for actual usage

## Constructor Parameters

### `title: str`
**Type**: `str`  
**Required**: Yes  
**Description**: Title displayed in the dialog header.

**Example**:
```python
dialog = Dialog(title="Confirm Action")
dialog = Dialog(title="User Settings")
```

### `width: Literal["large", "small"] = "small"`
**Type**: `Literal["large", "small"]`  
**Default**: `"small"`  
**Description**: Width of the dialog modal.

**Options**:
- `"small"`: Compact dialog for simple interactions (confirmations, alerts)
- `"large"`: Wider dialog for forms and complex content

**Example**:
```python
# Small dialog for confirmation
confirm = Dialog(title="Confirm", width="small")

# Large dialog for form
form = Dialog(title="User Details", width="large")
```

### `failsafe: bool = False`
**Type**: `bool`  
**Default**: `False`  
**Inherited from**: `Canvas`  
**Description**: Enable failsafe error handling mode.

### `failhandler: Callable[[Exception], Union[NoReturn, bool]] = None`
**Type**: `Optional[Callable]`  
**Default**: `None`  
**Inherited from**: `Canvas`  
**Description**: Custom error handler for dialog errors.

### `strict: bool = True`
**Type**: `bool`  
**Default**: `True`  
**Inherited from**: `Canvas`  
**Description**: Enable strict type checking and validation.

## Attributes

### Public Attributes

Inherited from `Canvas`:
- `failsafe: bool` - Failsafe mode setting
- `failhandler: Optional[Callable]` - Error handler function
- `strict: bool` - Strict mode setting

### Dialog-Specific Attributes

#### `_title: str`
**Type**: `str`  
**Protected**  
**Description**: The dialog's title text.

#### `_width: Literal["large", "small"]`
**Type**: `Literal["large", "small"]`  
**Protected**  
**Description**: The dialog's width configuration.

### Protected Attributes

#### `_body: Schema`
**Type**: `Schema`  
**Inherited from**: `Canvas`  
**Description**: Internal schema managing component hierarchy.

## Methods

### Abstract Methods

Dialog inherits all abstract methods from `Canvas`:

- `add_component()` - Must be implemented by subclass
- `add_container()` - Must be implemented by subclass
- `serialize()` - Must be implemented by subclass

### Dialog-Specific Methods

#### `start()`
```python
def start(self, *args, **kwargs) -> None:
    """
    Start the dialog rendering process.
    
    This method initiates the display of the modal dialog, wrapping the content
    in Streamlit's @dialog decorator with the configured title and width.
    """
```

**Description**: Initiates dialog display as a modal overlay.

**Behavior**:
1. Wraps `_body` in `@st.dialog(title=self._title, width=self._width)` decorator
2. Renders all components in the dialog
3. Dialog blocks main UI interaction until dismissed
4. Remains open until closed by user or programmatically

**Implementation Details**:
```python
def start(self, *args, **kwargs):
    """Start the dialog rendering process."""
    self.__render_on_dialog()

def __render_on_dialog(self):
    """Internal method to wrap body in @st.dialog decorator."""
    @dialog(title=self._title, width=self._width)
    def render():
        self._body()
    
    return render()
```

**Example**:
```python
# Concrete implementation (AppDialog)
dlg = AppDialog(title="Confirm", width="small")
dlg.add_component(st.warning, "Are you sure?")
dlg.add_component(st.button, "Yes", key="yes")
dlg.start()  # Displays modal dialog
```

#### `__call__()`
```python
def __call__(self, *args, **kwargs):
    """
    Call the dialog with the provided arguments.
    
    This allows the dialog to be called as a function, which invokes start().
    """
    return self.start()
```

**Description**: Enables calling dialog instance directly.

**Example**:
```python
dialog = AppDialog(title="Alert")
dialog.add_component(st.info, "Information")

# Can call directly
dialog()  # Equivalent to dialog.start()

# Useful in effects
app.add_component(st.button, "Show", key="btn").add_effect(dialog)
```

### Inherited Methods

From `Canvas`:
- `set_failsafe()` - Configure failsafe mode
- `set_failhandler()` - Set error handler
- `set_strict()` - Configure strict mode
- `__getitem__()` - Access components by key/index
- `main_body` property - Access component layer

## Implementation Notes

### Internal Rendering Mechanism

The `Dialog` class uses a private method to wrap rendering:

```python
def __render_on_dialog(self):
    """
    Render the dialog on the canvas.
    
    This method is responsible for rendering the dialog as a modal overlay.
    It wraps the dialog body in Streamlit's @dialog decorator.
    """
    @dialog(title=self._title, width=self._width)
    def render():
        self._body()
    
    return render()
```

**Key Points**:
1. Uses `@st.dialog` decorator from Streamlit
2. Passes `title` and `width` parameters
3. Wraps the `_body()` schema execution
4. Creates modal overlay behavior

### Modal Behavior

Dialogs created from this class:
- Overlay the main application
- Block interaction with underlying UI
- Require explicit dismissal (close button or programmatic close)
- Can access and modify session state
- Render independently from main page

### Event-Driven Design

Dialogs are designed to be triggered by events:
- Button clicks
- Component effects
- Conditional logic
- State changes

**Not** designed to be called unconditionally on every rerun (would show constantly).

## Usage Patterns

### Basic Dialog Pattern

Since `Dialog` is abstract, it's typically used through `AppDialog`:

```python
from declarative_streamlit.base import AppPage, AppDialog
import streamlit as st

app = AppPage()

# Create dialog
dialog = AppDialog(title="Confirm Action", width="small")
dialog.add_component(st.warning, "Are you sure?")
dialog.add_component(st.button, "Confirm", key="confirm")
dialog.add_component(st.button, "Cancel", key="cancel")

# Trigger on button click
app.add_component(st.button, "Delete", key="delete").add_effect(dialog)

app.start()
```

### Effect-Triggered Pattern

```python
# Dialog triggered as an effect of component interaction
dialog = AppDialog(title="Details")
dialog.add_component(st.info, "Additional information")

# Trigger when button is clicked
app.add_component(st.button, "More Info", key="info").add_effect(dialog)
```

### Conditional Display Pattern

```python
from declarative_streamlit.base import SessionState

show_dialog = SessionState("show_dialog", initial_value=False)

if show_dialog.value:
    dialog = AppDialog(title="Message")
    dialog.add_component(st.success, "Operation complete!")
    dialog.add_component(
        st.button, "OK", key="ok"
    ).add_effect(
        lambda val: show_dialog.set_value(False) if val else None
    )
    dialog.start()
```

## Design Considerations

### Why Dialog is Abstract

`Dialog` is kept abstract to:
1. **Separation of Concerns**: Core dialog logic separated from application features
2. **Extensibility**: Allows different dialog implementations (e.g., AppDialog)
3. **Interface Definition**: Defines contract without prescribing implementation
4. **Consistency**: Maintains architecture pattern with Canvas and Fragment

### Relationship to AppDialog

```python
# Dialog - Abstract base defining interface
class Dialog(Canvas, metaclass=ABCMeta):
    # Core dialog functionality
    pass

# AppDialog - Concrete implementation
class AppDialog(Dialog):
    # Implements abstract methods
    # Adds application-specific features (standard support)
    pass
```

Users interact with `AppDialog`, which provides:
- Concrete implementations of abstract methods
- Additional features (standards, naming)
- Full component management
- Ready-to-use dialog functionality

## Best Practices

### 1. Use AppDialog for Actual Dialogs

```python
# Don't instantiate Dialog directly
# dialog = Dialog(title="Title")  # Abstract, won't work

# Use AppDialog
dialog = AppDialog(title="Confirmation")
```

### 2. Always Provide a Title

```python
# Good - clear title
dialog = AppDialog(title="Confirm Deletion")

# Less clear
dialog = AppDialog(title="Dialog")  # Not descriptive
```

### 3. Choose Appropriate Width

```python
# Small for simple interactions
confirm = AppDialog(title="Confirm", width="small")

# Large for forms and complex content
form = AppDialog(title="User Form", width="large")
```

### 4. Provide Dismiss Actions

```python
# Always give users a way to close
dialog.add_component(st.button, "Close", key="close")
dialog.add_component(st.button, "Cancel", key="cancel")
```

### 5. Trigger via Effects

```python
# Good - triggered by user action
app.add_component(st.button, "Show", key="show").add_effect(dialog)

# Avoid - shows on every rerun
# dialog.start()  # Would show constantly
```

## Error Handling

### Abstract Method Errors

```python
# Wrong - Dialog is abstract
try:
    dialog = Dialog(title="Title")  # Can't instantiate
except TypeError as e:
    print("Dialog is abstract")

# Correct - Use concrete implementation
dialog = AppDialog(title="Title")  # OK
```

### Missing Title

```python
# Title is required
try:
    dialog = AppDialog()  # Missing title
except TypeError:
    print("Title is required")

# Correct
dialog = AppDialog(title="My Dialog")  # OK
```

### Invalid Width

```python
# Invalid width values
try:
    dialog = AppDialog(title="Test", width="medium")  # Not valid
except:
    print("Width must be 'small' or 'large'")

# Correct
dialog = AppDialog(title="Test", width="small")  # OK
dialog = AppDialog(title="Test", width="large")  # OK
```

## Performance Considerations

### Dialog Content

Keep dialog content focused and lightweight:
```python
# Good - focused content
dialog.add_component(st.write, "Message")
dialog.add_component(st.button, "OK", key="ok")

# Avoid - heavy content
# dialog.add_component(st.dataframe, huge_dataframe)  # Slow
```

### Avoid Excessive Triggers

```python
# Don't trigger on every interaction
# Use specific events

# Good - specific trigger
app.add_component(st.button, "Action", key="action").add_effect(dialog)

# Avoid - triggers too often
# every_component.add_effect(dialog)  # Too many triggers
```

## Streamlit Dialog Compatibility

`Dialog` wraps Streamlit's `@st.dialog` decorator. Key compatibility notes:

1. **Modal Behavior**: Blocks main UI interaction
2. **Dismissal**: User can click outside or use close button
3. **State Access**: Can access session state
4. **Component Support**: Supports most Streamlit components
5. **No Nesting**: Cannot open dialogs from within dialogs

**Limitations** (from Streamlit):
- Cannot nest dialogs (dialog within dialog)
- Limited sidebar access from within dialog
- Some advanced features may have restrictions

## Related Components

- **[Canvas](./canvas.md)** - Base class that Dialog extends
- **[AppDialog](./app-dialog.md)** - Concrete implementation for use in applications
- **[Fragment](./fragment.md)** - Sister class for fragment functionality
- **[AppPage](./app-page.md)** - Can trigger dialogs

## See Also

- [Streamlit Dialogs](https://docs.streamlit.io/library/api-reference/execution-flow/st.dialog)
- [Canvas Documentation](./canvas.md) - Base class details
- [AppDialog Documentation](./app-dialog.md) - Concrete usage

---

**Navigation**: [README](./README.md) | [Canvas](./canvas.md) | [AppDialog](./app-dialog.md) | [Fragment](./fragment.md)
