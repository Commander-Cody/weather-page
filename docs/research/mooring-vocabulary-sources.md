# Mooring vocabulary sources for weather and tide terms

Research for [issue #5](https://github.com/Commander-Cody/weather-page/issues/5). Sourcing only — this
document hands over raw material and links. The repo owner writes the Frisian text.

**Date of research:** 2026-08-09.

## How to read this document

Every Frisian word below is quoted from a citable source, with the citation next to it. Nothing here
was translated, guessed at, or generated. Where a term the interface will need could not be found in
a source, it is listed in [Gaps](#gaps-terms-that-could-not-be-sourced) rather than invented.

Two caveats on the material itself:

- The Nordfriisk Instituut grammar is a **preliminary version** ("Vorläufige Version, Stand
  31.12.2020"), self-labelled as such on every page. The printed 2021 edition supersedes it.
- Grammar examples are quoted from a two-column PDF. Each pairing below was checked in context, but
  if a term is load-bearing, verify it against the page rather than trusting this file.

Register warning: the dictionary is a general-language dictionary, not a meteorological one. Many
entries are idioms and everyday speech. A weather page needs a **terse, headline register** — the
prior art in [Prior art](#prior-art-material-already-written-in-mooring) is worth more for that than
any word list.

---

## Bottom line

| Question | Answer |
| --- | --- |
| Is there a machine-readable route into friesisch.net? | No API, no bulk download, no sitemap. But search is a plain `GET` URL that returns server-rendered HTML — scrapable. See [below](#friesischnet). |
| Is any of it openly licensed? | **No.** Nothing found carries an open licence. Every source is all-rights-reserved or silent. Reuse needs permission. |
| Is there a published Mooring grammar? | Yes, free PDF, and it is good — numerals, clock, dates, weekdays all covered. |
| Does prior art in this exact domain exist? | Yes: daily Mooring radio news (FriiskFunk), an NDR Mooring podcast, and a state-ministry school curriculum with a "Wääder / Wetter" vocabulary block. |
| Are compass, weekday, month, time-of-day and numeral strings sourceable? | **Yes, all of them.** See [Sourced terms](#sourced-terms). |
| Beaufort / wind-force scale? | **No.** Genuine gap — see [Gaps](#gaps-terms-that-could-not-be-sourced). |

---

## friesisch.net

<https://friesisch.net/> — "Nordfriesisches Onlinewörterbuch", run by **Frasche Rädj / Friesenrat
Sektion Nord e.V.**

### What it is

Roughly 36,000 words, terms and detailed explanations for mainland Frisian (Mooring), online since
early 2021; Söl'ring was added in April 2024, with Fering and Öömrang since added and Halunder
planned. Funded by the Federal Government Commissioner for Culture and the Media via the Friisk
Stifting. Source: [Friesenrat, "Nordfriesisches
Onlinewörterbuch"](https://friesenrat.de/2024/04/12/nordfriesisches-onlinewoerterbuch/) and
[friesisch.net "Allgemeines"](https://www.friesisch.net/allgemeines).

Besides the dictionary it has a verb conjugator and a pronunciation aid ([Friesenrat, as
above](https://friesenrat.de/2024/04/12/nordfriesisches-onlinewoerterbuch/)).

### Machine-readable route in — the useful finding

There is **no API and no bulk download**, and no sitemap (`/sitemap.xml` returns 404). But the search
form is a `GET` form, so every lookup has a **stable, shareable URL** that returns server-rendered
HTML:

```
https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=<German word, URL-encoded>
```

- `dynamicLanguage`: `2` = Mooring (Festland), `3` = Söl'ring, `4` = Fering, `5` = Öömrang. Read off
  the `<select>` on the homepage.
- `staticLanguage=1` and `sourceLanguageType=static` mean "the source language is German".
- Results sit in `article.entry` blocks: `strong.entry__source-string` is the German headword,
  `h3.entry__headline` the Mooring translation, and `p.entry__translation` elements come in
  German/Frisian pairs as usage examples.
- `robots.txt` is permissive (`User-agent: * / Disallow:`), so crawling is not disallowed — but see
  licensing below, which is the actual constraint.
- The search is a **prefix/substring match on German**, so a query returns the headword plus
  neighbours (`Wind` also returns `Windmühle`, `windeln`, …). Filter on exact headword match.

**Practical recommendation:** do not build a scraper into the site's runtime. Use the URL above by
hand while writing strings, and paste the confirmed terms into the language file. That keeps the
attribution question simple and does not put load on a minority-language volunteer project.

### Weather and tide coverage

Good, and better than expected. The usage examples are the valuable part. Verified present:
`Wind`, `Wetter`, `Regen`, `Sturm`, `Flut`, `Ebbe`, `Gezeiten`, `Hochwasser`, `Niedrigwasser`,
`Wasserstand`, `Sturmflut`, `Springflut`, `Sonne`, `Sonnenaufgang`, `Sonnenuntergang`, `Wolke`,
`Bewölkung`, `Nebel`, `Schnee`, `Gewitter`, `Hagel`, `Frost`, `Temperatur`, `Grad`, `Warnung`,
`Vorhersage`, `Meer`, `Nordsee`, `Küste`, `Deich`, `Watt`, `Wattenmeer`, all months, all weekdays,
all compass points.

Verified **absent**: `Windstärke`, `Beaufort`, `Windgeschwindigkeit`, `Wetterwarnung`, `Tide`,
`Nipptide`, `Regenwahrscheinlichkeit`, `Luftfeuchtigkeit`, `Millimeter`, `Wassertiefe`, `Normalnull`.

### Licensing

There is **no open licence**. Two statements bear on reuse, and neither grants it:

- The imprint says only that the site's own use of the material was cleared by the rights holders:
  "Die Verwendung der digitalen Medien sowie der textlichen Inhalte ist von den Urhebern genehmigt
  worden" — [friesisch.net Impressum](https://friesisch.net/impressum).
- "Allgemeines" states that further use of the database requires approval from the Ferring Stiftung,
  for the material they contributed (the island dialects) —
  [friesisch.net Allgemeines](https://www.friesisch.net/allgemeines).

For **Mooring**, the responsible body is the Friesenrat, not the Ferring Stiftung
([friesisch.net Kontakt](https://friesisch.net/kontakt)). So: individual words used to write an
interface are almost certainly fine as ordinary dictionary use, but **copying the database is not**.
If in doubt, ask — contact details in [Who to talk to](#who-to-talk-to).

### Contact

Frasche Rädj / Friesenrat Sektion Nord e.V., Friisk Hüs, Süderstraße 6, 25821 Bräist/Bredstedt ·
+49 4671-6024150 · <info@friesenrat.de>. For Mooring specifically, that is the right address.
Source: [friesisch.net Kontakt](https://friesisch.net/kontakt).

---

## Nordfriisk Instituut

<https://www.nordfriiskinstituut.eu/> — the central research institute for North Frisian language,
history and culture, in Bredstedt.

### The online Mooring grammar — the single most useful document found

**Friesische Gebrauchsgrammatik — Mooringer FRASCH**, by Antje Arfsten, Anne Paulsen-Schwarz and
Lena Terhart, with Henriette Boysen and Erk Petersen. Verlag Nordfriisk Instituut, Bräist/Bredstedt,
2020. 180 pages.

- **Free PDF:**
  <https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf>
- Announcement and background:
  [Nordfriisk Instituut, "Grammatik des Mooringer
  Friesisch"](https://www.nordfriiskinstituut.eu/aktuelles/news/grammatik-des-mooringer-friesisch/)
- Marked **"Vorläufige Version, Stand 31.12.2020, © Nordfriisk Instituut"** on every page. Copyright
  line: "© Verlag Nordfriisk Instituut, Bräist/Bredstedt, NF · 2020". Free to download, **not**
  openly licensed.
- Printed edition: 192 pp., €16.80, via the [Nordfriisk Instituut
  Verlag](https://verlag.nordfriiskinstituut.eu/weblooden/produkt/friesische-gebrauchsgrammatik-mooringer-friesisch/).
  Buy it — the printed version is the one to cite, and it is the corrected text.
- Method note worth knowing: the authors did not only compile the existing literature; they analysed
  video and audio recordings of native speakers to check current usage
  ([announcement](https://www.nordfriiskinstituut.eu/aktuelles/news/grammatik-des-mooringer-friesisch/)).

Chapters directly relevant to this project: §1 Schreibweise und Aussprache (orthography), §7
Numeralia (cardinals, ordinals, clock times, dates, arithmetic), §8 Adverbien (weekday adverbs,
today/tomorrow/yesterday forms).

There is a companion volume for **Fering**, useful later given that Fering is a planned extension:
<https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Fering.pdf>

### Friesische Wortbildung — Mooringer Friesisch

Same authors, 2021, 70 pages, free PDF, also a preliminary version
("Vorläufige Version, Stand 31.12.2021, © Nordfriisk Instituut"):
<https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Wortbildung_-_MOORING.pdf>

Covers how Mooring builds words from prefixes and suffixes — verbs, adjectives, nouns, adverbs. Not a
word list, but the right reference when a needed compound is not in the dictionary and the owner
wants to know whether a form is well-built. Listed on the institute's
[E-Books page](https://www.nordfriiskinstituut.eu/futuur/audio-e-books-historische-buecher/e-books/).

### Other downloadable material

The institute's [E-Books
page](https://www.nordfriiskinstituut.eu/futuur/audio-e-books-historische-buecher/e-books/) also
offers free PDFs of literary works by Peter Jensen and N. A. Johannsen, and the complete index to the
*Nordfriesisches Jahrbuch* 1965–2021. Note that the literary texts are historical and their spelling
is not current Mooring orthography — useful for flavour, not for interface strings.

Eight teaching PDFs on regional history (Biikebrennen, dikes, Frisian freedom, …) are listed on the
parent page:
<https://www.nordfriiskinstituut.eu/futuur/audio-e-books-historische-buecher/>

No licensing statement appears on any of these pages.

### Teaching material — online course platform

<https://moodle.nordfriiskinstituut.de/> — free online Frisian courses. As of the research date it
offers **Söl'ring only**, with "Fering, Mooring and Öömrang to follow later". Registration is free
but manual: email first and last name plus a chosen username to `liirskap@nordfriiskinstituut.de`.
Nothing downloadable. **Not usable for this project yet**, but worth re-checking when Mooring lands.

### Contact — for the human reviewer

Verein Nordfriesisches Institut e.V., Süderstraße 30, 25821 Bräist/Bredstedt ·
+49 4671 6012-0 · <info@nordfriiskinstituut.de> · Director: Dr. Christoph Schmidt.
Source: [Nordfriisk Instituut Impressum](https://www.nordfriiskinstituut.eu/impressum/).

This is the right first address for "would someone look over my Frisian?". The Friesenrat
(<info@friesenrat.de>) is the second, and is arguably the better one for Mooring specifically, since
they own the dictionary.

---

## Other dictionaries

### friisk.org

<https://friisk.org/> — a translator, verb conjugator and pronunciation guide built by Tanno
Hüttenrauch and Michael Wehar (<nurdfriisk@gmail.com>).

**How it differs: it is Söl'ring-first.** The primary pairs are German↔Söl'ring and English→Söl'ring.
It references other varieties — Fering, Halligfriesisch, Karrharder, Nordergoesharder, Öömrang,
Wiedingharder — but **Mooring is not its focus**, and Tanno Hüttenrauch is credited on friesisch.net
as the *Sylter Friesisch* contributor ([friesisch.net
Impressum](https://friesisch.net/impressum), [friesisch.net Kontakt](https://friesisch.net/kontakt)).

**Verdict for this project: low value.** Useful if the page ever grows a Söl'ring variant. Do not use
it for Mooring — cross-dialect borrowing is exactly the kind of error that is hard to spot and
embarrassing to ship. No licence, API or download information published.

### Thesaurus des Nordfriesischen (Kiel)

<https://www.frisistik-thesaurus.uni-kiel.de/> — an academic database of North Frisian texts,
glossaries, grammars and bibliographies, run by ISFAS at Christian-Albrechts-Universität zu Kiel. It
is the reference corpus the Nordfriisk Instituut grammar itself cites (grammar bibliography, p. 180).

**Currently not publicly accessible** — access requires CAU affiliation and VPN. As of March 2024 the
department had funding for an assistant to work out how to offer the thesaurus as open source in
future. Contact: Christoph Winter, <c.winter@isfas.uni-kiel.de>.

Worth an email if a term proves impossible to source elsewhere.

### Print dictionaries

- **Frasch Uurdebök. Wörterbuch der Mooringer Mundart**, Bo Sjölin, Alastair G. H. Walker, Ommo
  Wilts, Nordfriesische Wörterbuchstelle der CAU Kiel; Karl Wachholtz, Neumünster (ISBN
  3-529-04615-9). This is the **reference dictionary of Mooring** and the work the modern orthography
  is anchored to. Cited in the [Gebrauchsgrammatik
  bibliography](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)
  (p. 180) as "Sjölin, Bo et al: Frasch Uurdebök. Wörterbuch der Mooringer Mundart, Neumünster 2002".
  Catalogue record: [WorldCat
  OCLC 22615546](https://search.worldcat.org/oclc/22615546).
- **Basiswörterbuch Deutsch-Friesisch**, Ingeline Hamann (transfer into Bökingharde Frisian) with the
  Bökingharde working group, 2000, 240 pp., ~2,500 words and ~2,800 example sentences, €12.50 — sold
  by [Friisk Foriining](https://friiske.de/de/produkt/basisworterbuch-deutsch-friesisch/). No digital
  edition. The example-sentence density makes this the best *paper* source for register.

---

## Prior art: material already written in Mooring

This section is worth more than the dictionaries. It shows how Mooring speakers actually phrase this
material.

### FriiskFunk — daily radio, mainland news in Frasch

<https://www.oksh.de/mitmachen/senden/friiskfunk/> — North Frisian daily radio on Offener Kanal
Westküste (Westküste FM), weekdays 08:00–10:00, running since 25 September 2010. The daily mix
carries **news from the mainland in frasch**, from Sylt in sölring, and from Amrum and Föhr in
fering/öömrang. Run jointly by the Ferring Stiftung and Offener Kanal SH.

- Programme listing: <https://www.oksh.de/mitmachen/senden/friiskfunk/friiskfunk-sendungen/>
- Live stream: <https://www.oksh.de/wk/hoeren/westkueste-fm-livestream/>

**This is the closest thing to a spoken Mooring weather report that exists.** Daily news bulletins are
exactly the terse register a weather page needs. Listening to a week of mainland segments — or asking
the FriiskFunk team directly — is likely the single highest-yield action on this whole ticket.

### NDR — "Frasch for enarken"

NDR 1 Welle Nord broadcasts a Frisian segment within "Von Binnenland und Waterkant", Wednesdays
20:05–21:00 on the Sylt and Flensburg transmitters, plus an on-demand podcast **"Frasch for enarken"**
— the title itself is Mooring.

- Programme page: <https://www.ndr.de/wellenord/sendungen/friesisch/index.html>
- Podcast: <https://www.ndr.de/wellenord/podcast4978.html>
- Both listed by the [Friesenrat, "Nachrichten in friesischer
  Sprache"](https://friesenrat.de/nachrichten-in-friesischer-sprache/)

### School curriculum — Schleswig-Holstein Ministry of Education

**Leitfaden für den Friesischunterricht an Schulen in Schleswig-Holstein (Primarstufe), 2015**,
published by the Ministerium für Schule und Berufsbildung des Landes Schleswig-Holstein:
<https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf>

It contains a per-dialect vocabulary and theme table, and the **Frasch column has a "Wääder /
Wetter" block and a "Tide / Zeiten" block** — i.e. an official, citable, Mooring weather word list.
Content quoted in [Sourced terms](#weather-and-sky) below (see p. 22 of the PDF). It also has a
§4.1.6.3.1 "Frasch" grammar section and a §4.1.6.4 "Rechtschreibung" section.

This document is a state publication and, unlike the dictionary, is unambiguously public material.

### *Nordfriesland* magazine

Published by the Nordfriisk Instituut for over five decades. **Not available online**: "Aus
urheberrechtlichen Gründen können wir Artikel in der Regel nicht online zur Verfügung stellen" —
readers are directed to the on-site library. There is a searchable **index** (author, keyword, theme,
period), but no full text:
<https://www.nordfriiskinstituut.eu/futuur/artikel-datenbank-1/>

Product page: <https://verlag.nordfriiskinstituut.eu/weblooden/produkt/zeitschrift-nordfriesland/>

**Verdict: low yield for this project.** The index is worth a search for tide/weather themes if the
owner visits the library, but it cannot be consulted remotely, and much of the magazine is in German
rather than Frisian.

### Community organisations

- **Friisk Foriining** — <https://friiske.de/>, founded 1923, ~600 members. Publishes and supports
  bilingual schoolbooks, expands Frisian teaching in Nordfriesland schools, and runs an annual
  Frisian-language autumn school ("Friisk Harfsthuuchschölj"). Sells the Basiswörterbuch above. A
  plausible source of a volunteer proofreader.
- **Rökefloose** — the Frisian youth organisation Friisk Foriining works with. Referenced on
  [friiske.de](https://friiske.de/en/the-organisation/). Could not confirm any periodical of that name;
  do not cite it as a publication.
- **Church publications** — nothing found. Frisian-language church material exists historically, but
  no online, citable, Mooring-language source in this domain surfaced. Treat as unsearched rather than
  as established absent.

### Existing Mooring weather page

**None found.** No Mooring-language weather or tide site appears to exist. That is a point in the
project's favour and also means there is no register to copy for the specific job of labelling a
forecast — the closest models remain FriiskFunk and the school curriculum.

---

## Sourced terms

Every term below carries a citation. **`[FN:X]`** means: friesisch.net, Mooring lookup for German
headword *X*, at
`https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=X`
(URL-encode umlauts). **`[GG]`** means the [Friesische Gebrauchsgrammatik —
Frasch](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)
PDF, with section and page. **`[LF]`** means the [Leitfaden Friesischunterricht Primarstufe
2015](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf),
p. 22.

Note on articles: Mooring nouns are cited with their gender article — `di` (masc.), `jü` (fem.),
`dåt` (neut.). Keep them; the grammar notes gender is given in the dictionary because only the
D-article distinguishes all three genera ([GG §3.1](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)).

### Compass directions

| German | Mooring | Source |
| --- | --- | --- |
| Norden | `dåt norden` | [FN:Norden](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Norden) |
| Süden | `dåt sööden` (also `sööder`), `dåt süsen` | [FN:Süden](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=S%C3%BCden) |
| Osten | `dåt ååst(en)` | [FN:Osten](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Osten) |
| Westen | `dåt weest`, `dåt weesten` | [FN:Westen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Westen) |
| Nordwesten | `dåt Nordweest(en)` | [FN:Nordwesten](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Nordwesten) |
| Nordosten | `di/dåt nordååst` | [FN:Nordwesten](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Nordwesten) (same result page) |
| Südosten | `dåt söödååsten` | [FN:Südosten](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=S%C3%BCdosten) |
| Südwest | `dåt söödweesten` | [FN:Südwesten](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=S%C3%BCdwesten) |
| nordwestlich (adj.) | `nordweest` | [FN:Nordwesten](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Nordwesten) |
| Himmelsrichtung | `jü hamelsruchting; -e` | [FN:Himmelsrichtung](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Himmelsrichtung) |

**Wind-direction phrasing** — this is what the UI actually needs, and it is attested:

| German | Mooring | Source |
| --- | --- | --- |
| Der Wind weht aus Südwest. | `E win wait üt söödweest.` | [GG §"üt" (Präpositionen), p. 83](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf) |
| der Wind kommt von Osten | `e win kamt foon ååst(en)` / `dåt wait foont ååst` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind), [FN:Osten](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Osten) |
| der Wind kommt von Norden | `e win kamt foont/üt norden` | [FN:Norden](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Norden) |
| der Wind hat nach Norden gedreht | `e win as am e nord gängen` / `eeftert norden amgängen` | [FN:Norden](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Norden) |
| der Wind dreht sich | `e win låpt am` / `drait ham` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| er weiß, woher der Wind weht | `hi wiitj hiilj gödj, foon huken kånte e win wait` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |

Academic background, if the owner wants to get the directional idiom right: **Christoph Winter, *Der
Kompass der Nordfriesen. Sprachliche Kodierung absoluter Orientierung am Beispiel der
Himmelsrichtungen und Richtungspartikeln im Nordfriesischen***, dissertation CAU Kiel 2020, published
2023 by Franz Steiner Verlag (ZDL-Beihefte 194); awarded the Elise-Reimarus-Preis 2023. Cited in the
[GG bibliography, p. 180](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf);
author page: [ISFAS
Kiel](https://www.isfas.uni-kiel.de/de/frisistik/mitarbeitende/b.a.-christoph-winter); prize
announcement: [Akademie der Wissenschaften in
Hamburg](https://www.awhamburg.de/aktuell/aktuelles/detailseite/frisist-christoph-winter-hat-den-elise-reimarus-preis-2023-erhalten.html).

This matters more than it looks. North Frisian encodes **absolute** orientation (`ap`, `dil`, `üt`,
`ouer`, `am` used geographically), which is unusual for a European language. A wind-direction label
translated word-for-word from German may read wrong. This is the reference for getting it right, and
a strong argument for a human reviewer.

### Wind

| German | Mooring | Source |
| --- | --- | --- |
| Wind | `di win` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| ein kühler Wind | `en koulen win` / `en köljåftien win` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| ein heftiger Wind | `en stiwen win` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| eine steife Brise | `en stiwen win` | [FN:steif](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=steif) |
| ein schneidender Wind | `en scharpen win` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| ein lauer Wind | `en louen win` / `en liisen win` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| der Wind weht | `di win wait` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| der Wind nimmt zu | `e win namt bai` / `e win brüset ap` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| der Wind flaut ab | `e win flaut ouf` / `lounet ouf` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| es kommt Wind auf | `dåt fångt önj tu waien` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| Windbö | `di håålwin; -e`, `di stiitj; -e`, `di winpüst` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| Bö(e) | Windböe: `di håålwin; -e`; Regenböe: `di (rin)flååge; -` | [FN:Böe](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=B%C3%B6e) |
| windig | `wini`, `püsti` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| es war sehr windig | `dåt wus sün püsti wääder` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| windstill | `loun`, `luukloun` (völlig windstill) | [FN:Windstille](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Windstille) |
| es ist windstill | `dåt as en stal wääder` | [FN:Windstille](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Windstille) |
| Windrichtung (as compound part) | `di winfoone` (Windfahne / Wetterfahne) | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| Windenergie | `jü winenergii` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| gegen den Wind | `lik iinj(önj) e win` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |
| mit dem Wind | `ma e win` | [FN:Wind](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wind) |

**Trap:** `win` is also the word for *Wein* (wine) — "Schan wat nuch en glees win" = "Wollen wir beide
noch ein Glas Wein" ([GG §5.1.1 Dual](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)).
Context disambiguates in a weather page, but be aware.

### Storm

| German | Mooring | Source |
| --- | --- | --- |
| Sturm | `di storm; -e` | [FN:Sturm](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sturm) |
| es kommt Sturm auf | `deer kamt en storm ap` | [FN:Sturm](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sturm) |
| ein heftiger Sturm | `en ärjen storm` / `en ünnooselen storm` | [FN:Sturm](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sturm) |
| Sturmbö | `jü stormflååg; -e` | [FN:Sturm](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sturm) |
| Sturmwind | `di stormwin` | [FN:Sturm](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sturm) |
| stürmisch | `stormi`, `brüsi`, `rüsi`, `ruuschi`, `orkel` | [FN:Sturm](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sturm) |
| stürmisches Wetter | `en stormi/orkel/brüsi wääder`; `en wunerk wääder` (storm with snow or rain) | [FN:Sturm](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sturm) |
| wir haben stürmisches Wetter | `dåt as rüsi önjt wääder` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| **Sturmwarnung** | `jü stormwoorschouing; -e`, `jü stormmalding; -e` | [FN:Sturm](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sturm) |
| Warnung | `jü woorschouing; -e` | [FN:Warnung](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Warnung) |
| Sturmflut | `jü stormflödj; -e` | [FN:Sturmflut](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sturmflut) |

`stormwoorschouing` / `stormmalding` is the highest-value single find for the DWD-warnings feature.

### Weather and sky

| German | Mooring | Source |
| --- | --- | --- |
| Wetter | `dåt wääder` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter), [GG §1.1, p. 9](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf) |
| wie ist das Wetter heute? | `huk wääder as et diling?` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| wie ist das Wetter heute? (school phrasing) | `hü as dåt wääder diling?` | [LF, p. 22](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf) |
| Wetterbericht | `di wääderberucht` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter); also `min wansch-wääderberucht` in [LF, p. 22](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf) |
| Wetterkarte | `jü wääderkoord; -e` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| Wetterlage | `di wääderlååge` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| Wetterwarte | `jü wääderstatsjoon; -e` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| Vorhersage | `jü forütseeding; -e` | [FN:Vorhersage](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Vorhersage) |
| es ist schönes Wetter | `dåt as moi wääder` / `fain wääder` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| wechselhaftes Wetter | `wanschlik wääder` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| beständiges Wetter | `bestandi wääder` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| regnerisches Wetter | `reeni wääder` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| schlechtes Wetter | `hiinj wääder`, `fül wääder` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| das Wetter klart auf | `dåt wårt nuch huug wääder` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| das Wetter wird trocken | `dåt wääder seet ap` | [FN:Wetter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wetter) |
| Sonne | `jü san; -e` | [FN:Sonne](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sonne) |
| Sonnenschein | `di sanschin` | [FN:Sonne](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sonne) |
| **Sonnenaufgang** | `di sanapgung; -e` | [FN:Sonnenaufgang](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sonnenaufgang) |
| **Sonnenuntergang** | `di sanunergung; -e` | [FN:Sonnenuntergang](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sonnenuntergang) |
| Wolke | `jü wulk; wulkene`, `jü woolken; -e` | [FN:Wolke](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wolke) |
| Bewölkung | `di ouertooch` | [FN:Bewölkung](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Bew%C3%B6lkung) |
| wolkenlos | `deer as ai en wulk bai e hamel` | [FN:Wolke](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wolke) |
| Himmel (in "vom Himmel") | `e hamel` | [GG §3 (E-Artikel)](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf) |
| Regen | `di rin` | [FN:Regen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Regen) |
| es gibt Regen | `et jeeft rin` / `we foue rin` | [FN:Regen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Regen) |
| es sieht nach Regen aus | `dåt schucht üt eefter rin` | [GG §"eefter" (Präpositionen)](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf) |
| leichter Regen | `en äiwenen rin` | [FN:Regen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Regen) |
| Nieselregen | `di muschrin` | [FN:Regen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Regen) |
| starker (strömender) Regen | `di gootrin`, `en uusenen/giitjenen rin` | [FN:Regen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Regen) |
| Regenschauer | `jü rinflååg; -e` (also `di (rin)flååge; -`), `dåt schöör; schöre` | [FN:Regen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Regen) |
| Regenwetter | `dåt rinwääder` | [FN:Regen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Regen) |
| Nebel | `di mist`, `di nääbel`, `di diise` (light mist) | [FN:Nebel](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Nebel) |
| Schnee | `di snii` | [FN:Schnee](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Schnee) |
| Schneesturm | `di sniistorm; -e` | [FN:Schnee](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Schnee) |
| Gewitter | `dåt tunerwääder` | [FN:Gewitter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Gewitter) |
| Gewitterschauer | `di/jü tunerflååg; -e` | [FN:Gewitter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Gewitter) |
| Hagel | `di häägel` | [FN:Hagel](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Hagel) |
| Frost | `di froost` | [FN:Frost](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Frost) |
| Frostwetter | `dåt froostwääder` | [FN:Frost](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Frost) |
| Temperatur | `jü temperatuur; -e` | [FN:Temperatur](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Temperatur) |
| die Temperatur steigt | `e temperatuur steecht` / `gungt amhuuch` | [FN:steigen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=steif) (under "steigen") |
| Grad | `di grood; -e` | [FN:Grad](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Grad) |
| Feuchtigkeit | `di fucht`, `jü fuchtihäid` | [FN:Feuchtigkeit](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Feuchtigkeit) |
| das Barometer fällt | `dåt wääderglees gungt dil` | [FN:fallen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=fallen) |

**School-curriculum weather word list (Frasch column, verbatim):**

> `sanschin, rin, snii ... - wurm, kölj, wätj, wini, misti ...`
> `hü as dåt wääder diling?`
> `We schriwe arken däi ap, hü dåt wääder as.`
> `Min wansch-wääderberucht`

— [Leitfaden Friesischunterricht Primarstufe 2015, p. 22](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf).
So: `wurm` warm, `kölj` cold, `wätj` wet, `wini` windy, `misti` foggy — a state-published set of
weather adjectives. `wurm` is confirmed by the dictionary's comparative: "heute ist es wesentlich
wärmer als gestern" = `diling as et ordi wat wurmer as anjörsne`
([FN:Westen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Westen), under "wesentlich").

### Water, tide and coast

| German | Mooring | Source |
| --- | --- | --- |
| Wasser | `dåt wååder` | [GG §1.3, p. 20](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf) |
| **Ebbe** | `jü eebe` | [FN:Ebbe](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Ebbe) |
| **Flut** | `jü flödj; -e`, `dåt wååder` | [FN:Flut](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Flut) |
| Ebbe und Flut | `eebe än flödj` | [FN:Ebbe](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Ebbe), [FN:Gezeiten](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Gezeiten) |
| **Gezeiten** | `eebe än flödj` | [FN:Gezeiten](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Gezeiten) |
| steigende Flut | `dåt kaamen wååder` | [FN:Flut](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Flut) |
| Flutzeit | `jü flödjtid` | [FN:Flut](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Flut) |
| Flutmarke | `dåt flödjmårk; -e` | [FN:Flut](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Flut) |
| **Hochwasser** | `dåt huugwååder` | [FN:Hochwasser](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Hochwasser) |
| **Niedrigwasser** | `dåt läichwååder` | [FN:Niedrigwasser](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Niedrigwasser) |
| **Wasserstand** | `di wååderstånd; -e`, `di wååderpäägel` | [FN:Wasserstand](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Wasserstand) |
| Springflut | `jü sprängflödj; -e` | [FN:Springflut](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Springflut) |
| **das Wasser steigt** | `dåt wååder steecht` | [FN:steigen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=steif) (under "steigen") |
| **das Hochwasser ist um 20 cm gefallen** | `dåt huugwååder as am twunti cm saked` | [FN:fallen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=fallen) |
| Meeresspiegel | `di wååderspäägel` | [FN:Meer](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Meer) |
| Meer / See | `di siie; -`; die See: `jü siie; -` | [FN:Meer](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Meer) |
| **Nordsee** | `e Weestsiie` (esp. w.r.t. Schleswig-Holstein), `di Nordsiie` | [FN:Nordsee](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Nordsee) |
| Nordsee / Ostsee (school list) | `weestsiie / ååstsiie` | [LF, p. 22](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf) |
| **Wattenmeer** | `dåt heef`, `dåt wåt` | [FN:Watt](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Watt) |
| Wattstrom / Priel | `di priil; -e`, `dåt lai; -e`, `dåt rindel; rindle` | [FN:Watt](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Watt) |
| Küste | `di küst; -e`; Uferkante des Wattenmeeres: `di heefskånt; -e` | [FN:Küste](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=K%C3%BCste) |
| Küstenschutz | `di küstenschuts` | [FN:Küste](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=K%C3%BCste) |
| Deich | `di dik; -e` | [FN:Deich](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Deich) |
| Deichvorland | `dåt büterlönj` | [FN:Deich](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Deich) |
| Strand (school list) | `di strönj` | [LF, p. 22](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf) |
| Nordfriesland | `Nordfraschlönj` | [LF, p. 22](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf) |

The pair `dåt wååder steecht` / `dåt huugwååder … saked` is the attested rise/fall verb pair for a
water-level chart. `sake` (to fall, of water) is not the same verb as `fåle` (to fall, of objects) —
worth preserving.

### Times of day

| German | Mooring | Source |
| --- | --- | --- |
| Morgen (noun) | `di mjarn; -e` | [FN:Morgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Morgen) |
| am Morgen | `am mjarnem` | [FN:Morgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Morgen) |
| Vormittag | `di formadi`, `di iirmadi` | [FN:Vormittag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Vormittag) |
| Mittag | `di madi` (no plural) | [FN:Mittag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Mittag) |
| Nachmittag | `di eeftermadi; -e` | [FN:Nachmittag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Nachmittag) |
| Abend | `di een; -e` | [FN:Abend](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Abend) |
| Nacht | `jü nåcht; -e` | [FN:Nacht](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Nacht) |
| in der Nacht | `önj e nåcht`; nachts: `am nåchtem` | [FN:Nacht](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Nacht) |
| morgens / abends / mittags / nachts | `am mjarnem` / `am eenmen` / `am madiem` / `am nåchtem` | [FN:Morgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Morgen), [FN:Abend](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Abend), [FN:Mittag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Mittag), [FN:Nacht](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Nacht) |
| Morgendämmerung | `di fordäi`, `di likstendäi` | [FN:Morgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Morgen) |
| Morgengrauen | `di deeringe`, `di fordäi` | [FN:Morgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Morgen) |
| Abenddämmerung | `di eenhärnge` | [FN:Abend](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Abend) |
| Morgenrot | `dåt däisrüüdj` | [FN:Morgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Morgen) |
| Abendrot | `di eenglaame` | [FN:Abend](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Abend) |
| Abendnebel | `di eenmist`, `di eennääbel` | [FN:Abend](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Abend) |
| Tag | `di däi; deege` | [FN:Tag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Tag) |
| Tageszeit | `jü däistid`, `jü tid foon e däi` | [FN:Tag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Tag) |
| Woche | `jü waag; -e` | [FN:Woche](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Woche) |
| Wochenende | `dåt waagiinje; -` | [FN:Woche](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Woche) |
| Stunde / Minute | `jü stün; -e` / `jü minuut; -e` | [FN:Stunde](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Stunde), [FN:Minute](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Minute) |

**Relative days** — the highest-frequency strings of all. The grammar derives them with the `-ling`
suffix ([GG ch. 8 Adverbien, p. 88](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)):

| German | Mooring | Source |
| --- | --- | --- |
| heute | `diling` | [GG p. 88](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf), [FN:heute](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=heute) |
| heute Morgen | `mårling` (also `mååling`) | [GG p. 88](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf), [FN:Morgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Morgen) |
| heute Mittag | `tumadi` | [FN:Mittag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Mittag) |
| heute Nachmittag | `eeftermadi` | [FN:Nachmittag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Nachmittag) |
| heute Abend | `eeling` | [GG p. 88](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf), [FN:Abend](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Abend) |
| heute Nacht | `nåchtling` | [GG p. 88](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf) |
| diese Woche | `waagling` | [GG p. 88](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf) |
| dieses Jahr | `jarling` | [GG p. 88](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf) |
| morgen | `mjarne` | [FN:Morgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Morgen) |
| morgen früh | `mjarneeder` | [FN:Morgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Morgen) |
| morgen Abend | `mjarneene`, `mjarne eene` | [FN:Morgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Morgen) |
| übermorgen | `ouremjarne` (also `ouerdemjarne`, `ordimjarne`) | [FN:übermorgen](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=%C3%BCbermorgen) |
| gestern | `änjörnse` / `anjörsne` | [GG p. 88](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf) |
| vorgestern | `äniirjörsne` | [GG p. 88](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf) |
| jetzt | `nü` | [FN:jetzt](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=jetzt) |

**Careful:** `mjarn` = *morning*, `mjarne` = *tomorrow*. One letter apart, and `diling as weensdi ...,
mjarne as törsdi ...` in the school curriculum confirms `mjarne` in the "tomorrow" sense
([LF, p. 22](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf)).
For a page whose whole layout is "today / tomorrow / next six days", get this pair reviewed.

### Days of the week

| German | Mooring | "on ...s" (adverbial) |
| --- | --- | --- |
| Montag | `di moundi` | `moundäis`, `di moundi`, `en moundi` |
| Dienstag | `di täisdi; -deege` | `täisdäis`, `di täisdi`, `en täisdiem` |
| Mittwoch | `di weensdi` | `weensdäis`, `en weensdi` |
| Donnerstag | `di törsdi; -deege` | `törsdäis`, `di törsdi`, `en törsdiem` |
| Freitag | `di fraidi` | `fraidäis`, `en fraidi`, `am fraidiem` |
| Samstag / Sonnabend | `di saneene; -` | `di saneene`, `en saneene` |
| Sonntag | `di saandi; -e` | `saandäis`, `di saandi` |

Sources: [GG ch. 8 Adverbien, p. 88](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)
for the `-däis` adverbs and the note that `saneene` has no `-däis` form (only `di saneene`); and
friesisch.net for the nouns: [Montag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Montag),
[Dienstag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Dienstag),
[Mittwoch](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Mittwoch),
[Donnerstag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Donnerstag),
[Freitag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Freitag),
[Samstag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Samstag),
[Sonnabend](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sonnabend),
[Sonntag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sonntag).

The grammar explains the `-di` / `-däi` alternation: the shortening of `däi` to `-di` is undone when
`-s` is added. `di saandimjarn` (Sonntagmorgen) shows the compound pattern
([FN:Sonntag](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Sonntag)).

**Abbreviations for a narrow column are a gap** — see [Gaps](#gaps-terms-that-could-not-be-sourced).

### Months

Two parallel sets: an international one and a native one. Both are given by the dictionary.

| German | International | Native | Source |
| --- | --- | --- | --- |
| Januar | `di januar` | `di ismoune` | [FN:Januar](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Januar) |
| Februar | `di februar` | `di biikenmoune` | [FN:Februar](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Februar) |
| März | `di marts` (also `märts`), `di martsmoune` | `di uursmoune` | [FN:März](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=M%C3%A4rz) |
| April | `di april` | `di gjarsmoune` | [FN:April](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=April) |
| Mai | `di moi` | `di krölemoune` | [FN:Mai](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Mai) |
| Juni | `di juuni` | `di samermoune` | [FN:Juni](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Juni) |
| Juli | `di juuli` | `di foodermoune` | [FN:Juli](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Juli) |
| August | `di august` | `di beeridmoune` | [FN:August](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=August) |
| September | `di septämber` | `di harfstmoune` | [FN:September](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=September) |
| Oktober | `di oktoober` (also `uktoober`) | `di stormmoune` | [FN:Oktober](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Oktober) |
| November | `di nowämber` | `di mistmoune` | [FN:November](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=November) |
| Dezember | `di detsämber` | `di jülmoune` | [FN:Dezember](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Dezember) |

Month is `di moune` ([GG §4.1 Pluralbildung](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf):
"e moune > moune  Monate"). **All month names are masculine** — the grammar states this explicitly
when explaining date agreement ([GG §7.7](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)).

The native names are the more interesting choice for a Frisian-only page, and the school curriculum
uses one: "di jarste moune önjt iir as ismoune"
([LF, p. 22](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf)).
Note the grammar's own date examples use the international set (`di jarste janewoore` — note the
different spelling `janewoore` there vs. `januar` in the dictionary). **This spelling discrepancy is
real and unresolved; ask a reviewer which to use.**

Seasons: `uurs` (spring), `samer` (summer), `harfst` (autumn), `wunter` (winter); `iirstide` =
seasons ([LF, p. 22](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf)).
The grammar corroborates `en/am uursem`, `en/am samrem`, `en/am wuntrem`
([GG, adverbs of time](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)).

### Numerals

All from [GG §7.1, p. 66](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf).

| | | | |
| --- | --- | --- | --- |
| 0 `nul` | 10 `tiin` | 20 `twunti` | 30 `dörti` / `dorti` |
| 1 `iinj` | 11 `alwen` | 21 `iinjäntwunti` | 40 `fäärti` / `fjarti` |
| 2 `tou` | 12 `tweelwen` / `tweelew` | 22 `touäntwunti` | 50 `füfti` |
| 3 `trii` | 13 `tratäin` | 23 `triiäntwunti` | 60 `süsti` |
| 4 `fjouer` | 14 `fjouertäin` | 24 `fjoueräntwunti` | 70 `soowenti` |
| 5 `fiiw` | 15 `füftäin` | 25 `fiiwäntwunti` | 80 `tachenti` |
| 6 `seeks` | 16 `seekstäin` | 26 `seeksäntwunti` | 90 `näägenti` |
| 7 `soowen` | 17 `soowentäin` | 27 `soowenäntwunti` | 100 `hunert` |
| 8 `oocht` | 18 `oochtäin` | 28 `oochtäntwunti` | 200 `touhunert` |
| 9 `nüügen` | 19 `nüügentäin` | 29 `nüügenäntwunti` | 1.000 `duusend` |

Ordinals ([GG §7.7, p. 69](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)),
formed with `-d(e)` (2nd–4th), `-t(e)` (5th–12th), `-st(e)` (13th up):
1. `jarst/-e`, 2. `tweed/-e` (also `ouder/-e`, `lääder/-e`), 3. `treed/-e`, 4. `fiird/-e`,
5. `füft/-e`, 6. `seekst/-e`, 7. `soowenst/-e`, 8. `oochst/-e`, 9. `nüügenst/-e`, 10. `tiinst/-e`,
11. `alwenst/-e`, 12. `tweelewst/-e`, 13. `tratäinst/-e`, 20. `twuntist/-e`, 30. `dortist/-e`,
100. `hunertst/-e`.

**Gender agreement matters for counting:** 1–3 inflect by gender. Masculine `ån hün – twäär hüne – tra
hüne`; feminine/neuter `iinj kåt – tou kåte – trii kåte`
([GG §7.2, p. 66](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)).
Any templated string like "{n} days" or "{n} hours" must therefore agree with the noun's gender —
a real i18n constraint, not a stylistic one.

**Measures stay singular after a number:** `Ik brük nuch twäär pün suker` (two pounds of sugar);
`Dåt hüs stoont tiin meter wid wach foon e stroote` (ten metres away)
([GG §7.2, p. 67](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)).
So `tiin meter`, not `*tiin meetere`. Same for years: `eefter trii iir`.

Metre is `di meeter; -e` ([FN:Meter](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Meter)),
percent `dåt prosänt; -e` (older: `di prusant; -e`)
([FN:Prozent](https://friesisch.net/suche?sourceLanguageType=static&staticLanguage=1&dynamicLanguage=2&searchString=Prozent)).

---

## Numeral, date and time formatting conventions

All from [GG §7](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf).

**Thousands separator is a dot, German-style.** The grammar writes `1.000 duusend` (§7.1) and
`Di woin heet 5.000 euro koosted` (§7.2). No decimal-comma example was found; German convention is
the safe assumption but is **not attested** — flag it for the reviewer.

**Clock times are written with a dot, not a colon.** §7.6 lists `8.15 Uhr`, `7.45 Uhr`, `7.30 Uhr`,
`13.00 Uhr`, `16.00 Uhr`, `20.00 Uhr` — German convention. Note this differs from an ISO-style
`08:15` and matters for the hour-by-hour axis.

**Spoken clock is 12-hour plus a daypart qualifier**, even where the written form is 24-hour
([GG §7.6, p. 68](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)):

| Written | Spoken |
| --- | --- |
| 13.00 Uhr | `e klook iinj (di tumadi)` |
| 16.00 Uhr | `e klook fjouer (di eeftermadi)` |
| 20.00 Uhr | `e klook oocht (di een)` |
| 2.00 Uhr | `e klook tou (önj e nåcht)` |
| 5.00 Uhr | `e klook fiiw (di mjarn)` |

Other clock phrases: `Wat as e klook?` (what time is it), `E klook as tweelwen`,
`Ik kam am e klook tweelwen` (I'm coming at twelve), `fiiring ouer oocht` (8.15),
`fiiring for oocht` (7.45), `huulwe oocht` (7.30 — note: *half eight* = 7.30, as in German, **not** as
in English), `fiiw minuute for huulwe oocht` (7.25), `tiin minuute ouer oocht` (8.10).

**Dates take the D-article and an `-e` ordinal**, because month names are all masculine
([GG §7.7, p. 70](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)):

- `di jarste janewoore` — the first of January / on the first of January
- `di triiäntwuntiste marts` — 23 March / on 23 March

Note there is no separate "on the …" form; the same phrase covers both. Asking the date:
`Wat for'n dootem hääwe we diling?` (§ on interrogatives).

**Arithmetic**, if a chart ever needs it ([GG §7.5, p. 68](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)):
`trii än seeks san nüügen` (3+6=9), `füftäin maner trii san tweelwen` (15−3=12),
`seeks tooche seeks san seeksändorti` (6×6=36), `oochtänfäärti döör oocht san seeks` (48÷8=6).

---

## Orthography

**Which standard applies:** the Mooring spelling in current use goes back to the **Rechtschreibung of
1955**, which the grammar names explicitly and describes as following the reduced vowel system
([GG §1.1, p. 9](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf)).
The reference implementation of it is the **Frasch Uurdebök** (Sjölin/Walker/Wilts, Nordfriesische
Wörterbuchstelle, CAU Kiel), and friesisch.net follows the same conventions.

**Is there a published rule set?** Not a standalone one that surfaced. The closest thing to a usable
rule set is **chapter 1 of the Gebrauchsgrammatik, "Schreibweise und Aussprache" (pp. 9–25)**, which
is free and detailed. The Schleswig-Holstein curriculum also has a §4.1.6.4 "Rechtschreibung" section
([LF](https://fachportal.lernnetz.de/files/Fachanforderungen%20und%20Leitf%C3%A4den/Grundschule_Primarstufe/Leitf%C3%A4den/Leitfaden_Friesisch_Primarstufe_Grundschule_2015.pdf)).
Treat the grammar as the rule set.

Rules that will bite a web project, all from
[GG §1, pp. 8–9](https://www.nordfriiskinstituut.eu/fileadmin/Content/Nordfriisk_Futuur/E-Books/Friesische_Gebrauchsgrammatik_-_Frasch.pdf):

- **Moderated lowercase.** Unlike German, everything is lowercase except sentence starts and proper
  names. So `dåt wääder`, not `dåt Wääder`. This is the single most visible convention on the page,
  and getting it wrong will look immediately wrong to a native reader.
- **The alphabet omits `q`, `v`, `x`, `y`, `z`, `ß`.** Loanwords are respelled: `kwartiir` (Quartier),
  `taksi` (Taxi), `süsteem` (System), `wits` (Witz). Bear this in mind for any technical term the
  page needs.
- **`c` occurs only in `ch` and `sch`.**
- **No consonant doubling to mark a short vowel.** Vowel length is shown by single vs. double *vowel*
  letters instead. Double vowel letters before voiced consonants mark a long vowel.
- **Special characters:** `å` (a distinct vowel), and the palatals written `dj`, `lj`, `nj`, `tj`.
  Plus `ä`, `ö`, `ü`, `üü`, `åå`, `ää`, `öö`, `ii`, `uu`, `oo`, `ee`. **Ensure the site's font stack
  and any URL slugs handle `å` correctly** — it is not a German character and is easy to lose in a
  toolchain. Test this early.
- **Hyphenation and punctuation follow German.**

Alphabet-and-diacritic checklist for a language file: `a å ä b c(d) d e ä f g h i j k l m n o ö p r s
t u ü w` plus digraphs `ch sch dj lj nj tj` and doubled vowels `åå ää ee ii oo öö uu üü`.

---

## Gaps: terms that could not be sourced

**Do not fill these in from a model. Each one needs a human or a source.**

| Needed for | Missing | Notes |
| --- | --- | --- |
| Wind strength labels | **Beaufort / Windstärke / Windgeschwindigkeit** | No entry for `Beaufort`, `Windstärke` or `Windgeschwindigkeit`. The graded adjectives (`loun` → `liisen` → `stiwen` → `scharpen` → `stormi` → `orkel`) exist but are **not a scale**, and no source orders them. Either show numbers with a sourced unit, or get a speaker to define a ladder. |
| Warnings | **Wetterwarnung** (generic) | `stormwoorschouing` / `stormmalding` (storm) and `woorschouing` (warning) are attested; the compound "Wetterwarnung" is not. |
| Rain | **Regenwahrscheinlichkeit** | No entry. `prosänt` is attested, so a phrasing can be built — but the phrasing itself must be written by a speaker, not assembled here. |
| Precipitation amount | **Millimeter** | No entry. `di meeter` is attested; the mm form is not. |
| Humidity | **Luftfeuchtigkeit** | No entry. `di fucht` / `jü fuchtihäid` (Feuchtigkeit) and `jü luft` (in `jü eenluft`) are attested separately; the compound is not. Humidity is on the locked variable list, so this needs resolving. |
| Cloud cover | **percentage phrasing** | `di ouertooch` (Bewölkung) is attested; "60 % Bewölkung" phrasing is not. |
| Sea temperature | **Wassertemperatur / Wassertiefe** | Neither has an entry. `jü temperatuur` and `dåt wååder` exist separately. Sea temperature is on the locked variable list. |
| Tide model | **astronomische Gezeiten / Sturmflutvorhersage / Nipptide** | `Tide` and `Nipptide` return nothing. The distinction between the astronomical tide and the surge-corrected forecast — the defining feature of this page — has **no attested Mooring vocabulary at all**. This is the biggest single gap and the one most worth an expert conversation. |
| Water level datum | **Normalnull / NHN / Pegelnullpunkt** | No entries. If heights are labelled against a datum, the label must be sourced. |
| UI chrome | **compass abbreviations (N/NO/O/SO/S/SW/W/NW)** | Full words are attested; no source shows an abbreviation convention for Mooring. Either spell them out or ask. |
| UI chrome | **weekday and month abbreviations** | Same problem. A narrow mobile column will want `Mo/Di/Mi/…`, but no Mooring abbreviation scheme was found. Do not invent one — spelling out `moundi` is safe. |
| Date order | **decimal comma** | Thousands-dot is attested; decimal separator is not. |
| Interface verbs | **laden / aktualisieren / Fehler / keine Daten** | Not investigated. All are ordinary vocabulary and should be lookup-able on friesisch.net, but were out of scope here. |
| Spelling conflict | `janewoore` (grammar) vs `januar` (dictionary) | Both are Nordfriisk-Instituut-adjacent sources and they disagree. Needs a ruling. |

---

## Who to talk to

The owner mentioned wanting a human reviewer. In rough order of fit:

1. **Frasche Rädj / Friesenrat Sektion Nord** — <info@friesenrat.de>, +49 4671-6024150, Friisk Hüs,
   Süderstraße 6, 25821 Bräist/Bredstedt. They own the Mooring dictionary and are named as the Mooring
   contact ([friesisch.net Kontakt](https://friesisch.net/kontakt)). Ask them about both review and
   reuse permission in the same email.
2. **Nordfriisk Instituut** — <info@nordfriiskinstituut.de>, +49 4671 6012-0, Süderstraße 30, 25821
   Bräist/Bredstedt ([Impressum](https://www.nordfriiskinstituut.eu/impressum/)). Authors of the
   grammar. Best address for orthography questions and for the `janewoore`/`januar` ruling.
3. **FriiskFunk** (Ferring Stiftung / Offener Kanal SH) —
   <https://www.oksh.de/mitmachen/senden/friiskfunk/>. They write and speak Mooring news daily. Best
   address for register questions and for how a wind or tide sentence should actually sound.
4. **Friisk Foriining** — <https://friiske.de/>. Community organisation, ~600 members, runs a
   Frisian-language autumn school. Plausible source of a volunteer proofreader.
5. **Christoph Winter, ISFAS Kiel** — <c.winter@isfas.uni-kiel.de>. The academic authority on North
   Frisian directional and compass language, and the Thesaurus contact. Worth an email specifically
   about wind-direction phrasing and about whether the Thesaurus can be consulted.

---

## Recommendations

1. **Do not scrape friesisch.net into the build.** Use the GET URL by hand, paste confirmed terms into
   the language file, and keep a `source` comment next to each string. The licensing position does not
   support redistribution of the database.
2. **Keep the citation with the string.** Whatever shape the language file takes, give every entry a
   source field. It makes review tractable and it makes the gap list above maintainable.
3. **Buy the printed Gebrauchsgrammatik** (€16.80). The free PDF is explicitly preliminary and the
   project will lean on it heavily.
4. **Send one email early**, to the Friesenrat, covering: reuse permission, a reviewer, and the
   tide-vocabulary gap. That single conversation unblocks more than any further desk research.
5. **Treat the tide-model vocabulary as a design risk, not a translation task.** There is no attested
   way to say "astronomical tide" vs "surge-corrected forecast" in Mooring. The page may need to
   express the distinction visually and with a plain sentence rather than with terminology.
