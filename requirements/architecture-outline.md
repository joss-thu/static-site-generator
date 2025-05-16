# Static site Generator - general outline

- Delete everything in the /public directory.

- Copy any static assets (HTML template, images, CSS, etc.) to the /public directory.

- Generate an HTML file for each Markdown file in the /content directory. For each Markdown file:
    - Open the file and read its contents.
    - Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
    - Convert each block into a tree of **HTMLNode** objects. For inline elements (like bold text, links, etc.) we will convert:
        - Raw markdown -> blocks -> text -> TextNode -> HTMLNode -> HTML

- Join all the HTMLNode blocks under one large parent HTMLNode for the pages.

- Use a recursive to_html() method to convert the HTMLNode and all its nested nodes to a giant HTML string and inject it in the HTML template.

- Write the full HTML string to a file for that page in the /public directory.

- -------
## textnode.py
- Enum TextType
- class TextNode(text, text_type, url)

## htmlnode.py
- HTMLNode(tag, value, children, props)
    - props_to_html(props) -> 
        str for tag parameters
    - to_html() -> 
    to be overrridden
- LeafNode() -> 
has Tag, value, props. No children allowed
- ParentNode() -> 
allows nested tags and multiple tags on the same level. Values are also permitted.

## transformation.py
### Text transformations
#### To Inline Textnode transformations:
- markdown_to_text_nodes(text) -> text_node 
Deal with markdown delimiters (for bold, italic, code etc.), images and links
1. split_text_delimiter()
2. split_text_image()
    - Extract the anchor text and corresponding image link
    - Convert the provided image part into TextNode of IMAGE type. Other parts are retained as Textnodes of type TEXT.
3. split_text_link()
    - Extract the anchor text and corresponding link
    - Convert the provided link part into TextNode of LINK type. Other parts are retained as Textnodes of type TEXT.
4. textnode_to_leaf_node(text_node) ->  LeafNode 
Convert markdown textnodes to html (leaf nodes) with suitable tags


### Block text transformations:
- Convert a block into a list of strings, seperated by the new line separations. Preserve all symbols, e.g. '-' should be preserved for a list.
- Identify the type of markdown node (bold, italics etc.) for the extracted list of strings, so that text nodes can be produced from these strings;
- which in turn can be converted to html nodes.


### To HTML transformations:
