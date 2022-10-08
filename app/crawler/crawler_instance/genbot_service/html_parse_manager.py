# Local Imports
from abc import ABC
from html.parser import HTMLParser
from bs4 import BeautifulSoup


class html_parse_manager(HTMLParser, ABC):

    def __init__(self, m_html):
        super().__init__()
        self.m_html = m_html

    def parse_html_files(self):
        m_soup = BeautifulSoup(self.m_html, "html.parser")
        return m_soup.get_text()[1:500]
