import streamlit as st
from typing import Any
from uuid import uuid4
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import number_input
except ImportError:
    def number_input(*args: Any, **kwargs: Any) -> Any:
        st.warning("Number Input component not available in this Streamlit version")
        return None

try:
    from streamlit import slider
except ImportError:
    def slider(*args: Any, **kwargs: Any) -> Any:
        st.warning("Slider component not available in this Streamlit version")
        return None

try:
    from streamlit import date_input
except ImportError:
    def date_input(*args: Any, **kwargs: Any) -> Any:
        st.warning("Date Input component not available in this Streamlit version")
        return None

try:
    from streamlit import time_input
except ImportError:
    def time_input(*args: Any, **kwargs: Any) -> Any:
        st.warning("Time Input component not available in this Streamlit version")
        return None

try:
    from streamlit import text_input
except ImportError:
    def text_input(*args: Any, **kwargs: Any) -> Any:
        st.warning("Text Input component not available in this Streamlit version")
        return None

try:
    from streamlit import text_area
except ImportError:
    def text_area(*args: Any, **kwargs: Any) -> Any:
        st.warning("Text Area component not available in this Streamlit version")
        return None




class NumberInputRepresentation(CommonRepresentation[number_input]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Number Input",
                "min_value": 0,
                "max_value": 100,
                "value": 50,
                "step": 1,
                "key": str(uuid4()),
                "help": "This a generic number input",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(number_input)


class SliderRepresentation(CommonRepresentation[slider]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Slider",
                "min_value": 0,
                "max_value": 100,
                "step": 1,
                "key": str(uuid4()),
                "help": "This a generic slider",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(slider)


class DateInputRepresentation(CommonRepresentation[date_input]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Date Input",
                "value": "today",
                "key": str(uuid4()),
                "help": "This a generic date input",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(date_input)


class TimeInputRepresentation(CommonRepresentation[time_input]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Time Input",
                "value": "now",
                "key": str(uuid4()),
                "help": "This a generic time input",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(time_input)

class TextInputRepresentation(CommonRepresentation[text_input]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Text Input",
                "value": "",
                "key": str(uuid4()),
                "help": "This a generic text input",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(text_input)

class TextAreaRepresentation(CommonRepresentation[text_area]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Text Area",
                "value": "",
                "key": str(uuid4()),
                "help": "This a generic text area",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(text_area)

try:
    from streamlit import chat_input
except ImportError:
    def chat_input(*args: Any, **kwargs: Any) -> Any:
        st.warning("Chat Input component not available in this Streamlit version")
        return None


class ChatInputRepresentation(CommonRepresentation[chat_input]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "placeholder": "Type your message here...",
                "key": str(uuid4()),
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(chat_input)