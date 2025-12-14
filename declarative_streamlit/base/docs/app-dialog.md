# AppDialog

## Overview

`AppDialog` is an application-level class that extends the `Dialog` canvas to provide modal dialog functionality in Streamlit applications. Dialogs create focused, overlay UI elements that require user interaction before returning to the main application.

## Class Signature

```python
class AppDialog(Dialog):
    """
    Represents a dialog in the application with component management capabilities.
    
    This class provides methods to add components and containers to a dialog,
    manage the dialog schema, and handle dialog display through user interactions.
    """
    
    def __init__(
        self,
        title: str = None,
        width: Literal["large", "small"] = "small",
        failsafe: bool = False,
        failhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
        standard: BaseStandard = None,
    ) -> None
```

## Description

`AppDialog` wraps Streamlit's `@st.dialog` decorator in a declarative interface, enabling modal dialogs that:

- **Overlay Main UI**: Display on top of the main application
- **Block Interaction**: Require dismissal before accessing main UI
- **Support Components**: Can contain any Streamlit component
- **Configurable Size**: Choose between small and large widths
- **Event-Driven**: Triggered by user actions (button clicks, etc.)

### Key Features

1. **Modal Behavior**: Blocks interaction with main UI
2. **Declarative API**: Consistent with AppPage/AppFragment
3. **Component Management**: Add components like any other canvas
4. **Effect Integration**: Can be triggered as an effect of components
5. **Standard Support**: Apply configuration standards to dialog components

## Constructor Parameters

### `title: str = None`
**Type**: `Optional[str]`  
**Default**: `None`  
**Description**: Title displayed in the dialog header.

**Example**:
```python
dialog = AppDialog(title="Confirm Action")
```

**Note**: While optional, providing a title improves UX by clearly indicating the dialog's purpose.

### `width: Literal["large", "small"] = "small"`
**Type**: `Literal["large", "small"]`  
**Default**: `"small"`  
**Description**: Width of the dialog modal.

- `"small"`: Compact dialog for simple interactions
- `"large"`: Wider dialog for more complex content

**Example**:
```python
# Small dialog for confirmation
confirm_dialog = AppDialog(title="Confirm", width="small")

# Large dialog for forms
form_dialog = AppDialog(title="User Details", width="large")
```

### `failsafe: bool = False`
**Type**: `bool`  
**Default**: `False`  
**Inherited from**: `Canvas`  
**Description**: Enable failsafe mode for error resilience.

### `failhandler: Callable[[Exception], Union[NoReturn, bool]] = None`
**Type**: `Optional[Callable]`  
**Default**: `None`  
**Inherited from**: `Canvas`  
**Description**: Custom error handler for dialog errors.

### `strict: bool = True`
**Type**: `bool`  
**Default**: `True`  
**Inherited from**: `Canvas`  
**Description**: Enable strict type checking.

### `standard: BaseStandard = None`
**Type**: `Optional[BaseStandard]`  
**Default**: `None`  
**Description**: Configuration standard to apply to dialog components.

**Example**:
```python
from declarative_streamlit.config.common.stdstreamlit import StreamlitCommonStandard

dialog = AppDialog(
    title="Settings",
    standard=StreamlitCommonStandard()
)
```

## Attributes

### Public Attributes

Inherited from `Canvas`:
- `failsafe: bool`
- `failhandler: Optional[Callable]`
- `strict: bool`

### Protected Attributes

#### `_title: str`
**Type**: `str`  
**Description**: The dialog's title.

#### `_width: Literal["large", "small"]`
**Type**: `Literal["large", "small"]`  
**Description**: The dialog's width setting.

#### `_standard: Optional[BaseStandard]`
**Type**: `Optional[BaseStandard]`  
**Description**: Configuration standard applied to components.

#### `_body: Schema`
**Type**: `Schema`  
**Inherited from**: `Canvas`  
**Description**: Internal schema managing component hierarchy.

## Methods

### Component Management

#### `add_component()`
```python
def add_component(
    self,
    component: Union[Callable[..., Any], StreamlitComponentParser],
    *args: Any,
    **kwargs: Any,
) -> StreamlitComponentParser:
    """
    Add a component to the dialog.
    
    Args:
        component: The Streamlit component function or parser
        *args: Positional arguments for the component
        **kwargs: Keyword arguments for the component
        
    Returns:
        StreamlitComponentParser: Parser wrapping the component
        
    Raises:
        TypeError: If component is not callable
    """
```

**Description**: Add Streamlit components to the dialog.

**Example**:
```python
dialog = AppDialog(title="Confirm Delete")

dialog.add_component(st.warning, "Are you sure you want to delete this item?")
dialog.add_component(st.button, "Confirm", key="confirm_delete", type="primary")
dialog.add_component(st.button, "Cancel", key="cancel_delete")
```

