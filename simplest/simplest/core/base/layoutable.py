from typing import Dict, Any, Callable, Union, Optional, TypeVar, cast
from ..handlers.schema import Schema
from ..handlers.layer import Layer
from .models.layoutable import ComponentParserValidator, LayerIDValidator

T = TypeVar('T', bound='Layoutable')  # Type variable for method chaining



class Layoutable:
    """
    Base class for layoutable components that can organize content in layers.
    
    This class provides functionality for managing a schema with multiple layers,
    adding components to those layers, and rendering the layout in different formats.
    """
    
    def __init__(self):
        """Initialize a new Layoutable instance with an empty schema."""
        self.schema = Schema()
        self._column_based = False
        self._component_parser: Optional[Callable[..., Any]] = None

    def set_component_parser(self, component_parser: Callable[..., Any]) -> T:
        """
        Sets the component parser for the layoutable object.

        Args:
            component_parser (Callable[..., Any]): The component parser to be set.

        Returns:
            Layoutable: Returns the instance of the object to allow for method chaining.
            
        Raises:
            ValueError: If the component_parser is not callable.
        """
        # Validate component parser
        validator = ComponentParserValidator(parser=component_parser)
        self._component_parser = validator.parser
        return cast(T, self)
    
    def __render_column_based(
        self, based_component: Callable[..., Any], *args, **kwargs
    ) -> Any:
        """
        Renders the layout in a column-based format.
        

        Args:
            based_component (Callable[..., Any]): The base component used for rendering.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        
        Returns:
            Any: The rendered component.
        """
        # Create the base component
        c = based_component(*args, **kwargs)
        
        # Get the order of layers to render
        layers_to_render = (
            self.schema.main_body.order
            if self.schema.main_body.order
            else range(len(self.schema.main_body))
        )
        
        # Render each layer in its own column
        for k, layer_id in enumerate(layers_to_render):
            with c[k]:
                self.schema.main_body[layer_id]()
                
        return c

    def __render_row_based(
        self, based_component: Callable[..., Any], *args, **kwargs
    ) -> Any:
        """
        Renders the layout in a row-based format.


        Args:
            based_component (Callable[..., Any]): The base component used for rendering.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

            
        Returns:
            Any: The rendered component.
        """
        # Create the base component
        c = based_component(*args, **kwargs)
        
        # Render all layers in the same container
        with c:
            self.schema()
            
        return c
        

    def lrender(self, based_component: Callable[..., Any], *args, **kwargs) -> Any:
        """
        Renders the layout based on the provided component and layers.
        
        Args:
            based_component (Callable[..., Any]): The base component used for rendering.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
            
        Returns:
            Any: The rendered component.
            
        Raises:
            ValueError: If component_parser is not set.
        """
        if self._component_parser is None:
            raise ValueError("Component parser must be set before rendering")
            
        return self.__render_column_based(based_component, *args, **kwargs) \
            if self.is_column_based() else self.__render_row_based(based_component, *args, **kwargs)


    def add_component(self, component: Callable[..., Any], *args, **kwargs) -> Any:
        """
        Adds a component directly to the main layer.

        Args:
            component (Callable[..., Any]): The component to be added.
            *args: Additional positional arguments to be passed to the component.
            **kwargs: Additional keyword arguments to be passed to the component.

        Returns:
            Any: The parsed component that was added.
            
        Raises:
            ValueError: If component_parser is not set.
        """
        if self._component_parser is None:
            raise ValueError("Component parser must be set before adding components")
            
        comp = self._component_parser(component, *args, **kwargs)
        self.schema.add_component(comp)
        return comp

    def add_layer(self, idlayer: Union[int, str]) -> Layer:
        """
        Adds a specific layer to the layoutable object.

        Args:
            idlayer (Union[int, str]): The identifier of the layer to be added.

        Returns:
            Layer: The layer that was added.
        """
        # Validate layer ID
        validator = LayerIDValidator(layer_id=idlayer)
        return self.schema.add_layer(validator.layer_id)

    def add_to_layer(
        self, idlayer: Union[int, str], component: Callable[..., Any], *args, **kwargs
    ) -> Any:
        """
        Adds a component to a specific layer.

        Args:
            idlayer (Union[int, str]): The identifier of the layer to which the component will be added.
            component (Callable[..., Any]): The component to be added.
            *args: Additional positional arguments to be passed to the component.
            **kwargs: Additional keyword arguments to be passed to the component.

        Returns:
            Any: The parsed component that was added.
            
        Raises:
            ValueError: If component_parser is not set.
            KeyError: If the specified layer does not exist.
        """
        if self._component_parser is None:
            raise ValueError("Component parser must be set before adding components")
            
        # Validate layer ID
        validator = LayerIDValidator(layer_id=idlayer)
        layer_id = validator.layer_id
        
        # Check if the layer exists
        if layer_id not in self.schema:
            raise KeyError(f"Layer '{layer_id}' does not exist. Add it first with add_layer().")
            
        comp = self._component_parser(component, *args, **kwargs)
        self.schema[layer_id].add_component(comp)
        return comp

    def set_column_based(self, column_based: bool) -> T:
        """
        Sets the layout to be column-based or not.

        Args:
            column_based (bool): If True, sets the layout to be column-based. If False, sets it to be row-based.

        Returns:
            Layoutable: Returns the instance of the object to allow for method chaining.
        """
        if not isinstance(column_based, bool):
            raise ValueError("column_based must be a boolean")
            
        self._column_based = column_based
        return cast(T, self)

    def is_column_based(self) -> bool:
        """
        Check if the layout is column-based.

        Returns:
            bool: True if the layout is column-based, False otherwise.
        """
        return self._column_based
    
    def get_schema(self) -> Schema:
        """
        Get the current schema.
        
        Returns:
            Schema: The schema containing all layers and components.
        """
        return self.schema

    def clear(self) -> T:
        """
        Clear all components and layers from the schema.
        
        Returns:
            Layoutable: Returns the instance of the object to allow for method chaining.
        """
        self.schema = Schema()
        return cast(T, self)

    def serialize(self) -> Dict[str, Any]:
        """
        Serializes the layoutable object into a dictionary.

        Returns:
            dict: A dictionary containing the serialized data with keys:
                - "schema": The serialized schema.
                - "column_based": The column-based attribute of the layoutable object.
        """
        return {
            "schema": self.schema.serialize(),
            "column_based": self._column_based,
        }
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'Layoutable':
        """
        Creates a Layoutable instance from serialized data.
        
        Args:
            data (Dict[str, Any]): The serialized data.
            
        Returns:
            Layoutable: A new Layoutable instance.
        """
        instance = cls()
        instance._column_based = data.get("column_based", False)
        
        if "schema" in data:
            instance.schema = Schema.deserialize(data["schema"])
            
        return instance
