"""
Provides classes and functions for representing, manipulating, and converting HTML nodes,
as well as for detecting block types from markdown-like text.

Classes:
    BlockType (Enum): Enum representing common HTML block elements (paragraph, heading, code, quote, unordered list, ordered list).
    HTMLNode: Base class for HTML element nodes, intended to be extended by LeafNode and ParentNode.
    LeafNode: Represents an HTML node with no children (e.g., text, images, inline elements).
    ParentNode: Represents an HTML node that can contain child nodes (e.g., paragraphs, lists, block elements).

Functions:
    block_to_block_type(block_text): Determines the block type of a given text block based on markdown-like syntax.

Usage:
    These classes and functions are used to build and render HTML structures programmatically,
    and to parse markdown-like text into structured HTML nodes.
"""
from enum import Enum
import re

class BlockType(Enum):
    """
    Enum representing common HTML block elements.

    Members:
        - PARAGRAPH: A standard paragraph block.
        - HEADING: A heading block (e.g., <h1>, <h2>, ...).
        - CODE: A code block.
        - QUOTE: A blockquote.
        - ULIST: An unordered list.
        - OLIST: An ordered list.
    """
    PARAGRAPH = 'paragraph'
    HEADING = '#'
    CODE = 'code'
    QUOTE = 'quote'
    ULIST = 'unordered_list'
    OLIST = 'ordered_list'

