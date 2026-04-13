from playwright.async_api import async_playwright
import bs4

import utils.log
import config

logger = utils.log.get_logger(__name__)

async def get_page_async(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=config.WEB_CLIENT_HEADLESS)
        page = await browser.new_page()

        try:
            for _ in range(3):
                try:
                    await page.goto(url, wait_until="load", timeout=90000)
                    await page.wait_for_load_state("domcontentloaded")

                    await page.wait_for_timeout(config.WEB_CLIENT_TIMEOUT)
                    return bs4.BeautifulSoup(await page.content(), "html.parser")
                except Exception as e:
                    logger.debug(f"Error: {e}")
        finally:
            await browser.close()