import asyncio
import sys
import traceback
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from config import PLAYWRIGHT_TIMEOUT, HEADERS


# Extended stealth script — masks all common bot-detection vectors
STEALTH_SCRIPT = """
// 1. Hide webdriver flag
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

// 2. Fake plugins list
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5],
});

// 3. Fake language
Object.defineProperty(navigator, 'languages', {
    get: () => ['id-ID', 'id', 'en-US', 'en'],
});

// 4. Fix chrome object
window.chrome = { runtime: {} };

// 5. Fix permissions query
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications'
        ? Promise.resolve({ state: Notification.permission })
        : originalQuery(parameters)
);

// 6. WebGL vendor spoof
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    if (parameter === 37445) return 'Intel Inc.';
    if (parameter === 37446) return 'Intel Iris OpenGL Engine';
    return getParameter.call(this, parameter);
};
"""


def _is_windows_selector_loop() -> bool:
    if sys.platform != "win32":
        return False

    loop = asyncio.get_running_loop()
    return not isinstance(loop, asyncio.ProactorEventLoop)


def _fetch_html_in_proactor_loop(url: str) -> str:
    loop = asyncio.ProactorEventLoop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_fetch_html_with_playwright(url))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        asyncio.set_event_loop(None)
        loop.close()


async def fetch_html(url: str) -> str:
    if _is_windows_selector_loop():
        return await asyncio.to_thread(_fetch_html_in_proactor_loop, url)

    return await _fetch_html_with_playwright(url)


async def _fetch_html_with_playwright(url: str) -> str:
    """
    Launch headless Chromium with full stealth mode to bypass Cloudflare,
    navigate to URL, wait for page to fully render, return HTML string.
    Raises Exception with detailed message on failure.
    """
    last_error = None

    # Retry up to 2 times
    for attempt in range(1, 3):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--disable-blink-features=AutomationControlled",
                        "--disable-features=IsolateOrigins,site-per-process",
                        "--window-size=1280,800",
                    ],
                )

                context = await browser.new_context(
                    user_agent=HEADERS["User-Agent"],
                    locale="id-ID",
                    timezone_id="Asia/Jakarta",
                    viewport={"width": 1280, "height": 800},
                    java_script_enabled=True,
                    accept_downloads=False,
                    extra_http_headers={
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                    },
                )

                await context.add_init_script(STEALTH_SCRIPT)
                page = await context.new_page()

                # Block unnecessary resources to speed up loading
                await page.route(
                    "**/*.{png,jpg,jpeg,gif,svg,ico,woff,woff2,ttf,otf}",
                    lambda route: route.abort(),
                )

                try:
                    await page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=PLAYWRIGHT_TIMEOUT,
                    )

                    # Wait for Cloudflare challenge to pass (if any)
                    # Cloudflare usually resolves within 5 seconds
                    for _ in range(6):
                        title = await page.title()
                        if "just a moment" in title.lower() or "cloudflare" in title.lower():
                            await asyncio.sleep(2)
                        else:
                            break

                    # Ensure body is present
                    await page.wait_for_selector("body", timeout=15000)

                    # Small extra wait for JS-rendered content
                    await asyncio.sleep(1)

                    html = await page.content()
                finally:
                    await browser.close()

            return html

        except PlaywrightTimeout as e:
            last_error = f"Timeout on attempt {attempt} fetching '{url}': {str(e)}"
        except Exception as e:
            last_error = f"Error on attempt {attempt} fetching '{url}': {str(e)}\n{traceback.format_exc()}"

        # Wait before retry
        await asyncio.sleep(2)

    raise Exception(last_error or f"Failed to fetch '{url}' after 2 attempts")
