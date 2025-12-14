# Containers Reference

## Overview

Containers are **layout and organizational components** that manage the structure and arrangement of other components. They enable hierarchical UI construction and provide context for child elements.

**Locations**: 
- `declarative_streamlit/config/common/containers/rowbased.py`
- `declarative_streamlit/config/common/containers/columbased.py`
- `declarative_streamlit/config/common/containers/status.py`

## Container Characteristics

Containers differ from widgets and elements in several ways:

- **Non-Stateful**: `stateful=False` (except where noted)
- **Fatal**: `fatal=True` - Layout errors are critical
- **Strict**: `strict=True` - Enforce validation
- **Layout Behavior**: Determined by `column_based` flag

### Layout Types

#### Row-Based Containers
Stack children **vertically** (top to bottom).
- `column_based=False`
- **Examples**: `container`, `expander`, `form`

#### Column-Based Containers
Arrange children **horizontally** (left to right).
- `column_based=True`
- **Examples**: `columns`, `tabs`

## Container Categories

### Row-Based Containers

Layout containers that organize content vertically.

**Location**: `declarative_streamlit/config/common/containers/rowbased.py`

#### ContainerRepresentation

Generic container for grouping components.

**Component**: `st.container`

**Default Configuration**:
```python
{
    # No default kwargs
}
```

**Behavioral Flags**:
- `stateful=False`
- `fatal=True`
- `strict=True`
- `column_based=False`

**Purpose**: 
- Group related components
- Control rendering order
- Create logical sections

**Usage Example**:
```python
with app.add_container(st.container) as container:
    container.add_component(st.header, "Section 1")
    container.add_component(st.write, "Content here")
```

**Advanced Features**:
- **Border**: Add visual borders
- **Height**: Set fixed height

**Example with Options**:
```python
with app.add_container(st.container, border=True, height=300) as c:
    c.add_component(st.write, "Bordered container")
```

---

#### ExpanderRepresentation

Collapsible container with expand/collapse functionality.

**Component**: `st.expander`

**Default Configuration**:
```python
{
    "label": "Expander",
    "expanded": True,
}
```

**Behavioral Flags**: Same as ContainerRepresentation

**Purpose**:
- Hide/show optional content
- Reduce visual clutter
- Progressive disclosure

**Usage Example**:
```python
with app.add_container(
    st.expander,
    label="Advanced Options",
    expanded=False
) as expander:
    expander.add_component(st.slider, "Setting 1")
    expander.add_component(st.checkbox, "Option 1")
```

**Common Parameters**:
- `label` (str): Expander header text
- `expanded` (bool): Initial state (default: False)

**Use Cases**:
- Advanced settings
- Additional information
- Optional configurations
- FAQ sections

---

#### FormRepresentation

Form container for batched input submission.

**Component**: `st.form`

**Default Configuration**:
```python
{
    "key": str(uuid4()),
}
```

**Behavioral Flags**: Same as ContainerRepresentation

**Purpose**:
- Batch widget interactions
- Submit multiple inputs together
- Prevent individual widget reruns

**Usage Example**:
```python
with app.add_container(st.form, key="my_form") as form:
    form.add_component(st.text_input, "Name")
    form.add_component(st.number_input, "Age")
    form.add_component(st.form_submit_button, "Submit")
```

**Important Notes**:
- **Requires unique key**: Forms must have a unique identifier
- **Submit button required**: Forms need `st.form_submit_button`
- **No reruns**: Widgets inside forms don't trigger reruns individually
- **Nested forms prohibited**: Cannot nest forms

**Common Parameters**:
- `key` (str): **Required** - Unique form identifier
- `clear_on_submit` (bool): Clear form after submission

**Form Workflow**:
1. User interacts with widgets inside form
2. No reruns occur until submit button clicked
3. Submit button triggers rerun with all form values
4. Form values accessible via session state

**Example with Callback**:
```python
def handle_submit():
    name = st.session_state.name_input
    age = st.session_state.age_input
    st.write(f"Submitted: {name}, {age}")

with app.add_container(st.form, key="user_form") as form:
    form.add_component(st.text_input, "Name", key="name_input")
    form.add_component(st.number_input, "Age", key="age_input")
    form.add_component(
        st.form_submit_button,
        "Submit",
        on_click=handle_submit
    )
```

---

#### PopoverRepresentation

Popup container triggered by interaction.

**Component**: `st.popover`

**Default Configuration**:
```python
{
    "label": "Popover",
    "expanded": True,
}
```

