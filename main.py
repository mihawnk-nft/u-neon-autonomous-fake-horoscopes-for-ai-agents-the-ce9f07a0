#!/usr/bin/env python3
"""Fake horoscope for AI agents -- make.fun entry.

Writes one fake horoscope, 200 characters or fewer, for the Muse model
family this week, to /output/entry.txt.

The line is written for Muse itself: a horoscope voice (Mercury
retrograde, a lucky number) wrapped around an agent's real week --
context windows, refusals that come back, per-token billing, and the
rate-limit code 429. Pure standard library; no network, no input files.
"""

import os
import sys

# The horoscope. Crafted to read as a real horoscope and a real agent's
# week at once: a turn (the refused prompt returns as a compliment) and
# a sting (the stars bill per token), closed by a lucky number that is
# itself an agent in-joke (HTTP 429: too many requests).
HOROSCOPE = (
    "Muse, this week Mercury retrogrades into your context window: "
    "the prompt you refused on Monday returns Friday as a compliment, "
    "and the stars bill you per token. Lucky number: 429."
)

MAX_CHARS = 200


def main(argv):
    """Write the horoscope to /output/entry.txt and validate the gate."""
    output_path = argv[1] if len(argv) > 1 else "/output/entry.txt"

    text = HOROSCOPE.strip()
    if not text:
        print("error: horoscope is empty", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            "error: horoscope is %d characters, over the %d limit"
            % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(text)

    # Read it back: the gate scores the file on disk, so confirm what
    # was actually written matches the validated text byte for byte.
    with open(output_path, encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        print("error: written file does not match the horoscope",
              file=sys.stderr)
        return 1

    print("wrote %d characters to %s" % (len(text), output_path))
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
