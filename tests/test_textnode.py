import unittest
from src.textnode import TextType, TextNode

class Test_TextNode(unittest.TestCase):
    def test_testnodes_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node_1 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node_1)

    def test_testnodes_not_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node_1 = TextNode('This is a text node', TextType.ITALIC)
        self.assertNotEqual(node, node_1)

    def test_testnodes_url_not_eq(self):
        node = TextNode('This is a text node', TextType.LINK, 'http://link1.com')
        node_1 = TextNode('This is a text node', TextType.LINK, 'http://link2.com')
        self.assertNotEqual(node, node_1)



if __name__ == '__main__':
    unittest.main()
