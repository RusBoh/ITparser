import logging
import utils.log
import datetime

LOG_LEVEL = logging.DEBUG
LOG_FILE_PATH = f"logs/log-{datetime.datetime.now().date()}.txt"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

DB_FILE_PATH = "data/webs.db"

WEB_LIST_PATH = "configs/webs.txt"
PAGES_LIST = []

WEB_CLIENT_HEADLESS = True
WEB_CLIENT_TIMEOUT = 5000

PARSER_FIND_PATTERN = r"/(nabidka|job)/"

def set_pages_list():
    logger = utils.log.get_logger(__name__)

    logger.debug(f"Trying to get pages file ({WEB_LIST_PATH})")
    file = open(WEB_LIST_PATH, "r")

    for i in file:
        try:
            PAGES_LIST.append(i.replace("\n", ""))
        except Exception as e:
            logger.error(f"Exception: {e}")
    
    logger.debug(f"Fetched {len(PAGES_LIST)} page link(s) from file")