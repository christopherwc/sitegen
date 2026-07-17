from enum import Enum
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ","## ","### ","#### " ,"##### ","###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if blocktype_quote_check(block):
        return BlockType.QUOTE
    if blocktype_unordered_check(block):
        return BlockType.UNORDERED_LIST
    if blocktype_ordered_check(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def blocktype_quote_check(block):
    lines = block.split("\n")
    valid_quote = True
    for line in lines:
        if not line.startswith(">"):
            valid_quote = False
            break
    return valid_quote

def blocktype_unordered_check(block):
    lines = block.split("\n")
    valid_unlist = True
    for line in lines:
        if not line.startswith("- "):
            valid_unlist = False
            break
    return valid_unlist

def blocktype_ordered_check(block):
    lines = block.split("\n")
    valid_ordered = True
    expected_number = 1
    for line in lines:
        if not line.startswith(f"{expected_number}. "):
            valid_ordered = False
            break
        expected_number += 1
    return valid_ordered

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(ulist_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(olist_to_html_node(block))
    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    paragraph = " ".join(block.split("\n"))
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```\n") or not block.endswith("```"):
        raise ValueError("invalid code block syntax")
    else:
        text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        stripped = line.lstrip(">").strip()
        new_lines.append(stripped)
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        if not item.startswith("- "):
            raise ValueError("invalid unordered list item")
        text = item[2:]  # strip "- "
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        if not item[1:3] == ". ":
            raise ValueError("invalid ordered list item")
        text = item[3:]  # strip "N. "
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)