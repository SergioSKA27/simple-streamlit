# Elements Reference

## Overview

Elements are **display-only components** that present information to users without capturing input or maintaining state. This document provides a comprehensive reference for all element representations available in the declarative Streamlit library.

**Locations**:
- `declarative_streamlit/config/common/elements/text.py`
- `declarative_streamlit/config/common/elements/data.py`
- `declarative_streamlit/config/common/elements/media.py`
- `declarative_streamlit/config/common/elements/status.py`

## Element Characteristics

All elements share these common characteristics:

- **Non-Stateful**: `stateful=False` - Do not maintain state across reruns
- **Fatal**: `fatal=True` - Rendering errors are critical
- **Strict**: `strict=True` - Enforce validation
- **Non-Column-Based**: `column_based=False` - Not layout containers
- **No Keys**: Generally do not require unique identifiers

## Element Categories

### Text Elements

Components for displaying formatted text content.

**Location**: `declarative_streamlit/config/common/elements/text.py`

#### MarkdownRepresentation

Render Markdown-formatted text.

**Component**: `st.markdown`

**Default Configuration**:
```python
{
    "body": "Markdown",
    "help": "This a generic markdown",
}
```

**Behavioral Flags**:
- `stateful=False`
- `fatal=True`
- `strict=True`
- `column_based=False`

**Usage Example**:
```python
app.add_component(
    st.markdown,
    """
    # Heading
    **Bold** and *italic* text
    - List item 1
    - List item 2
    """
)
```

**Supported Markdown**:
- Headings (#, ##, ###)
- Bold (**text**) and italic (*text*)
- Lists (ordered and unordered)
- Links [text](url)
- Code blocks (```)
- Inline code (`code`)
- Blockquotes (>)
- Tables

**HTML Support**:
```python
app.add_component(
    st.markdown,
    '<span style="color: red">Red text</span>',
    unsafe_allow_html=True
)
```

**Common Parameters**:
- `body` (str): Markdown content
- `unsafe_allow_html` (bool): Allow raw HTML (use carefully)
- `help` (str): Tooltip text

---

#### TextRepresentation

Display plain text.

**Component**: `st.text`

**Default Configuration**:
```python
{
    "body": "Text",
    "help": "This a generic text",
}
```

**Behavioral Flags**: Same as MarkdownRepresentation

**Usage Example**:
```python
app.add_component(st.text, "Simple text without formatting")
```

**Characteristics**:
- No Markdown interpretation
- Preserves whitespace and newlines
- Monospace font
- Good for code snippets, logs, ASCII art

---

#### HeaderRepresentation

Large header text.

**Component**: `st.header`

**Default Configuration**:
```python
{
    "body": "Header",
    "help": "This a generic header",
}
```

**Behavioral Flags**: Same as MarkdownRepresentation

**Usage Example**:
```python
app.add_component(st.header, "Section Title")
```

**Visual Hierarchy**:
- Larger than subheader
- Smaller than title
- Used for major sections

---

#### SubheaderRepresentation

Medium header text.

**Component**: `st.subheader`

**Default Configuration**:
```python
{
    "body": "Subheader",
    "help": "This a generic subheader",
}
```

**Behavioral Flags**: Same as MarkdownRepresentation

**Usage Example**:
```python
app.add_component(st.subheader, "Subsection Title")
```

**Visual Hierarchy**:
- Smaller than header
- Used for subsections

---

#### TitleRepresentation

Largest header text (page title).

**Component**: `st.title`

**Default Configuration**:
```python
{
    "body": "Title",
    "help": "This a generic title",
}
```

**Behavioral Flags**: Same as MarkdownRepresentation

**Usage Example**:
```python
app.add_component(st.title, "Dashboard Application")
```

**Visual Hierarchy**:
- Largest text element
- Typically used once per page
- Page/app title

---

#### CaptionRepresentation

Small caption text.

**Component**: `st.caption`

**Default Configuration**:
```python
{
    "body": "Caption",
    "help": "This a generic caption",
}
```

**Behavioral Flags**: Same as MarkdownRepresentation

**Usage Example**:
```python
app.add_component(st.caption, "Last updated: 2024-01-01")
```

**Characteristics**:
- Smallest text size
- Muted color
- Used for metadata, footnotes

---

#### CodeRepresentation

Display syntax-highlighted code.

**Component**: `st.code`

**Default Configuration**:
```python
{
    "body": "Code",
    "language": "python",
}
```

**Behavioral Flags**: Same as MarkdownRepresentation

**Usage Example**:
```python
app.add_component(
    st.code,
    '''
def hello_world():
    print("Hello, World!")
    ''',
    language="python"
)
```

**Supported Languages**:
- Python, JavaScript, Java, C++, C#
- HTML, CSS, SQL
- JSON, YAML, XML
- Bash, PowerShell
- Many more via Pygments

**Common Parameters**:
- `body` (str): Code content
- `language` (str): Syntax highlighting language
- `line_numbers` (bool): Show line numbers

---

#### LatexRepresentation

Render LaTeX mathematical expressions.

**Component**: `st.latex`

**Default Configuration**:
```python
{
    "body": r"\LaTeX",
}
```

**Behavioral Flags**: Same as MarkdownRepresentation

**Usage Example**:
```python
app.add_component(
    st.latex,
    r'''
    E = mc^2
    '''
)
```

**Advanced Example**:
```python
app.add_component(
    st.latex,
    r'''
    \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
    '''
)
```

**Use Cases**:
- Mathematical formulas
- Scientific equations
- Academic content

---

#### BadgeRepresentation

Display badge/pill component.

**Component**: `st.badge`

**Default Configuration**:
```python
{
    "body": "Badge",
}
```

**Behavioral Flags**: Same as MarkdownRepresentation

**Usage Example**:
```python
app.add_component(st.badge, "New")
app.add_component(st.badge, "Beta", type="warning")
```

**Common Parameters**:
- `body` (str): Badge text
- `type` (str): Badge style ("default", "info", "success", "warning", "error")

---

#### HtmlRepresentation

Render raw HTML content.

**Component**: `st.html`

**Default Configuration**:
```python
{
    "body": "<p>HTML</p>",
}
```

**Behavioral Flags**: Same as MarkdownRepresentation

**Usage Example**:
```python
app.add_component(
    st.html,
    """
    <div style="background: #f0f0f0; padding: 20px;">
        <h2>Custom HTML</h2>
        <p>Rich formatting</p>
    </div>
    """
)
```

**Security Warning**: Sanitize user input to prevent XSS attacks.

---

### Data Elements

Components for displaying structured data.

**Location**: `declarative_streamlit/config/common/elements/data.py`

#### DataFrameRepresentation

Display interactive dataframe.

**Component**: `st.dataframe`

**Default Configuration**:
```python
{
    "data": example_df,  # Sample DataFrame
    "key": str(uuid4()),
}
```

**Example DataFrame**:
```python
example_df = DataFrame({
    "Column 1": [1, 2, 3],
    "Column 2": ["A", "B", "C"],
    "Column 3": [True, False, True],
})
```

**Behavioral Flags**:
- `stateful=False`
- `fatal=True`
- `strict=True`
- `column_based=False`

**Usage Example**:
```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "London", "Paris"]
})

