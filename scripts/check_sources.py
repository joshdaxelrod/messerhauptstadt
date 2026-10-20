"""
Download the police release behind every MesserHauptstadt case.

For each case in data/cases.csv (or a list you pulled yourself with
get_cases.py), this saves the release's headline and text
to output/review.csv, next to the case's title, so you can read every case
in one spreadsheet instead of clicking through 245 links.

It visits one page per second (about 5 minutes for 245 cases). If it stops,
run it again: it skips cases it has already done.

Usage:
    python3 scripts/check_sources.py
    python3 scripts/check_sources.py --limit 10   # try it on 10 cases first
    python3 scripts/check_sources.py --cases output/cases.csv   # your own pull
"""

import argparse
import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parent.parent
CASES = REPO / "data" / "cases.csv"
OUTPUT = REPO / "output"
REVIEW = OUTPUT / "review.csv"
COLUMNS = ["id", "title", "source", "release_title", "release_text"]


def release_text(url):
    html = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0 (research)"}).text
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    title = soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else ""
    body = soup.select_one("#layout-grid__area--maincontent") or soup.find("article") or soup
    text = re.sub(r"\s+", " ", body.get_text(" ", strip=True))
    return title, text.split("Polizei Berlin Pressearbeit")[0]  # drop the contact footer


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--limit", type=int, help="only download this many releases (for testing)")
    parser.add_argument("--cases", default=CASES, help="the list of cases to check (default: data/cases.csv)")
    args = parser.parse_args()

    OUTPUT.mkdir(exist_ok=True)
    cases = list(csv.DictReader(open(args.cases, encoding="utf-8")))
    done = set()
    if REVIEW.exists():
        done = {row["id"] for row in csv.DictReader(open(REVIEW, encoding="utf-8"))}
    todo = [c for c in cases if c["id"] not in done][: args.limit]
    print(f"{len(cases)} cases, {len(done)} already downloaded, {len(todo)} to go.")

    new_file = not REVIEW.exists()
    with open(REVIEW, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if new_file:
            writer.writeheader()
        for i, case in enumerate(todo, 1):
            try:
                title, text = release_text(case["source"])
            except requests.RequestException as error:
                title, text = f"[could not load: {error}]", ""
            writer.writerow({
                "id": case["id"],
                "title": case["title"],
                "source": case["source"],
                "release_title": title,
                "release_text": text,
            })
            f.flush()
            print(f"[{i}/{len(todo)}] {title[:70]}")
            time.sleep(1)

    print(f"\nSaved to output/{REVIEW.name}.")


if __name__ == "__main__":
    main()
