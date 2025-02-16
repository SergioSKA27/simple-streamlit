from typing import List, Dict, Any, Callable, NoReturn, Union, Literal


class Layoutable:
    def __init__(self):
        self.layers = {}  # type: Dict[Union[int, str], List[Callable[..., Any]]]
        self._colum_based = False  # type: bool
        self.oderf = []  # type: List[Union[int, str]]

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
            if not args and not kwargs:
                args = [len(self.layers)]

            k = 0
            c = based_component(*args, **kwargs)
            for layer in self.oderf if self.oderf else self.layers.keys():
                with c[k]:
                    for component in self.layers[layer]:
                        component()
                k += 1
        else:

            c = based_component(*args, **kwargs)
            for layer in self.oderf if self.oderf else self.layers.keys():
                with c:
                    for component in self.layers[layer]:
                        component()

    def add_layer(self, idlayer: Union[int, str], components: List[Callable[..., Any]]):
        """
        Adds a layer to the layout with the specified ID and components.

        Args:
            idlayer (Union[int, str]): The identifier for the layer. Can be an integer or a string.
            components (List[Callable[..., Any]]): A list of callable components to be added to the layer.

        Returns:
            self: The instance of the class to allow method chaining.
        """
        self.layers[idlayer] = components
        return self

    def add_component(self, idlayer: Union[int, str], component: Callable[..., Any]):
        """
        Adds a component to the specified layer.

        Args:
            idlayer (Union[int, str]): The identifier of the layer to which the component will be added.
            component (Callable[..., Any]): The component to be added to the layer.

        Returns:
            self: The instance of the class to allow method chaining.
        """
        if idlayer not in self.layers:
            self.layers[idlayer] = []
        self.layers[idlayer].append(component)
        return self

    def add_component_unparsed(
        self,
        idlayer: Union[int, str],
        parser: Callable[..., Any],
        component: Callable[..., Any],
        *args,
        **kwargs
    ):
        """
        Adds a component to a specified layer after parsing it.

        Args:
            idlayer (Union[int, str]): The identifier of the layer to which the component will be added.
            parser (Callable[..., Any]): A function that parses the component.
            component (Callable[..., Any]): The component to be parsed and added.
            *args: Additional positional arguments to be passed to the parser.
            **kwargs: Additional keyword arguments to be passed to the parser.

        Returns:
            Any: The parsed component that was added to the specified layer.
        """
        
        if idlayer not in self.layers:
            self.layers[idlayer] = []
        ps = parser(component, *args, **kwargs)
        self.layers[idlayer].append(ps)
        return self.layers[idlayer][-1]

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
            "layers": self.layers,
            "column_based": self._colum_based,
            "order": self.oderf
        }
