from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    ITALIC = "italic"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    
    def __eq__(self, target):
        if self.text == target.text and self.text_type==target.text_type and self.url == target.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_to_textnodes(text):
    pass
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        node_text = node.text
        node_text = node_text.split(delimiter, 1)
        new_nodes.append(TextNode(node_text.pop(0), TextType.TEXT))
        node_text = node_text[0]
        if delimiter not in node_text:
            raise Exception("Invalid Markdown Syntax")
        node_text = node_text.split(delimiter, 1)
        new_nodes.append(TextNode(node_text.pop(0), text_type))
        node_text = node_text[0]
        new_nodes.extend(split_nodes_delimiter([TextNode(node_text, TextType.TEXT)], delimiter, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        images_found = extract_markdown_images(node_text)
        if images_found == []:
            new_nodes.append(node)
            continue
        for image in images_found:
            full_image_text = f"![{image[0]}]({image[1]})"
            split_text = node_text.split(full_image_text, 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = split_text[1]
        if node_text != '':
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes
            

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        links_found = extract_markdown_links(node_text)
        if links_found == []:
            new_nodes.append(node)
            continue
        for link in links_found:
            full_link_text = f"[{link[0]}]({link[1]})"
            split_text = node_text.split(full_link_text, 1)
            if split_text[0] != '':
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = split_text[1]
        if node_text != '':    
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes