# CSV round-trip: does Mooring orthography survive a spreadsheet?

Findings for [#20](https://github.com/Commander-Cody/weather-page/issues/20). Gates the
CSV format choice made in [#8](https://github.com/Commander-Cody/weather-page/issues/8).

Harness lives in `docs/research/csv-round-trip/`. Everything below is measured, not
reasoned about.

## Short answer

**Yes. Mooring orthography survives a spreadsheet round-trip intact, in both editors.**
Across four LibreOffice filter configurations including a German locale, and three Google
Sheets passes, not one Frisian character changed: `å ä ö ü`, the doubled vowels
`åå ää öö üü`, the palatal digraphs `dj lj nj tj`, and the apostrophe in `Söl'ring` all
came back byte-for-byte. #8's CSV choice stands; the YAML fallback is not needed.

What does not survive is **numbers**, and in Sheets, **trailing whitespace**. The
character-set check from #8 notices none of it.

Five conditions, all cheap, in [Conditions](#conditions-on-the-answer).

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
with five rewritten cells — the checker returns `PASS`. `5000` and `2` are made entirely
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
columns and reject any change".

**Measured, and the safeguard holds up well.** Committing the original, overwriting it
with the LibreOffice output and running `git diff` produced **six changed lines**: one for
the dropped BOM, five for the actually-mangled cells. The damage is obvious at a glance,
not buried.

That result depended on `core.autocrlf=true`, which normalises CRLF back to LF on commit.
It is set at **machine level on the owner's Windows install, not in this repo**, so
nothing carried it to a fresh clone or to CI.

**Now pinned** in `.gitattributes`:

```
*.csv text eol=lf
```

Verified by switching `core.autocrlf` off to stand in for a Linux CI runner and diffing
the same returned file both ways:

| | changed lines |
| --- | --- |
| with the rule | **6** — the dropped BOM plus the five real changes |
| without it | **54** — every line in the file |

So the safeguard now survives being run somewhere other than this laptop.

## Google Sheets: gentler than LibreOffice, with one behaviour no setting controls

Run by the repo owner, three passes, outputs in `docs/research/csv-round-trip/google-sheets/`.

| pass | cell changes | what changed |
| --- | --- | --- |
| convert **on** (the default) | 3 | `007` → `7`, `=1+1` → `2`, `rin ` → `rin` |
| convert **off** | **1** | `rin ` → `rin` |
| hand-typed cells | 3 + the typed cells | same as convert-on |

**Turning conversion off reduces the damage to a single class**, and that class is
whitespace. Sheets was also *less* destructive than LibreOffice on import: `5.000`,
`1.3.` and the clock strings all survived even with conversion on, where a German-locale
LibreOffice rewrote the first two.

**The typing test came back clean, which was the least certain part of this.** Autocorrect
is the one path that fires on a translator rather than on a file, and it did not fire. The
hand-typed apostrophe came back as **U+0027**, straight, not `’`. The hand-typed
`å ä ö ü` came back as precomposed **NFC** codepoints, not decomposed. Checked at
codepoint level rather than by eye, because `å` and `a`+U+030A are indistinguishable on
screen.

**Trailing whitespace is trimmed unconditionally.** `rin ` came back as `rin` in all three
passes, including the one with conversion off. No import setting governs this. It is the
only Sheets behaviour that cannot be switched off, so the language file must never carry
significant leading or trailing whitespace — spacing belongs around the `{placeholder}`,
never at a cell edge.

**Neither editor preserves the BOM.** Sheets dropped it in all three passes; LibreOffice
dropped it whenever the output charset was stated. #8 proposed writing a BOM "so Excel
reads it correctly", which is still a fine reason to write one — but it is a **one-way
hint for the first open, not an invariant**. The build and the re-import check must accept
a file with or without it. Both editors produced correct UTF-8 regardless.

**Locale is part of what must be documented.** The Sheets passes ran under the owner's
account locale, and `5.000` / `1.3.` surviving is a locale-dependent result — a
German-locale LibreOffice rewrote both. Turning conversion off makes the question moot,
which is the main reason to prefer it over relying on any particular locale.

## Conditions on the answer

1. **Turn value conversion off on import.** Sheets: *Convert text to numbers, dates, and
   formulas* off. LibreOffice: quote every field on write, *quoted field as text* on,
   *detect special numbers* off. Locale then stops mattering.
2. **No significant leading or trailing whitespace in any cell** — Sheets trims it and
   nothing prevents that.
3. **The character check needs the `?`-position rule and NFC**, and must run three
   policies, not one.
4. **Do not depend on the BOM surviving.** Write it, accept its absence.
5. **Pin line endings** with `*.csv text eol=lf` in a `.gitattributes`.

## Not tested

**The Astro build and the rendered page.** The repo has no Astro install yet. Low risk and
re-checked when the build exists, per #20.

**Excel.** Not in the chain — the owner uses Sheets and LibreOffice. The BOM is written
partly for it, so if it ever enters the chain this needs re-running.

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
