from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class CommandType(str, Enum):
    """Tipos de comandos permitidos para componentes AST."""
    SET_ATTRIBUTE = "set_attribute"
    CALL_METHOD = "call_method"
    READ_STATE = "read_state"
    WRITE_STATE = "write_state"


# Tipo para definiciones sin procesar
ComponentDefinition = Dict[str, Any]


@dataclass(frozen=True, slots=True)
class AstComponentDefinition:
    """
    This class represents a component in an Abstract Syntax Tree (AST).
    It includes various attributes that define the component's properties,
    such as its name, type, attributes, reserved names, child elements,
    allowed commands, and whether it is reusable.

    Attributes:
        name (str): The name of the component.
        ctype (Optional[str]): The type of the component (e.g., "st.button").
        attributes (Dict[str, Any]): A dictionary of attributes associated with the component (e.g., {"label": str, "value": int}).
        reserved_names (Dict[str, str]): A mapping of reserved names for the component (e.g., {"action": str, "callback": "callable", "df": pd.DataFrame}).
        allowed_commands (Tuple[CommandType, ...]): A tuple of allowed command types for the component to execute.
    """
    
    name: str
    ctype: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    reserved_names: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> ComponentDefinition:
        """Exportar a diccionario estándar (para serialización)."""
        result = {
            "name": self.name,
            "ctype": self.ctype,
            "attributes": dict(self.attributes),
            "reserved_names": dict(self.reserved_names),
        }
        
        return result
    
    def is_attribute(self, name: str) -> bool:
        return name in self.attributes.keys()
    
    def is_reserved_name(self, name: str) -> bool:
        return name in self.reserved_names.keys()
    
    def validate_attribute(self, name: str, value: Any) -> bool:
        """
        Validate if the given value is acceptable for the specified attribute.

        Args:
            name (str): The name of the attribute.
            value (Any): The value to validate.
        Returns:
            bool: True if the value is valid for the attribute, False otherwise.
        """
        if name not in self.attributes:
            return False
        expected = self.attributes[name]
        if isinstance(expected, type):
            return isinstance(value, expected)
        if isinstance(expected, (list, tuple, set)):
            return value in expected
        return value == expected
    
    def validate_reserved_name(self, name: str, value: Any) -> bool:
        """
        Validate if the given value is acceptable for the specified reserved name.

        Args:
            name (str): The reserved name to validate.
            value (Any): The value to validate.
        Returns:
            bool: True if the value is valid for the reserved name, False otherwise.
        """
        if name not in self.reserved_names:
            return False
        expected = self.reserved_names[name]
        if expected == "callable":
            return callable(value)
        if isinstance(expected, type):
            return isinstance(value, expected)
        if isinstance(expected, (list, tuple, set)):
            return value in expected
        return value == expected

    
    @classmethod
    def from_dict(cls, data: ComponentDefinition) -> "AstComponentDefinition":
        """
        Create a validated instance from a dictionary.
        """
        return cls(**data)  # Create instance



