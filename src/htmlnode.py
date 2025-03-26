from textnode import TextType

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