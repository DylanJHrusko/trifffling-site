"""Fast checks that must pass before an image is built or deployed."""
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = self.h1 = ""
        self.scripts, self.styles, self.inline_scripts = [], [], 0
        self._in = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script":
            if attrs.get("src"):
                self.scripts.append(attrs["src"])
            else:
                self.inline_scripts += 1
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.styles.append(attrs["href"])
        if tag in ("title", "h1"):
            self._in = tag

    def handle_endtag(self, tag):
        self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "h1":
            self.h1 += data


def main():
    page = Page()
    page.feed((SITE / "index.html").read_text())
    checks = {
        "page has a title": bool(page.title.strip()),
        "heading names the site owner": "Dylan" in page.h1,
        "no inline scripts (CSP blocks them)": page.inline_scripts == 0,
        "every script and stylesheet exists": all(
            (SITE / ref.lstrip("/")).is_file() for ref in page.scripts + page.styles),
        "release note present": 'id="release-note"' in (SITE / "index.html").read_text(),
        "nginx hides its version": "server_tokens off;" in (ROOT / "nginx/default.conf").read_text(),
        "image runs as non-root": "USER 101" in (ROOT / "Dockerfile").read_text(),
    }
    for name, passed in checks.items():
        print(("PASS " if passed else "FAIL ") + name)
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