#### `add_container()`
```python
def add_container(
    self,
    container: Union[Callable[..., Any], StreamlitLayoutParser],
    *args: Any,
    **kwargs: Any,
) -> StreamlitLayoutParser:
    """
    Add a container to the dialog.
    
    Args:
        container: The Streamlit container function or parser
        *args: Positional arguments for the container
        **kwargs: Keyword arguments for the container
        
    Returns:
        StreamlitLayoutParser: Parser wrapping the container
        
    Raises:
        TypeError: If container is not callable
    """
```

**Description**: Add layout containers to organize dialog components.

**Example**:
```python
dialog = AppDialog(title="Form Dialog", width="large")

with dialog.add_container(st.container) as container:
    container.add_component(st.text_input, "Name", key="dialog_name")
    container.add_component(st.email, "Email", key="dialog_email")

with dialog.add_container(st.columns, 2).set_column_based(True) as cols:
    cols.add_component(st.button, "Save", key="save", type="primary")
    cols.add_component(st.button, "Cancel", key="cancel")
```

#### `add_function()`
```python
def add_function(
    self,
    function: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> StreamlitComponentParser:
    """
    Add a custom function to the dialog.
    
    Args:
        function: The function to execute
        *args: Arguments for the function
        **kwargs: Keyword arguments for the function
        
    Returns:
        StreamlitComponentParser: Parser wrapping the function
    """
```

**Example**:
```python
dialog = AppDialog(title="Processing")

def show_progress():
    with st.spinner("Processing..."):
        process_data()
    st.success("Complete!")

dialog.add_function(show_progress)
```

#### `add_fragment()`
```python
def add_fragment(
    self,
    fragment: Union[Callable[..., Any], Fragment],
) -> Fragment:
    """
    Add a fragment to the dialog.
    
    Args:
        fragment: Fragment instance or callable
        
    Returns:
        Fragment: The added fragment
    """
```

**Example**:
```python
dialog = AppDialog(title="Live Stats")

stats_fragment = AppFragment(name="dialog_stats", run_every=2)
stats_fragment.add_component(st.metric, "Status", "Active")

dialog.add_fragment(stats_fragment)
```

### Rendering

#### `start()`
```python
def start(self, *args, **kwargs) -> None:
    """
    Start the dialog rendering process.
    
    This wraps the dialog body in Streamlit's @dialog decorator
    and initiates dialog display.
    """
```

**Description**: Display the dialog. Automatically called when dialog is triggered as an effect.

**Behavior**:
1. Wraps body in `@st.dialog(title=self._title, width=self._width)`
2. Renders all dialog components
3. Dialog remains open until explicitly closed or dismissed

**Example**:
```python
dialog = AppDialog(title="Message")
dialog.add_component(st.info, "This is a dialog!")
dialog.add_component(st.button, "OK", key="dialog_ok")

# Trigger dialog (usually through effects)
dialog.start()
```

#### `__call__()`
```python
def __call__(self, *args, **kwargs):
    """Call the dialog, equivalent to start()."""
    return self.start()
```

**Description**: Allows calling dialog instance directly.

**Example**:
```python
dialog = AppDialog(title="Alert")
dialog.add_component(st.warning, "Warning message")

# Can call directly
dialog()  # Equivalent to dialog.start()
```

### Serialization

#### `serialize()`
```python
def serialize(self) -> Dict[str, Any]:
    """
    Serialize the dialog to a dictionary.
    
    Returns:
        Dict[str, Any]: Dictionary representation including:
            - __dialog__: Dialog schema
            - __config__: Configuration settings
    """
```

**Example**:
```python
dialog = AppDialog(title="Sample Dialog")
dialog.add_component(st.text, "Content")

data = dialog.serialize()
# {
#     "__dialog__": {...},
#     "__config__": {"strict": True, "failsafe": False}
# }
```

### Utility Methods

#### `__name__()`
```python
def __name__(self) -> str:
    """
    Get the dialog's name.
    
    Returns:
        str: Dialog name or class name
    """
```

#### `__repr__()`
```python
def __repr__(self) -> str:
    """String representation for debugging."""
    return f"Dialog({self.__str__()})"
```

## Usage Examples

### Basic Confirmation Dialog

```python
from declarative_streamlit.base import AppPage, AppDialog
import streamlit as st

AppPage.set_page_config(layout="wide")
app = AppPage()

# Create confirmation dialog
confirm_dialog = AppDialog(title="Confirm Deletion", width="small")
confirm_dialog.add_component(
    st.warning, "Are you sure you want to delete this item? This cannot be undone."
)
confirm_dialog.add_component(
    st.button, "Yes, Delete", key="confirm_yes", type="primary"
)
confirm_dialog.add_component(
    st.button, "Cancel", key="confirm_no"
)

# Main page
app.add_component(st.title, "Item Manager")
app.add_component(st.write, "Click the button to delete an item")

# Trigger dialog on button click
app.add_component(
    st.button, "Delete Item", key="delete_btn"
).add_effect(confirm_dialog)  # Dialog shown when button clicked

app.start()
```

