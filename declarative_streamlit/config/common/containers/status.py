import streamlit as st
from typing import Any
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import spinner
except ImportError:
    def spinner(*args: Any, **kwargs: Any) -> Any:
        st.warning("Spinner component not available in this Streamlit version")
        return None

try:
    from streamlit import status
except ImportError:
    def status(*args: Any, **kwargs: Any) -> Any:
        st.warning("Status component not available in this Streamlit version")
        return None


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