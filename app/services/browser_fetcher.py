from playwright.async_api import async_playwright

async def fetch_via_browser(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_load_state("networkidle")
            return await page.content()
        finally:
            await browser.close()
