import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_image(self):
        node = TextNode("This is alt text for an image", TextType.IMAGE, "https://imgs.search.brave.com/gcwOOYD00OXPSoDvIGk4yV64O2-MvnZyH8Wgf9QGvlw/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly93d3cu/aXN0b2NrcGhvdG8u/Y29tL3Jlc291cmNl/cy9pbWFnZXMvUGhv/dG9GVExQLzEwNTg4/MzQ2MTYuanBn")
        node2 = TextNode("This is alt text for an image", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_bold_in_text(self):
        node = TextNode("This is text with a **bold** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
        ])

    def test_italic_in_text(self):
        node = TextNode("This is text with an _italic_ word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT),
        ])

    def test_code_in_text(self):
        node = TextNode("This is text with a `code` block.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block.", TextType.TEXT),
        ])
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links_and_images(self):
        text = "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_no_image_or_link(self):
        text = "This text has no images or links"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertEqual(image_matches, [])
        self.assertEqual(link_matches, [])
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_and_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
        )
    
    def test_link_at_front(self):
        node = TextNode("[this](https://www.google.com) is google", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("this", TextType.LINK, "https://www.google.com"),
                TextNode(" is google", TextType.TEXT),
            ],
            new_nodes
        )
    
if __name__ == "__main__":
    unittest.main()