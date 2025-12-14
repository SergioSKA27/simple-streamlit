from streamlit import number_input,slider,date_input,time_input,text_input,text_area
from uuid import uuid4
from ..representation import CommonRepresentation




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
    chat_input = None


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