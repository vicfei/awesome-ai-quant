#!/usr/bin/env python3
"""Check every http(s) URL in markdown files. Exit 1 on dead links."""

from __future__ import annotations

import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL_RE = re.compile(r"https?://[^\s<>\")\]`]+")
SKIP_HOSTS = ("img.shields.io",)


def markdown_files() -> list[Path]:
    return sorted(ROOT.rglob("*.md"))


def urls_in_file(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return {u for u in URL_RE.findall(text) if not any(u.startswith(f"https://{h}") for h in SKIP_HOSTS)}


def check_url(url: str) -> tuple[str, int]:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "awesome-ai-quant/0.1"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return url, r.status
    except urllib.error.HTTPError as e:
        if e.code == 405:  # HEAD not allowed, try GET
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "awesome-ai-quant/0.1"})
                with urllib.request.urlopen(req, timeout=15) as r:
                    return url, r.status
            except Exception:
                return url, 0
        return url, e.code
    except Exception:
        return url, 0


def main() -> None:
    all_urls: set[str] = set()
    for f in markdown_files():
        all_urls |= urls_in_file(f)
    dead = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        for url, status in pool.map(check_url, sorted(all_urls)):
            mark = "ok" if status == 200 else "DEAD"
            print(f"{mark} ({status})\t{url}")
            if status != 200:
                dead.append(url)
    print(f"\n{len(all_urls)} URLs checked, {len(dead)} dead")
    sys.exit(1 if dead else 0)


if __name__ == "__main__":
    main()
