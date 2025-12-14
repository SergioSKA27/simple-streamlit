from streamlit import columns,tabs
from ..representation import CommonRepresentation


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
