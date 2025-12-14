# Widgets Reference

## Overview

Widgets are **interactive components** that capture user input and maintain state across Streamlit reruns. This document provides a comprehensive reference for all widget representations available in the `declarative_streamlit` library.

**Location**: `declarative_streamlit/config/common/widgets/`

## Widget Characteristics

All widgets share these common characteristics:

- **Stateful**: `stateful=True` - Maintain values across reruns via session state
- **Fatal**: `fatal=True` - Errors in widgets are considered critical
- **Strict**: `strict=True` - Enforce strict type checking and validation
- **Non-Column-Based**: `column_based=False` - Not layout containers
- **Unique Keys**: Include `key` parameter with UUID for state management

## Widget Categories

### Button Widgets

Interactive button components for triggering actions.

**Location**: `declarative_streamlit/config/common/widgets/buttons.py`

#### ButtonRepresentation

Standard clickable button.

**Component**: `st.button`

**Default Configuration**:
```python
{
    "label": "Button",
    "key": str(uuid4()),
    "help": "This a generic button",
}
```

**Behavioral Flags**:
- `stateful=True`
- `fatal=True`
- `strict=True`
- `column_based=False`

**Usage Example**:
```python
app.add_component(st.button, "Click Me")
```

**Common Parameters**:
- `label` (str): Button text
- `key` (str): Unique widget identifier
- `help` (str): Tooltip text
- `on_click` (callable): Callback function
- `disabled` (bool): Disable interaction

---

#### DownloadButtonRepresentation

Button that triggers file download.

**Component**: `st.download_button`

**Default Configuration**:
```python
{
    "label": "Download Button",
    "key": str(uuid4()),
    "help": "This a generic download button",
    "data": "Example data Text",
    "file_name": "example.txt",
    "mime": "text/plain",
    "on_click": "ignore",
}
```

**Behavioral Flags**: Same as ButtonRepresentation

**Usage Example**:
```python
app.add_component(
    st.download_button,
    label="Download CSV",
    data=csv_data,
    file_name="data.csv",
    mime="text/csv"
)
```

**Common Parameters**:
- `data` (str | bytes): Data to download
- `file_name` (str): Suggested filename
- `mime` (str): MIME type (e.g., "text/csv", "application/pdf")

---

#### FormSubmitButtonRepresentation

Button specifically for form submission.

**Component**: `st.form_submit_button`

**Default Configuration**:
```python
{
    "label": "Form Submit Button",
    "key": str(uuid4()),
    "help": "This a generic form submit button",
}
```

**Behavioral Flags**: Same as ButtonRepresentation

**Usage Example**:
```python
with app.add_container(st.form, "my_form") as form:
    form.add_component(st.text_input, "Name")
    form.add_component(st.form_submit_button, "Submit")
```

**Note**: Must be used within a `st.form` container.

---

#### LinkButtonRepresentation

Button that opens an external URL.

**Component**: `st.link_button`

**Default Configuration**:
```python
{
    "label": "Link Button",
    "help": "This a generic link button",
    "url": "https://streamlit.io",
}
```

**Behavioral Flags**: Same as ButtonRepresentation

**Usage Example**:
```python
app.add_component(
    st.link_button,
    label="Visit Streamlit",
    url="https://streamlit.io"
)
```

---

#### PageLinkRepresentation

Navigation link to another page in a multi-page app.

**Component**: `st.page_link`

**Default Configuration**:
```python
{
    "page": "pages/page1.py",
    "label": "Page Link",
    "help": "This a generic page link",
}
```

**Behavioral Flags**: Same as ButtonRepresentation

**Usage Example**:
```python
app.add_component(
    st.page_link,
    page="pages/dashboard.py",
    label="Dashboard"
)
```

---

### Input Widgets

Text and numeric input components.

**Location**: `declarative_streamlit/config/common/widgets/inputs.py`

#### TextInputRepresentation

Single-line text input.

**Component**: `st.text_input`

**Default Configuration**:
```python
{
    "label": "Text Input",
    "value": "",
    "key": str(uuid4()),
    "help": "This a generic text input",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(st.text_input, label="Username")
```

**Common Parameters**:
- `value` (str): Default/initial value
- `max_chars` (int): Maximum character limit
- `type` (str): "default" or "password"
- `placeholder` (str): Placeholder text

---

#### TextAreaRepresentation

Multi-line text input.

**Component**: `st.text_area`

**Default Configuration**:
```python
{
    "label": "Text Area",
    "value": "",
    "key": str(uuid4()),
    "help": "This a generic text area",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.text_area,
    label="Comments",
    height=200
)
```

**Common Parameters**:
- `height` (int): Height in pixels
- `max_chars` (int): Maximum character limit

---

#### NumberInputRepresentation

Numeric input with increment/decrement controls.

**Component**: `st.number_input`

**Default Configuration**:
```python
{
    "label": "Number Input",
    "min_value": 0,
    "max_value": 100,
    "value": 50,
    "step": 1,
    "key": str(uuid4()),
    "help": "This a generic number input",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.number_input,
    label="Age",
    min_value=0,
    max_value=120,
    value=25
)
```

