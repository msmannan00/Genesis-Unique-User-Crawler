from bs4 import BeautifulSoup
from crawler.constants.constant import CRAWL_SETTINGS_CONSTANTS
from crawler.crawler_instance.tor_controller.tor_controller import tor_controller
from crawler.crawler_instance.tor_controller.tor_enums import TOR_COMMANDS


class webRequestManager:

    def __init__(self):
        pass

    def load_url(self, p_url, p_custom_proxy):
        m_request_handler, headers = tor_controller.get_instance().invoke_trigger(TOR_COMMANDS.S_CREATE_SESSION, [True])
        try:
            page = m_request_handler.get(p_url, headers=headers, timeout=CRAWL_SETTINGS_CONSTANTS.S_URL_TIMEOUT, proxies=p_custom_proxy, allow_redirects=True, )
            soup = page.content
            if page == "" or page.status_code != 200:
                return p_url, False, page.status_code
            else:
                return page.url, True, str(soup)

        except Exception:
            return p_url, False, None
