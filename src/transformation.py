from src.textnode import TextType, TextNode
from src.htmlnode import ParentNode, LeafNode

def text_node_to_html_leaf_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.IMAGE:
            return LeafNode('img', '', props= {'src': text_node.url, 'alt' : text_node.text})
        case TextType.LINK:
            return LeafNode('a', text_node.text, props= {'href': text_node.url})
        case _:
            raise Exception('Markdown error: Invalid text type')

