from streamlit import button,download_button,form_submit_button,link_button,page_link
from uuid import uuid4
from ..representation import CommonRepresentation

class ButtonRepresentation(CommonRepresentation[button]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Button",
                "key": str(uuid4()),
                "help": "This a generic button",                
            },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(button)

class DownloadButtonRepresentation(CommonRepresentation[download_button]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Download Button",
                "key": str(uuid4()),
                "help": "This a generic download button",
                "data": "Example data Text",
                "file_name": "example.txt",
                "mime": "text/plain",
                "on_click": "ignore",
            },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(download_button)


class FormSubmitButtonRepresentation(CommonRepresentation[form_submit_button]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Form Submit Button",
                "key": str(uuid4()),
                "help": "This a generic form submit button",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(form_submit_button)

class LinkButtonRepresentation(CommonRepresentation[link_button]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Link Button",
                "help": "This a generic link button",
                "url": "https://example.com",
            },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(link_button)

class PageLinkRepresentation(CommonRepresentation[page_link]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Page Link",
                "help": "This a generic page link",
            },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(page_link)