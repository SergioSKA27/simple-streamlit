from typing import (
    List,
    Dict,
    Any,
    Callable,
    Union,
    Optional,
)
from .layer import Layer
import logging


logger = logging.getLogger(__name__)

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
            return self.main_body[key].__call__()
        return self._body()

    def __repr__(self) -> str:
        return f"Schema: {self._schema}\nBody: {self._body}"

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:

        return len(self._schema)

    def serialize(self) -> Dict[str, Any]:
        return self.main_body.serialize()
    
    @classmethod
    def deserialize(
        cls,
        data: List[dict[str, Any]],
        componentmap: dict[str, Any],
        component_parser: type = None,
        layer_parser: type = None,
        strict: bool = False,
    ) -> "Schema":
        """
        Unserializes a schema from a list of dictionaries.
        
        Args:
            layerid (str): The ID of the layer.
            data (List[dict[str, Any]]): The data to unserialize.
            componentmap (dict[str, Any]): A map of components.
            component_parser (type, optional): The component parser class. Defaults to None.
            layer_parser (type, optional): The layer parser class. Defaults to None.
            strict (bool, optional): Whether to use strict mode. Defaults to False.

        Returns:
            Schema: The unserialized schema.
        """
        schema = list(data.keys())[0] if data else "__body__"
        layer = Layer.deserialize(schema, data[schema], componentmap, component_parser, layer_parser, strict)
        schema_instance = cls(schema)
        schema_instance._body = layer
        schema_instance._schema = {schema: layer}

        return schema_instance

        