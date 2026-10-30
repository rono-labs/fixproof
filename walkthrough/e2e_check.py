#!/usr/bin/env python3
"""Headless check. Usage: e2e_check.py OUTDIR  (needs playwright and /usr/bin/chromium)."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
errors = []


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/chromium",
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1600, "height": 900})
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("requestfailed", lambda r: errors.append("failed " + r.url))
        base = (HERE / "index.html").as_uri()
        for sid, n in (("A", 13), ("C", 11), ("E", 5)):
            pg.goto(f"{base}?s={sid}&step=all")
            assert pg.locator("article.card").count() == n, sid
            assert pg.locator("#answer").count() == 1
            pg.screenshot(path=str(out / f"walkthrough-{sid}-start.png"))
            pg.evaluate("document.getElementById('answer').scrollIntoView({block:'start'})")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(out / f"walkthrough-{sid}-answer.png"))
            print(sid, "cards", n, "verdict", pg.locator("#verdict").all_inner_texts())
        pg.goto(base + "?s=A")
        pg.click("#next")
        pg.click("#tab-C")
        assert pg.locator("article.card").count() == 0
        pg.click("#tab-A")
        pg.click("#play")
        assert pg.inner_text("#play") == "Pause"
        pg.wait_for_timeout(5500)
        n = pg.locator("article.card").count()
        print("cards after play 5.5s:", n, pg.inner_text("#counter"))
        assert 3 <= n <= 5
        pg.screenshot(path=str(out / "walkthrough-A-midplay.png"))
        pg.click("#play")
        assert pg.inner_text("#play") == "Play"
        pg.click("#reset")
        assert pg.locator("article.card").count() == 0
        for i in range(14):
            pg.click("#next")
        assert pg.locator("article.card").count() == 13 and pg.locator("#second-turn").count() == 1
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(out / "walkthrough-A-manual-end.png"))
        text = pg.inner_text("body")
        assert "—" not in text and "TODO" not in text
        b.close()
    print("console errors:", len(errors), errors)
    sys.exit(1 if errors else 0)


main()
