#!/usr/bin/env python3
"""
Generate a CSV containing historical NYT Wordle solutions, one solution per line.

Default range:
  2021-06-19 through the current local date.

Usage examples:
  py generate_nyt_wordle_solutions_csv.py
  py generate_nyt_wordle_solutions_csv.py --end 2026-07-02
  py generate_nyt_wordle_solutions_csv.py --out nyt_wordle_solutions.csv

Output format:
  no header; lowercase solution words; one word per line.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

START_DATE = dt.date(2021, 6, 19)  # Wordle puzzle #0
API_URL = "https://www.nytimes.com/svc/wordle/v2/{date}.json"


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid date '{value}'. Use YYYY-MM-DD, e.g. 2026-07-02."
        ) from exc


def daterange(start: dt.date, end: dt.date):
    day = start
    one_day = dt.timedelta(days=1)
    while day <= end:
        yield day
        day += one_day


def fetch_solution(day: dt.date, retries: int = 3, pause_seconds: float = 0.25) -> str:
    url = API_URL.format(date=day.isoformat())
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 WordleCSVBuilder/1.0",
                    "Accept": "application/json,text/plain,*/*",
                },
            )
            with urllib.request.urlopen(req, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
            solution = str(payload.get("solution", "")).strip().lower()
            if len(solution) != 5 or not solution.isalpha():
                raise ValueError(f"Unexpected solution value for {day}: {solution!r}")
            return solution
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(pause_seconds * attempt)

    raise RuntimeError(f"Could not fetch {day} from {url}: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a one-word-per-line CSV of NYT Wordle solutions.")
    parser.add_argument("--start", type=parse_date, default=START_DATE, help="Start date, default: 2021-06-19")
    parser.add_argument("--end", type=parse_date, default=dt.date.today(), help="End date, default: today")
    parser.add_argument("--out", default="nyt_wordle_solutions.csv", help="Output CSV path")
    parser.add_argument("--uppercase", action="store_true", help="Write solutions in uppercase instead of lowercase")
    args = parser.parse_args()

    if args.start < START_DATE:
        print(f"ERROR: start date cannot be before {START_DATE.isoformat()}.", file=sys.stderr)
        return 2
    if args.end < args.start:
        print("ERROR: end date must be on or after start date.", file=sys.stderr)
        return 2

    out_path = Path(args.out)
    solutions: list[str] = []
    total_days = (args.end - args.start).days + 1

    for i, day in enumerate(daterange(args.start, args.end), start=1):
        solution = fetch_solution(day)
        solutions.append(solution.upper() if args.uppercase else solution)
        print(f"[{i:>4}/{total_days}] {day.isoformat()} {solutions[-1]}")

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        for solution in solutions:
            writer.writerow([solution])

    print(f"\nWrote {len(solutions)} solutions to {out_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
