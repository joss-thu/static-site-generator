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

[Classes overview](../code_metrics/classes_SSG.png) |
[Packages overview](../code_metrics/packages_SSG.png) |
[Methods dependencies](../code_metrics/method_dependencies.png)

