#!/usr/bin/env python3
"""Regenerate the star leaderboard in README.md / README.zh-CN.md.

Scans GitHub repo links from README entries, fetches current star counts,
diffs against the weekly snapshot in data/stars.json for weekly gain, and
rewrites the <!-- BEGIN/END: leaderboard --> marker block in both READMEs.
GitHub API via `gh` (uses GH_TOKEN/GITHUB_TOKEN or local auth).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
HISTORY = ROOT / "data" / "stars.json"
MARK_BEGIN = "<!-- BEGIN: leaderboard -->"
MARK_END = "<!-- END: leaderboard -->"
MD_LINK = re.compile(r"\[([^\]]+)\]\((https://github\.com/[^)]+)\)")
TOP_N = 10
# Referenced in the intro as comparison lists, not curated entries.
EXCLUDE = {
    "wilsonfreitas/awesome-quant",
    "georgezouq/awesome-ai-in-finance",
    "LLMQuant/awesome-trading-agents",
}


def tracked_repos() -> list[tuple[str, str]]:
    """(display name, owner/repo) from README.md, first occurrence wins."""
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    seen: dict[str, str] = {}
    for label, url in MD_LINK.findall(text):
        path = urlparse(url).path.strip("/")
        parts = path.split("/")
        if len(parts) < 2:
            continue
        slug = f"{parts[0]}/{parts[1]}"
        if slug in EXCLUDE:
            continue
        seen.setdefault(slug, label.strip())
    return [(label, slug) for slug, label in seen.items()]


def fetch_stars(slug: str) -> int | None:
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{slug}", "--jq", ".stargazers_count"],
            capture_output=True, text=True, timeout=30, check=True,
        )
        return int(out.stdout.strip())
    except Exception as e:  # noqa: BLE001 - keep going, report at the end
        print(f"WARN: {slug}: {e}", file=sys.stderr)
        return None


def fmt(total: int | None) -> str:
    if total is None:
        return "?"
    return f"{total/1000:.1f}k" if total >= 1000 else str(total)


def fmt_delta(d: int | None) -> str:
    return "—" if d is None else f"{d:+d}"


def build_block(now: dict[str, int], prev: dict[str, int], today: str) -> tuple[str, str]:
    """Return (english, chinese) leaderboard markdown."""
    totals = sorted(now.items(), key=lambda kv: -kv[1])
    gains = []
    for slug, total in now.items():
        if slug in prev:
            gains.append((slug, total - prev[slug]))
    gains.sort(key=lambda kv: -kv[1])

    def link(slug: str, stars: int | None = None) -> str:
        label = dict((s, l) for l, s in tracked_repos()).get(slug, slug.split("/")[-1])
        return f"[{label}](https://github.com/{slug})"

    rows_total_en = "\n".join(
        f"| {i} | {link(slug)} | {fmt(v)} | {fmt_delta(v - prev.get(slug, v) if slug in prev else None)} |"
        for i, (slug, v) in enumerate(totals[:TOP_N], 1)
    )
    rows_gain_en = "\n".join(
        f"| {i} | {link(slug)} | {fmt_delta(d)} | {fmt(now[slug])} |"
        for i, (slug, d) in enumerate(gains[:TOP_N], 1)
    )
    en = (
        f"{MARK_BEGIN}\n"
        f"_Auto-updated weekly by CI · last run {today} · weekly Δ compares against the previous snapshot._\n\n"
        f"**Top {TOP_N} by total stars**\n\n"
        f"| # | Project | ★ | Weekly Δ |\n|---|---|---:|---:|\n{rows_total_en}\n\n"
        f"**Top {TOP_N} by weekly gain**\n\n"
        f"| # | Project | Weekly Δ | ★ |\n|---|---|---:|---:|\n{rows_gain_en}\n"
        f"{MARK_END}"
    )

    rows_total_zh = "\n".join(
        f"| {i} | {link(slug)} | {fmt(v)} | {fmt_delta(v - prev.get(slug, v) if slug in prev else None)} |"
        for i, (slug, v) in enumerate(totals[:TOP_N], 1)
    )
    rows_gain_zh = "\n".join(
        f"| {i} | {link(slug)} | {fmt_delta(d)} | {fmt(now[slug])} |"
        for i, (slug, d) in enumerate(gains[:TOP_N], 1)
    )
    zh = (
        f"{MARK_BEGIN}\n"
        f"_CI 每周自动更新 · 最近一次 {today} · 周增量相对上一次快照计算_\n\n"
        f"**总星数 Top {TOP_N}**\n\n"
        f"| # | 项目 | ★ | 周增量 |\n|---|---|---:|---:|\n{rows_total_zh}\n\n"
        f"**周增速 Top {TOP_N}**\n\n"
        f"| # | 项目 | 周增量 | ★ |\n|---|---|---:|---:|\n{rows_gain_zh}\n"
        f"{MARK_END}"
    )
    return en, zh


def rewrite(path: Path, block: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARK_BEGIN not in text or MARK_END not in text:
        print(f"ERROR: markers missing in {path.name}", file=sys.stderr)
        return False
    head, rest = text.split(MARK_BEGIN, 1)
    _, tail = rest.split(MARK_END, 1)
    path.write_text(head + block + tail, encoding="utf-8")
    return True


def main() -> None:
    entries = tracked_repos()
    print(f"tracking {len(entries)} repos")
    now: dict[str, int] = {}
    for label, slug in entries:
        stars = fetch_stars(slug)
        if stars is not None:
            now[slug] = stars

    prev: dict[str, int] = {}
    if HISTORY.exists():
        prev = json.loads(HISTORY.read_text(encoding="utf-8")).get("repos", {})

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    en, zh = build_block(now, prev, today)
    ok = rewrite(ROOT / "README.md", en) and rewrite(ROOT / "README.zh-CN.md", zh)

    HISTORY.parent.mkdir(exist_ok=True)
    HISTORY.write_text(
        json.dumps({"updated": today, "repos": dict(sorted(now.items()))}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print(f"stars: {len(now)} fetched, snapshot saved to {HISTORY.relative_to(ROOT)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
