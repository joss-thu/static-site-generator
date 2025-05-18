"""textnode.py

Defines classes and functions for representing and manipulating markdown text nodes.

Classes:
    TextType (Enum): 
        Enum representing different types of text formatting (plain, bold, italic, code, link, image).
    TextNode: 
        Represents a piece of text with a specific type and optional URL.

Functions:
    get_text_type_from_delimiter(delimiter):
        Returns the corresponding TextType for a given markdown delimiter, or None if not found.

"""
from enum import Enum

class TextType(Enum):
    """
    Enum representing different types of text formatting for markdown nodes.

    Members:
        TEXT: Plain text (no formatting).
        BOLD: Bold text, represented by '**' in markdown.
        ITALIC: Italic text, represented by '_' in markdown.
        CODE: Inline code, represented by '`' in markdown.
        LINK: Hyperlink text.
        IMAGE: Image element.
    """

    TEXT = ''
    BOLD = '**'
    ITALIC = '_'
    CODE = '`'
    LINK = 'link'
    IMAGE = 'image'

def get_text_type_from_delimiter(delimiter):
    """
    Returns the corresponding TextType for a given markdown delimiter.

    Args:
        delimiter (str): 
            The markdown delimiter to look up (e.g., '**', '_', '`', 'link', 'image').

    Returns:
        TextType or None: 
            The matching TextType enum member if found, otherwise None.
    """

    return next((v for k, v in TextType.__members__.items() if v.value == delimiter), None)

class TextNode:
    """
    Represents a piece of text with a specific formatting type and optional URL.

    Attributes:
        text (str): The text content of the node.
        text_type (TextType): The formatting type of the text (e.g., plain, bold, italic, code, link, image).
        url (str or None): The URL associated with the text (used for links and images).

    Methods:
        __init__(text, text_type=TextType.TEXT, url=None):
            Initializes a TextNode with the given text, type, and optional URL.
        __eq__(other):
            Checks equality between this TextNode and another.
        __repr__():
            Returns a string representation of the TextNode instance.
    """

    def __init__(self, text, text_type = TextType.TEXT, url = None):
        """
        Initializes a TextNode instance.
        """

        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        """
        Checks equality between this TextNode and another.

        Args:
            other (TextNode): The node to compare with.

        Returns:
            bool: True if all attributes are equal, False otherwise.
        """

        return (
            self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url
        )
    
    def __repr__(self):
        """
        Returns a string representation of the TextNode instance.

        Returns:
            str: The string representation.
        """
        
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
