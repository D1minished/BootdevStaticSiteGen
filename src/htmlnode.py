from textnode import *
from blocknodes import *
import re

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # String representing the tag name
        self.value = value # String representing the value of the tag
        self.children = children # List of HTMLNode objects representing the children of this node
        self.props = props # Dictionary of key-value pairs representing the attributes of the HTML Tag (such as href in tag <a>)
    
    def __repr__(self):
        return f"---------------------------------------------\nHTMLNode\nTag:\t{self.tag}\nValue:\t{self.value}\nChildren:\t{self.children}\nProps:\t{self.props}\n---------------------------------------------"
        
    def to_html(self):
        raise Exception("NotImplementedError")
    
    def props_to_html(self):
        props_string = ""
        if self.props == None:
            return props_string
        for prop in self.props:
            props_string += f' {prop}="{self.props[prop]}"'
        return props_string


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        if self.props == None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("No parent tag")
        if self.children == None:
            raise ValueError(f"{self.tag} has no children")
        
        if self.props == None:
            html_string = f"<{self.tag}>"
        else:
            html_string = f"<{self.tag}"
            for prop in self.props:
                html_string += prop.to_html()
            html_string += ">"
        
        for child in self.children:
            if child.children != None:
                pass
            elif child.value == None:
                raise ValueError("a child has no value")
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("Text node not a supported type")
    
    match text_node.text_type:
        case TextType.TEXT:
            html_node = LeafNode(None, value=text_node.text)
            return html_node
        
        case TextType.ITALIC:
            html_node = LeafNode("i", value=text_node.text)
            return html_node
            
        case TextType.BOLD:
            html_node = LeafNode("b", value=text_node.text)
            return html_node
            
        case TextType.CODE:
            html_node = LeafNode("code", value=text_node.text)
            return html_node
            
        case TextType.LINK:
            html_node = LeafNode("a", value=text_node.text, props={"href": f"{text_node.url}"})
            return html_node
            
        case TextType.IMAGE:
            html_node = LeafNode("img", value=text_node.text, props={"src": f"{text_node.url}"})
            return html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    top_parent = ParentNode(tag="div", children=[])
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            top_parent.children.append(code_to_child(block))
            continue
        print(block)
        block_parent = block_to_html_node(block_type)
        children = text_to_children(block)
        block_parent.children = children
        top_parent.children.append(block_parent)
    return top_parent
    
def code_to_child(text):
    text_node = TextNode(text, TextType.CODE)
    pre_node = ParentNode(tag="pre", children=text_node)
    return pre_node
        
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    print(text)
    for node in text_nodes:
        print(f"----------------------\n{node.text}\n------------------------------")
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
    

def block_to_html_node(block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode(tag="p", children=[])
        case BlockType.QUOTE:
            return ParentNode(tag="blockquote", children=[])
        case BlockType.CODE:
            return ParentNode(tag="code", children=[])
        case BlockType.UNORDERED_LIST:
            return ParentNode(tag="ul", children=[])
        case BlockType.ORDERED_LIST:
            return ParentNode(tag="ol", children=[])
        case BlockType.HEADING:
            heading_start = re.match(r"(\*{1,6})")
            heading_tag = f"h{len(heading_start)}"
            return ParentNode(tag=heading_tag, children=[])