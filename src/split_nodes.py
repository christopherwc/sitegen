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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            original_text = node.text
            images = extract_markdown_images(original_text)

            if len(images) == 0:
                new_nodes.append(node)
                continue
            else:
                for image in images:
                    alt_text = image[0]
                    url = image[1]
                    substring = f"![{alt_text}]({url})"
                    sections = original_text.split(substring, 1)
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0],TextType.TEXT))
                    new_nodes.append(TextNode(alt_text,TextType.IMAGE,url=url))
                    original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text,TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            original_text = node.text
            links = extract_markdown_links(original_text)

            if len(links) == 0:
                new_nodes.append(node)
                continue
            else:
                for link in links:
                    link_text = link[0]
                    url = link[1]
                    substring = f"[{link_text}]({url})"
                    sections = original_text.split(substring, 1)
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0],TextType.TEXT))
                    new_nodes.append(TextNode(link_text,TextType.LINK,url=url))
                    original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text,TextType.TEXT))
    return new_nodes