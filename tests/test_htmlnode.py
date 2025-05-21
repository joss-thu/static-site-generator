import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode, HTMLTag
from src.textnode import TextType

class Test_HTMLNode(unittest.TestCase):
    # ------------------------------------------------------------------------
    # HTML nodes
    # ------------------------------------------------------------------------
    def test_htmlnodes_eq(self):
        li_node = HTMLNode('li', 'This is  a list element')
        li_node_1 = HTMLNode('li', 'This is  a list element')
        htmlnode = HTMLNode('ol', 'This is  a list', children=[li_node])
        htmlnode_2 = HTMLNode('ol', 'This is  a list', children=[li_node_1])
        self.assertEqual(htmlnode, htmlnode_2)

    def test_htmlnodes_not_eq(self):
        htmlnode = HTMLNode('img', 'This is  an image', props={'src': 'http://src.com', 'alt': 'alt text' })
        htmlnode_2 = HTMLNode('p', 'This is  a paragraph')
        self.assertNotEqual(htmlnode, htmlnode_2)

    def test_props_to_html(self):
        htmlnode = HTMLNode('a', 'This is  a paragraph', props = {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(HTMLNode.props_to_html(htmlnode), 'href="https://www.google.com" target="_blank"')

    def test_htmlnode_repr(self):
        htmlnode = HTMLNode('img', 'This is  an image', props={'src': 'http://src.com', 'alt': 'alt text' })
        self.assertEqual(repr(htmlnode), "HTMLNode(img, This is  an image, None, {'src': 'http://src.com', 'alt': 'alt text'})")

    # ------------------------------------------------------------------------
    # Leaf nodes
    # ------------------------------------------------------------------------
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_props_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    #test tag = none
    def test_leaf_tag_none(self):
        node = LeafNode("", "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    #test value = none
    def test_leaf_value_none(self):
        node = LeafNode("p", '')
        with self.assertRaises(ValueError):
            return node.to_html()
        
    #test value = none for img -> permitted
    def test_leaf_value_none(self):
        node = LeafNode("img", '', props = {'src': 'http://link.com', 'alt': 'alt_text'})
        self.assertEqual(node.to_html(), '<img src="http://link.com" alt="alt_text"></img>')


    #test children with value
    def test_leaf_children_to_html(self):
        child_node = HTMLNode('b', 'This is bold text')
        with self.assertRaises(TypeError):
            node = LeafNode('p', 'This is a paragraph', children = [child_node])
    
    # ------------------------------------------------------------------------
    # Parent nodes
    # ------------------------------------------------------------------------

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", 'This is a div', [child_node])
        self.assertEqual(parent_node.to_html(), "<div>This is a div<span>child</span></div>")

    #nested children:
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", children = [grandchild_node])
        parent_node = ParentNode("div", children = [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
  
    #multiple children
    def test_multiple_children(self):
        node = ParentNode(
        "p",
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    #nested and multiple children:
    def test_to_html_with_grandchildren(self):
        self.maxDiff = None
        # grandchild_node_0 = LeafNode("b", "grandchild")
        # child_node_0 = ParentNode("span", children = [grandchild_node_0])

        # grandchild_node_1 = LeafNode('li', 'grandchild_node_1')
        # grand_leaf_node = LeafNode('b', 'bolded text')
        # subchild = ParentNode('p', 'list element', [grand_leaf_node])
        # grandchild_node_2 = ParentNode('li', 'grandchild_node_2', [subchild])
        # child_node_1 = ParentNode("ul", children = [grandchild_node_1, grandchild_node_2])

        # grandchild_image_node = LeafNode('img', 'image_text', props = {'href': 'http://img.com'})
        # child_node_2 = ParentNode('p', children = [grandchild_image_node])
        
        # parent_node = ParentNode("div", children = [child_node_0, child_node_1, child_node_2])
        parent_node = ParentNode("div", children = [ParentNode("span", 
                                                               children = [LeafNode("b", "grandchild")]),
                                                    ParentNode("ul",
                                                               children = [LeafNode('li', 'grandchild_node_1'),
                                                                           ParentNode('li', 'grandchild_node_2',
                                                                                      children = [ParentNode('p', 'list element', 
                                                                                                             children = [LeafNode('b', 'bolded text')])
                                                                                                             ]),                    
                                                                            ]),
                                                    ParentNode('p',
                                                               children = [LeafNode('img', 'image_text', props = {'src': 'http://img.com'})])
                                                    ])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b>grandchild</b></span><ul><li>grandchild_node_1</li><li>grandchild_node_2<p>list element<b>bolded text</b></p></li></ul><p><img src="http://img.com">image_text</img></p></div>'
        )

    # check for tag
    def test_parent_tag_none(self):
        child_node = LeafNode('b', 'This is bold text')
        node = ParentNode("", "Hello, world!", [child_node])
        with self.assertRaises(ValueError):
            return node.to_html()
        
    # check for children
    def test_parent_children_none(self):
        node = ParentNode("", "Hello, world!", [])
        with self.assertRaises(ValueError):
            return node.to_html()
        
    # no children. 
    def test_nochildren(self):
        node = ParentNode('p', 'This is some text', None, None)
        with self.assertRaises(ValueError):
            return node.to_html()
        
    # check if leaf node
    # check html tags fro code, blockquote
    # Parent node with props
    def test_parent_node_with_props(self):
        node = ParentNode(
            tag = HTMLTag.IMAGE.value,
            value='',
            children=[LeafNode(HTMLTag.TEXT.value, 'This is a ',),
                      LeafNode(HTMLTag.BOLD.value,'bolded'),
                      LeafNode(HTMLTag.TEXT.value, ' text')],
            props={
                'src':"http://link.com",
                'alt':"alt_text"
            }

        )
        self.assertEqual(node.to_html(), '<img src="http://link.com" alt="alt_text">This is a <b>bolded</b> text</img>')


if __name__ == '__main__':
    unittest.main()