**Common Parameters**:
- `min_value` (int | float): Minimum allowed value
- `max_value` (int | float): Maximum allowed value
- `step` (int | float): Increment/decrement step
- `format` (str): Number format string (e.g., "%.2f")

---

#### SliderRepresentation

Slider for selecting numeric values.

**Component**: `st.slider`

**Default Configuration**:
```python
{
    "label": "Slider",
    "min_value": 0,
    "max_value": 100,
    "step": 1,
    "key": str(uuid4()),
    "help": "This a generic slider",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.slider,
    label="Temperature",
    min_value=-10,
    max_value=40,
    value=20
)
```

**Common Parameters**:
- `value` (number | tuple): Single value or range (start, end)
- `format` (str): Display format

---

#### DateInputRepresentation

Date picker widget.

**Component**: `st.date_input`

**Default Configuration**:
```python
{
    "label": "Date Input",
    "value": "today",
    "key": str(uuid4()),
    "help": "This a generic date input",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
from datetime import date

app.add_component(
    st.date_input,
    label="Select Date",
    value=date.today()
)
```

**Common Parameters**:
- `value`: Single date or date range
- `min_value` (date): Minimum selectable date
- `max_value` (date): Maximum selectable date

---

#### TimeInputRepresentation

Time picker widget.

**Component**: `st.time_input`

**Default Configuration**:
```python
{
    "label": "Time Input",
    "value": "now",
    "key": str(uuid4()),
    "help": "This a generic time input",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
from datetime import time

app.add_component(
    st.time_input,
    label="Select Time",
    value=time(9, 0)
)
```

---

#### ChatInputRepresentation

Chat-style text input.

**Component**: `st.chat_input`

**Default Configuration**:
```python
{
    "placeholder": "Type a message...",
    "key": str(uuid4()),
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.chat_input,
    placeholder="Enter your message"
)
```

---

### Selection Widgets

Widgets for selecting from predefined options.

**Location**: `declarative_streamlit/config/common/widgets/selections.py`

#### SelectboxRepresentation

Dropdown selection with single choice.

**Component**: `st.selectbox`

**Default Configuration**:
```python
{
    "label": "Select Box",
    "key": str(uuid4()),
    "help": "This a generic select box",
    "options": ["Option 1", "Option 2", "Option 3"],
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.selectbox,
    label="Choose Country",
    options=["USA", "Canada", "Mexico"]
)
```

**Common Parameters**:
- `options` (list): Available choices
- `index` (int): Default selection index
- `format_func` (callable): Custom display formatter

---

#### MultiselectRepresentation

Multi-selection dropdown.

**Component**: `st.multiselect`

**Default Configuration**:
```python
{
    "label": "Multi Select Box",
    "key": str(uuid4()),
    "help": "This a generic multi select box",
    "options": ["Option 1", "Option 2", "Option 3"],
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.multiselect,
    label="Select Colors",
    options=["Red", "Green", "Blue", "Yellow"]
)
```

**Returns**: List of selected values

---

#### RadioRepresentation

Radio button group (single selection).

**Component**: `st.radio`

**Default Configuration**:
```python
{
    "label": "Radio Box",
    "key": str(uuid4()),
    "help": "This a generic radio box",
    "options": ["Option 1", "Option 2", "Option 3"],
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.radio,
    label="Choose Size",
    options=["Small", "Medium", "Large"],
    horizontal=True
)
```

**Common Parameters**:
- `horizontal` (bool): Horizontal layout

---

#### CheckboxRepresentation

Single checkbox toggle.

**Component**: `st.checkbox`

**Default Configuration**:
```python
{
    "label": "Checkbox",
    "key": str(uuid4()),
    "help": "This a generic checkbox",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.checkbox,
    label="I agree to terms",
    value=False
)
```

**Returns**: Boolean value

---

#### ToggleRepresentation

Toggle switch widget.

**Component**: `st.toggle`

**Default Configuration**:
```python
{
    "label": "Toggle",
    "key": str(uuid4()),
    "help": "This a generic toggle",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.toggle,
    label="Enable notifications"
)
```

---

#### SelectSliderRepresentation

Slider for selecting from discrete options.

**Component**: `st.select_slider`

**Default Configuration**:
```python
{
    "label": "Select Slider",
    "key": str(uuid4()),
    "help": "This a generic select slider",
    "options": ["Option 1", "Option 2", "Option 3"],
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.select_slider,
    label="Rating",
    options=["Poor", "Fair", "Good", "Excellent"]
)
```

---

#### ColorPickerRepresentation

Color selection widget.

**Component**: `st.color_picker`

**Default Configuration**:
```python
{
    "label": "Color Picker",
    "key": str(uuid4()),
    "value": "#fafafa",
    "help": "This a generic color picker",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.color_picker,
    label="Choose Theme Color",
    value="#FF0000"
)
```

**Returns**: Hex color string

---

