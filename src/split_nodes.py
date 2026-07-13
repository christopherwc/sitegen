import re
from textnode import TextNode,TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Split text nodes into multiple nodes based on a delimiter.

    Args:
        old_nodes: A list of TextNode objects to parse.
        delimiter: The string delimiter to split by (e.g., "**" or "`").
        text_type: The TextType to apply to the text within the delimiters.

    Returns:
        A new list of TextNode objects with delimited text extracted.

    Raises:
        ValueError: If a closing delimiter is missing (resulting in an even
            number of split parts).
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else: # node.text_type is TextType.TEXT: 
            text_parts = node.text.split(delimiter)
            #Check for valid string
            if len(text_parts) % 2 == 0:
                raise Exception("Error this string is invalid")
            for index, text in enumerate(text_parts):
                if text == "":
                    continue
                elif index % 2 == 0:
                    temp_node = TextNode(text,TextType.TEXT)
                    new_nodes.append(temp_node)
                else:
                    temp_node = TextNode(text,text_type)
                    new_nodes.append(temp_node)
                
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches= re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches