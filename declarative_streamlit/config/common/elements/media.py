from streamlit import audio,video, image
from ..representation import CommonRepresentation




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