#### FeedbackRepresentation

Feedback/rating widget.

**Component**: `st.feedback`

**Default Configuration**:
```python
{
    "options": "stars",
    "key": str(uuid4()),
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.feedback,
    options="thumbs"  # or "stars", "faces"
)
```

---

#### PillsRepresentation

Pill-style selection widget.

**Component**: `st.pills`

**Default Configuration**:
```python
{
    "label": "Pills",
    "options": ["Option 1", "Option 2", "Option 3"],
    "key": str(uuid4()),
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.pills,
    label="Categories",
    options=["Tech", "Business", "Sports"]
)
```

---

#### SegmentedControlRepresentation

Segmented control widget for exclusive selection.

**Component**: `st.segmented_control`

**Default Configuration**:
```python
{
    "label": "Segmented Control",
    "options": ["Option 1", "Option 2", "Option 3"],
    "key": str(uuid4()),
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.segmented_control,
    label="View Mode",
    options=["List", "Grid", "Table"]
)
```

---

### Media Input Widgets

Widgets for media capture and file upload.

**Location**: `declarative_streamlit/config/common/widgets/media.py`

#### FileUploaderRepresentation

File upload widget.

**Component**: `st.file_uploader`

**Default Configuration**:
```python
{
    "label": "File Uploader",
    "key": str(uuid4()),
    "help": "This a generic file uploader",
    "type": ["csv", "txt"],
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.file_uploader,
    label="Upload Image",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)
```

**Common Parameters**:
- `type` (list): Allowed file extensions
- `accept_multiple_files` (bool): Allow multiple files

**Returns**: UploadedFile object or None

---

#### DataEditorRepresentation

Interactive data table editor.

**Component**: `st.data_editor`

**Default Configuration**:
```python
{
    "data": {},
    "key": str(uuid4()),
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
import pandas as pd

df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
app.add_component(
    st.data_editor,
    data=df,
    num_rows="dynamic"
)
```

**Returns**: Edited dataframe

---

#### CameraInputRepresentation

Webcam capture widget.

**Component**: `st.camera_input`

**Default Configuration**:
```python
{
    "label": "Camera Input",
    "key": str(uuid4()),
    "help": "This a generic camera input",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.camera_input,
    label="Take a photo"
)
```

**Returns**: Image file or None

---

#### AudioInputRepresentation

Audio recording widget.

**Component**: `st.audio_input`

**Default Configuration**:
```python
{
    "label": "Audio Input",
    "key": str(uuid4()),
    "help": "This a generic audio input",
}
```

**Behavioral Flags**: Standard widget flags

**Usage Example**:
```python
app.add_component(
    st.audio_input,
    label="Record audio"
)
```

**Returns**: Audio file or None

---

## Common Widget Patterns

### State Management

All widgets automatically manage state via unique keys:

```python
# State is preserved across reruns
button_clicked = app.add_component(
    st.button,
    "Click Me",
    key="my_button"
)

if button_clicked:
    st.write("Button was clicked!")
```

### Callbacks

Widgets support callback functions:

```python
def on_button_click():
    st.session_state.counter += 1

app.add_component(
    st.button,
    "Increment",
    on_click=on_button_click
)
```

### Disabled State

Most widgets support disabled parameter:

```python
app.add_component(
    st.text_input,
    "Username",
    disabled=True
)
```

### Help Text

All widgets support tooltip help:

```python
app.add_component(
    st.slider,
    "Value",
    help="Adjust the slider to change the value"
)
```

## Widget Lifecycle

1. **Initialization**: Widget representation created with defaults
2. **Registration**: Added to standard registry
3. **Lookup**: Retrieved when component added to app
4. **Parser Creation**: `generic_factory()` creates parser
5. **Rendering**: Parser renders widget with merged configuration
6. **State Management**: Widget state tracked in session state
7. **Rerun**: State persists across reruns

## Version Compatibility

All widget implementations include import fallbacks:

```python
try:
    from streamlit import widget_name
except ImportError:
    def widget_name(*args, **kwargs):
        st.warning("Widget not available in this Streamlit version")
        return None
```

This ensures graceful degradation with older Streamlit versions.

## Best Practices

1. **Always provide unique keys** for stateful widgets
2. **Use meaningful labels** for accessibility
3. **Provide help text** for complex widgets
4. **Set appropriate min/max values** for numeric inputs
5. **Handle None returns** from file upload widgets
6. **Use callbacks** for complex state management
7. **Test with disabled state** for form validation
8. **Consider mobile** when choosing widget types

## Related Documentation

- [Common Representations](./common-representations.md) - Base implementation
- [Containers Reference](./containers-reference.md) - Layout containers
- [Elements Reference](./elements-reference.md) - Display elements
- [Standards System](./standards.md) - Widget registration

## Conclusion

The widget system provides a comprehensive, type-safe collection of interactive components for building Streamlit applications. By leveraging the representation pattern with sensible defaults and consistent configuration, widgets enable rapid development of user interfaces while maintaining flexibility and extensibility.
