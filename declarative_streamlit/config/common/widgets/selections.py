from streamlit import selectbox, multiselect, radio, checkbox, select_slider,color_picker,toggle
from uuid import uuid4
from ..representation import CommonRepresentation


class SelectboxRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Select Box",
                "key": str(uuid4()),
                "help": "This a generic select box",
                "options": ["Option 1", "Option 2", "Option 3"],
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(selectbox)

class MultiselectRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Multi Select Box",
                "key": str(uuid4()),
                "help": "This a generic multi select box",
                "options": ["Option 1", "Option 2", "Option 3"],
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(multiselect)


class RadioRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Radio Box",
                "key": str(uuid4()),
                "help": "This a generic radio box",
                "options": ["Option 1", "Option 2", "Option 3"],
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(radio)


class CheckboxRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Checkbox",
                "key": str(uuid4()),
                "help": "This a generic checkbox",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(checkbox)

class SelectSliderRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Select Slider",
                "key": str(uuid4()),
                "help": "This a generic select slider",
                "options": ["Option 1", "Option 2", "Option 3"],
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(select_slider)


class ColorPickerRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Color Picker",
                "key": str(uuid4()),
                "value": "#fafafa",
                "help": "This a generic color picker",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(color_picker)

class ToggleRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Toggle",
                "key": str(uuid4()),
                "help": "This a generic toggle",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(toggle)

try:
    from streamlit import feedback
except ImportError:
    feedback = None

class FeedbackRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "options": "faces",
                "key": str(uuid4()),
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(feedback) if feedback else None

try:
    from streamlit import pills
except ImportError:
    pills = None

class PillsRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Pills",
                "key": str(uuid4()),
                "help": "This a generic pills",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(pills) if pills else None

try:
    from streamlit import segmented_control
except ImportError:
    segmented_control = None

class SegmentedControlRepresentation(CommonRepresentation):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Segmented Control",
                "key": str(uuid4()),
                "help": "This a generic segmented control",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(segmented_control) if segmented_control else None
