from enum import Enum

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
