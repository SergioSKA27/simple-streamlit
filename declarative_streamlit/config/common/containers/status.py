from streamlit import spinner,status
from ..representation import CommonRepresentation


class StatusRepresentation(CommonRepresentation[status]):
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
    
class SpinnerRepresentation(CommonRepresentation[spinner]):
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