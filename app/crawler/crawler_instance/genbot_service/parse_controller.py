# Local Imports
from copy import copy

from crawler.crawler_instance.genbot_service.html_parse_manager import html_parse_manager
from crawler.crawler_instance.local_shared_model.url_model import url_model


class parse_controller:

    m_static_parser = None
    m_html_parser = None

    def on_parse_html(self, p_html, p_request_model: url_model):
        return self.__on_html_parser_invoke(copy(p_request_model.m_url), p_html)

    def __on_html_parser_invoke(self, p_base_url, p_html):

        self.m_html_parser = html_parse_manager(p_base_url)
        self.m_html_parser.feed(p_html)
        return self.m_html_parser.parse_html_files()
