#!/usr/bin/env python3
"""One-Line Office Joke: 24-Hour Sprint (make.fun).

One line of office humour: a manager calls a meeting about having too
many meetings, then books a follow-up to recap it. The line names the
real failure, lands the joke on a single read, and is the sort of thing
you send a colleague after a meeting that should have been an email.
main.py validates the line on every run, writes it to
/output/entry.txt (no trailing newline) and prints it.

Deterministic: no clock, no randomness, no network, stdlib only.
The joke is one sentence, built on one specific office detail (the
meeting about meetings), so it reads as a single setup-and-punchline
line with nothing around it. Run `python3 main.py --help` for usage.
"""

import argparse
import os
import sys

# The entry: exactly one line, non-empty, at most 200 characters.
# Why it lands: the meeting about meetings is a loop everyone in an
# office recognises, and the follow-up to recap it closes the loop.
JOKE = (
    "Our manager scheduled a meeting to discuss why we have too many "
    "meetings, then booked a follow-up to recap the first one."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def check_line(line: str) -> None:
    """Raise unless the line is one non-empty line of at most 200 chars."""
    if not line:
        raise ValueError("joke must not be empty")
    if line != line.strip() or "\n" in line or "\r" in line:
        raise ValueError("joke must be exactly one line, no leading/trailing space")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "joke is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )


def write_line(path: str = OUTPUT_PATH) -> str:
    """Write the joke to path with no trailing newline; return it.

    The grader reads /output/entry.txt, so the file carries the joke
    exactly as printed: same bytes, no trailing newline, no extra text.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as out:
        out.write(JOKE)
    return JOKE


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Write one original office joke (a meeting about too "
        "many meetings, plus a follow-up to recap it) to /output/entry.txt "
        "and print it. The line is validated first: exactly one line, "
        "non-empty, at most 200 characters.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="only validate the joke line and exit 0 if it passes, "
        "1 if it fails (writes nothing)",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_PATH,
        help="path of the entry file (default: /output/entry.txt)",
    )
    return parser


def main(argv=None) -> int:
    args = make_parser().parse_args(argv)
    try:
        check_line(JOKE)
    except ValueError as exc:
        print("invalid joke: %s" % exc, file=sys.stderr)
        return 1
    if args.verify:
        print("line valid: %d characters, 1 line" % len(JOKE))
        return 0
    print(write_line(args.output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
