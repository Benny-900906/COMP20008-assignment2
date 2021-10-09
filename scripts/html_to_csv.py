"""
script for handling html files
"""

DEFAULT_HTML = 'raw_data/1_school_vce_performance.html'
DEFAULT_CSV  = 'raw_data/1_school_vce_performance.csv'

import html
from bs4 import BeautifulSoup

def html_to_csv(html_filename, csv_filename):
    """
    """

    # import the html
    with open(html_filename, 'r') as html_file:
        html = BeautifulSoup(html_file.read(), 'html.parser')
    
    print(html)

if __name__ == '__main__':
    html_to_csv(DEFAULT_HTML, DEFAULT_CSV)
