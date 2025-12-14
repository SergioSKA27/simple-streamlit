from typing import Any, Dict, Literal, Optional
from abc import ABCMeta, abstractmethod
from ...base.components.canvas import Canvas
from ...config.base.standard import BaseStandard

class Builder(metaclass=ABCMeta):

    def __init__(
        self,
        body: Dict[str, Any],
        component_match_strategy: Optional[Literal["strict", "partial"]] = "strict",
        standard: Optional[BaseStandard] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the builder with the given arguments and keyword arguments.
        Args:
            body: The body dictionary containing component definitions.
            component_match_strategy: The component matching strategy.
            standard: An optional standard configuration.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.args = args
        self.kwargs = kwargs
        self._body = body
        self.component_match_strategy = component_match_strategy
        self.standard = standard

    @abstractmethod
    def build(self, *args: Any, **kwargs: Any) -> Canvas:
        """
        Build the canvas from the body definition.
        """
        pass


    def _in_standard(self,name: str) -> bool:
        if self.standard:
            for rep in self.standard.representations:
                if self.component_match_strategy == "strict":
                    if name == str(rep):
                        return True
                elif self.component_match_strategy == "partial":
                    if name in str(rep):
                        return True
        return False