#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts"
CATEGORIES_DIR = ROOT / "blog" / "categories"


FRONT_MATTER_RE = re.compile(r"^---\\s*$", re.MULTILINE)


def parse_front_matter(text: str) -> dict[str, object]:
    matches = list(FRONT_MATTER_RE.finditer(text))
    if len(matches) < 2:
        return {}
    start = matches[0].end()
    end = matches[1].start()
    block = text[start:end]
    data: dict[str, object] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key == "categories":
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                if inner:
                    items = [v.strip().strip("'\"") for v in inner.split(",")]
                    data[key] = [v for v in items if v]
                else:
                    data[key] = []
            elif value:
                data[key] = [value.strip("'\"")]
            else:
                items = []
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    if not next_line.startswith(" "):
                        break
                    stripped = next_line.strip()
                    if stripped.startswith("- "):
                        items.append(stripped[2:].strip("'\""))
                    j += 1
                data[key] = items
                i = j - 1
        i += 1
    return data


def collect_categories() -> set[str]:
    categories: set[str] = set()
    for path in sorted(POSTS_DIR.glob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        data = parse_front_matter(text)
        values = data.get("categories", [])
        if isinstance(values, list):
            for item in values:
                if item:
                    categories.add(str(item))
    return categories


def write_category_page(name: str) -> None:
    slug = quote(name.lower())
    target_dir = CATEGORIES_DIR / slug
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "index.html"
    content = (
        "---\\n"
        "layout: category\\n"
        f'title: "Category: {name}"\\n'
        f"category: {name}\\n"
        f"permalink: /blog/categories/{slug}/\\n"
        "---\\n"
    )
    target_file.write_text(content, encoding="utf-8")


def main() -> None:
    categories = collect_categories()
    if not categories:
        print("No categories found.")
        return
    CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
    for name in sorted(categories, key=lambda s: s.lower()):
        write_category_page(name)
    print(f"Generated {len(categories)} category pages.")


if __name__ == "__main__":
    main()