### Form Dialog

```python
from declarative_streamlit.base import AppPage, AppDialog, SessionState
import streamlit as st

app = AppPage()

# Session state for form data
form_data = SessionState("form_data", initial_value={})

# Create form dialog
form_dialog = AppDialog(title="Add User", width="large")

form_dialog.add_component(st.text_input, "Full Name", key="dialog_name")
form_dialog.add_component(st.text_input, "Email", key="dialog_email")
form_dialog.add_component(
    st.selectbox, "Role", ["User", "Admin", "Manager"], key="dialog_role"
)

# Submit button with effect
form_dialog.add_component(
    st.button, "Submit", key="submit_user", type="primary"
).add_effect(
    lambda val: form_data.set_value({
        "name": st.session_state.get("dialog_name"),
        "email": st.session_state.get("dialog_email"),
        "role": st.session_state.get("dialog_role")
    }) if val else None
)

form_dialog.add_component(st.button, "Cancel", key="cancel_user")

# Main page
app.add_component(st.title, "User Management")
app.add_component(st.button, "Add New User", key="add_user_btn").add_effect(form_dialog)

# Display submitted data
if form_data.value:
    app.add_component(st.success, f"User added: {form_data.value}")

app.start()
```

### Information Dialog

```python
from declarative_streamlit.base import AppPage, AppDialog
import streamlit as st

app = AppPage()

# Info dialog
info_dialog = AppDialog(title="Help Information", width="large")
info_dialog.add_component(st.markdown, """
## How to Use This Application

1. **Step 1**: Select your preferences
2. **Step 2**: Configure settings
3. **Step 3**: Submit your data

For more information, visit our [documentation](#).
""")
info_dialog.add_component(st.button, "Got it!", key="close_help")

# Main page
app.add_component(st.title, "My Application")
app.add_component(st.button, "Help", key="help_btn").add_effect(info_dialog)

app.start()
```

### Conditional Dialog

```python
from declarative_streamlit.base import AppPage, AppDialog, SessionState
import streamlit as st

app = AppPage()

# State to track if user is logged in
is_logged_in = SessionState("is_logged_in", initial_value=False)

# Login dialog
login_dialog = AppDialog(title="Login Required", width="small")
login_dialog.add_component(st.warning, "Please log in to continue")
login_dialog.add_component(st.text_input, "Username", key="username")
login_dialog.add_component(st.text_input, "Password", type="password", key="password")
login_dialog.add_component(
    st.button, "Login", key="login_submit", type="primary"
).add_effect(
    lambda val: is_logged_in.set_value(True) if val else None
)

# Main page
app.add_component(st.title, "Protected Content")

# Show dialog if not logged in
if not is_logged_in.value:
    app.add_component(
        st.button, "Access Protected Content", key="access_btn"
    ).add_effect(login_dialog)
else:
    app.add_component(st.success, "You are logged in!")
    app.add_component(st.write, "Protected content here...")

app.start()
```

### Dialog with Fragments

```python
from declarative_streamlit.base import AppPage, AppDialog, AppFragment
import streamlit as st
import time

app = AppPage()

# Fragment for live updates within dialog
live_fragment = AppFragment(name="dialog_live", run_every=1)
live_fragment.add_component(
    st.metric, "Server Time", time.strftime("%H:%M:%S")
)

# Dialog containing fragment
monitor_dialog = AppDialog(title="Server Monitor", width="large")
monitor_dialog.add_component(st.subheader, "Live Server Status")
monitor_dialog.add_fragment(live_fragment)
monitor_dialog.add_component(st.button, "Close", key="close_monitor")

# Main page
app.add_component(st.title, "Server Dashboard")
app.add_component(
    st.button, "View Live Monitor", key="monitor_btn"
).add_effect(monitor_dialog)

app.start()
```

### Multi-Step Dialog

```python
from declarative_streamlit.base import AppPage, AppDialog, SessionState
import streamlit as st

app = AppPage()

# State to track dialog step
dialog_step = SessionState("dialog_step", initial_value=1)

# Multi-step dialog
wizard_dialog = AppDialog(title="Setup Wizard", width="large")

def render_step():
    step = dialog_step.value
    
    if step == 1:
        st.write("### Step 1: Basic Information")
        st.text_input("Company Name", key="company")
        if st.button("Next", key="step1_next"):
            dialog_step.set_value(2)
            
    elif step == 2:
        st.write("### Step 2: Configuration")
        st.selectbox("Region", ["US", "EU", "APAC"], key="region")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back", key="step2_back"):
                dialog_step.set_value(1)
        with col2:
            if st.button("Next", key="step2_next"):
                dialog_step.set_value(3)
                
    elif step == 3:
        st.write("### Step 3: Review")
        st.success("Setup complete!")
        if st.button("Finish", key="finish"):
            dialog_step.set_value(1)  # Reset for next time

wizard_dialog.add_function(render_step)

# Main page
app.add_component(st.title, "Application Setup")
app.add_component(
    st.button, "Start Setup Wizard", key="wizard_btn"
).add_effect(wizard_dialog)

app.start()
```

