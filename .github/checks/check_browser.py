"""Smoke checks in Chromium against a temporary loopback-only HTTP server."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

from check_site import ROOT, route, site_pages


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f"http://127.0.0.1:{server.server_port}"
    errors = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            for width in (390, 1280):
                context = browser.new_context(viewport={"width": width, "height": 900})
                # External services are not a release gate. Fonts use local fallbacks.
                context.route("**/*", lambda request: request.continue_()
                              if urlsplit(request.request.url).netloc == urlsplit(origin).netloc
                              else request.fulfill(status=200, body=""))
                page = context.new_page()
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on("response", lambda response: errors.append(f"HTTP {response.status}: {response.url}")
                        if response.status >= 400 else None)
                for path in site_pages():
                    url = origin + route(path)
                    response = page.goto(url, wait_until="networkidle")
                    if response is None or response.status != 200:
                        errors.append(f"Page unavailable: {url}")
                    if not page.locator("h1").is_visible():
                        errors.append(f"Hidden h1: {url}")
                    state = page.evaluate("""() => ({
                      overflow: document.documentElement.scrollWidth > innerWidth + 1,
                      broken: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src)
                    })""")
                    if state["overflow"] or state["broken"]:
                        errors.append(f"{width}px {url}: {state}")
                page.goto(origin + "/zamysleni/", wait_until="networkidle")
                expected = page.locator(".reading-list .reading-card a").first.get_attribute("href")
                page.goto(origin, wait_until="networkidle")
                if page.locator(".reading-latest").get_attribute("href") != expected:
                    errors.append("Latest-excerpt JavaScript link does not match first overview card")
                context.close()
            context = browser.new_context(java_script_enabled=False)
            page = context.new_page()
            page.goto(origin, wait_until="domcontentloaded")
            fallback = page.locator(".reading-latest").get_attribute("href")
            if not fallback or not fallback.startswith("/zamysleni/"):
                errors.append("Missing static latest-excerpt fallback")
            else:
                response = page.goto(origin + fallback, wait_until="domcontentloaded")
                if response.status != 200 or not page.locator("h1").is_visible():
                    errors.append("Static latest-excerpt fallback is broken")
            context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    if errors:
        raise SystemExit("\n".join(errors))
    print("PASS: desktop 1280px, mobile 390px, local resources, JavaScript and static fallback")


if __name__ == "__main__":
    main()