app.add_component(st.dataframe, df, use_container_width=True)
```

**Features**:
- Sortable columns
- Scrollable view
- Column resizing
- Search/filter (with styling)

**Common Parameters**:
- `data`: DataFrame, dict, list, or array
- `width` (int): Width in pixels
- `height` (int): Height in pixels
- `use_container_width` (bool): Fill container width
- `hide_index` (bool): Hide row index

**Styling**:
```python
styled_df = df.style.highlight_max(axis=0)
app.add_component(st.dataframe, styled_df)
```

---

#### TableRepresentation

Display static table.

**Component**: `st.table`

**Default Configuration**:
```python
{
    "data": example_df,
}
```

**Behavioral Flags**: Same as DataFrameRepresentation

**Usage Example**:
```python
app.add_component(st.table, df)
```

**Differences from Dataframe**:
- **Static**: No sorting or interaction
- **Full display**: Shows all rows (no scrolling)
- **Simpler**: No advanced features
- **Use case**: Small tables, final presentation

---

#### JSONRepresentation

Display JSON data with expandable tree.

**Component**: `st.json`

**Default Configuration**:
```python
{
    "body": example_df.to_json(),
    "expanded": True,
}
```

**Behavioral Flags**: Same as DataFrameRepresentation

**Usage Example**:
```python
data = {
    "name": "John",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York"
    }
}

app.add_component(st.json, data)
```

**Features**:
- Expandable/collapsible nodes
- Syntax highlighting
- Pretty printing
- Copy functionality

**Common Parameters**:
- `body`: Dict, list, or JSON string
- `expanded` (bool): Initially expanded

---

#### MetricRepresentation

Display KPI metric with optional delta.

**Component**: `st.metric`

**Default Configuration**:
```python
{
    "label": "Metric",
    "value": 100,
    "delta": 10,
    "help": "This a generic metric",
}
```

**Behavioral Flags**: Same as DataFrameRepresentation

**Usage Example**:
```python
app.add_component(
    st.metric,
    label="Revenue",
    value="$1.2M",
    delta="↑ 15%"
)
```

**Delta Colors**:
- Positive values: Green (by default)
- Negative values: Red (by default)
- Can be inverted with `delta_color="inverse"`

**Advanced Example**:
```python
col1, col2, col3 = st.columns(3)

