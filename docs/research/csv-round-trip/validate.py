# Character-set validation for the language CSV, per issue #8.
#
# #8 says: "validate the character set at build time against the Mooring alphabet
# from #5 -- no q v x y z ß, plus å and the palatals. That check catches
# corruption deterministically, because mojibake produces characters outside the
# alphabet."
#
# This is the throwaway implementation used to test that claim on #20.

import csv
import sys
import unicodedata

# Mooring alphabet, #5: 1955 spelling, moderated lowercase.
# a-z minus q v x y z, plus å ä ö ü. Palatals dj lj nj tj are digraphs of
# letters already in the set, so they need no extra codepoints.
MOORING_LETTERS = set("abcdefghijklmnoprstuw") | set("åäöü")
MOORING_LETTERS |= {c.upper() for c in MOORING_LETTERS}  # sentence starts, proper names

# Characters a rendered string may legitimately contain besides letters.
MOORING_PUNCT = set(" .,?!:;()-'/{}0123456789")

MOORING_ALLOWED = MOORING_LETTERS | MOORING_PUNCT

# Columns that are NOT reader-facing Frisian and must NOT be checked against the
# Mooring alphabet: `context` is a German gloss (contains ß, q, v, z), `note` is
# workflow state, `key` is an ASCII dotted key.
NON_VARIETY_COLUMNS = {"key", "context", "note"}

# Structural columns still get a check, just a different one.
KEY_ALLOWED = set("abcdefghijklmnopqrstuvwxyz0123456789._")


def describe(ch: str) -> str:
    try:
        name = unicodedata.name(ch)
    except ValueError:
        name = "<unnamed>"
    return f"U+{ord(ch):04X} {name}"


def check_file(path: str, varieties: list[str]) -> list[str]:
    problems: list[str] = []

    with open(path, "rb") as fh:
        raw = fh.read()

    # The BOM is a separate concern from the alphabet; strip it here and report
    # on it separately in the round-trip harness.
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"file is not valid UTF-8: {exc}"]

    rows = list(csv.DictReader(text.splitlines()))
    if not rows:
        return ["file has no data rows"]

    headers = list(rows[0].keys())
    for variety in varieties:
        if variety not in headers:
            problems.append(
                f"built variety '{variety}' has no column "
                f"(headers: {', '.join(headers)})"
            )

    for n, row in enumerate(rows, start=2):  # start=2: line 1 is the header
        key = (row.get("key") or "").strip()

        for ch in key:
            if ch not in KEY_ALLOWED:
                problems.append(f"line {n} key: {describe(ch)} in {key!r}")

        # Harness-only concession: `_test.*` rows carry deliberate hazard probes
        # (=1+1, "stormi", trailing space) that a real language file never has.
        # They are checked by byte-diff after the round trip, not by the alphabet.
        if key.startswith("_test."):
            continue

        for variety in varieties:
            if variety not in row:
                continue
            value = row.get(variety) or ""

            if value != value.strip() and value.strip():
                problems.append(
                    f"line {n} {variety}: leading/trailing whitespace in {value!r}"
                )

            if not value.strip():
                # #8: places.* rows are exempt; an absent override is correct.
                if not key.startswith("places."):
                    problems.append(f"line {n} {variety}: empty cell for {key!r}")
                continue

            # NFC check: 'a' + combining ring renders as 'å' but is different
            # bytes. Without this, decomposed text passes the alphabet check.
            if unicodedata.normalize("NFC", value) != value:
                problems.append(
                    f"line {n} {variety}: not NFC-normalised (decomposed "
                    f"accents) in {value!r}"
                )

            # A lossy transcode replaces every non-ASCII character with "?",
            # which the alphabet cannot reject -- "?" is legal, because
            # `hü as dåt wääder diling?` needs it. Position makes it decidable:
            # a real "?" ends a sentence, a corrupted one sits inside a word.
            for i, ch in enumerate(value):
                if ch in "?!" and i != len(value) - 1:
                    problems.append(
                        f"line {n} {variety}: {describe(ch)} not at end of cell "
                        f"-- likely a lossy transcode -- in {value!r}"
                    )
                    break

            for ch in value:
                if ch not in MOORING_ALLOWED:
                    problems.append(
                        f"line {n} {variety}: {describe(ch)} in {value!r}"
                    )
                    break  # one report per cell is enough

    return problems


def main() -> int:
    path = sys.argv[1]
    varieties = sys.argv[2:] or ["mooring"]
    problems = check_file(path, varieties)
    if problems:
        print(f"FAIL {path}  ({len(problems)} problem(s))")
        for p in problems[:15]:
            print(f"  - {p}")
        if len(problems) > 15:
            print(f"  ... and {len(problems) - 15} more")
        return 1
    print(f"PASS {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
