import streamlit as st
from typing import Any
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import header
except ImportError:
    def header(*args: Any, **kwargs: Any) -> Any:
        st.warning("Header component not available in this Streamlit version")
        return None

try:
    from streamlit import subheader
except ImportError:
    def subheader(*args: Any, **kwargs: Any) -> Any:
        st.warning("Subheader component not available in this Streamlit version")
        return None

try:
    from streamlit import title
except ImportError:
    def title(*args: Any, **kwargs: Any) -> Any:
        st.warning("Title component not available in this Streamlit version")
        return None

try:
    from streamlit import caption
except ImportError:
    def caption(*args: Any, **kwargs: Any) -> Any:
        st.warning("Caption component not available in this Streamlit version")
        return None

try:
    from streamlit import markdown
except ImportError:
    def markdown(*args: Any, **kwargs: Any) -> Any:
        st.warning("Markdown component not available in this Streamlit version")
        return None

try:
    from streamlit import code
except ImportError:
    def code(*args: Any, **kwargs: Any) -> Any:
        st.warning("Code component not available in this Streamlit version")
        return None

try:
    from streamlit import latex
except ImportError:
    def latex(*args: Any, **kwargs: Any) -> Any:
        st.warning("Latex component not available in this Streamlit version")
        return None

try:
    from streamlit import text
except ImportError:
    def text(*args: Any, **kwargs: Any) -> Any:
        st.warning("Text component not available in this Streamlit version")
        return None


class HeaderRepresentation(CommonRepresentation[header]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "Header",
                "help": "This a generic header",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(header)


class SubheaderRepresentation(CommonRepresentation[subheader]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "Subheader",
                "help": "This a generic subheader",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(subheader)

class TitleRepresentation(CommonRepresentation[title]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "Title",
                "help": "This a generic title",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(title)

class CaptionRepresentation(CommonRepresentation[caption]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "Caption",
                "help": "This a generic caption",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(caption)

class MarkdownRepresentation(CommonRepresentation[markdown]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "Markdown",
                "help": "This a generic markdown",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(markdown)

class CodeRepresentation(CommonRepresentation[code]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "print('Hello World')",
                "language": "python",
                "line_numbers": True,
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(code)


class LatexRepresentation(CommonRepresentation[latex]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": r"e^{i \pi} + 1 = 0",
                "help": "This a generic latex",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(latex)

class TextRepresentation(CommonRepresentation[text]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "Text",
                "help": "This a generic text",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(text)


try:
    from streamlit import html
except ImportError:
    def html(*args: Any, **kwargs: Any) -> Any:
        st.warning("HTML component not available in this Streamlit version")
        return None

class HtmlRepresentation(CommonRepresentation[html]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "<h1>HTML</h1>",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(html)


try:
    from streamlit import badge
except ImportError:
    def badge(*args: Any, **kwargs: Any) -> Any:
        st.warning("Badge component not available in this Streamlit version")
        return None

class BadgeRepresentation(CommonRepresentation[badge]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Badge",
                "icon": ":material/thumb_up:",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(badge)