"""Command-line interface:  python -m ecosort.cli "banana peel"   (or run with no args for a chat loop)."""

from __future__ import annotations

import argparse
import json

from .pipeline import EcoSort


def _print(a) -> None:
    print(f"\n  Item   : {a.item}")
    print(f"  Stream : {a.stream.upper()}")
    print(f"  Why    : {a.why}")
    print(f"  Dispose: {a.dispose}")
    print(f"  Source : {a.source}")
    if a.note:
        print(f"  Note   : {a.note}")
    print()


def main() -> None:
    p = argparse.ArgumentParser(description="EcoSort Campus: which waste stream does this item belong to?")
    p.add_argument("item", nargs="*", help="item name, e.g. 'banana peel'")
    p.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = p.parse_args()

    bot = EcoSort()
    if args.item:
        a = bot.ask(" ".join(args.item))
        print(json.dumps(a.to_dict(), indent=2) if args.json else "", end="")
        if not args.json:
            _print(a)
        return

    print(f"EcoSort Campus (mode: {bot.mode}). Type an item, or 'q' to quit.")
    while True:
        try:
            q = input("item> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in {"q", "quit", "exit"}:
            break
        if q:
            _print(bot.ask(q))


if __name__ == "__main__":
    main()
