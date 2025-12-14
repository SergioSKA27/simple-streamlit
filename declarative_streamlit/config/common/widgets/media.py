import streamlit as st
from typing import Any
from uuid import uuid4
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import file_uploader
except ImportError:
    def file_uploader(*args: Any, **kwargs: Any) -> Any:
        st.warning("File Uploader component not available in this Streamlit version")
        return None

try:
    from streamlit import data_editor
except ImportError:
    def data_editor(*args: Any, **kwargs: Any) -> Any:
        st.warning("Data Editor component not available in this Streamlit version")
        return None

try:
    from streamlit import camera_input
except ImportError:
    def camera_input(*args: Any, **kwargs: Any) -> Any:
        st.warning("Camera Input component not available in this Streamlit version")
        return None


class FileUploaderRepresentation(CommonRepresentation[file_uploader]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "File Uploader",
                "key": str(uuid4()),
                "help": "This a generic file uploader",
                "type": ["csv", "txt"],
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(file_uploader)

class DataEditorRepresentation(CommonRepresentation[data_editor]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "data": {},
                "key": str(uuid4()),
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(data_editor)

class CameraInputRepresentation(CommonRepresentation[camera_input]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Camera Input",
                "key": str(uuid4()),
                "help": "This a generic camera input",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(camera_input)


try:
    from streamlit import audio_input
except ImportError:
    def audio_input(*args: Any, **kwargs: Any) -> Any:
        st.warning("Audio Input component not available in this Streamlit version")
        return None

class AudioInputRepresentation(CommonRepresentation[audio_input]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "label": "Audio Input",
                "key": str(uuid4()),
                "help": "This a generic audio input",
                },
            stateful=True,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(audio_input)