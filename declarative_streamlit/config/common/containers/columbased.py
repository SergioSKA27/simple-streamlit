import streamlit as st
from typing import Any
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import columns
except ImportError:
    def columns(*args: Any, **kwargs: Any) -> Any:
        st.warning("Columns component not available in this Streamlit version")
        return None

try:
    from streamlit import tabs
except ImportError:
    def tabs(*args: Any, **kwargs: Any) -> Any:
        st.warning("Tabs component not available in this Streamlit version")
        return None


class ColumnsRepresentation(CommonRepresentation[columns]):
    def __init__(self) -> None:
        super().__init__(
            stateful=False,
            fatal=True,
            strict=True,
            column_based=True,
        )

        self.set_type(columns)
    

class TabsRepresentation(CommonRepresentation[tabs]):
    def __init__(self) -> None:
        super().__init__(
            stateful=False,
            fatal=True,
            strict=True,
            column_based=True,
        )

        self.set_type(tabs)