class HTMLNode:
    """Represents the basic HTML element node.

    This class is intended to be extended by the `LeafNode` and `ParentNode` classes.
    
    Attributes:
        tag (str or None):
            The HTML tag for the elements.
            - 'b' -> bold,
            - 'i' -> italic,
            - 'code' -> code,
            - 'img' -> image,
            - 'a' -> link,
            - '' -> None (for plain text)

        value (str or None): 
            The text value for the HTML node.
            
        children (list[HTMLNode] or None):
            List of child HTMLNode objects, if any.
        
        props (dict or None):
            Dictionary of HTML attributes (e.g., {'src': 'img.png', 'alt': 'desc'}).
    
    Methods:
        __init__(tag=None, value=None, children=None, props=None):
            Initializes an HTMLNode instance with the given tag, value, children, and props.
        
        to_html():
            Converts the HTMLNode instance to its HTML string representation.
            Should be implemented by subclasses. Raises NotImplementedError if called on HTMLNode.
        
        props_to_html():
            Converts the props dictionary to a string of HTML attributes.
       
        __eq__(other):
            Checks equality between this HTMLNode and another.
        
        __repr__():
            Returns a string representation of the HTMLNode instance.
    """

    def __init__(self, tag = None, value = None, children = None, props = None):
        """
        Initializes an HTMLNode instance.

        """

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Converts the HTMLNode instance to its HTML string representation.
        
        This method should be implemented by subclasses (LeafNode or ParentNode).
        
        Raises:
            NotImplementedError: If called on the base HTMLNode class.
        """
        
        raise NotImplementedError('Method not defined for generic html node')
    
    def props_to_html(self):
        """
        Converts the props dictionary to a string of HTML attributes.

        Returns:
            str: A string of HTML attributes (e.g., 'src="img.png" alt="desc"').

        """

        return ' '.join([f'{k}="{v}"' for k,v in self.props.items()])

    def __eq__(self, other):
        """
        Checks equality between this HTMLNode and another.

        Args:
            other (HTMLNode): The node to compare with.

        Returns:
            bool: True if all attributes are equal, False otherwise.

        """

        return (
            self.tag == other.tag and 
            self.value == other.value and 
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self):
        """
        Returns a string representation of the HTMLNode instance.

        Returns:
            str: The string representation.

        """

        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    
class LeafNode(HTMLNode):
    """
    Represents an HTML node with no children (a leaf node).

    This class is used for HTML elements that do not contain other HTML nodes,
    such as text, images, or inline elements.

    Attributes:
        tag (str or None): 
            The HTML tag for the element (e.g., 'b', 'img', 'a').

        value (str or None): 
            The text or value for the HTML node.

        props (dict or None): 
            Dictionary of HTML attributes (e.g., {'src': 'img.png', 'alt': 'desc'}).

    Methods:
        to_html(): 
            Returns the HTML string representation of the leaf node.

    """
    def __init__(self, tag = None, value = None, props = None):
        """
        Initializes a LeafNode instance.
        """

        super().__init__(tag, value, None, props)

    def to_html(self):
        """
        Converts the LeafNode instance to its HTML string representation.

        Returns:
            str: The HTML string for this leaf node.

        Raises:
            ValueError: If no value is provided for the leaf node (except for 'img' tags with an empty value).
        """

        if not self.value: # '' value is permitted for img tags!
            if not(self.tag == 'img' and self.value == ''):
                raise ValueError('Invalid HTML: No value provided for leaf node')
        if self.tag:
            attr = ' ' + self.props_to_html() if self.props else ''
            return f'<{self.tag}{attr}>{self.value}</{self.tag}>'
        return self.value

class ParentNode(HTMLNode):
    """
    Represents an HTML node that can contain child nodes (a parent node).

    This class is used for HTML elements that can have other HTML nodes as children,
    such as paragraphs, lists, or block elements.

    Attributes:
        tag (str or None): 
            The HTML tag for the element (e.g., 'div', 'ul', 'p').

        value (str or None): 
            The text or value for the HTML node (optional, may be used for wrappers).
        
        children (list[HTMLNode] or None): 
            List of child HTMLNode objects.
        
        props (dict or None): 
            Dictionary of HTML attributes (e.g., {'class': 'my-class'}).

    Methods:
        __init__(tag=None, value=None, children=None, props=None):
            Initializes a ParentNode instance with the given tag, value, children, and props.

        to_html():
            Converts the ParentNode instance and its children to an HTML string representation.
    """

    def __init__(self, tag = None, value = None , children = None, props = None):
        """
        Initializes a ParentNode instance.
        """

        super().__init__(tag, value, children, props)

    def to_html(self):
        """
        Converts the ParentNode instance and its children to an HTML string representation.

        Returns:
            str: 
                The HTML string for this parent node and its children.

        Raises:
            ValueError: If no tag or no children are provided for the parent node.
        """

        if type(self) == ParentNode:
            if not self.tag:
                raise ValueError('Invalid HTML: No tag provided for parent node')
            if not self.children:
                raise ValueError('Invalid HTML: No children provided for parent node')
        attr = ' ' + self.props_to_html() if self.props else ''
        html_text =''
        for node in self.children:
            value = self.value if self.value else ''
            html_text += value + node.to_html()
        return f'<{self.tag}{attr}>{html_text}</{self.tag}>'

def block_to_block_type(block_text):
    """
    Determines the block type of a given text block.

    Analyzes the input text and returns the corresponding BlockType enum value
    based on markdown-like syntax patterns (e.g., headings, code blocks, quotes, lists).

    Args:
        block_text (str): 
            The text block to analyze.

    Returns:
        BlockType: 
            The type of block detected (e.g., HEADING, CODE, QUOTE, ULIST, OLIST, PARAGRAPH).

    Raises:
        Exception: 
            If an ordered list is detected but the numbering format is invalid.
    """

    heading_pattern = r'^(#{1,6} )'
    if re.findall(heading_pattern, block_text):
        return BlockType.HEADING
    
    code_pattern = r'^```.*```$'
    if re.findall(code_pattern, block_text):
        return BlockType.CODE
    
    quote_pattern = r'^> (.*)'
    if re.findall(quote_pattern, block_text, re.MULTILINE):
        return BlockType.QUOTE

    ulist_pattern = r'^- (.*)'
    if re.findall(ulist_pattern, block_text, re.MULTILINE):
        return BlockType.ULIST
    
    olist_pattern = r'^([0-9]+\. .*)'
    matches = re.findall(olist_pattern, block_text, re.MULTILINE)
    if matches:
        numbers = []
        for match in matches:
            list_num = re.findall(r'^([0-9]+)', match)
            if len(list_num) == 1:
                numbers.append(int(list_num[0], 10))
            else:
                raise Exception('Error: illegal list format')
        if numbers == list(range(1, len(numbers)+1)) or numbers[::-1] == list(range(1, len(numbers)+1)):
            return BlockType.OLIST
        else:
            return BlockType.PARAGRAPH
    else:
        return BlockType.PARAGRAPH
    