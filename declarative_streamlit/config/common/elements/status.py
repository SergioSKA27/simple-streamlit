from streamlit import success,error,warning,info
from ..representation import CommonRepresentation

class SuccessRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "Success",
                "icon": ":material/check_circle:",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(success)

class ErrorRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "Error",
                "icon": ":material/error:",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(error)

class WarningRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "Warning",
                "icon": ":material/warning:",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(warning)

class InfoRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": "Info",
                "icon": ":material/info:",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(info)