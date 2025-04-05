from typing import List, Dict, Any, Callable, NoReturn, Union, Literal
from ..handlers.schema import Schema
from ..handlers.layer import Layer



class Layoutable:
    def __init__(self):
        self.schema = Schema() # type: Schema
        self._colum_based = False  # type: bool
        self._component_parser = None 
    
    def set_component_parser(self, component_parser: Callable[..., Any]):
        """
        Sets the component parser for the layoutable object.

        Args:
            component_parser (Callable[..., Any]): The component parser to be set.

        Returns:
            self: Returns the instance of the object to allow for method chaining.
        """
        self._component_parser = component_parser
        return self

    def lrender(self, based_component: Callable[..., Any], *args, **kwargs):
        """
        Renders the layout based on the provided component and layers.
        Parameters:
        based_component (Callable[..., Any]): The base component used for rendering.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
        Returns:
        None
        """
        if self._colum_based:
            k = 0
            c = based_component(*args, **kwargs)
            for l in self.schema.main_body.order if len(self.schema.main_body.order) > 0 else range(len(self.schema.main_body)):
                with c[k]:
                    self.schema.main_body[l]()
                k += 1
            
        else:
            c = based_component(*args, **kwargs)
            with c:
                self.schema()
        return c
            
        

    def add_component(self, component: Callable[..., Any], *args, **kwargs) -> Layer:
        """
        Adds a component directly to the main layer.

        Args:
            idlayer (Optional[Union[int, str]]): The identifier of the layer to which the component will be added.
            component (Callable[..., Any]): The component to be added.
            *args: Additional positional arguments to be passed to the component.
            **kwargs: Additional keyword arguments to be passed to the component.
        
        Returns:
            Layer: The layer to which the component was added.
        """
        comp = self._component_parser(component, *args, **kwargs)
        self.schema.add_component(comp)
        return comp


    def add_layer(self, idlayer: Union[int, str]):
        """
        Adds a specific layer to the layoutable object.
        
        Args:
            idlayer (Union[int, str]): The identifier of the layer to be added.
        
        Returns:
            Layer: The layer that was added.
        """
        return self.schema.add_layer(idlayer)
    
    def add_to_layer(self, idlayer: Union[int, str], component: Callable[..., Any], *args, **kwargs):
        """
        Adds a component to a specific layer.

        Args:
            idlayer (Union[int, str]): The identifier of the layer to which the component will be added.
            component (Callable[..., Any]): The component to be added.
            *args: Additional positional arguments to be passed to the component.
            **kwargs: Additional keyword arguments to be passed to the component.
        
        Returns:
            Layer: The layer to which the component was added.
        """
        comp = self._component_parser(component, *args, **kwargs)
        self.schema[idlayer].add_component(comp)
        return comp
    
    


    def set_column_based(self, column_based: bool):
        """
        Sets the layout to be column-based or not.

        Args:
            column_based (bool): If True, sets the layout to be column-based. If False, sets it to be row-based.

        Returns:
            self: Returns the instance of the object to allow for method chaining.
        """
        self._colum_based = column_based
        return self

    def is_column_based(self):
        """
        Check if the layout is column-based.

        Returns:
            bool: True if the layout is column-based, False otherwise.
        """
        return self._colum_based
    
    def serialize(self):
        """
        Serializes the layoutable object into a dictionary.

        Returns:
            dict: A dictionary containing the serialized data with keys:
                - "layers": The layers of the layoutable object.
                - "column_based": The column-based attribute of the layoutable object.
                - "order": The order attribute of the layoutable object.
        """
        return {
            "schema": self.schema.serialize(),
            "column_based": self._colum_based,
        }

