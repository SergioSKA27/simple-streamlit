import streamlit as st
from typing import Any
from ..representation import CommonRepresentation

# Try to import components, fallback to mock using st.warning if not available
try:
    from streamlit import audio
except ImportError:
    def audio(*args: Any, **kwargs: Any) -> Any:
        st.warning("Audio component not available in this Streamlit version")
        return None

try:
    from streamlit import video
except ImportError:
    def video(*args: Any, **kwargs: Any) -> Any:
        st.warning("Video component not available in this Streamlit version")
        return None

try:
    from streamlit import image
except ImportError:
    def image(*args: Any, **kwargs: Any) -> Any:
        st.warning("Image component not available in this Streamlit version")
        return None




class ImageRepresentation(CommonRepresentation[image]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "image": "https://picsum.photos/200/300",
                "caption": "This is generic image",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(image)


class VideoRepresentation(CommonRepresentation[video]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "data": "https://youtu.be/vrwoIZtQSuI?si=Q72tpS79GIZb06S5",
                "autoplay": True,
                "muted": True,
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(video)

class AudioRepresentation(CommonRepresentation[audio]):
    def __init__(self) -> None:
        super().__init__(
            default_kwargs={
                "data": "http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3",
                },
            stateful=False,
            fatal=True,
            strict=True,
            column_based=False,
        )

        self.set_type(audio)

