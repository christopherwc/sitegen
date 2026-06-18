class HTMLNode:
    """
    Represents a node in an HTML document tree.

    Can represent a raw text node, a parent node with children, or a leaf node.
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Initializes an HTMLNode.

        Args:
            tag (str, optional): The HTML tag name (e.g., "p", "div", "a").
            value (str, optional): The text content inside the tag.
            children (list, optional): A list of child HTMLNode objects.
            props (dict, optional): A dictionary of HTML attributes (e.g., {"href": "url"}).
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        """
        Renders the node and its children as an HTML string.
        
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement to_html method")
    
    def props_to_html(self):
        """
        Converts the properties dictionary into a string of HTML attributes.
        
        Returns:
            str: Formatted attributes with leading spaces, or an empty string.
        """
        if self.props is None or self.props == {}:
            return ""
        
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
            
        return result  # Added this so the method returns the constructed string
    
    def __repr__(self):
        """Returns a string representation of the HTMLNode object for debugging."""
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"