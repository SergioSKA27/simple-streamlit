import streamlit as st
from typing import Any
from uuid import uuid4
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import selectbox
except ImportError:
    def selectbox(*args: Any, **kwargs: Any) -> Any:
        st.warning("Selectbox component not available in this Streamlit version")
        return None

try:
    from streamlit import multiselect
except ImportError:
    def multiselect(*args: Any, **kwargs: Any) -> Any:
        st.warning("Multiselect component not available in this Streamlit version")
        return None

try:
    from streamlit import radio
except ImportError:
    def radio(*args: Any, **kwargs: Any) -> Any:
        st.warning("Radio component not available in this Streamlit version")
        return None

try:
    from streamlit import checkbox
except ImportError:
    def checkbox(*args: Any, **kwargs: Any) -> Any:
        st.warning("Checkbox component not available in this Streamlit version")
        return None

try:
    from streamlit import select_slider
except ImportError:
    def select_slider(*args: Any, **kwargs: Any) -> Any:
        st.warning("Select Slider component not available in this Streamlit version")
        return None

try:
    from streamlit import color_picker
except ImportError:
    def color_picker(*args: Any, **kwargs: Any) -> Any:
        st.warning("Color Picker component not available in this Streamlit version")
        return None

try:
    from streamlit import toggle
except ImportError:
    def toggle(*args: Any, **kwargs: Any) -> Any:
        st.warning("Toggle component not available in this Streamlit version")
        return None


class SelectboxRepresentation(CommonRepresentation[selectbox]):
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

class MultiselectRepresentation(CommonRepresentation[multiselect]):
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


class RadioRepresentation(CommonRepresentation[radio]):
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


class CheckboxRepresentation(CommonRepresentation[checkbox]):
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

class SelectSliderRepresentation(CommonRepresentation[select_slider]):
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


class ColorPickerRepresentation(CommonRepresentation[color_picker]):
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

class ToggleRepresentation(CommonRepresentation[toggle]):
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
    def feedback(*args: Any, **kwargs: Any) -> Any:
        st.warning("Feedback component not available in this Streamlit version")
        return None

class FeedbackRepresentation(CommonRepresentation[feedback]):
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

        self.set_type(feedback)

try:
    from streamlit import pills
except ImportError:
    def pills(*args: Any, **kwargs: Any) -> Any:
        st.warning("Pills component not available in this Streamlit version")
        return None

class PillsRepresentation(CommonRepresentation[pills]):
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

        self.set_type(pills)

try:
    from streamlit import segmented_control
except ImportError:
    def segmented_control(*args: Any, **kwargs: Any) -> Any:
        st.warning("Segmented Control component not available in this Streamlit version")
        return None

class SegmentedControlRepresentation(CommonRepresentation[segmented_control]):
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

        self.set_type(segmented_control)