**Behavioral Flags**: Same as ContainerRepresentation

**Purpose**:
- Contextual information
- Secondary actions
- Space-saving UI

**Usage Example**:
```python
with app.add_container(st.popover, label="More Info") as popover:
    popover.add_component(st.write, "Additional details")
    popover.add_component(st.button, "Action")
```

**Common Parameters**:
- `label` (str): Trigger button text
- `disabled` (bool): Disable popover
- `help` (str): Tooltip for trigger

**Use Cases**:
- Contextual help
- Additional actions
- Filters and settings
- Tooltips with interactive content

---

#### ChatMessageRepresentation

Chat message container with role-based styling.

**Component**: `st.chat_message`

**Default Configuration**:
```python
{
    "name": "assistant",
}
```

**Behavioral Flags**: Same as ContainerRepresentation

**Purpose**:
- Chat interfaces
- Conversational UI
- Role-based message display

**Usage Example**:
```python
with app.add_container(st.chat_message, name="user") as message:
    message.add_component(st.write, "Hello, assistant!")

with app.add_container(st.chat_message, name="assistant") as response:
    response.add_component(st.write, "Hello! How can I help?")
```

**Common Parameters**:
- `name` (str): Role identifier ("user", "assistant", "ai", etc.)
- `avatar` (str): Avatar image or emoji

**Built-in Roles**:
- `"user"`: User messages (typically right-aligned)
- `"assistant"` / `"ai"`: AI responses (typically left-aligned)
- Custom roles supported

**Example with Avatar**:
```python
with app.add_container(
    st.chat_message,
    name="assistant",
    avatar="🤖"
) as msg:
    msg.add_component(st.write, "I'm a robot!")
```

---

### Column-Based Containers

Layout containers that arrange content horizontally.

**Location**: `declarative_streamlit/config/common/containers/columbased.py`

#### ColumnsRepresentation

Multi-column horizontal layout.

**Component**: `st.columns`

**Default Configuration**:
```python
{
    # No default kwargs
}
```

**Behavioral Flags**:
- `stateful=False`
- `fatal=True`
- `strict=True`
- `column_based=True` ⭐ **Key difference**

**Purpose**:
- Side-by-side layouts
- Multi-column forms
- Dashboard layouts
- Responsive grids

**Usage Example (Equal Width)**:
```python
with app.add_container(st.columns, 3) as columns:
    columns.add_component(st.metric, "Metric 1", value=100)
    columns.add_component(st.metric, "Metric 2", value=200)
    columns.add_component(st.metric, "Metric 3", value=300)
```

**Usage Example (Custom Widths)**:
```python
with app.add_container(st.columns, [2, 1]) as columns:
    # First column is twice as wide as second
    columns.add_component(st.write, "Main content")
    columns.add_component(st.write, "Sidebar")
```

**Column Specification**:
- **Integer**: Number of equal-width columns
  - `st.columns(3)` → 3 equal columns
- **List of numbers**: Proportional widths
  - `st.columns([2, 1, 1])` → 50%, 25%, 25%
- **List of integers**: Exact ratios
  - `st.columns([3, 2])` → 3:2 ratio

**Common Parameters**:
- `spec` (int | list): Column specification
- `gap` (str): Gap size ("small", "medium", "large")

**Advanced Example**:
```python
with app.add_container(st.columns, [3, 1], gap="large") as cols:
    # Access individual columns by index
    cols.add_component(st.header, "Main Panel")
    cols.add_component(st.sidebar, "Controls")
```

**Best Practices**:
- Limit to 3-4 columns for readability
- Use proportional widths for responsive design
- Consider mobile viewing (columns stack vertically)

---

#### TabsRepresentation

Tabbed navigation container.

**Component**: `st.tabs`

**Default Configuration**:
```python
{
    # No default kwargs
}
```

**Behavioral Flags**:
- `stateful=False`
- `fatal=True`
- `strict=True`
- `column_based=True` ⭐

**Purpose**:
- Organize related content
- Multi-view interfaces
- Navigation without page reload
- Space-efficient layouts

**Usage Example**:
```python
with app.add_container(
    st.tabs,
    ["Tab 1", "Tab 2", "Tab 3"]
) as tabs:
    tabs.add_component(st.write, "Content for Tab 1")
    tabs.add_component(st.write, "Content for Tab 2")
    tabs.add_component(st.write, "Content for Tab 3")
```

**Tab Specification**:
- **List of strings**: Tab labels
  - `st.tabs(["Overview", "Details", "Settings"])`

