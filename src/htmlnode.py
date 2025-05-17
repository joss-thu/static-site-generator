"""Classes and functions used to manipulate the HTML nodes.
"""
from enum import Enum
import re

class BlockType(Enum):
    """BlockType Enum

    The BlockType Enum for the common HTML elements. The minimum list of elements are:

    - PARAGRAPH
    - HEADING
    - CODE
    - QUOTE
    - ULIST
    - OLIST

    """
    PARAGRAPH = 'paragraph'
    HEADING = '#'
    CODE = 'code'
    QUOTE = 'quote'
    ULIST = 'unordered_list'
    OLIST = 'ordered_list'

class HTMLNode:
    """
    Represents the basic HTML element node.

    This class is intended to be extended by the `LeafNode` and `ParentNode` classes.

    Attributes:
        tag (str or None): The HTML tag for the elements.
        - 'b' -> bold,
        - 'i' -> italic,
        - 'code' -> code,
        - 'img' -> image,
        - 'a' -> link,
        - '' -> None (for plain text)
        value (str or None): The text value for the HTML node.
        children (list[HTMLNode] or None): List of child HTMLNode objects, if any.
        props (dict or None): Dictionary of HTML attributes (e.g., {'src': 'img.png', 'alt': 'desc'}).
   
    """
    def __init__(self, tag = None, value = None, children = None, props = None):
        """
        Initializes an HTMLNode instance.

        Args:
            tag (str or None): The HTML tag for the elements.
                - 'b' -> bold,
                - 'i' -> italic,
                - 'code' -> code,
                - 'img' -> image,
                - 'a' -> link,
                - '' -> None (for plain text)
            value (str or None): The text value for the HTML node.
            children (list[HTMLNode] or None): List of child HTMLNode objects, if any.
            props (dict or None): Dictionary of HTML attributes (e.g., {'src': 'img.png', 'alt': 'desc'}).
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
    def __init__(self, tag = None, value = None, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value: # '' value is permitted for img tags!
            if not(self.tag == 'img' and self.value == ''):
                raise ValueError('Invalid HTML: No value provided for leaf node')
        if self.tag:
            attr = ' ' + self.props_to_html() if self.props else ''
            return f'<{self.tag}{attr}>{self.value}</{self.tag}>'
        return self.value

class ParentNode(HTMLNode):
    def __init__(self, tag = None, value = None , children = None, props = None):
        super().__init__(tag, value, children, props)

    def to_html(self):
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
    