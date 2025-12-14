import streamlit as st
from typing import Any
from uuid import uuid4
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import button
except ImportError:
    def button(*args: Any, **kwargs: Any) -> Any:
        st.warning("Button component not available in this Streamlit version")
        return None

try:
    from streamlit import download_button
except ImportError:
    def download_button(*args: Any, **kwargs: Any) -> Any:
        st.warning("Download Button component not available in this Streamlit version")
        return None

try:
    from streamlit import form_submit_button
except ImportError:
    def form_submit_button(*args: Any, **kwargs: Any) -> Any:
        st.warning("Form Submit Button component not available in this Streamlit version")
        return None

try:
    from streamlit import link_button
except ImportError:
    def link_button(*args: Any, **kwargs: Any) -> Any:
        st.warning("Link Button component not available in this Streamlit version")
        return None

try:
    from streamlit import page_link
except ImportError:
    def page_link(*args: Any, **kwargs: Any) -> Any:
        st.warning("Page Link component not available in this Streamlit version")
        return None

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