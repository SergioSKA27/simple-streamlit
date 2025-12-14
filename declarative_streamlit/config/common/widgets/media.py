from streamlit import file_uploader,data_editor,camera_input
from uuid import uuid4
from ..representation import CommonRepresentation


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
    audio_input = None

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

        self.set_type(audio_input) if audio_input else None