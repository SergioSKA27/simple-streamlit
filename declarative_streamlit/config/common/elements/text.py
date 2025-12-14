from streamlit import header, subheader, title, caption, markdown, code, latex,text
from ..representation import CommonRepresentation


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
    html = None

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

        self.set_type(html) if html else None


try:
    from streamlit import badge
except ImportError:
    badge = None

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

        self.set_type(badge) if badge else None