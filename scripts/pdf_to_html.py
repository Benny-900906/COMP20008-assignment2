"""
a module for handling PDFs

if you want to run this, you'll need pdftotree,
which needs Java

"""

import pdftotree

DEFAULT_PDF  = 'raw_data/1_school_vce_performance.pdf'
DEFAULT_HTML = 'raw_data/1_school_vce_performance.html'

def pdf_to_html(pdf_filename, html_filename):
    """
        take a PDF file and convert it to an HTML file
    """

    html = pdftotree.parse(pdf_filename)

    with open(html_filename, 'w') as html_file:
        html_file.write(html)


if __name__ == '__main__':
    pdf_to_html(DEFAULT_PDF, DEFAULT_HTML)