## Best Practices

### 1. Provide Clear Titles
```python
# Good - clear purpose
dialog = AppDialog(title="Confirm Deletion")

# Less clear
dialog = AppDialog(title="Dialog")
```

### 2. Choose Appropriate Width
```python
# Small for simple confirmations
confirm = AppDialog(title="Confirm", width="small")

# Large for forms and complex content
form = AppDialog(title="User Form", width="large")
```

### 3. Include Dismiss Actions
```python
# Always provide a way to close
dialog.add_component(st.button, "Cancel", key="cancel")
dialog.add_component(st.button, "OK", key="ok")
```

### 4. Use Effects to Trigger
```python
# Good - triggered by user action
app.add_component(
    st.button, "Show Dialog", key="show"
).add_effect(dialog)

# Avoid - shows on every rerun
# dialog.start()  # Don't call directly unless intentional
```

### 5. Handle State Appropriately
```python
# Use session state for dialog data
dialog_data = SessionState("dialog_input", initial_value="")

dialog.add_component(
    st.text_input, "Input", key="dialog_text"
).add_effect(
    lambda val: dialog_data.set_value(val)
)
```

### 6. Keep Dialogs Focused
```python
# Good - single purpose
confirm_dialog.add_component(st.warning, "Confirm action?")
confirm_dialog.add_component(st.button, "Yes", key="yes")

# Avoid - too much content
# Don't put entire forms with 20 fields in a dialog
```

## Error Handling

### Common Issues

#### Dialog doesn't appear
**Cause**: Dialog not triggered properly  
**Solution**: Ensure dialog is called via effect

```python
# Wrong - won't trigger
app.add_component(st.button, "Show", key="btn")
dialog.start()  # Called on every rerun, not on click

# Correct - triggered on click
app.add_component(st.button, "Show", key="btn").add_effect(dialog)
```

#### Dialog shows on every rerun
**Cause**: Dialog called unconditionally  
**Solution**: Only call through effects or conditional logic

```python
# Wrong
dialog.start()  # Shows every time

# Correct
if st.session_state.get("show_dialog"):
    dialog.start()
```

#### Components not appearing in dialog
**Cause**: Components added after dialog is displayed  
**Solution**: Add all components before triggering dialog

```python
# Correct order
dialog = AppDialog(title="Dialog")
dialog.add_component(st.write, "Content")  # Add first
app.add_component(st.button, "Show", key="btn").add_effect(dialog)  # Trigger second
```

## Streamlit Dialog Compatibility

`AppDialog` wraps Streamlit's `@st.dialog` decorator. Key compatibility notes:

1. **Modal Behavior**: Blocks main UI interaction
2. **Dismissal**: Can be dismissed by clicking outside or using close button
3. **State**: Accesses same session state as main app
4. **Nested Components**: Supports most Streamlit components
5. **Reruns**: Dialog reruns independently when components interact

**Limitations** (from Streamlit):
- Cannot open dialogs from within dialogs (nested dialogs)
- Some advanced widgets may have limited support

## Performance Considerations

### Dialog Content Size
Keep dialog content focused and lightweight:
```python
# Good - focused content
dialog.add_component(st.write, "Simple message")
dialog.add_component(st.button, "OK", key="ok")

# Avoid - heavy content
# dialog.add_component(st.dataframe, huge_dataframe)  # Slow to render
```

### Avoid Excessive Reruns
```python
# Don't trigger on every interaction
# Use effects for specific events
app.add_component(st.button, "Specific Action", key="specific").add_effect(dialog)
```

## Related Components

- **[Dialog](./dialog.md)** - Base Dialog canvas class
- **[AppPage](./app-page.md)** - Main page that can trigger dialogs
- **[AppFragment](./app-fragment.md)** - Fragment that can contain dialogs
- **[Canvas](./canvas.md)** - Base canvas abstraction

## See Also

- [Streamlit Dialog Documentation](https://docs.streamlit.io/library/api-reference/execution-flow/st.dialog)
- [Examples](../../examples/) - Dialog usage examples
- [Effects System](../../core/docs/event-system.md) - Understanding effects

---

**Navigation**: [README](./README.md) | [Canvas](./canvas.md) | [AppPage](./app-page.md) | [AppFragment](./app-fragment.md) | [SessionState](./session-state.md)
