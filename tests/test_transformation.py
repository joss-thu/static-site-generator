import unittest
from src.textnode import TextNode, TextType
# from src.htmlnode import ParentNode, LeafNode
from src.transformation import text_node_to_html_leaf_node

class test_transformations(unittest.TestCase):
    def test_values(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")

        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.to_html(), "<i>This is an italic text node</i>")

        node = TextNode("This is a code block node", TextType.CODE)
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.to_html(), "<code>This is a code block node</code>")

        node = TextNode("This is image alt text", TextType.IMAGE, 'http://img_link.com')
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props, {"src": "http://img_link.com", "alt": "This is image alt text"})
        self.assertEqual(html_node.to_html(), '<img src="http://img_link.com" alt="This is image alt text"></img>')

        node = TextNode("This is link text", TextType.LINK, 'http://link.com')
        html_node = text_node_to_html_leaf_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.props, {"href": "http://link.com"})
        self.assertEqual(html_node.to_html(), '<a href="http://link.com">This is link text</a>')

if __name__ == '__main__':
    unittest.main()
