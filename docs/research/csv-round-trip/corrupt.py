# Produces deliberately corrupted copies of the fixture, so we can check that
# #8's character-set validation ACTUALLY FIRES rather than merely existing.
#
# Each case is a real failure mode of a spreadsheet round trip, not a synthetic one.

import pathlib
import unicodedata

HERE = pathlib.Path(__file__).parent
SRC = HERE / "strings-nobom.csv"
OUT = HERE / "corrupt"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    text = SRC.read_text(encoding="utf-8")
    cases: dict[str, bytes] = {}

    # 1. Classic mojibake: UTF-8 bytes read as cp1252, then re-saved as UTF-8.
    #    This is what "å" -> "Ã¥" looks like. The single most likely outcome of
    #    an editor guessing the encoding wrong on import.
    cases["mojibake-cp1252.csv"] = (
        text.encode("utf-8").decode("cp1252", errors="replace").encode("utf-8")
    )

    # 2. Same, but read as latin-1 (no undefined bytes, so it round-trips
    #    silently -- strictly nastier than case 1).
    cases["mojibake-latin1.csv"] = (
        text.encode("utf-8").decode("latin-1").encode("utf-8")
    )

    # 3. Lossy downgrade: saved as cp1252 with unmappable characters replaced.
    #    å ä ö ü all EXIST in cp1252, so this one is the interesting case --
    #    the file is legal cp1252 and looks fine in a German editor.
    cases["saved-as-cp1252.csv"] = text.encode("cp1252", errors="replace")

    # 4. ASCII with "?" for everything non-ASCII -- the "? appears in text
    #    nobody re-reads" failure named on #20.
    cases["ascii-question-marks.csv"] = text.encode("ascii", errors="replace")

    # 5. NFD decomposition: "å" becomes "a" + combining ring. Renders
    #    identically, different bytes. A naive "contains å" check misses this.
    cases["nfd-decomposed.csv"] = unicodedata.normalize("NFD", text).encode("utf-8")

    # 6. Autocorrect turning a straight apostrophe into a typographic one.
    #    Fires when a translator TYPES a cell, not on import.
    cases["curly-apostrophe.csv"] = text.replace("'", "’").encode("utf-8")

    # 7. Non-breaking space substituted for a normal space.
    cases["nbsp.csv"] = text.replace("t n", "t n").encode("utf-8")

    for name, data in cases.items():
        (OUT / name).write_bytes(data)
        print(f"wrote {name} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
