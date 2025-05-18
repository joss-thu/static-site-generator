"""Classes and functions used to manipulate the markdown text nodes.
"""
from enum import Enum

class TextType(Enum):
    TEXT = ''
    BOLD = '**'
    ITALIC = '_'
    CODE = '`'
    LINK = 'link'
    IMAGE = 'image'

def get_text_type_from_delimiter(delimiter):
    return next((v for k, v in TextType.__members__.items() if v.value == delimiter), None)

class TextNode:
    def __init__(self, text, text_type = TextType.TEXT, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url
        )
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
