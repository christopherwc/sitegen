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

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Node must have a tag")
        if self.children is None or self.children == []:
            raise ValueError("Parent Node must have at least one Child Node")
        holder = []
        for child in self.children:
            holder.append(child.to_html())
        children_html ="".join(holder)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

