"""
transformation.py

Provides functions for transforming markdown text into structured text nodes and HTML nodes.

Functions:
    text_node_to_html_leaf_node(text_node):
        Converts a TextNode instance to a corresponding LeafNode for HTML rendering.

    split_text_into_nodes_delimiter(old_nodes, delimiter):
        Splits text nodes into multiple nodes based on a markdown delimiter (e.g., '**', '_', '`').

    extract_markdown_links(text):
        Extracts markdown-style links from the given text.

    extract_markdown_images(text):
        Extracts markdown-style images from the given text.

    split_text_image_into_text_nodes(old_nodes):
        Splits text nodes into separate nodes for images and surrounding text.

    split_text_links_into_text_nodes(old_nodes):
        Splits text nodes into separate nodes for links and surrounding text.

    text_to_text_nodes(text):
        Converts a markdown string into a list of TextNode objects, handling formatting, images, and links.

    markdown_to_blocks(markdown_text):
        Splits markdown text into blocks separated by double newlines.

Usage:
    Use these functions to parse markdown content, extract formatting, and convert it into a structure suitable for HTML rendering.
"""

from src.textnode import TextType, TextNode, get_text_type_from_delimiter
from src.htmlnode import ParentNode, LeafNode
import re

def text_node_to_html_leaf_node(text_node):
    """
    Converts a TextNode instance to a corresponding LeafNode for HTML rendering.

    Args:
        text_node (TextNode): The TextNode to convert.

    Returns:
        LeafNode: The corresponding HTML leaf node.

    Raises:
        Exception: If the text type is invalid.
    """

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
    """
    Splits text nodes into multiple nodes based on a markdown delimiter.

    Args:
        old_nodes (list[TextNode]): List of TextNode objects to process.
        delimiter (str): The markdown delimiter to split on (e.g., '**', '_', '`').

    Returns:
        list[TextNode]: List of TextNode objects with formatting applied.
    """

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

def extract_markdown_links(text):
    """
    Extracts markdown-style links from the given text.

    Args:
        text (str): The text to search for links.

    Returns:
        list[tuple[str, str]]: List of (link_text, url) tuples.
    """
    # pattern =  r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    pattern = r'(?<!!)\[([\s\S]+?)\]\(([\s\S]+?)\)'
    return re.findall(pattern, text)

def extract_markdown_images(text):
    """
    Extracts markdown-style images from the given text.

    Args:
        text (str): The text to search for images.

    Returns:
        list[tuple[str, str]]: List of (alt_text, url) tuples.
    """

    # pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    pattern = r'(?<=!)\[([\s\S]+?)\]\(([\s\S]+?)\)'
    return re.findall(pattern, text)

def split_text_image_into_text_nodes(old_nodes):
    """
    Splits text nodes into separate nodes for images and surrounding text.

    Args:
        old_nodes (list[TextNode]): List of TextNode objects to process.

    Returns:
        list[TextNode]: List of TextNode objects with images separated.

    Raises:
        Exception: If no nodes are passed.
    """

    new_nodes = []
    if old_nodes:
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            
            md_images = extract_markdown_images(old_node.text)
            
            text_extracted = old_node.text
            nodes = []
       
            for md_image in md_images:
                if text_extracted:
                    chunks = text_extracted.split(f'![{md_image[0]}]({md_image[1]})',1)
                    
                    if chunks[0] != '':
                        new_node = TextNode(chunks[0], TextType.TEXT)
                        nodes.append(new_node)   
                    nodes.append(TextNode(f'{md_image[0]}', TextType.IMAGE, f'{md_image[1]}'))
                    
                    text_extracted = chunks[1]
            if text_extracted:
                nodes.append(TextNode(text_extracted, TextType.TEXT))
            new_nodes.extend(nodes)
        return new_nodes
    else:
        raise Exception('Error: No nodes passed')
    
def split_text_links_into_text_nodes(old_nodes):
    """
    Splits text nodes into separate nodes for links and surrounding text.

    Args:
        old_nodes (list[TextNode]): List of TextNode objects to process.

    Returns:
        list[TextNode]: List of TextNode objects with links separated.

    Raises:
        Exception: If no nodes are passed.
    """

    new_nodes = []
    if old_nodes:
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            
            md_images = extract_markdown_links(old_node.text)
            
            text_extracted = old_node.text
            nodes = []
       
            for md_image in md_images:
                if text_extracted:
                    chunks = text_extracted.split(f'[{md_image[0]}]({md_image[1]})',1)
                    
                    if chunks[0] != '':
                        new_node = TextNode(chunks[0], TextType.TEXT)
                        nodes.append(new_node)   
                    nodes.append(TextNode(f'{md_image[0]}', TextType.LINK, f'{md_image[1]}'))
                    
                    text_extracted = chunks[1]
            if text_extracted:
                nodes.append(TextNode(text_extracted, TextType.TEXT))
            new_nodes.extend(nodes)
        return new_nodes
    else:
        raise Exception('Error: No nodes passed')
    
def text_to_text_nodes(text):
    """
    Converts a markdown string into a list of TextNode objects, handling formatting, images, and links.

    Args:
        text (str): The markdown text to convert.

    Returns:
        list[TextNode]: List of TextNode objects representing the parsed text.

    Raises:
        Exception: If no text is passed.
    """
        
    if text:
        text_nodes =  [TextNode(text, TextType.TEXT)]
        for delimiter in ['**', '_', '`']:
            text_nodes = split_text_into_nodes_delimiter(text_nodes, delimiter)
        text_nodes = split_text_image_into_text_nodes(text_nodes)
        text_nodes = split_text_links_into_text_nodes(text_nodes)
        return text_nodes
    else:
        raise Exception('Error: No text passed')
    
def markdown_to_blocks(markdown_text):
    """
    Splits markdown text into blocks separated by double newlines.

    Args:
        markdown_text (str): The markdown text to split.

    Returns:
        list[str]: List of text blocks.

    Raises:
        Exception: If the input is empty or only whitespace.
    """
        
    text = markdown_text.strip()
    if text.isspace() or text == "":
        raise Exception('Error: Empty block!')
    else:
        return text.split('\n\n')


