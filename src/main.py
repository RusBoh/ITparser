import config, sqlite3, asyncio
from utils import log


async def main():
    #Setting root logger
    log.set_logger(config.LOG_LEVEL, config.LOG_FILE_PATH, config.LOG_FORMAT)
    logger = log.get_logger(__name__)

    from parser import parser
    from pipeline import exporter 

    logger.info("Parser started")

    try:
        logger.info("Connecting to db...")
        db = sqlite3.connect(config.DB_FILE_PATH)
        cursor = db.cursor()

    except Exception as e:
        logger.fatal(f"Fatal error: {e}")
        return

    try:
        #Creating table...
        logger.info("Creating table...")
        exporter.del_table(cursor, "items")
        exporter.create_table(cursor, "items", {"url": "TEXT", "title": "TEXT"})
        db.commit()

        #Reading links from config file...
        logger.info("Reading links from config file...")
        config.set_pages_list()

        #Getting all links from pages...
        logger.info("Getting all links from pages...")
        tasks = [parser.parse_page(i) for i in config.PAGES_LIST]
        pages = await asyncio.gather(*tasks)

        #Extracting links from pages...
        logger.info("Extracting links from pages...")

        links = []
        [links.extend(parser.create_item_links(i)) for i in pages]
        links = list(set(links))
        
        logger.info(f"Total links got: {len(links)}")

        #Getting item pages from links...
        logger.info("Getting item pages from links...")
        tasks = [parser.parse_item_page(i) for i in links]
        items = await asyncio.gather(*tasks)

        #Saving items to db...
        logger.info("Saving items to db...")
        [exporter.add_item(cursor, "items", {"url": i[0], "title": i[1]}) for i in items]

        db.commit() #Commiting changes

        logger.info("Changes committed")

    except Exception as e:
        logger.fatal(f"Fatal error: {e}")

    cursor.close()
    db.close()


if __name__ == "__main__":
    asyncio.run(main())