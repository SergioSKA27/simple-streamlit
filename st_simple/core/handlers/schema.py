from typing import (
    List,
    Dict,
    Any,
    Callable,
    NoReturn,
    Union,
    Literal,
    Sequence,
    Optional,
)
from .layer import Layer


class Schema:
    def __init__(
        self,
        body_name: Optional[str] = None,
    ):
        self._body = Layer("__body__" if not body_name else body_name)
        self._schema = {}  # type: Dict[Union[int, str], Layer]

    def _set_layer_prop(self, layer: Layer):
        setattr(self, layer.idlayer, layer)

    def add_layer(self, idlayer: Optional[Union[int, str]]):
        self._schema[idlayer] = Layer(idlayer)
        self._body.add_component(self._schema[idlayer])
        self._set_layer_prop(self._schema[idlayer])
        return self._schema[idlayer]

    def add_component(
        self,
        component: Callable[..., Any],
    ) -> Callable[..., Any]:
        self._body.add_component(component)
        return component

    @property
    def main_body(self):
        return self._body

    def set_body_name(self, name: str) -> "Schema":
        self._body.set_idlayer(name)
        return self

    def __getitem__(self, index) -> Union[Layer, Callable[..., Any]]:
        return self._schema[index]

    def __call__(self, key=None) -> Union[Layer, Callable[..., Any]]:
        if key:
            return self.main_body[key]()
        return self._body()

    def __repr__(self) -> str:
        return f"Schema: {self._schema}\nBody: {self._body}"

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:

        return len(self._schema)

    def serialize(self) -> Dict[str, Any]:
        return self.main_body.serialize()
