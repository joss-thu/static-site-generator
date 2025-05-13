import unittest
from src.textnode import TextNode, TextType
# from src.htmlnode import ParentNode, LeafNode
from src.transformation import (
    text_node_to_html_leaf_node, split_text_into_nodes_delimiter,
    extract_markdown_links, extract_markdown_images, split_text_image_into_text_nodes,
    split_text_links_into_text_nodes, text_to_text_nodes
)

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

    # ------------------------------------------------------------------------
    # Extract from links and images
    # markdown links and images
    # ------------------------------------------------------------------------
    def test_extract_markdown_links_positive(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://link.com) and [link_1](https://link_1.com)"
        )
        self.assertListEqual([("link", "https://link.com"), ("link_1", "https://link_1.com")], matches)

    # Test image extraction - positive case
    def test_extract_markdown_images_positive(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image 1](https://i.imgur.com/zjjcJKZJJ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image 1", "https://i.imgur.com/zjjcJKZJJ.png")], matches)

    def test_extract_markdown_links_negative(self):
        matches = extract_markdown_links(
            "This is text with an ![link](https://link.com) and ![link_1](https://link_1.com)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_negative(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and [image_1](https://i.imgur.com/zjjcJKZJJ.png)"
        )
        self.assertListEqual([], matches)

    # ------------------------------------------------------------------------
    # Extract from markdown links and images
    # EXtract to appropriate textnodes- markdown images
    # ------------------------------------------------------------------------
    # Empty list of nodes 
    def test_split_text_images(self):
        nodes = []
        with self.assertRaises(Exception):
            return split_text_image_into_text_nodes(nodes)
        
    # Texttype != Text
    def test_split_text_images_not_Text(self):
        node = TextNode('This is text with an ![image](http://img.com/)', TextType.IMAGE)
        self.assertEqual(split_text_image_into_text_nodes([node])[0], node)

    # standard case
    def test_split_text_images_standard_case(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with trailing text.",
            TextType.TEXT,
        )
        new_nodes = split_text_image_into_text_nodes([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" with trailing text.", TextType.TEXT),
            ],
            new_nodes,
        )

    # image at beginnng and end of sentence
    def test_split_text_images_at_start_end(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_text_image_into_text_nodes([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # no links
    def test_split_text_images_no_links(self):
        node = TextNode(
            "This is text with no links.",
            TextType.TEXT,
        )
        new_nodes = split_text_image_into_text_nodes([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links.", TextType.TEXT),
            ],
            new_nodes,
        )
    
    # ------------------------------------------------------------------------
    # Extract from markdown links and images
    # EXtract to appropriate textnodes- markdown links
    # ------------------------------------------------------------------------
    # Empty list of nodes 
    def test_split_text_links(self):
        nodes = []
        with self.assertRaises(Exception):
            return split_text_links_into_text_nodes(nodes)
        
    # Texttype != Text
    def test_split_text_links_not_Text(self):
        node = TextNode('This is text with an [link](http://link.com/)', TextType.LINK)
        self.assertEqual(split_text_links_into_text_nodes([node])[0], node)

    # standard case
    def test_split_text_links_standard_case(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) with trailing text.",
            TextType.TEXT,
        )
        new_nodes = split_text_links_into_text_nodes([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" with trailing text.", TextType.TEXT),
            ],
            new_nodes,
        )

    # # image at beginnng and end of sentence
    def test_split_text_links_at_start_end(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_text_links_into_text_nodes([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # # no links
    def test_split_text_links_no_links(self):
        node = TextNode(
            "This is text with no links.",
            TextType.TEXT,
        )
        new_nodes = split_text_links_into_text_nodes([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links.", TextType.TEXT),
            ],
            new_nodes,
        )
    # ------------------------------------------------------------------------
    # Text to appropriate TextNodes
    # ------------------------------------------------------------------------
    def test_text_to_text_nodes(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        self.assertListEqual(text_to_text_nodes(text), 
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
    )

if __name__ == '__main__':
    unittest.main()
