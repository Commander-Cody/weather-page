# Generates the round-trip test fixture for weather-page issue #20.
#
# Frisian cells use ONLY vocabulary already sourced on #5 / supplied by the owner.
# Rows keyed `_test.*` are character-inventory and spreadsheet-hazard probes, not
# words -- nothing here is invented Frisian.

import csv
import io
import pathlib

OUT = pathlib.Path(__file__).parent

HEADER = ["key", "context", "note", "mooring", "fering"]

ROWS = [
    # --- real strings, attested vocabulary only -----------------------------
    ["freshness.updated", "aktualisiert {time}", "", "aktualisiird {time}", ""],
    ["wind.0", "flau", "unverified", "loun", ""],
    ["wind.1", "leicht", "unverified", "liis", ""],
    ["wind.2", "steif", "unverified", "stif", ""],
    ["wind.3", "scharf", "unverified", "scharp", ""],
    ["wind.4", "böig", "unverified", "brüsi", ""],
    ["wind.5", "stürmisch", "unverified", "stormi", ""],
    ["wind.6", "Orkan", "unverified", "orkel", ""],
    ["compass.n", "der Norden", "", "dåt norden", ""],
    ["compass.s", "der Süden", "", "dåt sööden", ""],
    ["compass.e", "der Osten", "", "dåt ååsten", ""],
    ["compass.w", "der Westen", "", "dåt weesten", ""],
    ["compass.sw", "der Südwesten", "", "dåt söödweesten", ""],
    ["headline.wind_from_sw", "Der Wind weht aus Südwest.", "",
     "E win wait üt söödweest.", ""],
    ["relday.today", "heute", "", "diling", ""],
    ["relday.tomorrow", "morgen", "", "mårling", ""],
    ["relday.night", "nachts", "", "nåchtling", ""],
    ["relday.yesterday_evening", "gestern Abend, abends",
     "Komma steht absichtlich im context-Feld", "änjörnse", ""],
    ["months.native.1", "Januar (germanische Reihe)", "", "di ismoune", ""],
    ["months.native.2", "Februar (germanische Reihe)", "", "di biikenmoune", ""],
    ["months.intl.1", "Januar", "Schreibkonflikt janewoore/januar offen",
     "janewoore", ""],
    ["months.intl.2", "Februar", "", "fääberwoor", ""],
    ["var.humidity", "Luftfeuchtigkeit", "", "luftfuchtihäid", ""],
    ["var.water_temp", "Wassertemperatur", "", "wåådertemperatuur", ""],
    ["water.astronomical", "astronomische Tide", "", "astronoomsche tide", ""],
    ["water.corrected", "korrigierte Wasserstandsvorhersage", "",
     "korigiird (wååderpäägel)forütseeding", ""],
    ["cond.sun", "Sonnenschein", "", "sanschin", ""],
    ["cond.rain", "Regen", "", "rin", ""],
    ["cond.snow", "Schnee", "", "snii", ""],
    ["cond.fog", "neblig", "", "misti", ""],
    ["cond.cold", "kalt", "", "kölj", ""],
    ["cond.wet", "nass", "", "wätj", ""],
    ["cond.windy", "windig", "", "wini", ""],
    ["question.weather_today", "Wie ist das Wetter heute?", "",
     "hü as dåt wääder diling?", ""],
    # Apostrophe in a REAL (validated) row, not just a _test row -- otherwise the
    # curly-quote corruption case never reaches a checked cell.
    ["ui.variety_soelring", "Söl'ring (Name der Sylter Varietät)", "",
     "Söl'ring", ""],
    ["places.list", "Söl'ring native: List", "kein Override noetig", "", ""],
    ["places.hoernum", "Söl'ring native: Hörnum", "", "", ""],

    # --- character inventory probes ----------------------------------------
    ["_test.vowels", "Testzeile Sondervokale", "nicht uebersetzen",
     "å ä ö ü åå ää öö üü", ""],
    ["_test.palatals", "Testzeile Palatal-Digraphen", "nicht uebersetzen",
     "dj lj nj tj", ""],
    ["_test.alphabet", "Testzeile erlaubtes Alphabet", "nicht uebersetzen",
     "abcdefghijklmnoprstuw", ""],

    # --- spreadsheet hazard probes -----------------------------------------
    ["_test.clock", "Testzeile Uhrzeit mit Punkt (#5: Punkt statt Doppelpunkt)",
     "nicht uebersetzen", "09.14", ""],
    ["_test.clock_2400", "Testzeile Uhrzeit 20.00", "nicht uebersetzen",
     "20.00", ""],
    ["_test.thousands", "Testzeile Tausenderpunkt", "nicht uebersetzen",
     "5.000", ""],
    ["_test.decimal", "Testzeile Dezimalkomma", "nicht uebersetzen",
     "1,5", ""],
    ["_test.leading_zero", "Testzeile fuehrende Null", "nicht uebersetzen",
     "007", ""],
    ["_test.date_like", "Testzeile datumsaehnlich", "nicht uebersetzen",
     "1.3.", ""],
    ["_test.formula", "Testzeile Gleichheitszeichen am Anfang",
     "nicht uebersetzen", "=1+1", ""],
    ["_test.plus", "Testzeile Pluszeichen am Anfang", "nicht uebersetzen",
     "+2", ""],
    ["_test.apostrophe", "Testzeile Apostroph", "nicht uebersetzen",
     "Söl'ring", ""],
    ["_test.comma_in_cell", "Testzeile Komma im Feld", "nicht uebersetzen",
     "loun, liis, stif", ""],
    ["_test.quotes", "Testzeile Anfuehrungszeichen", "nicht uebersetzen",
     '"stormi"', ""],
    ["_test.trailing_space", "Testzeile Leerzeichen am Ende",
     "nicht uebersetzen", "rin ", ""],
    ["_test.placeholder", "Testzeile Platzhalter", "nicht uebersetzen",
     "{source} {time}", ""],
]


def build_csv_text() -> str:
    buf = io.StringIO()
    # lineterminator="\n": LF, so a CRLF in the output is itself a diff signal.
    w = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writerow(HEADER)
    w.writerows(ROWS)
    return buf.getvalue()


def main() -> None:
    text = build_csv_text()
    (OUT / "strings-bom.csv").write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
    (OUT / "strings-nobom.csv").write_bytes(text.encode("utf-8"))
    print(f"rows={len(ROWS)} bytes={len(text.encode('utf-8'))}")


if __name__ == "__main__":
    main()
