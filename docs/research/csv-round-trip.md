# CSV round-trip: does Mooring orthography survive a spreadsheet?

Findings for [#20](https://github.com/Commander-Cody/weather-page/issues/20). Gates the
CSV format choice made in [#8](https://github.com/Commander-Cody/weather-page/issues/8).

Harness lives in `docs/research/csv-round-trip/`. Everything below is measured, not
reasoned about. The Google Sheets leg is **not** covered — see [Not tested](#not-tested).

## Short answer

**Mooring orthography survives LibreOffice intact.** Across four filter configurations
including a German locale, not one Frisian character changed: `å ä ö ü`, the doubled
vowels `åå ää öö üü`, the palatal digraphs `dj lj nj tj`, and the apostrophe in
`Söl'ring` all came back byte-for-byte.

What does not survive is **numbers**. Four cells were silently rewritten, and the
character-set check from #8 does not notice.

## The corruption everyone expects does not happen; a different one does

The feared failure — `å` arriving as `Ã¥` or `?` — did not occur once. LibreOffice reads
and writes UTF-8 correctly.

The failure that did occur is value coercion. With minimal quoting and a German locale:

| cell | before | after |
| --- | --- | --- |
| `_test.thousands` | `5.000` | `5000` |
| `_test.leading_zero` | `007` | `7` |
| `_test.date_like` | `1.3.` | `01.03.26` |
| `_test.formula` | `=1+1` | `2` |
| `_test.plus` | `+2` | `2` |

`=1+1` becoming `2` is the sharpest of these: the spreadsheet evaluated a cell rather
than storing it.

**The clock format is safe.** #5 sets the clock with a dot (`09.14`, `20.00`), which
looked like the most exposed string on the page. It is not. German date detection needs a
trailing dot or a year, so `01.05`, `09.12`, `11.03`, `07.07`, `12.01` and `08.15` all
survived unquoted even in a German locale. Only `1.3.` — with the trailing dot — became a
date. This was worth checking rather than assuming: `09.14` and `20.00` are invalid dates
(month 14, month 0) and would have passed for the wrong reason.

## Both holes in #8's character-set check

#8 argued the build-time character check "catches corruption deterministically, because
mojibake produces characters outside the alphabet". That is true of encoding corruption
and false of everything else. Two concrete misses:

**1. It cannot see value coercion.** Run against the LibreOffice output above — the one
with four rewritten cells — the checker returns `PASS`. `5000` and `2` are made entirely
of legal characters. A character-set check is the wrong instrument for this class of
damage; the defence is #8's *other* safeguard, the column diff.

**2. A lossy transcode to `?` passes the alphabet.** `?` has to be legal, because
`hü as dåt wääder diling?` needs it. So `dåt` degrading to `d?t` slips through — and `?`
in text nobody re-reads is the exact failure #20 was opened to prevent.

That one is fixable, and the fix is cheap: **`?` and `!` are only legal as the final
character of a cell.** A real question mark ends a sentence; a transcoded one sits inside
a word. With that rule added, the case is caught.

## Corruption cases the check does catch

Seven deliberate corruptions, all detected, clean file still passing:

| case | caught by |
| --- | --- |
| UTF-8 read as cp1252 (`å` → `Ã¥`) | alphabet |
| UTF-8 read as latin-1 | alphabet |
| saved as cp1252 | file is not valid UTF-8 |
| non-ASCII replaced with `?` | **`?`-position rule (new)** |
| NFD decomposition (`a` + combining ring) | NFC check **(new)** and alphabet |
| straight apostrophe → `’` | alphabet |
| space → non-breaking space | alphabet |

Two of these needed rules #8 did not specify. **NFD** is the quieter one: `å` as `a` +
U+030A renders identically and is different bytes, so a check that merely asks "does this
contain `å`" is satisfied. Requiring NFC normalisation catches it outright.

## Three character-set policies, not one

The check cannot run uniformly over the file. The `context` column holds a German gloss,
so it contains `ß`, `q`, `v` and `z` — every one of them forbidden in Mooring. Running the
Mooring alphabet over it fails the build on correct data.

- **Variety columns** (`mooring`, `fering`, …) — the Mooring alphabet, NFC, `?!` at end only.
- **`key`** — `a-z 0-9 . _` only.
- **`context`, `note`** — not checked. Translator-facing and workflow text.

## Settings that make the round trip clean

With **every field quoted on write**, *quoted field as text* on, and *detect special
numbers* off, the round trip produced **zero cell changes** in a German locale. Both parts
matter: "quoted as text" protects only fields that are actually quoted, and Python's
default `QUOTE_MINIMAL` does not quote `5.000`.

Two file-level differences remain in every configuration and are not cell damage:

- **Line endings become CRLF.** LibreOffice always writes CRLF.
- **The BOM is dropped whenever the output charset is stated explicitly.** Measured:
  default options preserved it, and every run passing charset `76` (UTF-8) lost it.

Neither corrupts a string, but both matter for #8's re-import safeguard — "diff the other
columns and reject any change". A raw diff of a returned file reports every line as
changed, and a reviewer who sees a wall of red stops reading. **Normalise BOM and line
endings before diffing**, or the safeguard is noise.

## Not tested

**Google Sheets.** It needs the owner's account, so it could not be driven here. It is
also the more aggressive coercer of the two, and its parser shares no code with
LibreOffice — none of the results above transfer to it. Checklist for running that leg is
in the resolution comment on #20.

**The Astro build and the rendered page.** The repo has no Astro install yet. Low risk and
re-checked when the build exists, per #20.

## Harness

```
docs/research/csv-round-trip/
  make_fixture.py   builds the fixture: attested vocabulary + hazard probes
  validate.py       the #8 character-set check, plus the NFC and `?`-position rules
  corrupt.py        the seven deliberate corruptions
  compare.py        BOM / line endings / byte identity / per-cell diff
```

Every Frisian cell uses vocabulary already sourced on #5 or supplied by the owner. Rows
keyed `_test.*` are character-inventory and hazard probes, not words — nothing here is
invented Frisian.

Reproduce:

```bash
python make_fixture.py && python corrupt.py && python validate.py strings-nobom.csv mooring
```
