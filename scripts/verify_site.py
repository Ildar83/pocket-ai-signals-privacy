"""Read-only HTTP and mobile checks for the published static privacy page."""
import argparse
import json
import re
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("--output", default="verification")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
expected_page = BeautifulSoup((root / "docs/index.html").read_text(), "html.parser")
expected_article = expected_page.find("article")
assert expected_article is not None
expected = normalize(expected_article.get_text())

with urlopen(args.url, timeout=30) as response:
    status = response.status
    content = response.read().decode("utf-8")
    content_type = response.headers.get("Content-Type", "")
assert status == 200 and "text/html" in content_type
public = BeautifulSoup(content, "html.parser")
public_article = public.find("article")
assert public_article is not None
assert normalize(public_article.get_text()) == expected
assert not public.select("script, img, iframe, form, button, video")
assert len(public.select("h2")) == 9
with urlopen(urljoin(args.url, "styles.css"), timeout=30) as response:
    assert response.status == 200
with urlopen(urljoin(args.url, "manus-routes.json"), timeout=30) as response:
    routes = json.load(response)
    assert routes == {"routes": [{"path": "/", "title": "Privacy Policy — Pocket AI Signals"}]}

results = {"url": args.url, "http_status": status, "content_type": content_type,
           "full_text_matches": True, "sections": 9, "javascript_required": False,
           "anonymous_access": True, "viewports": []}
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/chromium", headless=True,
                                args=["--no-sandbox", "--disable-dev-shm-usage"])
    for width in [320, 390, 768, 1440]:
        context = browser.new_context(viewport={"width": width, "height": 844},
                                      java_script_enabled=False,
                                      is_mobile=width < 768, device_scale_factor=1)
        page = context.new_page()
        response = page.goto(args.url, wait_until="networkidle", timeout=60000)
        assert response and response.status == 200
        assert normalize(page.locator("article").text_content() or "") == expected
        geometry = page.evaluate("""() => ({
          viewport: innerWidth,
          scrollWidth: document.documentElement.scrollWidth,
          paragraphs: [...document.querySelectorAll('p,li')].map(e => ({
            font: parseFloat(getComputedStyle(e).fontSize),
            left: e.getBoundingClientRect().left,
            right: e.getBoundingClientRect().right
          }))
        })""")
        assert geometry["scrollWidth"] <= geometry["viewport"]
        assert all(e["font"] >= 16 and e["left"] >= 0 and
                   e["right"] <= width + 1 for e in geometry["paragraphs"])
        assert len(context.cookies()) == 0
        results["viewports"].append({"width": width, "no_horizontal_overflow": True,
                                      "body_font_min_px": min(e["font"] for e in geometry["paragraphs"]),
                                      "no_cookies": True})
        if width == 390:
            page.screenshot(path=str(out / "mobile-top.png"))
            page.locator("h2").last.scroll_into_view_if_needed()
            page.screenshot(path=str(out / "mobile-contact.png"))
        context.close()
    browser.close()
(out / "checks.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(results, ensure_ascii=False, indent=2))
