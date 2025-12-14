from typing import Any, Union, Dict, List, Optional, Tuple, TypeVar,Literal,cast

from .representation import BaseRepresentation

T = TypeVar("T", bound="BaseStandard")  # Type variable for method chaining

class BaseStandard:
    """
    Base class for a collection of standard representations.
    It helps to manage the standard representations and their configurations.
    """
    

    def __new__(cls, *args: Any, **kwargs: Any) -> T:
        if not hasattr(cls, "_instance"):
            cls._instance = super(BaseStandard, cls).__new__(cls)
        return cls._instance

    def __init__(self,
                 bindings: Dict[Any, Union[BaseRepresentation, Tuple[str, ...]]],
                 defaultbinding: Literal["type", "name"] = "type",
    ):
        """
        Initialize the standard with bindings and default binding type.

        Args:
            bindings (Dict[Any, Union[BaseRepresentation, Tuple[str, ...]]]): A dictionary mapping types from other standards and their
                corresponding representations. It overrides the default representation of the standard.
            defaultbinding (str): The default binding type. Can be "type" or "name".
                Defaults to "type".
        """
        self.bindings = bindings
        self.defaultbinding = defaultbinding
        self.representations: List[BaseRepresentation] = []

    def add_representation(self, representation: BaseRepresentation) -> T:
        """
        Add a representation to the standard.

        Args:
            representation (BaseRepresentation): The representation to add.
        """
        self.representations.append(representation)
        return cast(T, self)
    
    def get_similar(self, value: Any) -> Optional[BaseRepresentation]:
        """
        Get a representation similar to the given value.

        Args:
            value (Any): The value to search for.
        
        Returns:
            Optional[BaseRepresentation]: The found representation or None.
        """
        if isinstance(value, str):
            return self.__search_by_name(value)
        return self._search_by_type(value)
    
    def _search_by_type(self, typ: Any) -> Optional[BaseRepresentation]:
        """
        Search for a representation by type.

        Args:
            typ (Any): The type to search for.

        Returns:
            Optional[BaseRepresentation]: The found representation or None.
        """
        for rep in self.representations:
            if rep == typ:
                if bind := self._find_binding(rep):
                    return bind
                return rep
        return None
    
    def _find_binding(self, typ: Any) -> Optional[BaseRepresentation]:
        """
        Find a binding for the given type.

        Args:
            typ (Any): The type to search for.

        Returns:
            Optional[BaseRepresentation]: The found representation or None.
        """
        if len(self.bindings) == 0:
            return None
        
        for key, value in self.bindings.items():
            if typ == key:
                if isinstance(value, BaseRepresentation):
                    return value
                elif isinstance(value, tuple):
                    for rep in value:
                        if rep == typ:
                            return rep
        
        return None


    def _search_by_name(self, name: str) -> Optional[BaseRepresentation]:
        """
        Search for a representation by name.

        Args:
            name (str): The name to search for.

        Returns:
            Optional[BaseRepresentation]: The found representation or None.
        """
        for rep in self.representations:
            if name == rep:
                if bind := self._find_binding(rep):
                    return bind
                return rep
        return None
    

    def __getitem__(self, key: Any) -> Optional[BaseRepresentation]:
        """
        Get a representation by key.

        Args:
            key (Any): The key to search for.

        Returns:
            Optional[BaseRepresentation]: The found representation or None.
        """
        if self.defaultbinding == "type":
            return self._search_by_type(key)
        elif self.defaultbinding == "name":
            return self._search_by_name(key)
        else:
            raise ValueError("Invalid default binding type. Use 'type' or 'name'.")

    def get_representations(self,stringfy: bool = False) -> List[Union[BaseRepresentation,str]]:
        """
        Get all representations in the standard.

        Args:
            stringfy (bool): Whether to return string representations. Defaults to False.

        Returns:
            List[Union[BaseRepresentation,str]]: List of representations or their string forms.
        """
        if stringfy:
            return [rep.get_str_representation() for rep in self.representations]
        
        return self.representations 

