import re
from enum import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    
    for block in blocks:
        stripped_blocks.append(block.strip())
    
    final_blocks = []
    for block in stripped_blocks:
        if block == "":
            continue
        final_blocks.append(block)
    return final_blocks

def block_to_block_type(text):
    if re.match(r"\*{1,6} ", text):
        return BlockType.HEADING
    if re.fullmatch(r"`{3}[\s\S]*`{3}", text):
        return BlockType.CODE
    if re.match(r"(>.*(\n))", text):
        return BlockType.QUOTE
    if re.match(r"(-.*(\n))", text):
        return BlockType.UNORDERED_LIST
    if re.match(r"(\..*(\n))", text):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH