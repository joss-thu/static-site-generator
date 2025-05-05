from src.textnode import TextType, TextNode, get_text_type_from_delimiter
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

def split_text_into_nodes_delimiter(old_nodes, delimiter):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or not (delimiter in old_node.text):
            new_nodes.append(old_node)
            continue
        chunks = old_node.text.split(delimiter)
        if len(chunks) % 2 == 0: # Delimiter split text will always have odd length. Hence if the delimiter is not closed, 
            # it is used as a normal text eg: **bolded_text**, where _does not signify italic delimiter. Pass the node as is!
            new_nodes.append(old_node)
            continue
        nodes = []
        for index in range(len(chunks)): # Delimiter formatted text will always appear on odd indices.
            if not chunks[index]:
                continue
            if index % 2 == 0:
                node = TextNode(chunks[index], TextType.TEXT)
            else:
                node = TextNode(chunks[index], get_text_type_from_delimiter(delimiter))
            nodes.append(node)
        new_nodes.extend(nodes)
    return new_nodes
