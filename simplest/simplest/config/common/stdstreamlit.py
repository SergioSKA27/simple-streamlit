from typing import Any, Callable, Union
from ..base.standard import BaseStandard


from .widgets.buttons import (
    ButtonRepresentation,
    DownloadButtonRepresentation,
    FormSubmitButtonRepresentation,
    LinkButtonRepresentation,
    PageLinkRepresentation,
)
from .widgets.selections import (
    SelectboxRepresentation,
    MultiselectRepresentation,
    RadioRepresentation,
    CheckboxRepresentation,
    SelectSliderRepresentation,
    ColorPickerRepresentation,
    ToggleRepresentation,
    FeedbackRepresentation,
    PillsRepresentation,
)
from .widgets.inputs import (
    TextInputRepresentation,
    TextAreaRepresentation,
    NumberInputRepresentation,
    DateInputRepresentation,
    TimeInputRepresentation,
    ChatInputRepresentation,
    SliderRepresentation,
)

from .widgets.media import (
    FileUploaderRepresentation,
    DataEditorRepresentation,
    CameraInputRepresentation,
    AudioInputRepresentation,
)


from .elements.data import (
    DataFrameRepresentation,
    JSONRepresentation,
    TableRepresentation,
    MetricRepresentation,
)

from .elements.status import (
    SuccessRepresentation,
    ErrorRepresentation,
    WarningRepresentation,
    InfoRepresentation,
)

from .elements.text import (
    MarkdownRepresentation,
    CodeRepresentation,
    TextRepresentation,
    HeaderRepresentation,
    SubheaderRepresentation,
    TitleRepresentation,
    CaptionRepresentation,
    LatexRepresentation,
    BadgeRepresentation,
    HtmlRepresentation,
)

from .elements.media import (
    ImageRepresentation,
    VideoRepresentation,
    AudioRepresentation,
)

from .containers.rowbased import (
    ContainerRepresentation,
    ExpanderRepresentation,
    FormRepresentation,
    PopoverRepresentation,
    ChatMessageRepresentation,
)

from .containers.columbased import ColumnsRepresentation, TabsRepresentation

from .containers.status import StatusRepresentation, SpinnerRepresentation


class StreamlitCommonStandard(BaseStandard):
    """
    A standard representation for common elements in Streamlit.
    It helps to manage the standard representations and their configurations.
    """

    def __init__(self) -> None:
        super().__init__(
            bindings={},
            defaultbinding="name",
        )
        # Widgets
        self.add_representation(ButtonRepresentation())
        self.add_representation(DownloadButtonRepresentation())
        self.add_representation(FormSubmitButtonRepresentation())
        self.add_representation(LinkButtonRepresentation())
        self.add_representation(PageLinkRepresentation())
        self.add_representation(SelectboxRepresentation())
        self.add_representation(MultiselectRepresentation())
        self.add_representation(RadioRepresentation())
        self.add_representation(CheckboxRepresentation())
        self.add_representation(SelectSliderRepresentation())
        self.add_representation(ColorPickerRepresentation())
        self.add_representation(ToggleRepresentation())
        self.add_representation(FeedbackRepresentation())
        self.add_representation(PillsRepresentation())
        self.add_representation(TextInputRepresentation())
        self.add_representation(TextAreaRepresentation())
        self.add_representation(NumberInputRepresentation())
        self.add_representation(DateInputRepresentation())
        self.add_representation(TimeInputRepresentation())
        self.add_representation(ChatInputRepresentation())
        self.add_representation(SliderRepresentation())
        self.add_representation(FileUploaderRepresentation())
        self.add_representation(DataEditorRepresentation())
        self.add_representation(CameraInputRepresentation())
        self.add_representation(AudioInputRepresentation())
        # Elements
        self.add_representation(DataFrameRepresentation())
        self.add_representation(JSONRepresentation())
        self.add_representation(TableRepresentation())
        self.add_representation(MetricRepresentation())
        self.add_representation(SuccessRepresentation())
        self.add_representation(ErrorRepresentation())
        self.add_representation(WarningRepresentation())
        self.add_representation(InfoRepresentation())
        self.add_representation(MarkdownRepresentation())
        self.add_representation(CodeRepresentation())
        self.add_representation(TextRepresentation())
        self.add_representation(HeaderRepresentation())
        self.add_representation(SubheaderRepresentation())
        self.add_representation(TitleRepresentation())
        self.add_representation(CaptionRepresentation())
        self.add_representation(LatexRepresentation())
        self.add_representation(BadgeRepresentation())
        self.add_representation(HtmlRepresentation())
        self.add_representation(ImageRepresentation())
        self.add_representation(VideoRepresentation())
        self.add_representation(AudioRepresentation())

        # Containers
        self.add_representation(ContainerRepresentation())
        self.add_representation(ExpanderRepresentation())
        self.add_representation(FormRepresentation())
        self.add_representation(PopoverRepresentation())
        self.add_representation(ChatMessageRepresentation())
        self.add_representation(ColumnsRepresentation())
        self.add_representation(TabsRepresentation())
        self.add_representation(StatusRepresentation())
        self.add_representation(SpinnerRepresentation())
        
        
