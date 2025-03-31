from typing import (
    List,
    Any,
    Callable,
    Union,
    Sequence,
)
from uuid import uuid4


class Layer:
    def __init__(
        self,
        _id: Union[int, str],
        elements: Sequence[Callable[..., Any]] = None,
        order: Sequence[Union[int, str]] = None,
    ):
        self._id = _id or uuid4().hex
        self.elements = elements or []

        self._order = order or []

    @property
    def idlayer(self) -> Union[int, str]:
        return self._id

    def set_idlayer(self, idlayer: Union[int, str]) -> "Layer":
        self._id = idlayer
        return self

    @property
    def order(self) -> Sequence[Union[int, str]]:
        return self._order

    def set_order(self, order: Sequence[Union[int, str]]) -> "Layer":
        self._order = order
        return self

    def add_component(self, component: Callable[..., Any]) -> Callable[..., Any]:
        self.elements.append(component)
        return self.elements[-1]

    def __getitem__(self, index) -> Union[Callable[..., Any], "Layer"]:
        if isinstance(index, str):
            for el in self.elements:
                if "key" in el.kwargs and el.kwargs["key"] == index:
                    return el
        return self.elements[index]

    def __call__(self, key=None) -> Union[Callable[..., Any], List[Callable[..., Any]]]:
        if key:
            # You can also use the key to render only a specific component
            return self.__getitem__(key).parse()()
        if not self.order:
            return [el.parse()() for el in self.elements]
        return [self.__getitem__(el).parse()() for el in self.order]

    def __repr__(self) -> str:
        return f"Layer: {self.idlayer}"

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:
        return len(self.elements)

    def __iter__(self):
        for el in self.elements:
            yield el

    def __setitem__(self, key, value):
        self.elements[key] = value
        return self

    def serialize(self) -> dict[str, Any]:
        return {self.idlayer: [el.serialize() for el in self.elements]}
