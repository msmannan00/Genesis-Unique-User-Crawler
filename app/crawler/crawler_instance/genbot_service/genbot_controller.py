# Local Imports
from crawler.crawler_instance.genbot_service.genbot_enums import ICRAWL_CONTROLLER_COMMANDS
from crawler.crawler_instance.local_shared_model.url_model import url_model, url_model_init
from crawler.crawler_instance.tor_controller.tor_controller import tor_controller
from crawler.crawler_instance.tor_controller.tor_enums import TOR_COMMANDS
from crawler.crawler_services.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.crawler_services.redis_manager.redis_enums import REDIS_COMMANDS, REDIS_KEYS
from crawler.crawler_instance.genbot_service.parse_controller import parse_controller
from crawler.crawler_instance.genbot_service.web_request_handler import webRequestManager
from crawler.crawler_services.url_duplication_manager.html_duplication_controller import html_duplication_controller
from crawler.crawler_shared_directory.log_manager.log_controller import log
from crawler.crawler_shared_directory.request_manager.request_handler import request_handler

import os
import sys
import xxhash


class genbot_controller(request_handler):
    hashseed = os.getenv('PYTHONHASHSEED')
    if not hashseed:
        os.environ['PYTHONHASHSEED'] = '0'
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def __init__(self):
        self.__m_web_request_handler = webRequestManager()
        self.__html_duplication_handler = html_duplication_controller()
        self.__m_html_parser = parse_controller()

    def validate_duplicate_host_url(self, p_request_url, p_raw_html, p_full_content):

        m_hash_duplication_key = str(xxhash.xxh64_intdigest(p_full_content))
        m_hashed_duplication_status = redis_controller.get_instance().invoke_trigger(REDIS_COMMANDS.S_GET_STRING, [m_hash_duplication_key, None, 60 * 60 * 24 * 5])
        if m_hashed_duplication_status is None:
            files = redis_controller.get_instance().invoke_trigger(REDIS_COMMANDS.S_GET_LIST, [REDIS_KEYS.RAW_HTML_CODE + p_request_url, None, None])
            m_max_similarity = 0
            for html in files:
                m_similarity = self.__html_duplication_handler.verify_structural_duplication(p_raw_html, html)
                if m_similarity > m_max_similarity:
                    m_max_similarity = m_similarity

            print(m_max_similarity, flush=True)
            redis_controller.get_instance().invoke_trigger(REDIS_COMMANDS.S_SET_LIST, [REDIS_KEYS.RAW_HTML_CODE + p_request_url, p_raw_html, None, None])
            redis_controller.get_instance().invoke_trigger(REDIS_COMMANDS.S_SET_FLOAT, [REDIS_KEYS.RAW_HTML_SCORE + p_request_url, m_max_similarity, None])
            if m_max_similarity < 0.90:
                return True, True

        return False, True

    def __trigger_url_request(self, p_request_model: url_model):
        try:
            self.__m_proxy, self.__m_tor_id = tor_controller.get_instance().invoke_trigger(TOR_COMMANDS.S_PROXY, [])
            m_redirected_url, m_response, m_raw_html = self.__m_web_request_handler.load_url(p_request_model.m_url, self.__m_proxy)
            if m_response is True:
                m_parsed_model, m_images = self.__m_html_parser.on_parse_html(m_raw_html, p_request_model)
                return self.validate_duplicate_host_url(p_request_model.m_url, m_raw_html, m_parsed_model.m_extended_content)
            else:
                return False, False

        except Exception as ex:
            print(ex, flush=True)
            return False, False

    # Wait For Crawl Manager To Provide URL From Queue
    def start_crawler_instance(self, p_request_url):
        m_duplicate_status, m_request_status = self.__trigger_url_request(url_model_init(p_request_url, 0))
        if m_duplicate_status:
            log.g().s(p_request_url + " : SUCCESS")
        elif m_request_status:
            log.g().w(p_request_url + " : DUPLICATE")
        else:
            log.g().e(p_request_url + " : FAILED")

        return m_request_status

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == ICRAWL_CONTROLLER_COMMANDS.S_START_CRAWLER_INSTANCE:
            return self.start_crawler_instance(p_data[0])


def genbot_instance(p_url):
    try:
        log.g().i(p_url + " : STARTED")
        m_crawler = genbot_controller()
        return m_crawler.invoke_trigger(ICRAWL_CONTROLLER_COMMANDS.S_START_CRAWLER_INSTANCE, [p_url])
    except Exception as ex:
        log.g().e(str(ex) + " : LOCAL EXCEPTION")
