#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "blog"
OUT = ROOT / "_posts"

ENTRY_RE = re.compile(r"<div class=\"entry-content\">(.*?)</div>", re.S)
TITLE_RE = re.compile(r"<h1 class=\"entry-title\">(.*?)</h1>", re.S)
DATE_RE = re.compile(r"<time class='entry-date' datetime='([^']+)'")
CATEGORY_RE = re.compile(r"class='category'[^>]*>([^<]+)</a>")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def extract_post(html: str) -> tuple[str, str, list[str], str]:
    title_match = TITLE_RE.search(html)
    if not title_match:
        raise ValueError("Missing entry title")
    title = re.sub(r"\s+", " ", title_match.group(1)).strip()

    date_match = DATE_RE.search(html)
    if not date_match:
        raise ValueError("Missing entry date")
    date = date_match.group(1).strip()

    categories = [c.strip() for c in CATEGORY_RE.findall(html)]

    entry_match = ENTRY_RE.search(html)
    if not entry_match:
        raise ValueError("Missing entry content")
    content = entry_match.group(1).strip()

    return title, date, categories, content


def main() -> None:
    OUT.mkdir(exist_ok=True)
    posts = sorted(SRC.glob("20??/*/*/*/index.html"))
    if not posts:
        raise SystemExit("No legacy posts found")

    for path in posts:
        rel = path.relative_to(ROOT)
        # blog/2015/03/18/slug/index.html
        try:
            _, year, month, day, slug, _ = rel.parts
        except ValueError:
            raise SystemExit(f"Unexpected path layout: {rel}")

        html = path.read_text(encoding="utf-8")
        title, date, categories, content = extract_post(html)

        filename = f"{year}-{month}-{day}-{slug}.html"
        out_path = OUT / filename

        categories_yaml = "[" + ", ".join(yaml_quote(c) for c in categories) + "]" if categories else "[]"

        front_matter = [
            "---",
            "layout: post",
            f"title: {yaml_quote(title)}",
            f"date: {date}",
            f"categories: {categories_yaml}",
            f"permalink: /blog/{year}/{month}/{day}/{slug}/",
            "legacy: true",
            "---",
            "",
        ]

        body = "\n".join(front_matter) + "{% raw %}\n" + content + "\n{% endraw %}\n"
        out_path.write_text(body, encoding="utf-8")

    print(f"Wrote {len(posts)} posts to {OUT}")


if __name__ == "__main__":
    main()
