import streamlit as st
from typing import Any
from uuid import uuid4
from pandas import DataFrame
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import dataframe
except ImportError:
    def dataframe(*args: Any, **kwargs: Any) -> Any:
        st.warning("Dataframe component not available in this Streamlit version")
        return None

try:
    from streamlit import json
except ImportError:
    def json(*args: Any, **kwargs: Any) -> Any:
        st.warning("JSON component not available in this Streamlit version")
        return None

try:
    from streamlit import table
except ImportError:
    def table(*args: Any, **kwargs: Any) -> Any:
        st.warning("Table component not available in this Streamlit version")
        return None

try:
    from streamlit import metric
except ImportError:
    def metric(*args: Any, **kwargs: Any) -> Any:
        st.warning("Metric component not available in this Streamlit version")
        return None

example_df = DataFrame({
    "Column 1": [1, 2, 3],
    "Column 2": ["A", "B", "C"],
    "Column 3": [True, False, True],
})


class DataFrameRepresentation(CommonRepresentation[dataframe]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "data": example_df,
                "key": str(uuid4()),
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(dataframe)

class JSONRepresentation(CommonRepresentation[json]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "body": example_df.to_json(),
                "expanded": True,
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(json)

class TableRepresentation(CommonRepresentation[table]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "data": example_df,
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(table)


class MetricRepresentation(CommonRepresentation[metric]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Metric",
                "value": 100,
                "delta": 10,
                "help": "This a generic metric",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(metric)

