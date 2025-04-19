from uuid import uuid4
from streamlit import container, expander, form
from ..representation import CommonRepresentation


class ContainerRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(container)


class ExpanderRepresentation(CommonRepresentation):
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


class FormRepresentation(CommonRepresentation):
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
    popover = None


class PopoverRepresentation(CommonRepresentation):
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

        self.set_type(popover) if popover is not None else None


try:
    from streamlit import chat_message
except ImportError:
    chat_message = None


class ChatMessageRepresentation(CommonRepresentation):
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

        self.set_type(chat_message) if chat_message is not None else None
