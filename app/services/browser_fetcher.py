from playwright.async_api import async_playwright


async def fetch_via_browser(url: str) -> str:
    async with async_playwright() as p:

        # Launch chromium with anti-detection args
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="en-US"
        )

        page = await context.new_page()

        try:
            # Go to page
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)

            # Wait for JS rendering
            await page.wait_for_load_state("networkidle")

            # Small extra buffer for heavy JS sites
            await page.wait_for_timeout(2000)

            content = await page.content()
            return content

        finally:
            await browser.close()
