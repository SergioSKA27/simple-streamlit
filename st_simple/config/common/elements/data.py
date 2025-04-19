from streamlit import dataframe, json, table,metric
from uuid import uuid4
from pandas import DataFrame
from ..representation import CommonRepresentation

example_df = DataFrame({
    "Column 1": [1, 2, 3],
    "Column 2": ["A", "B", "C"],
    "Column 3": [True, False, True],
})


class DataFrameRepresentation(CommonRepresentation):
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

class JSONRepresentation(CommonRepresentation):
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

class TableRepresentation(CommonRepresentation):
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


class MetricRepresentation(CommonRepresentation):
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