with col1:
    app.add_component(st.metric, "Users", "1,234", "+12%")
with col2:
    app.add_component(st.metric, "Revenue", "$56K", "+8%")
with col3:
    app.add_component(
        st.metric,
        "Churn",
        "2.3%",
        "-0.5%",
        delta_color="inverse"  # Red is good for churn decrease
    )
```

---

### Media Elements

Components for displaying images, video, and audio.

**Location**: `declarative_streamlit/config/common/elements/media.py`

#### ImageRepresentation

Display images.

**Component**: `st.image`

**Default Configuration**:
```python
{
    "image": "https://picsum.photos/200/300",
    "caption": "This is generic image",
}
```

**Behavioral Flags**:
- `stateful=False`
- `fatal=True`
- `strict=True`
- `column_based=False`

**Usage Example**:
```python
app.add_component(
    st.image,
    "path/to/image.png",
    caption="My Image",
    use_column_width=True
)
```

**Supported Sources**:
- Local file paths
- URLs
- NumPy arrays
- PIL images
- BytesIO objects

**Common Parameters**:
- `image`: Image source
- `caption` (str): Image caption
- `width` (int): Display width
- `use_column_width` (bool): Fill column width
- `clamp` (bool): Clamp pixel values
- `channels` (str): "RGB" or "BGR"

**Multiple Images**:
```python
images = ["img1.png", "img2.png", "img3.png"]
app.add_component(st.image, images, width=200)
```

---

#### VideoRepresentation

Display video player.

**Component**: `st.video`

**Default Configuration**:
```python
{
    "data": "https://youtu.be/vrwoIZtQSuI?si=Q72tpS79GIZb06S5",
    "autoplay": True,
    "muted": True,
}
```

**Behavioral Flags**: Same as ImageRepresentation

**Usage Example**:
```python
app.add_component(
    st.video,
    "path/to/video.mp4",
    start_time=10
)
```

**Supported Sources**:
- Local video files
- YouTube URLs
- Video URLs
- Bytes

**Supported Formats**:
- MP4
- WebM
- OGG

**Common Parameters**:
- `data`: Video source
- `format` (str): MIME type (auto-detected)
- `start_time` (int): Start position in seconds
- `autoplay` (bool): Auto-play on load
- `muted` (bool): Start muted
- `loop` (bool): Loop playback

---

#### AudioRepresentation

Display audio player.

**Component**: `st.audio`

**Default Configuration**:
```python
{
    "data": "http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3",
}
```

**Behavioral Flags**: Same as ImageRepresentation

**Usage Example**:
```python
app.add_component(
    st.audio,
    "path/to/audio.mp3",
    format="audio/mp3"
)
```

**Supported Sources**:
- Local audio files
- Audio URLs
- Bytes

**Supported Formats**:
- MP3
- WAV
- OGG
- FLAC

**Common Parameters**:
- `data`: Audio source
- `format` (str): MIME type
- `start_time` (int): Start position
- `loop` (bool): Loop playback

---

### Status Elements

Components for displaying status messages and notifications.

**Location**: `declarative_streamlit/config/common/elements/status.py`

#### SuccessRepresentation

Display success message.

**Component**: `st.success`

**Default Configuration**:
```python
{
    "body": "Success",
    "icon": ":material/check_circle:",
}
```

**Behavioral Flags**:
- `stateful=False`
- `fatal=True`
- `strict=True`
- `column_based=False`

**Usage Example**:
```python
app.add_component(st.success, "Operation completed successfully!")
```

**Visual Style**:
- Green background
- Checkmark icon
- Success semantics

---

#### ErrorRepresentation

Display error message.

**Component**: `st.error`

**Default Configuration**:
```python
{
    "body": "Error",
    "icon": ":material/error:",
}
```

**Behavioral Flags**: Same as SuccessRepresentation

**Usage Example**:
```python
app.add_component(st.error, "An error occurred: Invalid input")
```

**Visual Style**:
- Red background
- Error icon
- Error semantics

---

#### WarningRepresentation

Display warning message.

**Component**: `st.warning`

**Default Configuration**:
```python
{
    "body": "Warning",
    "icon": ":material/warning:",
}
```

**Behavioral Flags**: Same as SuccessRepresentation

**Usage Example**:
```python
app.add_component(st.warning, "Please save your work before proceeding")
```

**Visual Style**:
- Yellow/amber background
- Warning icon
- Warning semantics

---

#### InfoRepresentation

Display informational message.

**Component**: `st.info`

**Default Configuration**:
```python
{
    "body": "Info",
    "icon": ":material/info:",
}
```

**Behavioral Flags**: Same as SuccessRepresentation

**Usage Example**:
```python
app.add_component(st.info, "ℹ️ Tip: You can use keyboard shortcuts")
```

**Visual Style**:
- Blue background
- Info icon
- Informational semantics

---

## Element Usage Patterns

### Text Hierarchy

```python
app.add_component(st.title, "Application Title")
app.add_component(st.header, "Section 1")
app.add_component(st.subheader, "Subsection 1.1")
app.add_component(st.markdown, "Body content with **formatting**")
app.add_component(st.caption, "Additional notes")
```

### Data Presentation

```python
# Metrics dashboard
with st.columns(3) as cols:
    cols.add_component(st.metric, "Users", "1,234", "+12%")
    cols.add_component(st.metric, "Revenue", "$56K", "+8%")
    cols.add_component(st.metric, "Growth", "15%", "+2%")

