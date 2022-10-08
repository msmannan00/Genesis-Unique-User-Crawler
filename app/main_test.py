import os
import sys

import xxhash
from crawler.crawler_services.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.crawler_services.redis_manager.redis_enums import REDIS_COMMANDS, REDIS_CONNECTIONS

hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, [sys.executable] + sys.argv)

REDIS_CONNECTIONS.S_DATABASE_IP = "localhost"
REDIS_CONNECTIONS.S_DATABASE_PASSWORD = ""

m_hash_duplication_key = str(xxhash.xxh64_intdigest("TESTxxxxx"))
m_hashed_duplication_status = redis_controller.get_instance().invoke_trigger(REDIS_COMMANDS.S_GET_STRING, [m_hash_duplication_key, None, None])
xx = redis_controller.get_instance().invoke_trigger(REDIS_COMMANDS.S_SET_STRING, [m_hash_duplication_key, "TESTxxxxx", None])


redis_controller.get_instance().invoke_trigger(REDIS_COMMANDS.S_CLEAN, [])
