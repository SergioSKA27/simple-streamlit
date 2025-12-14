import streamlit as st
from typing import Any
from uuid import uuid4
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import container
except ImportError:
    def container(*args: Any, **kwargs: Any) -> Any:
        st.warning("Container component not available in this Streamlit version")
        return None

try:
    from streamlit import expander
except ImportError:
    def expander(*args: Any, **kwargs: Any) -> Any:
        st.warning("Expander component not available in this Streamlit version")
        return None

try:
    from streamlit import form
except ImportError:
    def form(*args: Any, **kwargs: Any) -> Any:
        st.warning("Form component not available in this Streamlit version")
        return None


class ContainerRepresentation(CommonRepresentation[container]):
    def __init__(self) -> None:
        super().__init__(
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(container)


class ExpanderRepresentation(CommonRepresentation[expander]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Expander",
                "expanded": True,
            },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(expander)


class FormRepresentation(CommonRepresentation[form]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "key": str(uuid4()),
            },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(form)


try:
    from streamlit import popover
except ImportError:
    def popover(*args: Any, **kwargs: Any) -> Any:
        st.warning("Popover component not available in this Streamlit version")
        return None


class PopoverRepresentation(CommonRepresentation[popover]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Popover",
                "expanded": True,
            },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(popover)


try:
    from streamlit import chat_message
except ImportError:
    def chat_message(*args: Any, **kwargs: Any) -> Any:
        st.warning("Chat Message component not available in this Streamlit version")
        return None


class ChatMessageRepresentation(CommonRepresentation[chat_message]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "name": "ai",
            },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(chat_message)
