import bs4, re
import config
import parser.functions
import utils.log

from utils import web_client


logger = utils.log.get_logger(__name__)

def get_main_element(soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
    logger.debug("Finding main element...")
    mains = soup.find_all("main")

    for i in mains:
        if not i.find("main"):
            return i

def create_item_links(item: tuple) -> list:
    links = []
    logger.debug(f"Extracting links from page {item[0]}...")
    for i in item[1]:
        try:
            if re.match(r"^https?://", i):
                links.append(i)
            else:
                links.append(re.match(r"^https?://[\w+.?]+", item[0]).group() + i)
        except Exception as e:
            logger.debug(f"Error: {e} - skip item {item[1]}")
    
    return links

async def parse_page(url: str):
    logger.debug(f"Getting page from link {url}...")
    page = await web_client.get_page_async(url)
    
    if not page:
        return (url, [])

    logger.debug(f"Getting item list from page {url}...")
    try:
        items = parser.functions.pipe(page, [
                get_main_element,
                lambda x: x.find_all("a", class_ = re.compile(r"^(?!.*hidden).*$"), href = re.compile(config.PARSER_FIND_PATTERN)),
                lambda x: [i.get("href") for i in x],
        ])
    except Exception as e:
        logger.debug(f"Error: {e}")
        return (url, [])
    logger.debug(f"Got {len(items)} items")

    return (url, items)

async def parse_item_page(url: str):
    logger.debug(f"Getting page from link {url}...")
    page = await web_client.get_page_async(url)

    logger.debug("Getting title of item")

    title = ""
    try:
        title = parser.functions.pipe(page, [
            lambda x: x.find(parser.functions.is_header).text,
        ])
    except Exception as e:
        logger.debug(f"Error: {e}")

    return (url, title)