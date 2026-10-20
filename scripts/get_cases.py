"""
Step 1: Pull MesserHauptstadt's cases.

The map loads its cases from a database at api.messermaps.de, asking for a
date range and a state. This script makes the same request the site's own
code makes and saves the cases to output/cases_raw.json, plus a spreadsheet
of each case's title, date, place and source link.

I found the database by watching the browser's developer tools (Network
tab) while the map loaded: the request to api.messermaps.de shows up there,
with the key in its headers.

Set the access key before running:

    export MESSER_API_KEY=afd-berlin

Usage:
    python3 scripts/get_cases.py
    python3 scripts/get_cases.py --start 2026-03-21 --end 2026-04-21 --state be
"""

import argparse
import csv
import json
import os
from pathlib import Path

import requests

API = "https://api.messermaps.de/v1/incidents/knifecrimes"
OUTPUT = Path(__file__).resolve().parent.parent / "output"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--start", default="2000-01-01", help="earliest incident date, YYYY-MM-DD")
    parser.add_argument("--end", default="2100-01-01", help="latest incident date, YYYY-MM-DD")
    parser.add_argument("--state", default="be", help="two-letter state code; 'be' is Berlin")
    args = parser.parse_args()

    key = os.environ.get("MESSER_API_KEY")
    if not key:
        raise SystemExit("Set MESSER_API_KEY first (see the top of this script).")

    response = requests.get(
        API,
        params={"start-date": args.start, "end-date": args.end, "state": args.state},
        headers={"x-api-key": key, "User-Agent": "Mozilla/5.0 (research)"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    cases = data.get("incidents", [])

    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "cases_raw.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    with open(OUTPUT / "cases.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "title", "city", "source"])
        for case in cases:
            writer.writerow([
                case.get("_id", ""),
                (case.get("committed_timestamp") or "")[:10],
                case.get("title", ""),
                case.get("city", ""),
                case.get("link_source", ""),
            ])
    print(f"Saved {len(cases)} cases to output/cases.csv and output/cases_raw.json")


if __name__ == "__main__":
    main()
