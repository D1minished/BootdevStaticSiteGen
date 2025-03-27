from blocknodes import *
import unittest

class TestBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_block(self):
        md = '*** This is a heading block'
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, block_type)
    
    def test_code_block(self):
        md = '''
```
This is a code block
```
        '''
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)
    
    def test_quote_block(self):
        md = '''
>This is 
>A quote block
        '''
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)
    
    def test_unordered_list_block(self):
        md = '''
- This
- is 
- an
- unordered
- list
        '''
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)
    
    def test_unordered_list_block(self):
        md = '''
. This
. is 
. an
. unordered
. list
        '''
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)
        
    def test_paragraph_block(self):
        md = '''
This is a paragraph
        '''
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)