from typing import Any, Callable, Union
from streamlit import file_uploader,data_editor,camera_input
from uuid import uuid4
from ..representation import CommonRepresentation


class FileUploaderRepresentation(CommonRepresentation):
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

class DataEditorRepresentation(CommonRepresentation):
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

class CameraInputRepresentation(CommonRepresentation):
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
    audio_input = None

class AudioInputRepresentation(CommonRepresentation):
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

        self.set_type(audio_input) if audio_input else None