from streamlit import spinner,status
from ..representation import CommonRepresentation


class StatusRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Status",
                "expanded": True,
            },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(status)
    
class SpinnerRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "text": "Spinner",
            },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(spinner)