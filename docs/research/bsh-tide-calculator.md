# BSH tide calculator (`gezeiten.bsh.de`) — licence, fees, contents, cadence

Research for [issue #12](https://github.com/Commander-Cody/weather-page/issues/12). Investigated against
primary sources only: BSH's own *Entgeltverzeichnis* PDF including Anlage 2 and Anlage 4 in full, the
site's own format-description files, the site's station JSON, the site's own pages, and HTTP metadata
measured directly. Every claim below carries the URL of the source that owns it.

Live measurements were taken on **2026-08-14, roughly 20:00–22:15 CEST**. **No licence checkbox was
ticked and no tide data file was downloaded** — see [§11](#11-what-was-deliberately-not-done).

---

## Verdict — yes, this data may be republished on a free public page

**Anlage 4 permits it in one sentence, without qualification and without asking anyone.**

> „Die Nutzung der digitalen Gezeitendaten ist entgeltfrei. Dies schließt die kommerzielle Nutzung und
> Veröffentlichung mit ein. Es bedarf hierzu keiner schriftlichen Zustimmung des BSH."
>
> *"The use of the digital tide data is free of charge. This includes commercial use and publication. No
> written consent from the BSH is required for this."*
>
> — *Entgeltverzeichnis für digitale Daten des BSH*, Stand 01/26, Anlage 4, p.14
> ([PDF](https://www.bsh.de/DE/Das_BSH/Gebuehren_Preise_Liz/Gebuehren_und_Preise/_Anlagen/Downloads/Entgeltverzeichnis-digitale-Daten.pdf?__blob=publicationFile&v=22))

The door is open. **But the door does not lead where the ticket hoped.** The two stations the roster
actually wanted — `suedwesthoern` for the Wiedingharde and `st-peter-ording_bad` — are *Interpolierter
Pegel*, and BSH's own page for each says in plain words that **they carry no heights at all**. On a page
where [every height is a **deviation**](../../CONTEXT.md), a source with no heights is not a source.

What *is* on offer, and was not anticipated by the ticket, is bigger: **six roster-relevant stations that
the forecast API serves as peaks-only gauges do have a full-year astronomical curve here**, including
`westerland` — ADR-0002's single clearest case.

So: **usable, licence-clean, and it upgrades five of the ten peaks-only places — but it does not solve
the Wiedingharde, and it does not add Sankt Peter-Ording.**

---

## TL;DR — the answers the ticket asked for

| Question | Answer | Confidence |
| --- | --- | --- |
| **May it be republished on a free public page?** | **Yes.** Anlage 4 grants free use *including publication*, explicitly, with no written consent needed. | Read in full |
| **Does a fee attach?** | **No** — not to the download, not to the republishing. Fees exist only on the *bestellspezifische* order route (custom formats / early data). | Read in full |
| **Attribution required?** | **Yes, and in a prescribed form** — Anlage 2, Ziffer 5 (10). **Different from the forecast API's CC BY 4.0 line.** Needs a fourth credit line, not a tweak to the existing BSH one. | Read in full |
| **Is it CC BY 4.0?** | **No.** It is a click-through contract (AGB + Anlage 4), not an open licence. | Read in full |
| **Is it astronomical only?** | **Yes — but "astronomical" is BSH's word for *astronomy plus mean meteorological conditions*,** derived from years of gauge measurements. No surge, no live measurement. | Quoted |
| **Does it go stale?** | **No.** Per calendar year, fixed at publication, valid for the whole year. First source in the project with no meaningful **data age**. | Measured + quoted |
| **Programmatic access?** | **Yes, technically** — deterministic unauthenticated URLs, no server-side gate. **But `filebox.bsh.de/robots.txt` is `Disallow: /`.** See [§8](#8-release-cadence-and-programmatic-access). | Measured |
| **Stations in this region** | **36**, against the forecast API's 23. Not the 39 the ticket assumed. | Measured |
| **Curve availability** | **17 of 36** regionally have a curve file. **Every interpolated gauge has none.** | Measured, 36/36 probed |
| **`suedwesthoern` usable?** | **No.** HW times only — no heights, no low water. | BSH's own page |
| **`st-peter-ording_bad` usable?** | **No.** HW and NW times only — no heights. | BSH's own page |

---

## 1. The licence, read rather than summarised

The acceptance text on every station page names three documents:

> „Das **"Entgeltverzeichnis für digitale Daten des BSH"** mit den **"Allgemeinen Geschäftsbedingungen
> (AGB) zur Abgabe von digitalen Daten des BSH mit einem einfachen Nutzungsrecht" (Anlage 2)** und den
> **"Gesonderten Nutzungsbedingungen des BSH für digitale Gezeitendaten" (Anlage 4)** habe ich gelesen und
> akzeptiert."
>
> — <https://gezeiten.bsh.de/suedwesthoern>

All three are the same 14-page PDF, *Stand 01/26*, in force for digital products from 01.01.2026
([source](https://www.bsh.de/DE/Das_BSH/Gebuehren_Preise_Liz/Gebuehren_und_Preise/_Anlagen/Downloads/Entgeltverzeichnis-digitale-Daten.pdf?__blob=publicationFile&v=22), p.1). Note the URL path segment is
`Gebuehren_Preise_Liz`, not the `Gebuehren_Preise_Lizenzen` that appears in search results and on some BSH
pages — the latter 404s. The `v=` parameter is ignored; every value returns the same 331,635-byte file.

### 1a. Anlage 2 alone would forbid this outright

Anlage 2 is a restrictive internal-use contract. Its operative clause:

> „(2) **Verwendungszweck** — Die Bestellerin/der Besteller darf die Daten **ausschließlich für interne
> Zwecke**, d. h. für eigene persönliche bzw. interne geschäftliche Zwecke nutzen."
>
> *"(2) Purpose of use — The orderer may use the data **exclusively for internal purposes**, i.e. for their
> own personal or internal business purposes."*
>
> — Anlage 2, Ziffer 5 (2), p.9

and

> „(6) **Jegliche anderweitige Nutzung, die über die in Absatz (2) genannten Verwendungszwecke hinausgeht,
> bedarf der schriftlichen Zustimmung des BSH.**"
>
> *"(6) **Any other use going beyond the purposes named in paragraph (2) requires the written consent of
> the BSH.**"*
>
> — Anlage 2, Ziffer 5 (6), p.9

Read alone, that is a flat no: a public web page is not an internal purpose. This is presumably why the
ticket treated the annexes as a blocker.

### 1b. Anlage 4 overrides it, and says so

Anlage 4 opens by setting the precedence rule, then reverses the outcome:

> „Für die Nutzung von digitalen Gezeitendaten des BSH gelten die „Allgemeinen Geschäftsbedingungen (AGB)
> zur Abgabe von digitalen Daten des BSH mit einem einfachen Nutzungsrecht", **soweit hier keine speziellen
> Nutzungsbedingungen geregelt sind.**
>
> **Die Nutzung der digitalen Gezeitendaten ist entgeltfrei. Dies schließt die kommerzielle Nutzung und
> Veröffentlichung mit ein. Es bedarf hierzu keiner schriftlichen Zustimmung des BSH.**
>
> **Gezeitendaten eines Kalenderjahres dürfen erst ab dem 1. August des Vorjahres über das Internet
> (Webseiten, Apps) veröffentlicht werden.**
>
> Werden die Daten für eine Veröffentlichung durch Dritte bearbeitet, dann trägt die Bearbeiterin/der
> Bearbeiter die Verantwortung für die Richtigkeit der veränderten und anschließend veröffentlichten
> Daten."
>
> *"For the use of digital tide data of the BSH the 'General Terms and Conditions (AGB) for the supply of
> digital data of the BSH with a simple right of use' apply, **insofar as no special conditions of use are
> regulated here.**
>
> **The use of the digital tide data is free of charge. This includes commercial use and publication. No
> written consent of the BSH is required for this.**
>
> **Tide data for a calendar year may not be published on the internet (websites, apps) before 1 August of
> the preceding year.**
>
> If the data is edited by third parties for publication, then the editor bears responsibility for the
> correctness of the altered and subsequently published data."*
>
> — Anlage 4, p.14

Three things follow, and none of them are ambiguous:

1. **Publication on the open internet is expressly contemplated and expressly permitted.** Anlage 4 names
   "Webseiten, Apps" as the medium. It is not a grudging silence — it is the case the clause is *about*.
2. **Free of charge covers the use, not merely the acquisition.** „Die Nutzung … ist entgeltfrei"
   attaches to *use*, and the sentence goes on to include commercial use and publication in that.
3. **Editing for publication is anticipated.** The last paragraph does not restrict derivation; it assigns
   *responsibility for correctness* to whoever edits. The page derives, resamples and re-renders — so that
   responsibility lands on this project. Anlage 2's Ziffer 5 (3) already permits editing („Die Bestellerin/
   der Besteller darf die Daten bearbeiten (z. B. generalisieren, thematisch erweitern)", p.9).

**There is no ambiguity here worth an email.** `gezeiten@bsh.de` remains the right address if the repo
owner wants written comfort, and [§12](#12-a-question-for-gezeitenbshde-if-one-is-wanted) drafts one — but
the question of "may this be republished" is settled by the text.

### 1c. Two constraints that survive into the design

**The 1 August rule binds this project, not just BSH.** It is phrased as a restriction on the publisher,
so the page may not show 2027 tide data before 2026-08-01. Since the page's horizon is "today plus six
days", this only ever bites in the last week of July, when the following year is still months away — so in
practice it is inert. Worth a one-line comment in the job rather than a code path.

**„Die aufgrund dieses Vertrages zur Verfügung gestellten Daten dürfen in keinem Fall für Navigationszwecke
verwendet werden."** — *"The data provided under this contract may under no circumstances be used for
navigation purposes."* (Anlage 2, Ziffer 5 (2), p.9). BSH reinforces this on the download panel itself:

> „Die zum Download angebotenen Gezeitendaten werden **nicht durch Nachrichten für Seefahrer (NfS)
> korrigiert.**"
>
> *"The tide data offered for download are not corrected by Notices to Mariners (NfS)."*
>
> — <https://gezeiten.bsh.de/suedwesthoern>

The page is a weather page for looking at the Wadden Sea, not a navigation aid, so this costs nothing —
but it is a reason not to drift the water lane toward anything that reads as navigational.

---

## 2. Fees — none attach to this use

The *Entgeltverzeichnis* is a fee schedule, and it does list a price against tide predictions. **That price
belongs to a different acquisition route than the one this project would use.**

**The route that is free.** Anlage 3 is the list of *Grundversorgung* products, headed „Übersicht der
digitalen Produkte der Grundversorgung (**ohne Entgelt**)" — *without charge*. Entry 3 is
**„Digitale Gezeitendaten"**, under „Digitale Produkte verfügbar unter: www.bsh.de" (p.13). That is the
website download. Anlage 3 states that Anlage 2 and Anlage 4 govern it — which is exactly the pair the
acceptance checkbox names.

**The route that costs money.** Anlage 1, lfd. Nr. 5 „Gezeitenvorausberechnungen" (p.3):

| Sub-item | Text | Fee |
| --- | --- | --- |
| 5.1 | „Keine Standardversorgung" | — |
| 5.2 | „Bestellspezifische Versorgung — Gezeitenvorausberechnungen für einen oder mehrere Orte für die Monate Januar bis Dezember eines Jahres" | „Bereitstellungsentgelt **ab dem 6. Ort pro Jahr: 25,00 € pro Ort**" |
| 5.2 | early/provisional data | „Bereitstellungsentgelt für frühzeitige (vorläufige) Daten pro Ort und Jahr: **50,00 €** (Nutzungsbedingungen gemäß Anlage 4)" |

This is the [order form](https://formulare.bsh.de/lip/action/invoke.do?id=SV_best_gezdat_de) route, and
BSH's own start page says precisely when it applies:

> „Wünschen Sie **individuelle Gezeitendaten** (z.B. eine andere Bezugshöhe) oder brauchen Sie Daten
> **frühzeitig** für das nächste Jahr? Dann nutzen Sie bitte dieses Formular zum Bestellen. … Beachten Sie
> bitte, dass bei der Bestellung von Gezeitendaten, **die nicht den Standardformaten entsprechen**, oder
> bei **vorläufigen Daten** ein Bereitstellungsentgelt anfallen kann."
>
> — <https://gezeiten.bsh.de/>

**So: neither the download nor the republishing costs anything, as long as the standard-format files from
the station pages are used and nobody asks for next year's data early.** The 25 €/place and 50 €/place
figures are the price of *not* using the free route. Note also that even on the paid route the first five
places per year are free of the per-place charge — irrelevant here, but it shows the fee is aimed at bulk
custom orders, not at public reuse.

Two other fee tables were checked and do not apply: Tabelle 1 (hourly staff rates for
*Bereitstellungsentgelt*, 80,53 €–124,87 €/h, p.5) applies to bespoke provision; Tabelle 2
(*Entgeltfestsetzung bei Lizenzen*, pp.6–7) covers licensed *chart* products — including a web tariff of
„0,10 € per eintausend Seitenaufrufe" with a 250 € annual minimum, which would be alarming if it applied.
It does not: „Im Rahmen dieses Vertrages werden derzeit **nur Seekartendaten** lizenziert" (p.7, *"Under
this contract currently only nautical chart data is licensed"*). Tide data is not chart data, and Anlage 4
declares its use free outright.

---

## 3. Attribution — a fourth credit line, not a variation of the third

**This is the part where the tide calculator differs most sharply from the forecast API, and the answer is
that BSH tide-calculator data needs its own, differently-worded credit.**

### 3a. What is required

Anlage 4 regulates fee and publication but says nothing about attribution — so by its own precedence rule
(„soweit hier keine speziellen Nutzungsbedingungen geregelt sind"), Anlage 2's attribution clause stands:

> „**(10) Quellenhinweis** — Die Bestellerin/der Besteller sowie etwaige Dritte haben **bei jeder
> Darstellung** wie folgt auf die Datenquelle hinzuweisen: **„Datenquelle: Datensatzbezeichnung ©,
> Bundesamt für Seeschifffahrt und Hydrographie, Ort, Jahr"**."
>
> *"(10) Source reference — The orderer and any third parties must reference the data source **on every
> presentation** as follows: "Data source: dataset designation ©, Federal Maritime and Hydrographic Agency,
> place, year"."*
>
> — Anlage 2, Ziffer 5 (10), p.10

Note what this is: a **prescribed string with a prescribed shape** („wie folgt"), required **„bei jeder
Darstellung"** — on every presentation, not once in a colophon. It carries four slots: dataset name, ©,
BSH, place, year.

### 3b. How it differs from the forecast API's line

| | Forecast API (`WaterLevelForecast`) | Tide calculator (`gezeiten.bsh.de`) |
| --- | --- | --- |
| Instrument | **CC BY 4.0**, an open licence | **AGB + Anlage 4**, a click-through contract |
| Attribution form | „**The form is freely selectable**" | „**wie folgt**" — prescribed shape |
| Licence link | Required (CC BY 4.0 URL) | **Not applicable — there is no licence to link** |
| Indicate changes | Required by CC BY 4.0 | Not required; instead Anlage 4 assigns *responsibility for correctness* to the editor |
| BSH's own strapline | „Amtliche **Wasserstandsvorhersage** des Bundes gemäß §1 SeeAufG" (`properties.copyright`) | „Amtliche **Gezeitendaten** gemäß §1 SeeAufG" (site footer) |

The two straplines are genuinely different sentences from BSH itself. **Linking CC BY 4.0 next to tide data
would be a factual error** — it would claim an open licence over data that is not openly licensed, and
would tell readers they may reuse it under terms BSH has not granted.

The tide site's own footer and its station JSON give the raw material:

> „© Bundesamt für Seeschifffahrt und Hydrographie (BSH). Das BSH übernimmt für die hier angegebenen
> Informationen keine Gewähr. Amtliche Gezeitendaten gemäß §1 SeeAufG."
>
> — <https://gezeiten.bsh.de/> (footer)

> `"copyright_note": "©Bundesamt für Seeschifffahrt und Hydrographie (BSH). Das BSH übernimmt für die angegebenen Informationen keine Gewähr."`
>
> — <https://gezeiten.bsh.de/data/tides_overview.json>

### 3c. Consequence for the map's three locked credit lines

The map locks three: Open-Meteo, BSH CC BY 4.0, DWD. **Adopting the tide calculator makes it four**, and
the fourth cannot be merged into the existing BSH line because the two BSH products are under different
instruments with different obligations. Something of the shape (wording to be authored in Mooring by the
repo owner, as with the others):

> Astronoomsche tide: Datenquelle: Gezeitenvorausberechnungen ©, Bundesamt für Seeschifffahrt und
> Hydrographie, Hamburg, 2026. Das BSH übernimmt für die angegebenen Informationen keine Gewähr.

The *elements* that are mandatory: the four slots of the Anlage 2 form (dataset designation, ©, BSH, place,
year) and its presence on every presentation. Everything else is discretionary. **No CC BY link on this
line.**

One practical note: „Ort, Jahr" is most naturally read as BSH's place and the data's year — Hamburg is
BSH's tide-service seat (Bernhard-Nocht-Str. 78, 20359 Hamburg; the format description is headed
„Bundesamt für Seeschifffahrt und Hydrographie, Hamburg"), and the year is the calendar year the file is
valid for. *Inferred* — the clause does not define the slots.

---

## 4. What is actually on offer — the stations

`https://gezeiten.bsh.de/data/tides_overview.json` is a plain 38 KB JSON array of **172 gauges**
nationwide, six fields each: `station_name`, `bshnr`, `latitude`, `longitude`, `gauge_group`, `seo_id`.
Served with `ETag` and `Cache-Control: max-age=60`; `Last-Modified: Thu, 09 Jul 2026 11:33:45 GMT`.
**No `Access-Control-Allow-Origin` header** — not browser-callable cross-origin, unlike the forecast API.

`gauge_group` maps to the start-page legend, which BSH translates itself:

| `gauge_group` | German legend | English legend | Count (national) |
| :---: | --- | --- | ---: |
| 1 | „Pegel" | "Tide gauge" | 142 |
| 2 | „**Interpolierter Pegel**" | "**Interpolated station**" | 26 |
| 3 | „Ostsee-Pegel" | "Tide gauge (Baltic Sea)" | 4 |

Sources: <https://gezeiten.bsh.de/> and <https://gezeiten.bsh.de/en/>.

### 4a. The regional count is 36, not 39

Taking the same stretch of coast the forecast API calls `Nordfriesland bis Elbmündung (inkl. Helgoland)` —
from `meldorf_sperrwerk_aussenpegel` in the south to `list_west` in the north — the tide calculator carries
**36 stations against the forecast API's 23**. (A slightly wider box down to 54.05°N picks up
`trischen_west` for 37; the forecast API's own area stops at Meldorf.) **The ticket's figure of 39 could not
be reproduced** from `tides_overview.json`; 36 is the measured number.

**All 23 forecast-API stations are present here**, under the same `seo_id`. The 13 additional ones:

| `seo_id` | `bshnr` | group | lat, lon | Curve file? |
| --- | --- | :---: | --- | :---: |
| `list_west` | 616P | **2** | 55.0542, 8.4000 | no |
| `rantumdamm` | 623A | 1 | 54.8600, 8.3133 | no |
| `suedwesthoern` | 634P | **2** | 54.7964, 8.6597 | no |
| `hoernum_west` | 624A | **2** | 54.7581, 8.2744 | no |
| `langeness_nord` | 632F | 1 | 54.6656, 8.6314 | no |
| `langeness_hilligenley` | 632D | **2** | 54.6186, 8.5472 | no |
| `nordstrandischmoor` | 649A | 1 | 54.5497, 8.7978 | no |
| `holmer_siel` | 649B | 1 | 54.5283, 8.8692 | **yes** |
| `rummelloch_west` | 642C | 1 | 54.4867, 8.5528 | no |
| `suedfall_fahrwasserkante` | 653P | 1 | 54.4472, 8.7525 | no |
| `everschopsiel` | 654E | 1 | 54.4086, 8.8278 | **yes** |
| `st-peter-ording_bad` | 657P | **2** | 54.3089, 8.5781 | no |
| `blauort_norderpiep` | 666P | 1 | 54.1686, 8.6750 | no |

**Correction to the ticket:** it lists `langeness_nord`, `rantumdamm`, `nordstrandischmoor`, `holmer_siel`
and `everschopsiel` among the `gauge_group` 2 stations. They are **group 1**. The regional group-2 set is
exactly five: `list_west`, `suedwesthoern`, `hoernum_west`, `langeness_hilligenley`, `st-peter-ording_bad`.

---

## 5. The interpolated gauges are a dead end for this project

This is the finding that decides the Wiedingharde question, and it comes straight from BSH's own station
pages — no download, no acceptance, just the public page a visitor sees.

**`suedwesthoern`** (<https://gezeiten.bsh.de/suedwesthoern>) prints two notices above its table:

> „**Keine Gezeitenhöhen und Niedrigwasserangaben verfügbar, NW fällt trocken**
> Diese Vorausberechnungen wurden **im festen Zeitunterschied zu Helgoland, Binnenhafen** erstellt."
>
> *"No tide heights and no low water data available, low water falls dry. These predictions were produced
> at a **fixed time difference to Helgoland, Binnenhafen**."*

Its table has four columns — Datum, Uhrzeit, Ereignis, Phase — and **no height column at all**. Every row
is `HW`; there are no `NW` rows.

**`st-peter-ording_bad`** (<https://gezeiten.bsh.de/st-peter-ording_bad>):

> „**Keine Gezeitenhöhen verfügbar**
> Diese Vorausberechnungen wurden im festen Zeitunterschied zu **Büsum, Schleuse** erstellt."

Its table has HW *and* NW rows, but again **no height column**.

That is what „Interpolierter Pegel" means at BSH: **times only, carried across from a reference gauge by a
fixed time offset.** It is the same idea as the *Gezeitenunterschiede* published in the Gezeitentafeln for
„circa 700 weitere Orte" (<https://gezeiten.bsh.de/>).

Only the *mean* values exist for these stations — Südwesthörn publishes MHW 3,41 m / MSpHW 3,54 / MNpHW
3,23 over SKN and MHWI 12:59, „gültig für 2026" — but a mean is not a series.

**Why this is fatal here.** `CONTEXT.md` defines **deviation** as how far a high or low water sits above
or below its normal, and states that "every height on the page is a deviation". A station that publishes no
per-event height cannot produce a deviation. Südwesthörn additionally has no low water at all, so it could
not fill the peaks-only water lane either.

**`osterley` stays.** The three Wiedingharde places keep the pairing `docs/places.md` already records.
Checked directly (<https://gezeiten.bsh.de/osterley>): Osterley is group 1, its table carries the full
`Höhe über SKN [m]` column with HW and NW, and it shows no interpolation notice — it is a real gauge with
real heights. It simply has no curve file (see §6). **Nothing in `docs/places.md` needs to change for the
Wiedingharde, and the "preferred source not yet available" note against `suedwesthoern` should be closed as
*not usable*, not as *still waiting*.**

Likewise **Sankt Peter-Ording does not become a candidate.** The gap list in `docs/places.md` says it
"becomes a candidate if that product turns out to be usable" — the product is usable, but *that station*
is not.

Measured corroboration across all five regional group-2 stations, from `Content-Length` alone (HEAD
requests, no bodies retrieved), 2026 high/low-water files:

| Station | group | bytes | reading |
| --- | :---: | ---: | --- |
| `husum_schleuse`, `westerland`, `osterley`, … (28 stations) | 1 | ~122,0xx | HW+NW **with** heights |
| `groede_anleger`, `nordstrandischmoor` | 1 | ~61,4xx | **half the rows** — HW only, with heights |
| `list_west`, `hoernum_west`, `langeness_hilligenley`, `st-peter-ording_bad` | **2** | ~82,4xx | HW+NW, **shorter rows** — no heights |
| `suedwesthoern` | **2** | 41,644 | **half of that** — HW only, no heights |

The size clusters line up exactly with what the pages say, and the ~61 KB group-1 pair reveals a second
thing worth noting: **`groede_anleger` is high-water-only too.** That matches the sibling research, which
recorded `groede_anleger` returning only 2 official peaks from the forecast API where every other station
returned 4 (`docs/research/bsh-water-level-api.md`, §4). *Row-count arithmetic is inferred; the byte counts
and the two station pages are measured.*

---

## 6. The curve — what is really on offer, and where

The curve is the prize, and it is distributed on a different axis than the forecast API's split.

**Measured by HEAD request across all 36 regional stations** (existence probe only — no file bodies
retrieved), for both 2026 and 2027: **17 stations have a curve file, 19 do not.** The two years agree
station-for-station.

| | Forecast API | Tide calculator |
| --- | --- | --- |
| Stations, this coast | 23 | 36 |
| With a curve | **9** | **17** |
| Curve horizon | ~136 h, rolling | **the whole calendar year** |
| Curve content | astronomical **and** surge-corrected on a shared grid | **astronomical only** |

### 6a. The six stations that change the roster

Stations the forecast API serves as **peaks-only gauges** that *do* have a full-year astronomical curve
here:

| Station | Used by which places (`docs/places.md`) |
| --- | --- |
| `westerland` | `westerland` |
| `wyk` | `wyk` |
| `schluettsiel` | `langenhorn` (borrowed) |
| `pellworm_anleger` | `pellworm` |
| `strucklahnungshoern` | `nordstrand` |
| `meldorf_sperrwerk_aussenpegel` | — (outside the roster) |

Plus `holmer_siel` and `everschopsiel`, which are not in the forecast API at all but do carry curves.

**And the ones that stay peaks-only** — no curve file at either 2026 or 2027:

| Station | Used by which places |
| --- | --- |
| `osterley` | `klanxbuell`, `emmelsbuell-horsbuell`, `neukirchen` |
| `der_strand_hamburger_hallig` | `hamburger-hallig`, `bredstedt` |

**Net effect on the roster: five of the ten peaks-only places gain a local astronomical curve**
(`westerland`, `wyk`, `pellworm`, `nordstrand`, `langenhorn`), and five do not (the three Wiedingharde
places, `hamburger-hallig`, `bredstedt`).

`westerland` is the one that matters most. ADR-0002 chose it as the rule's clearest win precisely because
every curve gauge on Sylt is 97–128 minutes out of phase with it. Verified directly
(<https://gezeiten.bsh.de/westerland>): Westerland's table carries the full `Höhe über SKN [m]` column with
HW and NW, its Gezeitengrundwerte are published (MHW 2,43 m / MNW 0,62 m over SKN, „gültig für 2026"), and
its curve file exists. **The place that most needed a local curve can now have one.**

### 6b. Is the curve a real computed series, or interpolated between peaks?

**It is a computed series.** The clean argument is availability, and it is measured rather than asserted:

`osterley`, `munkmarsch`, `amrum_odde`, `foehrer_ley_nord`, `rantumdamm`, `langeness_nord`,
`der_strand_hamburger_hallig`, `pellworm_hoogerfaehre`, `rummelloch_west`, `suedfall_fahrwasserkante`,
`suederoogsand`, `blauort_norderpiep` and `trischen_west` are all group-1 stations publishing **full HW and
NW peaks with heights** (~122 KB files) — and **none of them has a curve file.** If the curve were an
interpolation between known peaks, BSH could produce it for every one of them at no cost. It does not.
The curve therefore requires something the peaks do not supply — a harmonic constituent set — and exists
only where BSH has performed that analysis.

The format description supports this: the E-format header field `C01 Analyse-Ber` is documented as
"method of analysis (**independent or with reference station**) **+ number of tidal constituents**"
(<https://filebox.bsh.de/index.php/s/SbJ3z5NBkpOZloY/download?path=%2F&files=format_e_english.txt>), and
the data rows carry a distinct line kind `K = Punkt auf Kurve` / "K = curve data" alongside `H` and `N`.

*What remains inferred:* that the curve rows at a given station are evaluated from constituents at each
10-minute step rather than smoothed from the peaks by BSH internally. Reading `C01` in an actual file
header would settle it — see [§11](#11-what-was-deliberately-not-done).

### 6c. Resolution and span, measured without opening a file

BSH states the curve file is „Zeiten und Höhen in **10 Minuten-Schritten**" (<https://gezeiten.bsh.de/suedwesthoern>).
That is confirmed arithmetically from `Content-Length` alone:

| File (Husum, `510P`) | bytes |
| --- | ---: |
| high/low water 2026 | 122,037 |
| high/low water 2027 | 122,123 |
| **curve 2026** | **4,642,281** |
| **curve 2027** | **4,642,367** |

The E-format is fixed-width, 86 bytes per data row including the line terminator. A full year at 10-minute
steps is 365 × 144 = **52,560 points**; the high/low-water file at 122,037 bytes works out to ~1,411 peak
rows. 52,560 + 1,411 ≈ 53,971 rows × 86 B = 4,641,506 B, plus a ~690-byte header = **4,642,196 B** against
a measured 4,642,281 — one row out. **The curve file is a whole-year 10-minute grid with the HW/NW turning
points inserted into the same series.** (That is the same shape as the forecast API's `curve`, which also
splices exact turning times into a 10-minute grid.) Note too that the 2026 and 2027 curve files differ by
exactly 86 bytes — one row — which is what a fixed-width yearly series should look like.

*This paragraph is arithmetic on measured byte counts, not a reading of file contents. It is marked
inferred, though the fit is tight enough to be relied on for sizing the job.*

**~4.6 MB per station-year, uncompressed.** For the five roster places that would take a curve, plus their
high/low-water files, that is roughly **23 MB fetched once a year**.

---

## 7. The text file format

BSH publishes one format description covering both text files, in German and English, and it is **not**
behind the acceptance checkbox — it is a separate link, and it was read in full:

- German: <https://filebox.bsh.de/index.php/s/SbJ3z5NBkpOZloY/download?path=%2F&files=format_e.txt>
- English: <https://filebox.bsh.de/index.php/s/SbJ3z5NBkpOZloY/download?path=%2F&files=format_e_english.txt>

Both dated **30.10.2023**, section „M11 Gezeiten", 7 KB, **ISO-8859 encoded** (not UTF-8 — the HTTP header
claims `charset=UTF-8` and is wrong; decode as Latin-1).

### 7a. Shape

`#`-separated, fixed-width columns, one header block then data rows, `I_E` to start and `EEE` to end.

Header fields that matter here:

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `A02 Daten-Art` | „Vorausberechnungen" (predictions) or „Beobachtungen" (observations) | **Confirms in-band that a file is prediction, not measurement** |
| `A06 GT-Jahr` | year of validity | the file's own statement of which calendar year it is |
| `A07 Def.-Jahr` | „Verwendete Wasserstandsbeobachtungen — methodisch gewähltes letztes Jahr und ggf. Gesamtzeitraum in Jahren" | which observation period the prediction was derived from |
| `A11 Zeitzone` | „gesetzliche Zeitzone des Ortes, (Normalzeit)" | e.g. `UTC+ 1h00min (MEZ)` |
| `B01 Sommerzeit` | present only „wenn die Zeiten in Sommerzeit berechnet sind" | **absent in these files — see 7c** |
| `C01 Analyse-Ber` | method + number of tidal constituents | independent vs. reference-station |
| `C03 Höhenniveau` | `PNP` \| `NHN` \| `SKN` | the datum the heights are in |
| `C05 EinheitHöhe` | `m` \| `dm` \| `cm` \| `mm` \| `ft` | **do not assume metres — read this field** |
| `D01 PNP u. NHN` | gauge zero relative to NHN [m] | |
| `D02 SKN u. NHN` | chart datum relative to NHN [m] | |
| `D03 SKN ü. PNP` | chart datum above gauge zero [m] | |
| `F01/F02 MHWI/MNWI` | mean lunitidal intervals [h:min] | |
| `G01 MHW` / `G02 MNW` | mean high / mean low water [m] | **the denominator of every deviation, in-band** |

Data row layout (columns, from the description):

| Cols | Field |
| --- | --- |
| 1–3 | `VB1` = data without heights, `VB2` = data with heights |
| 5–12 | gauge number, e.g. `DE__508P` |
| 14 | moon phase: `0` new, `1` first quarter, `2` full, `3` last quarter |
| 16 | `H` high water, `N` low water, **`K` point on the curve** |
| 18–19 | weekday |
| 21–30 | date `[Tag.Monat.Jahr]` |
| 32–36 | time `[Stunden:Minuten]` |
| 38–43 | height `[m]` |
| 45 | quality flag: `1` = „gestört (WSV)", `7` = „Ausreißer (BSH)" |
| 47–49 | day-of-year |
| 51–56 | time zone, e.g. `+ 1:00` |
| 58–64 | transit number (HW/NW only) |
| 69 | `1`–`4`: HW/NW to upper/lower transit |
| 71–84 | Julian date [days], **UTC** |

**`VB1` vs `VB2` is the machine-readable form of the interpolated-gauge problem in §5**: an interpolated
station's rows are `VB1` — no heights.

### 7b. Datum

The download panel states both text files are **`Pegelnullpunkt (PNP)`** — gauge zero — while the
*Gezeitentafel-Ansicht* PDF is `Seekartennull (SKN)` and the web table defaults to SKN
(<https://gezeiten.bsh.de/suedwesthoern>). The `C03` header field carries it per file, so read the field
rather than trusting the panel.

**This is the same datum as the forecast API**, whose values are all "in centimetres relative to the local
gauge zero" (`docs/research/bsh-water-level-api.md`, §3b) — **but the units differ: the forecast API is
centimetres, the E-format is metres** (per `C05`). Anything that mixes the two products must convert.

**A bonus worth naming.** The forecast API does *not* publish `gaugezero_relative_to_nhn` at its 14
peaks-only stations, which is why `docs/research/bsh-water-level-api.md` §2 concluded "at these stations
you cannot convert to NHN or chart datum at all". The tide calculator supplies exactly that constant, in
band, for every station: BSH's own note on the download panel says the dataset „enthält Metadaten mit
**Differenzen zwischen Pegelnullpunkt, Normalhöhennull und Seekartennull**, soweit verfügbar". **The tide
calculator closes the forecast API's datum gap** even at stations where its curve is of no use.

### 7c. Time zone — the one real hazard

Both text files are, per the download panel, **„durchgängig Standardzeit (Winterzeit, MEZ)"** — *year-round
standard time (winter time, CET)*, i.e. **UTC+1 all year, with no daylight-saving jump**. The `B01
Sommerzeit` header field, which the format description says appears „wenn die Zeiten in Sommerzeit
berechnet sind", is therefore absent.

**This is a different convention from every other source in the project.** The forecast API uses German
*legal* time with an explicit offset that switches `+02:00`/`+01:00`
(`docs/research/bsh-water-level-api.md`, §3c); the tide calculator's web table offers legal time as an
option but the *files* are fixed at MEZ. Rows do carry the offset explicitly in columns 51–56, and each row
also carries a Julian date in **UTC** (columns 71–84) — the latter is the safest join key if the project
wants to sidestep the whole question.

The four downloads and their conventions, from the panel
(<https://gezeiten.bsh.de/suedwesthoern>, English at <https://gezeiten.bsh.de/en/suedwesthoern>):

| Product | Content | Datum | Time zone |
| --- | --- | --- | --- |
| Gezeitenkalender-Ansicht (PDF) | times only | — | legal time (MESZ/MEZ) |
| Gezeitentafel-Ansicht (PDF) | times and heights | SKN | year-round MEZ |
| **Txt-Datei Hoch-/Niedrigwasser** | times and heights of HW/NW | **PNP** | year-round MEZ |
| **Txt-Datei Kurve** | **times and heights in 10-minute steps** | **PNP** | year-round MEZ |

---

## 8. Release cadence and programmatic access

### 8a. Cadence — confirmed, and it is exactly the 1 August rule

BSH states it on every station page:

> „Die Daten für das nächste Kalenderjahr stehen **etwa ab August des aktuellen Jahres** hier zum Download
> bereit."
>
> — <https://gezeiten.bsh.de/suedwesthoern>

Measured on **2026-08-14**: the **2027** files are already live (HTTP 200 for all 36 regional high/low-water
files and all 17 curve files). This is not a coincidence of timing — it is Anlage 4's rule showing through:
BSH may not publish year *Y* online before 1 August of *Y−1*, and it evidently publishes right at that
boundary.

**Only two years are hosted at a time.** Probed for `husum_schleuse`:

| Year | high/low water | curve |
| --- | :---: | :---: |
| 2023 | 404 | 404 |
| 2024 | 404 | 404 |
| 2025 | 404 | 404 |
| **2026** | **200** | **200** |
| **2027** | **200** | **200** |
| 2028 | 404 | 404 |

**Design consequence: BSH does not keep an archive.** Once 2026 rolls off, BSH's copy is gone. If the page
ever needs to render a past date, **the project's own stored copy is the only copy** — the yearly fetch is
not a convenience, it is the archive. That sits well with `CONTEXT.md`'s **last good** concept, but it
inverts the usual reasoning: last good exists here because the upstream deletes, not because the upstream
fails.

### 8b. Programmatic access — technically yes, with a robots caveat

There is **no API**, but the download URLs are fully deterministic. Read from the site's own
`common.js` (<https://gezeiten.bsh.de/gezeiten/common.js>):

```
https://filebox.bsh.de/index.php/s/SbJ3z5NBkpOZloY/download?path=/vb_hwnw/deu{YEAR}&files=DE__{BSHNR}{YEAR}.txt
https://filebox.bsh.de/index.php/s/SbJ3z5NBkpOZloY/download?path=/vb_kurv/deu{YEAR}&files=DE__{BSHNR}{YEAR}.txt
https://filebox.bsh.de/index.php/s/SbJ3z5NBkpOZloY/download?path=/vb_gtgk/deu{YEAR}&files=exgtvb_DE__{BSHNR}{YEAR}.pdf
https://filebox.bsh.de/index.php/s/SbJ3z5NBkpOZloY/download?path=/vb_gtgk/deu{YEAR}&files=exgkvb_DE__{BSHNR}{YEAR}.pdf
```

`{BSHNR}` is the `bshnr` from `tides_overview.json` left-padded to 5 chars with `_` (e.g. `634P` →
`_634P`, giving `DE__634P`).

Three things follow, and they pull in different directions:

1. **The acceptance checkbox is a client-side gate only.** `pegel.js` (<https://gezeiten.bsh.de/gezeiten/pegel.js>)
   simply appends `<a href="…">` elements when the box is checked; the URLs carry no token. Confirmed by
   HEAD request: the files answer `200 text/plain` with no acceptance step. **This does not make the terms
   optional** — Anlage 2, Ziffer 2 (1) says the contract comes about „durch die Bestellung/den Abruf **und**
   die Akzeptierung der online vorliegenden Allgemeinen Geschäftsbedingungen" (p.8). Retrieval without
   acceptance is retrieval outside the contract, and Anlage 4's permission to publish flows *from* that
   contract. **A scheduled job should be understood as acting on an acceptance the repo owner has made, not
   as a way around it.**
2. **`filebox.bsh.de/robots.txt` is `User-agent: * / Disallow: /`.** (`gezeiten.bsh.de/robots.txt` is 404 —
   no restrictions there.) A once-a-year fetch of two known URLs per station is not crawling, and robots.txt
   binds crawlers rather than user-directed retrieval — but it is a clear signal that BSH does not intend
   filebox to be machine-harvested. **This is a judgement call for the repo owner, and it is the single
   genuine reason to write to `gezeiten@bsh.de`.** See §12.
3. **There is also a per-station JSON the site itself uses** —
   `https://gezeiten.bsh.de/data/DE_{bshnr padded to 5 with _}_tides.json`, e.g.
   `https://gezeiten.bsh.de/data/DE__634P_tides.json` (HEAD: `200 application/json`). Read from `common.js`,
   it carries `years` (with `has_curve`, `has_height`, `level`), the Gezeitengrundwerte, `pegelonline_uuid`,
   and `hwnw_prediction.data` — **the high/low-water series, but not the curve**. It sits on the same host
   as the public pages, behind no checkbox, with no robots restriction. **If a scheduled job is wanted, this
   is the more defensible endpoint for peaks** — the curve remains download-only.

### 8c. What a job would look like

Once a year, some time after 1 August, for each place taking tide-calculator data:

1. `GET tides_overview.json` (38 KB, has `ETag`) to resolve `seo_id` → `bshnr`.
2. `GET` the next year's curve file (~4.6 MB) and/or high/low-water file (~122 KB) per station.
3. Parse the E-format header for `C03`/`C05`/`G01`/`G02`/`D01`, then the `K`/`H`/`N` rows.
4. Store it. **BSH will delete its copy; yours is the archive.**

No polling, no cadence tuning, no staleness threshold. A single annual job, and the rest of the year it
does nothing.

---

## 9. Staleness — the ticket's hypothesis holds

`CONTEXT.md` defines the **astronomical tide** as "a calculation, not a measurement, so it never goes
stale — a series fetched hours ago is still exactly right for days ahead". The tide calculator is the pure
case of that: a series fetched in August is exactly right for the following December.

**It is astronomical only.** BSH is explicit that the two products are different things:

> „**Die Gezeitenvorausberechnung gibt den Wasserstand an, wie er aufgrund der astronomischen Konstellation
> und unter mittleren meteorologischen Bedingungen erwartet werden kann.** … Der tatsächlich eintretende
> Wasserstand kann aufgrund des Wetters (zum Beispiel bei auf- oder ablandigem Wind) **deutlich** von der
> Gezeitenvorausberechnung abweichen. Deshalb erstellt das BSH zusätzlich vier Mal am Tag eine
> Wasserstandsvorhersage."
>
> *"The tidal prediction states the water level as it can be expected on the basis of the astronomical
> constellation and under mean meteorological conditions. … The water level that actually occurs can differ
> significantly from the tidal prediction because of the weather (for example onshore or offshore wind).
> That is why the BSH additionally produces a water level forecast four times a day."*
>
> — <https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/Gezeiten/gezeiten_node.html>

The station pages repeat it above every table: „**Aktuelle Windverhältnisse werden in den
Vorausberechnungen nicht berücksichtigt!**" — *current wind conditions are not taken into account in the
predictions* (<https://gezeiten.bsh.de/suedwesthoern>). And the file header names its own kind in band:
`A02 Daten-Art: Vorausberechnungen` vs `Beobachtungen`.

**So: no surge, no measurement. Confirmed.**

### One honest wrinkle in the glossary

`CONTEXT.md` defines the astronomical tide as "the tide predicted from **the moon and sun alone**". BSH's
own definition is narrower in one direction and wider in another: *astronomical constellation* **and under
mean meteorological conditions**, with the constants derived from real gauge measurements —

> „Wie die Gezeiten an einem bestimmten Ort genau verlaufen, hängt neben der Astronomie auch wesentlich von
> der Gestalt und der Tiefe des Meeres ab. … **Eine gute Gezeitenvorausberechnung basiert deshalb auch auf
> den Pegelmessungen der Wasserstände aus den vergangenen Jahren.**"
>
> — <https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/Gezeiten/gezeiten_node.html>

This does not change the staleness conclusion at all — the calculation is still fixed for the year and
still carries no weather of the day. But "moon and sun alone" is not quite what BSH computes, and the
glossary entry may be worth a one-word softening if the repo owner cares about precision. **The property
the project relies on — never goes stale — is intact.**

### Data age, precisely

The data age of a tide-calculator series is not zero and not meaningless: it is **the time since BSH
generated the file**, recorded in band in `A01 Hersteller` (the format description's example shows
`M1103/BSH-Hamburg, 26.06.2018 09:59:01` for the 2019 file — generated roughly six months before the year
it covers). By the end of a calendar year that age is around 18 months. **But no staleness threshold should
be set against it**, because the quantity does not degrade: `CONTEXT.md` says the staleness threshold is
"set at that source's normal worst-case data age plus one missed publication", and here a missed
publication is an annual, not a daily, event. The honest treatment is that this source has **no staleness
threshold** — the first such source in the project — and that what needs monitoring instead is *whether
next year's file arrived*, checked once, some time after 1 August.

---

## 10. What this means for the roster

**Not designed here — ADR-0002's re-pairing is a later ticket.** Stated only so the later ticket starts
from measured facts.

The door the ticket asked about is open: a **local astronomical tide from the tide calculator paired with a
borrowed surge from the nearest forecast gauge** is licence-clean, fee-free and technically available. It
would serve ADR-0002's local-data-wins rule better than either product alone, because the thing being
borrowed changes character — instead of borrowing a neighbour's *whole curve* (and with it a high-water
time that can be two hours wrong at Westerland), only the *surge* is borrowed, while the timing and shape
stay local.

The concrete effect, measured:

| Place | Current | With the tide calculator |
| --- | --- | --- |
| `westerland` | peaks-only | **local astronomical curve** |
| `wyk` | peaks-only | **local astronomical curve** |
| `pellworm` | peaks-only | **local astronomical curve** |
| `nordstrand` | peaks-only | **local astronomical curve** |
| `langenhorn` | peaks-only (borrows `schluettsiel`) | **astronomical curve at `schluettsiel`** |
| `hamburger-hallig`, `bredstedt` | peaks-only | unchanged — `der_strand_hamburger_hallig` has no curve |
| `klanxbuell`, `emmelsbuell-horsbuell`, `neukirchen` | peaks-only | unchanged — `osterley` has no curve |

**Five of ten peaks-only places gain a local astronomical curve; five do not.** The peaks-only water lane
that ADR-0002 called "a first-class case to design, not an edge case to tolerate" stays first-class — it
just covers a quarter of the roster instead of half.

Three consequences the later ticket will have to weigh, flagged and not resolved:

- **ADR-0002's "the astronomical curve has to be interpolated at peaks-only places" stops being true at
  five of them.** At those five the drawn line would be BSH's, not ours. At the other five it stays ours.
  The ADR's consequence list would need amending.
- **A place drawing a tide-calculator curve is drawing two products fused.** The astronomical tide from one
  source, the surge borrowed from another, on one axis. `docs/places.md` would need a field saying where
  the astronomical tide comes from, separately from `gauge` — and the attribution in §3c has to appear
  wherever that is shown.
- **The units and time zone differ between the two products** (§7b, §7c). Any fusion converts m↔cm and
  reconciles fixed MEZ against switching legal time.

---

## 11. What was deliberately not done

Per the ticket's hard limits:

- **The licence acceptance checkbox was never ticked.** All licence text was read from the published PDF,
  which requires no acceptance.
- **No tide data file was downloaded.** Existence, size and content type of the yearly `.txt` files were
  established by **HTTP HEAD requests, which transfer no body**. This is stated plainly because it is the
  method behind several numbers above.
- **No email was sent.** A draft is in §12 for the repo owner.
- The **format-description files were downloaded and read in full** — they are documentation, sit outside
  the acceptance checkbox as a separate link, and the ticket asked for them.
- The public station pages were **viewed as a visitor**, which is how §5's decisive quotes were obtained.
  No acceptance and no download is involved in viewing them.

### What a download would settle

Two facts remain inferred rather than read, and both would be settled by **one file: the 2026 curve file
for a single station, e.g. `husum_schleuse`** —
`.../download?path=/vb_kurv/deu2026&files=DE__510P2026.txt`, 4,642,281 bytes:

1. **`C01 Analyse-Ber`** — whether the curve station is analysed „selbständig" and with how many tidal
   constituents. This confirms §6b's conclusion that the curve is computed rather than smoothed.
2. **The exact row inventory** — that the file really is a 10-minute grid with `K` rows plus `H`/`N` rows,
   and that `C05` is metres. §6c derives this from byte arithmetic; reading the first 50 lines would prove
   it.

Both are header-and-first-page facts. **Neither is load-bearing for the verdict** — the licence answer, the
fee answer, the attribution answer, the station inventory, the curve availability map and the staleness
answer are all established without them. **This is a decision for the repo owner**, and the acceptance it
requires is a decision only the repo owner can make.

---

## 12. A question for `gezeiten@bsh.de`, if one is wanted

Not needed for the licence — Anlage 4 is clear. **The one genuinely open question is §8b's robots.txt
conflict**, which no document resolves. Drafted for the repo owner to send, or not:

> Betreff: Automatisierter jährlicher Abruf der Gezeitenvorausberechnungen
>
> Sehr geehrte Damen und Herren,
>
> ich betreibe eine kleine, kostenfreie, nicht-kommerzielle Webseite mit Wetter- und Wasserstandsdaten für
> einige nordfriesische Orte und möchte Ihre Gezeitenvorausberechnungen (Txt-Dateien Kurve und
> Hoch-/Niedrigwasser) dort veröffentlichen. Die Bedingungen der Anlagen 2 und 4 des Entgeltverzeichnisses
> habe ich gelesen und akzeptiere sie; die Quellenangabe nach Anlage 2, Ziffer 5 (10) wird auf jeder
> Darstellung erscheinen.
>
> Zwei Fragen:
>
> 1. Ich würde die Dateien einmal jährlich automatisiert abrufen (etwa 20 Dateien, einmal im Jahr nach dem
>    1. August). Die robots.txt auf `filebox.bsh.de` untersagt allerdings jeglichen automatisierten Zugriff.
>    Ist ein solcher jährlicher Abruf in Ihrem Sinne, oder bevorzugen Sie den manuellen Download über die
>    Pegelseiten?
> 2. Gibt es eine dokumentierte, für den maschinellen Zugriff vorgesehene Schnittstelle für die
>    Gezeitendaten, vergleichbar der `WaterLevelForecast`-API?
>
> Vielen Dank und freundliche Grüße

---

## 13. Open questions not answerable from primary sources

Stated explicitly rather than guessed:

1. **Whether the 17-station regional curve set is stable year to year.** Measured for 2026 and 2027, which
   agree exactly. Two years is not a guarantee.
2. **Whether `filebox.bsh.de`'s `Disallow: /` is intended to cover a once-yearly targeted fetch.** No BSH
   document addresses it. §12 drafts the question.
3. **`C01 Analyse-Ber` and the constituent count** — see §11.
4. **What „Ort, Jahr" means in the Anlage 2 attribution string.** Hamburg and the data year is the natural
   reading and matches the format description's own header; the clause does not define the slots.
5. **Whether `/data/DE_*_tides.json` is a supported interface or an internal detail.** It is undocumented,
   read from the site's own JavaScript, and could change without notice.
6. **Whether the per-station JSON exposes the curve.** It exposes `has_curve` as a flag and
   `hwnw_prediction.data` as a series; the curve appears to be download-only. *Inferred from `pegel.js`,
   which renders only a peaks table and uses `has_curve` solely to decide whether to show a download link.*
7. **Any uptime or availability commitment.** None found, as with the forecast API. The only operational
   statement is the „etwa ab August" cadence.
8. **Whether BSH ever revises a published year's file in place.** No `Last-Modified` is served by filebox,
   so a job cannot detect a revision by header alone. `A01 Hersteller` inside the file carries the
   generation timestamp.

---

## Sources

Primary, all consulted directly:

- **BSH, *Entgeltverzeichnis für digitale Daten des BSH*, Stand 01/26, 14 pp.** — <https://www.bsh.de/DE/Das_BSH/Gebuehren_Preise_Liz/Gebuehren_und_Preise/_Anlagen/Downloads/Entgeltverzeichnis-digitale-Daten.pdf?__blob=publicationFile&v=22>
  (Anlage 1 pp.2–4; Tabelle 1 p.5; Tabelle 2 pp.6–7; **Anlage 2 pp.8–11**; Anlage 3 p.13; **Anlage 4 p.14**;
  Anlage 5 p.14)
- BSH, *Beschreibung des BSH E-Format*, 30.10.2023 (German) — <https://filebox.bsh.de/index.php/s/SbJ3z5NBkpOZloY/download?path=%2F&files=format_e.txt>
- BSH, *description of BSH E-Format*, 30.10.2023 (English) — <https://filebox.bsh.de/index.php/s/SbJ3z5NBkpOZloY/download?path=%2F&files=format_e_english.txt>
- Tide calculator start page (legend, licence pointer, order form) — <https://gezeiten.bsh.de/> and <https://gezeiten.bsh.de/en/>
- Station pages, viewed as a visitor — <https://gezeiten.bsh.de/suedwesthoern>, <https://gezeiten.bsh.de/st-peter-ording_bad>, <https://gezeiten.bsh.de/westerland>, <https://gezeiten.bsh.de/osterley>
- Station inventory — <https://gezeiten.bsh.de/data/tides_overview.json>
- Site JavaScript (download URL patterns, per-station JSON endpoint, checkbox behaviour) — <https://gezeiten.bsh.de/gezeiten/common.js>, <https://gezeiten.bsh.de/gezeiten/pegel.js>
- BSH, "Gezeiten" topic page (prediction vs forecast, Gezeitengrundwerte, Bezugshöhen) — <https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/Gezeiten/gezeiten_node.html>
- BSH custom tide data order form — <https://formulare.bsh.de/lip/action/invoke.do?id=SV_best_gezdat_de>
- `robots.txt` — <https://filebox.bsh.de/robots.txt> (`Disallow: /`), <https://gezeiten.bsh.de/robots.txt> (404)

Repo context: [`CONTEXT.md`](../../CONTEXT.md),
[ADR-0002](../adr/0002-local-gauge-data-wins-over-a-borrowed-curve.md),
[`docs/places.md`](../places.md), [`docs/research/bsh-water-level-api.md`](bsh-water-level-api.md).

Contact of record for this product: Gezeitendienst, `gezeiten@bsh.de`, Karina Stockmann,
+49 40 3190-31100 (<https://gezeiten.bsh.de/>).
