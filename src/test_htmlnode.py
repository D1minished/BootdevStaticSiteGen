import unittest
from htmlnode import *

class testHTMLNode(unittest.TestCase):
    def test_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_one(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    
    def test_props_two(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a_ref(self):
        node = LeafNode("a", "Hello, world!", props={"href": 'https://www.google.com'})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Hello, world!</a>")
    
    def test_leaf_to_html_b_(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")
    
    def test_leaf_to_html_text(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_many_children(self):
        child_node = LeafNode("span", "child1")
        child_node_2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node, child_node_2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
