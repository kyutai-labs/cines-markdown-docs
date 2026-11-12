# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.31",
#   "beautifulsoup4>=4.12",
#   "markdownify>=0.13",
# ]
# ///
"""Mirror the CINES Adastra user documentation as Markdown.

Crawls https://dci.dci-gitlab.cines.fr/webextranet/ (a Sphinx site), extracts
the main article of each page, converts it to Markdown and writes it to
`docs/<same path>.md`. Internal links are rewritten to point to the local
Markdown files so agents can follow them with plain file reads.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import time
from collections import deque
from pathlib import Path, PurePosixPath
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup, NavigableString
from markdownify import MarkdownConverter

BASE_URL = "https://dci.dci-gitlab.cines.fr/webextranet/"
ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs"
SKIP_PAGES = {"genindex.html", "search.html", "py-modindex.html"}

session = requests.Session()
session.headers["User-Agent"] = "cines-markdown-docs (+https://github.com/kyutai-labs/cines-markdown-docs)"


def fetch(url: str) -> requests.Response:
    for attempt in range(5):
        try:
            r = session.get(url, timeout=60)
            if r.status_code < 500:
                return r
        except requests.RequestException as e:  # noqa: PERF203
            err = e
        time.sleep(2**attempt)
    raise RuntimeError(f"failed to fetch {url}: {locals().get('err') or r.status_code}")


def rel_path(url: str) -> str | None:
    """Return the page path relative to BASE_URL, or None if out of scope."""
    url, _ = urldefrag(url)
    if not url.startswith(BASE_URL):
        return None
    path = url[len(BASE_URL):].split("?")[0]
    if path == "" or path.endswith("/"):
        path += "index.html"
    if not path.endswith(".html") or path.startswith("_"):
        return None
    if path in SKIP_PAGES:
        return None
    return path


def seed_pages() -> list[str]:
    pages = ["index.html"]
    try:
        js = fetch(urljoin(BASE_URL, "searchindex.js")).text
        m = re.search(r'"docnames":\s*(\[.*?\])', js)
        if m:
            pages += [d + ".html" for d in json.loads(m.group(1))]
    except Exception as e:  # pragma: no cover - best effort
        print(f"warning: could not read searchindex.js: {e}", file=sys.stderr)
    return pages


class Converter(MarkdownConverter):
    def __init__(self, page_path: str, known_pages: set[str], **kw):
        super().__init__(**kw)
        self.page_url = urljoin(BASE_URL, page_path)
        self.page_dir = PurePosixPath(page_path).parent
        self.known_pages = known_pages

    def _rewrite(self, href: str) -> str:
        if not href or href.startswith(("mailto:", "tel:", "javascript:")):
            return href
        absolute = urljoin(self.page_url, href)
        target, frag = urldefrag(absolute)
        rp = rel_path(target)
        if rp is not None and rp in self.known_pages:
            md = PurePosixPath(rp).with_suffix(".md")
            rel = _relpath(md, self.page_dir)
            return rel + (f"#{frag}" if frag else "")
        return absolute

    def convert_a(self, el, text, *args, **kwargs):
        if el.get("href"):
            el["href"] = self._rewrite(el["href"])
        return super().convert_a(el, text, *args, **kwargs)

    def convert_img(self, el, text, *args, **kwargs):
        if el.get("src"):
            el["src"] = urljoin(self.page_url, el["src"])
        return super().convert_img(el, text, *args, **kwargs)


def _relpath(target: PurePosixPath, start: PurePosixPath) -> str:
    import os.path

    return os.path.relpath(str(target), str(start) if str(start) != "" else ".").replace("\\", "/")


def code_language(el) -> str:
    for parent in el.parents:
        for cls in parent.get("class", []) or []:
            if cls.startswith("highlight-"):
                lang = cls[len("highlight-"):]
                return "" if lang in ("default", "none", "text") else lang
    return ""


def clean_article(article) -> None:
    for sel in ["a.headerlink", "script", "style", "div.rst-footer-buttons", "button.copybtn"]:
        for t in article.select(sel):
            t.decompose()
    # Sphinx-design tabs: turn tab labels into bold headings so content isn't lost.
    for label in article.select("div.sd-tab-set > label"):
        label.name = "p"
        label.string = f"**[Tab] {label.get_text(strip=True)}**"
    for inp in article.select("div.sd-tab-set > input"):
        inp.decompose()
    # Admonitions: prefix with their title.
    for adm in article.select("div.admonition"):
        title = adm.find(class_="admonition-title")
        if title:
            title.name = "p"
            title.string = f"**{title.get_text(strip=True)}**"
    # Line-numbered code tables: keep only code column.
    for linenos in article.select("td.linenos"):
        linenos.decompose()
    # Keep Sphinx section ids / label targets as explicit HTML anchors so that
    # rewritten `page.md#label` links still resolve.
    for el in article.select("section[id], span[id]"):
        if el.find_parent("pre") or (el.name == "span" and el.get_text(strip=True)):
            continue
        el.insert_before(NavigableString(f"\n\n@@ANCHOR:{el['id']}@@\n\n"))


def page_to_markdown(path: str, html: str, known: set[str]) -> tuple[str, set[str]]:
    soup = BeautifulSoup(html, "html.parser")
    links: set[str] = set()
    page_url = urljoin(BASE_URL, path)
    for a in soup.find_all("a", href=True):
        rp = rel_path(urljoin(page_url, a["href"]))
        if rp:
            links.add(rp)

    article = soup.select_one('div[itemprop="articleBody"]') or soup.select_one('div[role="main"]') or soup.body
    clean_article(article)
    title = soup.title.get_text(strip=True).split(" — ")[0] if soup.title else path

    md = Converter(
        path,
        known,
        heading_style="ATX",
        bullets="-",
        code_language_callback=code_language,
        escape_underscores=False,
        escape_asterisks=False,
    ).convert_soup(article)
    md = re.sub(r"@@ANCHOR:([^@]+)@@", r'<a id="\1"></a>', md)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    header = f"<!-- Source: {page_url} -->\n<!-- Title: {title} -->\n\n"
    return header + md + "\n", links


def outline(md: str, max_level: int = 3) -> list[tuple[int, str, str]]:
    """(level, heading text, anchor) for h2..h{max_level}, using the last anchor seen."""
    result = []
    anchor = None
    in_code = False
    for line in md.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        m = re.fullmatch(r'<a id="([^"]+)"></a>', line)
        if m:
            anchor = anchor or m.group(1)
            continue
        h = re.match(r"(#{2,6}) (.+)", line)
        if h and anchor and len(h.group(1)) <= max_level:
            result.append((len(h.group(1)), h.group(2).strip(), anchor))
        if line.strip():
            anchor = None
    return result


def main() -> None:
    queue = deque(dict.fromkeys(seed_pages()))
    seen: set[str] = set(queue)
    pages: dict[str, str] = {}

    # First pass: fetch everything (BFS over internal links).
    while queue:
        path = queue.popleft()
        r = fetch(urljoin(BASE_URL, path))
        if r.status_code != 200 or "text/html" not in r.headers.get("content-type", ""):
            print(f"skip {path}: HTTP {r.status_code}", file=sys.stderr)
            continue
        r.encoding = "utf-8"
        pages[path] = r.text
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            rp = rel_path(urljoin(urljoin(BASE_URL, path), a["href"]))
            if rp and rp not in seen:
                seen.add(rp)
                queue.append(rp)
        print(f"fetched {path}", file=sys.stderr)

    if len(pages) < 10:
        sys.exit(f"only {len(pages)} pages fetched, refusing to overwrite docs/")

    known = set(pages)
    tmp = ROOT / "docs.tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    titles: dict[str, str] = {}
    outlines: dict[str, list[tuple[int, str, str]]] = {}
    for path, html in sorted(pages.items()):
        md, _ = page_to_markdown(path, html, known)
        outlines[path] = outline(md)
        out = tmp / PurePosixPath(path).with_suffix(".md")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        titles[path] = md.splitlines()[1].removeprefix("<!-- Title: ").removesuffix(" -->")

    # Flat index of every page for quick grepping by agents.
    lines = ["# Adastra documentation index", "", f"Mirrored from {BASE_URL}", ""]
    for path in sorted(titles):
        md_path = PurePosixPath(path).with_suffix(".md")
        lines.append(f"- [{titles[path]}]({md_path})")
        for level, text, anchor in outlines[path]:
            lines.append(f"{'  ' * (level - 1)}- [{text}]({md_path}#{anchor})")
    (tmp / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    shutil.rmtree(OUT_DIR, ignore_errors=True)
    tmp.rename(OUT_DIR)
    print(f"wrote {len(pages)} pages to {OUT_DIR}", file=sys.stderr)


if __name__ == "__main__":
    main()
