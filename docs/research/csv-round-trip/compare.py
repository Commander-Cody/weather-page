# Compares an original language CSV against a copy that has been through an
# editor. Reports BOM, line endings, byte identity, and any cell that changed.

import csv
import pathlib
import sys


def load(path: pathlib.Path):
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    body = raw[3:] if bom else raw
    crlf = b"\r\n" in body
    try:
        text = body.decode("utf-8")
        decode_error = None
    except UnicodeDecodeError as exc:
        text, decode_error = "", str(exc)
    rows = list(csv.reader(text.splitlines())) if text else []
    return {
        "raw": raw,
        "bom": bom,
        "crlf": crlf,
        "decode_error": decode_error,
        "rows": rows,
    }


def main() -> int:
    before = load(pathlib.Path(sys.argv[1]))
    after = load(pathlib.Path(sys.argv[2]))
    label = sys.argv[3] if len(sys.argv) > 3 else sys.argv[2]

    print(f"=== {label}")
    print(f"  bom:   {before['bom']} -> {after['bom']}")
    print(f"  crlf:  {before['crlf']} -> {after['crlf']}")
    print(f"  bytes: {len(before['raw'])} -> {len(after['raw'])}"
          f"  identical={before['raw'] == after['raw']}")

    if after["decode_error"]:
        print(f"  NOT VALID UTF-8: {after['decode_error']}")
        return 1

    b_rows, a_rows = before["rows"], after["rows"]
    if len(b_rows) != len(a_rows):
        print(f"  ROW COUNT CHANGED: {len(b_rows)} -> {len(a_rows)}")

    header = b_rows[0] if b_rows else []
    if a_rows and a_rows[0] != header:
        print(f"  HEADER CHANGED: {header} -> {a_rows[0]}")

    changes = 0
    for n, (b_row, a_row) in enumerate(zip(b_rows, a_rows), start=1):
        for col, (b_cell, a_cell) in enumerate(zip(b_row, a_row)):
            if b_cell != a_cell:
                changes += 1
                name = header[col] if col < len(header) else f"col{col}"
                key = b_row[0] if b_row else "?"
                print(f"  line {n} [{key}].{name}: {b_cell!r} -> {a_cell!r}")
        if len(b_row) != len(a_row):
            changes += 1
            print(f"  line {n}: field count {len(b_row)} -> {len(a_row)}")

    print(f"  cell changes: {changes}")
    return 1 if changes else 0


if __name__ == "__main__":
    raise SystemExit(main())
