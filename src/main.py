import config
from utils import log


def main():
    log.set_logger(config.LOG_LEVEL, config.LOG_FILE_PATH, config.LOG_FORMAT)
    logger = log.get_logger(__name__)

    logger.info("Parser started")

    logger.info("Reading links from config file...")
    try:
        config.set_pages_list()
    except Exception as e:
        logger.fatal(f"Fatal error: {e}")
        return

    from utils import web_client

    pages = []
    logger.info("Getting pages from links...")
    for i in config.PAGES_LIST:
        try:
            pages.append(web_client.get_page(i))
        except Exception as e:
            logger.error(f"Error: {e}")
    
    print(len(pages))

if __name__ == "__main__":
    main()