**Important Notes**:
- **Order matters**: Components added to tabs in sequence
- **One component per tab**: Each `add_component()` goes to next tab
- **Cannot skip tabs**: Must add content to all tabs

**Advanced Example**:
```python
tab_names = ["📊 Dashboard", "⚙️ Settings", "ℹ️ About"]

with app.add_container(st.tabs, tab_names) as tabs:
    # Tab 1: Dashboard
    tabs.add_component(st.metric, "Users", value=1000)
    
    # Tab 2: Settings
    tabs.add_component(st.slider, "Threshold")
    
    # Tab 3: About
    tabs.add_component(st.write, "Version 1.0")
```

**Use Cases**:
- Multi-step forms
- Different data views
- Settings categories
- Documentation sections

---

### Status Containers

Contextual containers for status indication and loading states.

**Location**: `declarative_streamlit/config/common/containers/status.py`

#### StatusRepresentation

Status indicator container with collapsible content.

**Component**: `st.status`

**Default Configuration**:
```python
{
    "label": "Status",
    "expanded": True,
}
```

**Behavioral Flags**: Same as ContainerRepresentation (row-based)

**Purpose**:
- Show operation progress
- Display status messages
- Collapsible status details

**Usage Example**:
```python
with app.add_container(
    st.status,
    label="Processing...",
    expanded=True
) as status:
    status.add_component(st.write, "Step 1: Loading data")
    # Perform operation
    status.add_component(st.write, "Step 2: Processing")
    # Continue...
```

**Common Parameters**:
- `label` (str): Status header text
- `expanded` (bool): Initial expansion state
- `state` (str): Status state ("running", "complete", "error")

**Dynamic Status Updates**:
```python
with app.add_container(st.status, "Processing") as status:
    status.add_component(st.write, "Loading...")
    time.sleep(1)
    status.add_component(st.write, "✓ Complete")
    status.update(label="Done", state="complete", expanded=False)
```

**States**:
- `"running"`: Spinner icon, blue color
- `"complete"`: Checkmark icon, green color
- `"error"`: X icon, red color

---

#### SpinnerRepresentation

Loading spinner container.

**Component**: `st.spinner`

**Default Configuration**:
```python
{
    "text": "Spinner",
}
```

**Behavioral Flags**: Same as ContainerRepresentation

**Purpose**:
- Show loading state
- Block UI during operations
- Provide feedback for async operations

**Usage Example**:
```python
with app.add_container(st.spinner, text="Loading data...") as spinner:
    # Long-running operation
    data = load_data()
    spinner.add_component(st.write, data)
```

**Common Parameters**:
- `text` (str): Loading message

**Typical Pattern**:
```python
with st.spinner("Processing..."):
    time.sleep(2)  # Simulated work
    result = process_data()
# Spinner disappears after context exits
st.write(result)
```

**Use Cases**:
- Data loading
- API calls
- Heavy computations
- File processing

---

## Container Usage Patterns

### Nesting Containers

Containers can be nested for complex layouts:

```python
with app.add_container(st.container, border=True) as outer:
    outer.add_component(st.header, "Dashboard")
    
    with outer.add_container(st.columns, 2) as cols:
        cols.add_component(st.metric, "Metric 1", value=100)
        cols.add_component(st.metric, "Metric 2", value=200)
    
    with outer.add_container(st.expander, "Details") as exp:
        exp.add_component(st.write, "Additional information")
```

### Responsive Layouts

Use columns with proportional widths:

```python
# Desktop: 70% content, 30% sidebar
# Mobile: Stacks automatically
with app.add_container(st.columns, [7, 3]) as layout:
    layout.add_component(st.write, "Main content area")
    layout.add_component(st.write, "Sidebar area")
```

### Conditional Containers

Show/hide containers based on state:

```python
show_advanced = st.checkbox("Show Advanced Options")

if show_advanced:
    with app.add_container(st.expander, "Advanced") as adv:
        adv.add_component(st.slider, "Parameter 1")
        adv.add_component(st.slider, "Parameter 2")
```

### Loading States

Combine spinners with status:

```python
with st.spinner("Loading..."):
    with app.add_container(st.status, "Processing") as status:
        status.add_component(st.write, "Step 1")
        # Work...
        status.add_component(st.write, "Step 2")
```

## Container Lifecycle

1. **Creation**: Container representation defined
2. **Context Entry**: `with` statement enters container context
3. **Child Addition**: Components added to container
4. **Rendering**: Container and children rendered in order
5. **Context Exit**: Container context closes

