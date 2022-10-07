import inspect
import sys
import logging
import os
import datetime
from termcolor import colored

if sys.platform == "win32":
    os.system('color')
else:
    pass


class log:
    __server_instance = None
    __instance = None

    def __configure_logs(self):
        self.__server_instance = logging.getLogger('genesis_logs')
        self.__server_instance.setLevel(logging.DEBUG)

        self.__server_instance.warning("Warning message", {'app': 'bloop'})
        self.__server_instance.info("Info message")

    # Initializations
    @staticmethod
    def g():
        if log.__server_instance is None:
            log()
        return log.__server_instance

    def __init__(self):
        log.__server_instance = self
        self.__configure_logs()

    def get_caller_class(self):
        m_prev_frame = inspect.currentframe().f_back.f_back
        return str(m_prev_frame.f_locals["self"].__class__.__name__)

    # Info Logs
    def i(self, p_log):
        filter_log = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " : " + self.get_caller_class() + " : " + str(p_log))

        # self.__server_instance.debug(filter_log)
        print(colored(filter_log, 'cyan'))

    # Success Logs
    def s(self, p_log):
        filter_log = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " : " + self.get_caller_class() + " : " + str(p_log))

        # self.__server_instance.info(filter_log)
        print(colored(filter_log, 'green'))

    # Warning Logs
    def w(self, p_log):
        filter_log = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " : " + self.get_caller_class() + " : " + str(p_log))

        # self.__server_instance.warning(filter_log)
        print(colored(filter_log, 'yellow'))

    # Error Logs
    def e(self, p_log):
        filter_log = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " : " + self.get_caller_class() + " : " + str(p_log))

        # self.__server_instance.error(filter_log)
        print(colored(filter_log, 'blue'))

    # Error Logs
    def c(self, p_log):
        filter_log = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " : " + self.get_caller_class() + " : " + str(p_log))

        # self.__server_instance.critical(filter_log)
        print(colored(filter_log, 'red'))
