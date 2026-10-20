"""
Step 3: Ask the database behind MesserHauptstadt for each state's totals.

The map only shows Berlin, but the database it reads from covers all of
Germany. This script asks it for the case total in each of the 16 states,
the same request the site makes for Berlin's statistics.

Totals change as the database grows, so you'll get today's numbers, not the
ones from the story. Set the access key before running:

    export MESSER_API_KEY=afd-berlin

Usage:
    python3 scripts/state_totals.py
"""

import csv
import os
import time
from pathlib import Path

import requests

API = "https://api.messermaps.de/v1/analytics/timedstats/knifecrimes"
OUTPUT = Path(__file__).resolve().parent.parent / "output"

STATES = {
    "be": "Berlin", "by": "Bavaria", "nw": "North Rhine-Westphalia",
    "bw": "Baden-Württemberg", "hh": "Hamburg", "st": "Saxony-Anhalt",
    "mv": "Mecklenburg-Vorpommern", "rp": "Rhineland-Palatinate",
    "sn": "Saxony", "th": "Thuringia", "he": "Hesse", "ni": "Lower Saxony",
    "sh": "Schleswig-Holstein", "bb": "Brandenburg", "sl": "Saarland",
    "hb": "Bremen",
}


def main():
    key = os.environ.get("MESSER_API_KEY")
    if not key:
        raise SystemExit("Set MESSER_API_KEY first (see the top of this script).")

    rows = []
    for code, name in STATES.items():
        try:
            data = requests.get(
                API,
                params={"state": code},
                headers={"x-api-key": key, "User-Agent": "Mozilla/5.0 (research)"},
                timeout=20,
            ).json()
            total = data["incidents"]["total"] if data.get("status") == "success" else None
        except (requests.RequestException, KeyError, ValueError):
            total = None
        rows.append({"state": name, "code": code, "total_cases": total})
        print(f"{name:<25} {total}")
        time.sleep(1)

    rows.sort(key=lambda r: r["total_cases"] or 0, reverse=True)
    OUTPUT.mkdir(exist_ok=True)
    with open(OUTPUT / "state_totals.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["state", "code", "total_cases"])
        writer.writeheader()
        writer.writerows(rows)
    print("\nSaved to output/state_totals.csv")


if __name__ == "__main__":
    main()
