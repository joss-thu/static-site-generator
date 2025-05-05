import unittest
from src.textnode import TextNode, TextType
# from src.htmlnode import ParentNode, LeafNode
from src.transformation import text_node_to_html_leaf_node, split_text_into_nodes_delimiter

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
    # ------------------------------------------------------------------------
    # Split into nodes
    # ------------------------------------------------------------------------
    # Texttype != Text
    def test_split_into_nodes_delimiter_text_type_not_Text(self):
        node = TextNode('This is text with a **bolded phrase** in the middle', TextType.BOLD)
        self.assertEqual(split_text_into_nodes_delimiter([node], TextType.BOLD.value)[0], node)

    # Delimiter not found 
    def test_split_into_nodes_delimiter_not_found(self):
        node = TextNode('This is text with a **bolded phrase** in the middle', TextType.TEXT)
        self.assertEqual(split_text_into_nodes_delimiter([node], TextType.ITALIC.value)[0], node)

    # Test main functionality
    def test_split_standard(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_text_into_nodes_delimiter([node], TextType.CODE.value)
        self.assertListEqual(new_nodes, [ TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    # malformed formating
    def test_split_malformed_delimiter(self):
        node = TextNode("This is text with a **code block word", TextType.TEXT)
        self.assertEqual(split_text_into_nodes_delimiter([node], TextType.BOLD.value)[0], node)
        
    # multiple delimiters
    def test_multiple_delimiters(self):
        self.maxDiff = None
        node_1 = TextNode('This is a text with **bolded** , _italicised_ and `code blocked` text.')
        node_2 =  TextNode('_italicised text_ in the beginning.')
        node_3 =  TextNode('At the end, there is **bolded_text**')
        new_nodes = split_text_into_nodes_delimiter([node_1, node_2, node_3], TextType.CODE.value)
        new_nodes = split_text_into_nodes_delimiter(new_nodes, TextType.BOLD.value)
        new_nodes = split_text_into_nodes_delimiter(new_nodes, TextType.ITALIC.value)
        self.assertListEqual(new_nodes, [
            TextNode('This is a text with ', TextType.TEXT),
            TextNode('bolded', TextType.BOLD),
            TextNode(' , ', TextType.TEXT),
            TextNode('italicised', TextType.ITALIC),
            TextNode(' and ', TextType.TEXT),
            TextNode('code blocked', TextType.CODE),
            TextNode(' text.', TextType.TEXT),

            TextNode('italicised text', TextType.ITALIC),
            TextNode(' in the beginning.', TextType.TEXT),

            TextNode('At the end, there is ', TextType.TEXT),
            TextNode('bolded_text', TextType.BOLD),
        ])

if __name__ == '__main__':
    unittest.main()