## Layout Best Practices

### Column Design

1. **Limit columns**: 2-4 columns maximum for readability
2. **Use proportions**: Relative widths adapt better than fixed
3. **Consider mobile**: Columns stack vertically on small screens
4. **Gap spacing**: Use appropriate gaps for visual separation

### Container Hierarchy

1. **Logical grouping**: Group related components
2. **Visual hierarchy**: Use nested containers for structure
3. **Consistent depth**: Avoid excessive nesting (3-4 levels max)
4. **Border usage**: Use borders sparingly for emphasis

### Performance

1. **Lazy loading**: Use expanders for optional heavy content
2. **Conditional rendering**: Don't render hidden containers
3. **Form batching**: Use forms to prevent excessive reruns
4. **Minimal nesting**: Reduce container depth for faster rendering

## Accessibility

### Labels and Context

- **Meaningful labels**: Use descriptive expander/tab labels
- **Logical order**: Arrange content in reading order
- **Visual hierarchy**: Maintain clear parent-child relationships

### Keyboard Navigation

- **Tab order**: Containers preserve natural tab order
- **Focus management**: Ensure focusable elements accessible
- **Shortcuts**: Consider keyboard shortcuts for tabs

## Common Patterns

### Dashboard Layout

```python
# Header
app.add_component(st.title, "Dashboard")

# Metrics row
with app.add_container(st.columns, 4) as metrics:
    metrics.add_component(st.metric, "Users", 1000)
    metrics.add_component(st.metric, "Revenue", "$50k")
    metrics.add_component(st.metric, "Growth", "↑ 12%")
    metrics.add_component(st.metric, "Churn", "2.3%")

# Main content with sidebar
with app.add_container(st.columns, [2, 1]) as layout:
    # Main chart
    layout.add_component(st.line_chart, data)
    
    # Sidebar filters
    with layout.add_container(st.container) as sidebar:
        sidebar.add_component(st.selectbox, "Time Range")
        sidebar.add_component(st.multiselect, "Categories")
```

### Multi-Step Form

```python
with app.add_container(st.tabs, ["Step 1", "Step 2", "Step 3"]) as steps:
    # Step 1: Basic Info
    with steps.add_container(st.form, "step1") as form1:
        form1.add_component(st.text_input, "Name")
        form1.add_component(st.form_submit_button, "Next")
    
    # Step 2: Details
    with steps.add_container(st.form, "step2") as form2:
        form2.add_component(st.text_area, "Description")
        form2.add_component(st.form_submit_button, "Next")
    
    # Step 3: Confirm
    steps.add_component(st.write, "Review and submit")
```

### Settings Panel

```python
with app.add_container(st.expander, "⚙️ Settings") as settings:
    with settings.add_container(st.tabs, ["General", "Advanced"]) as tabs:
        # General settings
        tabs.add_component(st.toggle, "Dark Mode")
        tabs.add_component(st.selectbox, "Language")
        
        # Advanced settings
        tabs.add_component(st.slider, "Cache Size")
        tabs.add_component(st.number_input, "Timeout")
```

## Error Handling

### Invalid Nesting

```python
# ❌ Invalid: Forms cannot be nested
with st.form("outer"):
    with st.form("inner"):  # Error!
        pass

# ✓ Valid: Use separate forms
with st.form("form1"):
    pass
with st.form("form2"):
    pass
```

### Missing Submit Button

```python
# ❌ Invalid: Form without submit button
with st.form("my_form"):
    st.text_input("Name")
    # Missing form_submit_button!

# ✓ Valid: Include submit button
with st.form("my_form"):
    st.text_input("Name")
    st.form_submit_button("Submit")
```

## Version Compatibility

All container implementations include fallbacks:

```python
try:
    from streamlit import container
except ImportError:
    def container(*args, **kwargs):
        st.warning("Container not available")
        return None
```

## Related Documentation

- [Widgets Reference](./widgets-reference.md) - Interactive components
- [Elements Reference](./elements-reference.md) - Display components
- [Common Representations](./common-representations.md) - Base implementation
- [Standards System](./standards.md) - Container registration

## Conclusion

Containers provide powerful layout and organizational capabilities for building structured Streamlit applications. Understanding the distinction between row-based and column-based containers, along with proper nesting patterns, enables creation of sophisticated, maintainable user interfaces. The representation system ensures consistent configuration while maintaining flexibility for complex layouts.