# Detailed data
app.add_component(st.dataframe, df, use_container_width=True)

# Summary table
app.add_component(st.table, summary_df)
```

### Status Messaging

```python
if success:
    app.add_component(st.success, "✓ Data saved successfully")
elif warning_condition:
    app.add_component(st.warning, "⚠️ Some fields are empty")
else:
    app.add_component(st.error, "❌ Failed to save data")
```

### Media Gallery

```python
with st.columns(3) as gallery:
    gallery.add_component(st.image, "img1.jpg", caption="Image 1")
    gallery.add_component(st.image, "img2.jpg", caption="Image 2")
    gallery.add_component(st.image, "img3.jpg", caption="Image 3")
```

## Best Practices

### Text Elements

1. **Use semantic hierarchy**: Title → Header → Subheader → Body
2. **Limit title usage**: Typically one per page
3. **Markdown for rich text**: Use markdown for formatted content
4. **Code for syntax**: Use `st.code()` for code blocks, not `st.text()`

### Data Elements

1. **Dataframe for interaction**: Use `st.dataframe` for sortable data
2. **Table for static**: Use `st.table` for small, final presentations
3. **Metrics for KPIs**: Use `st.metric` for key performance indicators
4. **JSON for API responses**: Use `st.json` for structured data inspection

### Media Elements

1. **Optimize images**: Compress images for faster loading
2. **Provide captions**: Always add descriptive captions
3. **Use column width**: Set `use_column_width=True` for responsive images
4. **Local > Remote**: Local files load faster than URLs

### Status Messages

1. **Appropriate severity**: Match message type to situation
2. **Clear messaging**: Be specific about what succeeded/failed
3. **Actionable**: Include next steps or remediation
4. **Temporary vs Permanent**: Consider if message should persist

## Performance Considerations

### Large DataFrames

```python
# For large data, limit rows displayed
app.add_component(st.dataframe, large_df.head(100))

# Or use pagination
page = st.slider("Page", 1, 10)
rows_per_page = 50
start = (page - 1) * rows_per_page
end = start + rows_per_page
app.add_component(st.dataframe, large_df.iloc[start:end])
```

### Image Optimization

```python
from PIL import Image

# Resize large images
img = Image.open("large_image.jpg")
img.thumbnail((800, 800))
app.add_component(st.image, img)
```

### Conditional Rendering

```python
# Only render expensive elements when needed
if st.checkbox("Show detailed data"):
    app.add_component(st.dataframe, expensive_data)
```

## Accessibility

### Alt Text and Labels

```python
# Images
app.add_component(st.image, "chart.png", caption="Sales trend chart")

# Metrics
app.add_component(st.metric, label="Monthly Revenue", value="$50K")
```

### Semantic HTML

```python
# Use appropriate heading levels
app.add_component(st.title, "Main Title")      # <h1>
app.add_component(st.header, "Section")        # <h2>
app.add_component(st.subheader, "Subsection")  # <h3>
```

### Color Independence

```python
# Don't rely solely on color
# Bad: app.add_component(st.markdown, '<span style="color: red">Error</span>')
# Good:
app.add_component(st.error, "❌ Error message")
```

## Version Compatibility

All element implementations include import fallbacks:

```python
try:
    from streamlit import metric
except ImportError:
    def metric(*args, **kwargs):
        st.warning("Metric component not available")
        return None
```

## Related Documentation

- [Widgets Reference](./widgets-reference.md) - Interactive components
- [Containers Reference](./containers-reference.md) - Layout containers
- [Common Representations](./common-representations.md) - Base implementation
- [Standards System](./standards.md) - Element registration

## Conclusion

Elements provide comprehensive display capabilities for presenting information in Streamlit applications. From text formatting and data visualization to media playback and status messaging, the element system offers a rich toolkit for building informative, accessible user interfaces. Understanding when to use each element type and following best practices ensures optimal performance and user experience.
