#!/usr/bin/env python3
"""Optional local visual smoke test. Requires Playwright and accessible local browser."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research/screenshots'
OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for name,width,height in [('desktop',1440,960),('mobile',390,844)]:
        page=browser.new_page(viewport={'width':width,'height':height})
        errors=[]
        page.on('pageerror',lambda exc:errors.append(str(exc)))
        page.goto((ROOT/'index.html').as_uri())
        assert page.locator('[data-chapter]').count()==26
        page.screenshot(path=str(OUT/f'01-{name}-home.png'))
        page.locator('[data-chapter="14"]').click()
        assert '场景演练' in page.locator('#dialogBody').inner_text()
        page.screenshot(path=str(OUT/f'02-{name}-workshop.png'))
        page.locator('#closeDialog').click()
        assert page.locator('#zeroOrders').inner_text()=='12.2%'
        page.locator('#rewardRegion').select_option('no')
        assert '不具备当前官方奖励' in page.locator('#rewardResult').inner_text()
        page.locator('#eligibility').scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f'03-{name}-eligibility.png'))
        assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
        assert not errors,errors
        print('PASS',name)
        page.close()
    browser.close()
