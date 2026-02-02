#!/usr/bin/env python3
"""
Generate PDF documentation from markdown files.
Combines README.md, trade/get.md, and trade/post.md into a single PDF.
"""
import markdown
from weasyprint import HTML, CSS
from pathlib import Path

DOC_DIR = Path(__file__).parent.parent  # Points to doc/ directory

# CSS styling for the PDF
CSS_STYLES = """
@page {
    size: A4;
    margin: 2cm;
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 10px;
        color: #666;
    }
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

h1 {
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
    page-break-after: avoid;
}

h2 {
    color: #2980b9;
    margin-top: 30px;
    page-break-after: avoid;
}

h3 {
    color: #16a085;
    page-break-after: avoid;
}

code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: "SF Mono", Monaco, "Courier New", monospace;
    font-size: 10pt;
}

pre {
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 15px;
    overflow-x: auto;
    font-size: 9pt;
    page-break-inside: avoid;
}

pre code {
    background-color: transparent;
    padding: 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
    font-size: 10pt;
}

th, td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}

th {
    background-color: #3498db;
    color: white;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

blockquote {
    border-left: 4px solid #3498db;
    margin: 20px 0;
    padding: 10px 20px;
    background-color: #f9f9f9;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 30px 0;
}

.page-break {
    page-break-before: always;
}

ul, ol {
    margin: 10px 0;
    padding-left: 30px;
}

li {
    margin: 5px 0;
}

a {
    color: #3498db;
    text-decoration: none;
}
"""


def read_markdown(filepath: Path) -> str:
    """Read markdown file content."""
    return filepath.read_text()


def convert_to_html(md_content: str) -> str:
    """Convert markdown to HTML with extensions."""
    return markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite', 'toc']
    )


def main():
    # Read all markdown files
    readme = read_markdown(DOC_DIR / "README.md")
    get_doc = read_markdown(DOC_DIR / "trade" / "get.md")
    post_doc = read_markdown(DOC_DIR / "trade" / "post.md")

    # Combine content with page breaks
    combined_md = f"""{readme}

<div class="page-break"></div>

{post_doc}

<div class="page-break"></div>

{get_doc}
"""

    # Convert to HTML
    html_content = convert_to_html(combined_md)

    # Wrap in full HTML document
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>VOCSET API Documentation</title>
</head>
<body>
{html_content}
</body>
</html>
"""

    # Generate PDF (output to pdf/ subdirectory)
    output_path = DOC_DIR / "pdf" / "VOCSET_API_Documentation.pdf"
    HTML(string=full_html, base_url=str(DOC_DIR)).write_pdf(
        output_path,
        stylesheets=[CSS(string=CSS_STYLES)]
    )

    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    main()