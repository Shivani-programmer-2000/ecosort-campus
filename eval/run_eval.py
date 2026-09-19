"""Score the assistant on eval/test_items.csv.

    python eval/run_eval.py

Reports overall accuracy and, more importantly, *confidently wrong* answers
(a wrong stream given with confidence), which are worse than saying "Not sure".
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ecosort import EcoSort  # noqa: E402


def main() -> int:
    bot = EcoSort()
    rows = list(csv.DictReader(open(Path(__file__).with_name("test_items.csv"), encoding="utf-8")))
    correct = 0
    confident_wrong, missed = [], []
    for r in rows:
        a = bot.ask(r["item"])
        if a.stream == r["expected"]:
            correct += 1
        elif a.stream == "Not sure":
            missed.append((r["item"], r["expected"]))
        else:
            confident_wrong.append((r["item"], r["expected"], a.stream))
    n = len(rows)
    print(f"Mode: {bot.mode}")
    print(f"Accuracy: {correct}/{n} = {correct / n:.0%}")
    print(f"Confidently wrong: {len(confident_wrong)}")
    for x in confident_wrong:
        print("   ", x)
    print(f"Said 'Not sure' but the answer was in scope: {len(missed)}")
    for x in missed:
        print("   ", x)
    return 1 if confident_wrong else 0


if __name__ == "__main__":
    raise SystemExit(main())
