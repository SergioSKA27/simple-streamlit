import streamlit as st
from typing import Any
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import success
except ImportError:
    def success(*args: Any, **kwargs: Any) -> Any:
        st.warning("Success component not available in this Streamlit version")
        return None

try:
    from streamlit import error
except ImportError:
    def error(*args: Any, **kwargs: Any) -> Any:
        st.warning("Error component not available in this Streamlit version")
        return None

try:
    from streamlit import warning
except ImportError:
    def warning(*args: Any, **kwargs: Any) -> Any:
        st.warning("Warning component not available in this Streamlit version")
        return None

try:
    from streamlit import info
except ImportError:
    def info(*args: Any, **kwargs: Any) -> Any:
        st.warning("Info component not available in this Streamlit version")
        return None

class SuccessRepresentation(CommonRepresentation[success]):
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

class ErrorRepresentation(CommonRepresentation[error]):
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

class WarningRepresentation(CommonRepresentation[warning]):
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

class InfoRepresentation(CommonRepresentation[info]):
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