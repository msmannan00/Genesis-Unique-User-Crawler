# Local Imports

from crawler.crawler_instance.crawl_controller.crawl_enums import CRAWL_CONTROLLER_COMMANDS, CRAWL_MODEL_COMMANDS
from crawler.crawler_instance.crawl_controller.crawl_model import crawl_model
from crawler.crawler_shared_directory.request_manager.request_handler import request_handler


class crawl_controller(request_handler):

    # Local Variables
    __m_crawl_model = None

    # Initializations
    def __init__(self):
        self.__m_crawl_model = crawl_model()

    def __on_start(self):
        self.__m_crawl_model.invoke_trigger(CRAWL_MODEL_COMMANDS.S_INIT)

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == CRAWL_CONTROLLER_COMMANDS.S_RUN_CRAWLER:
            self.__on_start()
