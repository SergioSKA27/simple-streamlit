from typing import Any, Dict, Optional

from ..models.astcmp import AstComponentDefinition


class AstComponent:
    """
    A class representing a component in an Abstract Syntax Tree (AST).
    """

    def __init__(
        self,
        _id: str,
        definition: AstComponentDefinition,
        strict: Optional[bool] = False,
    ) -> None:
        """
        Initialize the AST component with an identifier and definition.

        Args:
            _id (str): The unique identifier for the component instance.
            definition (AstComponentDefinition): The definition of the to validate against.
            strict (Optional[bool]): Enforce strict validation on attributes, reserved names, and commands. Defaults to False.
        """
        self._id = _id
        self.definition = definition
        self._args: Dict[str, Any] = {}
        self._config: Dict[str, Any] = {}
        self._commands: Dict[str, Any] = {}
        self.children: Dict[str, "AstComponent"] = {}
        self.strict = strict

    def validate(self) -> bool:
        """
        Validate the component against its definition.

        Returns:
            bool: True if the component is valid, False otherwise.
        """
        _commands_flag = all(
            self.definition.command_exists(cmd)
            and self.definition.is_command_allowed(cmd)
            for cmd in self._commands.keys()
        )

        _attributes_flag = all(
            self.definition.is_attribute(attr)
            and self.definition.validate_attribute(attr, val)
            for attr, val in self._args.items()
        )

        _reserved_names_flag = all(
            self.definition.is_reserved_name(rname)
            and self.definition.validate_reserved_name(rname, val)
            for rname, val in self._config.items()
        )

        return _commands_flag and _attributes_flag and _reserved_names_flag

    def add_child(self, child: "AstComponent") -> None:
        """
        Add a child component to this component.

        Args:
            child (AstComponent): The child component to add.
        """
        self.children[child.identifier] = child

    def get_child(self, name: str) -> Optional["AstComponent"]:
        """
        Get a child component by name.

        Args:
            name (str): The name of the child component.

        Returns:
            Optional[AstComponent]: The child component if found, else None.
        """
        return self.children.get(name)
