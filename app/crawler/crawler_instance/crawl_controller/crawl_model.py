# Local Imports
import threading
import requests
from time import sleep
from crawler.constants import status
from crawler.constants.constant import CRAWL_SETTINGS_CONSTANTS, RAW_PATH_CONSTANTS
from crawler.constants.strings import MANAGE_CRAWLER_MESSAGES
from crawler.crawler_instance.crawl_controller.crawl_enums import CRAWL_MODEL_COMMANDS
from crawler.crawler_instance.genbot_service import genbot_controller
from crawler.crawler_instance.tor_controller.tor_controller import tor_controller
from crawler.crawler_instance.tor_controller.tor_enums import TOR_COMMANDS
from crawler.crawler_services.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.crawler_services.redis_manager.redis_enums import REDIS_COMMANDS
from crawler.crawler_services.helper_services.helper_method import helper_method
from crawler.crawler_shared_directory.log_manager.log_controller import log
from crawler.crawler_shared_directory.request_manager.request_handler import request_handler


class crawl_model(request_handler):

    # Start Crawler Manager
    def __install_live_url(self):
        m_request_handler, headers = tor_controller.get_instance().invoke_trigger(TOR_COMMANDS.S_CREATE_SESSION, [False])
        while True:
            try:
                m_response = m_request_handler.get(CRAWL_SETTINGS_CONSTANTS.S_START_URL, headers=headers, timeout=CRAWL_SETTINGS_CONSTANTS.S_URL_TIMEOUT, proxies={}, allow_redirects=True)
                break
            except Exception as ex:
                log.g().e(ex)
                sleep(50)

        return m_response.text.splitlines()

    def __post_updated_urls(self):
        try:
            response = requests.get(CRAWL_SETTINGS_CONSTANTS.S_UPDATE_URL + "?type=clean")
            log.g().s(response.text)

            with open(RAW_PATH_CONSTANTS.S_UNIQUE_HOST_FILE) as f:
                m_url_list = f.read().splitlines()

            for url in m_url_list:
                try:
                    requests.get(CRAWL_SETTINGS_CONSTANTS.S_UPDATE_URL+"?type=add&url=" + url)
                    log.g().s(url + " : url installed")
                except Exception:
                    pass

        except Exception as ex:
            log.g().e(ex)

    def __start_request(self):
        log.g().i(MANAGE_CRAWLER_MESSAGES.S_REINITIALIZING_CRAWLABLE_URL)

        m_counter = 0
        while True:
            m_live_url_list = self.__install_live_url()
            m_counter += 1
            for m_url_node in m_live_url_list:

                try:
                    while status.S_THREAD_COUNT >= CRAWL_SETTINGS_CONSTANTS.S_MAX_THREAD_COUNT:
                        sleep(0.1)
                        continue

                    status.S_THREAD_COUNT += 1
                    threading.Thread(target=genbot_controller.genbot_instance, args=[m_url_node]).start()
                except Exception as ex:
                    log.g().e(str(ex) + " : GLOBAL EXCEPTION")

            while status.S_THREAD_COUNT > 0:
                sleep(432000)
                continue

            if m_counter == 6:
                redis_controller.get_instance().invoke_trigger(REDIS_COMMANDS.S_CLEAN, [])
                helper_method.sort_result(RAW_PATH_CONSTANTS.S_UNIQUE_HOST_FILE)
                self.__post_updated_urls()
                log.g().s("GLOBAL DUPLICATION CRAWL FINISHED")
                log.g().s("Crawler Sleeping")
                sleep(15)
                log.g().s("Crawler Waking up")

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == CRAWL_MODEL_COMMANDS.S_INIT:
            self.__start_request()
