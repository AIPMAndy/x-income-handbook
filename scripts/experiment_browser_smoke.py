#!/usr/bin/env python3
"""Real headless Chromium smoke checks at three viewport sizes; not an iOS/Android device audit."""
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "screenshots" / "experiment"
OUT.mkdir(parents=True, exist_ok=True)
Handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{server.server_port}/experiment.html"
try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for label, width, height in [("mobile-360",360,780), ("mobile-390",390,844), ("desktop-1280",1280,900)]:
            context = browser.new_context(viewport={"width": width, "height": height}, accept_downloads=True)
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(url, wait_until="networkidle")
            assert page.locator("h1").count() == 1
            assert page.locator("#experimentCount").inner_text() == "0 条实验记录"
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), f"{label}: overflow initial"
            page.locator("#name").fill("仅用于浏览器测试：求职教程")
            page.locator("#impressions").fill("1000")
            page.locator("#visits").fill("50")
            page.locator("#leads").fill("5")
            page.locator("#orders").fill("1")
            page.locator("#revenue").fill("400")
            page.locator("#cost").fill("100")
            page.get_by_role("button", name="保存到当前浏览器").click()
            assert page.locator("#totalLeads").inner_text() == "5"
            assert page.locator("#visitRate").inner_text() == "5.00%"
            assert page.locator("#leadRate").inner_text() == "10.00%"
            assert page.locator("#orderRate").inner_text() == "20.00%"
            assert page.locator("#netContribution").inner_text() == "¥ 300"
            assert page.locator("#recordsBody tr").count() == 1
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), f"{label}: overflow with row"
            page.screenshot(path=str(OUT/f"{label}.png"), full_page=True)
            with page.expect_download() as download_info:
                page.locator("#exportCsv").click()
            download = download_info.value
            assert download.suggested_filename.endswith(".csv")
            page.reload(wait_until="networkidle")
            assert page.locator("#totalLeads").inner_text() == "5", "localStorage persistence failed"
            page.locator("#formatFilter").select_option("观点")
            assert page.locator("#recordsBody tr").count() == 0
            page.locator("#formatFilter").select_option("全部")
            assert page.locator("#recordsBody tr").count() == 1
            page.on("dialog", lambda dialog: dialog.accept())
            page.get_by_role("button", name="删除实验：仅用于浏览器测试：求职教程").click()
            assert page.locator("#recordsBody tr").count() == 0
            assert not errors, errors
            print(f"PASS {label}: form, ratios, local storage, CSV download, filter, delete and no overflow")
            context.close()
        browser.close()
finally:
    server.shutdown()
