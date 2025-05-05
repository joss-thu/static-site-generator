# from textnode import TextType, TextNode

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('Method not defined for generic html node')
    
    def props_to_html(self):
        return ' '.join([f'{k}="{v}"' for k,v in self.props.items()])

    def __eq__(self, other):
        return (
            self.tag == other.tag and 
            self.value == other.value and 
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self):
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
    

            
