from textnode import *

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
        