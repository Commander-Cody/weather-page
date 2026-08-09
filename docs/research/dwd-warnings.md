# DWD warnings: which source, and the closed lists to translate

Research for [issue #4](https://github.com/Commander-Cody/weather-page/issues/4). All endpoint checks were
performed live on **2026-08-09** between 16:17 and 16:35 UTC, from a plain `curl` with an
`Origin:` request header set to a foreign origin. Every header quoted below is copied from a real
response.

---

## 1. Verdict up front

**Recommended source: Bright Sky `/alerts` (`https://api.brightsky.dev/alerts`).**

**CORS verdict: the browser-fetch decision survives.** Three of the four candidates send
`Access-Control-Allow-Origin: *`. Only the official Open Data ZIP archive does not — and that is the
one option that was already awkward in a browser for other reasons. Live client-side warnings as
locked in [#1](https://github.com/Commander-Cody/weather-page/issues/1) do **not** need to be
reopened, and warnings do **not** have to move into the scheduled job.

There is also a **fourth candidate that the ticket did not list**, and it matters: DWD publishes a
plain JSON warnings feed on `www.dwd.de` that is *documented in DWD's own product overview* and
*does* send open CORS. It is the recommended fallback.

---

## 2. CORS, verified empirically

| # | Source | URL | `Access-Control-Allow-Origin` | Browser-fetchable? |
|---|--------|-----|-------------------------------|--------------------|
| 1 | DWD Open Data CAP | `https://opendata.dwd.de/weather/alerts/cap/…` | **absent** | **No** |
| 2 | WarnWetter app bucket | `https://app-prod-static.warnwetter.de/v16/warnings.json` | `*` | Yes |
| 3 | Bright Sky | `https://api.brightsky.dev/alerts` | `*` | Yes |
| 4 | DWD warnapp JSON | `https://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json` | `*` | Yes |

Raw evidence:

```
$ curl -s -D - -o /dev/null -H "Origin: https://example.com" \
    https://opendata.dwd.de/weather/alerts/cap/COMMUNEUNION_DWD_STAT/
HTTP/1.1 200 OK
Server: nginx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
            <- no Access-Control-Allow-Origin anywhere in the response

$ curl -s -D - -o /dev/null -H "Origin: https://example.com" \
    "https://api.brightsky.dev/alerts?lat=54.4858&lon=9.0576"
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Server: uvicorn

$ curl -s -D - -o /dev/null -H "Origin: https://example.com" \
    https://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, GET
Server: Apache

$ curl -s -D - -o /dev/null -H "Origin: https://example.com" \
    https://app-prod-static.warnwetter.de/v16/warnings.json
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, HEAD
Access-Control-Max-Age: 3000
```

Bright Sky's CORS is not an accident of hosting — it is configured in the application. The public
instance runs FastAPI's `CORSMiddleware` with `allow_origins=["*"]`
([`brightsky/web/app.py`](https://github.com/jdemaeyer/brightsky/blob/master/brightsky/web/app.py)).

All four are keyless. None requires an API key today, so the secrets rule from #1 (a keyed source
cannot be fetched client-side) is not triggered by any of them.

---

## 3. The candidates compared

### 3.1 Candidate 1 — DWD Open Data CAP (`opendata.dwd.de/weather/alerts/cap/`)

The authoritative product. Twelve product directories exist, crossing three axes: location grain
(`COMMUNEUNION` = municipalities, `DISTRICT` = districts), update logic (`DWD` = DWD rules,
`CELLS`/`EVENT` = neutral rules), and payload (`STAT` = full current state, `DIFF` = changes only)
— per the [Produktüberblick DWD Warnungen](https://www.dwd.de/DE/leistungen/opendata/help/warnungen/dwd_warnings_products_overview_de_pdf.pdf?__blob=publicationFile&v=7).

Measured from the live directory listing of `COMMUNEUNION_DWD_STAT` on 2026-08-09:

- **Freshness**: 303 German-language snapshots over 47.8 hours; median gap between snapshots
  **10.6 minutes**, max 10.9 minutes, with extra off-cycle files when warnings change. A
  `…_LATEST_…` alias always points at the newest.
- **Retention**: ~48 hours of history.
- **Format**: a ZIP per snapshot containing one CAP 1.2 XML file per alert. The snapshot fetched at
  16:30 UTC was 288 KB and held 83 XML files. Consuming this in a browser means downloading ~290 KB,
  unzipping it, and parsing 83 XML documents — for one town. It is the whole of Germany every time.
- **Languages**: DE, EN, FR, ES, and a MUL bundle that adds Arabic, Russian, Turkish and Polish.
- **CORS**: none. **This kills it for client-side use.**

Verdict: correct, complete, official — and unusable directly from the browser. It remains the
*upstream* of the recommended option.

### 3.2 Candidate 2 — WarnWetter app static bucket

`https://app-prod-static.warnwetter.de/v16/warnings.json` and `…/warnings_nowcast.json`.

- **Freshness**: excellent. Response headers carry `x-amz-meta-cache: max-age=30` and an explicit
  `x-amz-meta-next-refresh` 5 minutes ahead of `Last-Modified` (observed: `Last-Modified: …16:30:34`,
  `x-amz-meta-next-refresh: …16:35:33`).
- **CORS**: open (`Access-Control-Allow-Origin: *`).
- **Size**: `warnings.json` was 114 KB, `warnings_nowcast.json` 22 KB — again, all of Germany.
- **Format**: `warnings.json` is a map of WarnCellID → array of warnings; `warnings_nowcast.json` is
  a flat array carrying full `polygonGeometry` coordinate rings.
- **Stability**: this is the weak point, and it is visible in the data. The path is version-pinned
  at `/v16/`, which by itself records fifteen prior breaking iterations. The payload carries
  app-internal fields — `bn`, `triangles`, `svgPolygon`, `isVorabinfo`, `binnenSee`,
  `instructionHtml` — plus headers `x-amz-meta-minimum-api-version` and `x-amz-meta-backoff`. This
  is a private contract between DWD's servers and DWD's app. It is not described in any DWD
  document, and nothing obliges it to keep working.
- **Decisive defect**: **no CAP event code.** Warnings carry only `type` and `level`, an
  undocumented coarse recoding. Observed live: `(type 0, level 2) GEWITTER`, `(0,3) STARKES
  GEWITTER`, `(1,2) WINDBÖEN`, `(1,3) STURM`. `type` collapses ~52 CAP event codes into a handful of
  phenomenon buckets, and `level` is not CAP severity. Keying a translation table off this means
  keying off the German `event` *string*, with no stable numeric identity behind it.
- **Licence**: no copyright field in the payload at all.

Verdict: fast and CORS-clean, but undocumented, unstable by design, and it throws away the very
numeric vocabulary this project needs to translate.

### 3.3 Candidate 3 — Bright Sky `/alerts` (recommended)

- **Upstream**: Bright Sky ingests exactly one alerts source,
  `https://opendata.dwd.de/weather/alerts/cap/COMMUNEUNION_DWD_STAT/` — stated both in its OpenAPI
  description (`https://api.brightsky.dev/openapi.json`, "Data Sources" → "Alerts") and in the
  poller source ([`brightsky/polling.py` line 21](https://github.com/jdemaeyer/brightsky/blob/master/brightsky/polling.py)).
  So this is candidate 1, re-served as JSON with CORS.
- **Freshness**: measured, not assumed. The CAP snapshot published at 16:30 UTC contained alert
  `2.49.0.0.276.0.DWD.PVW.1786292040000.eb132795-…` with `effective` 16:14 UTC; querying Bright Sky
  at 16:35 UTC for one of that alert's cells (`809574464`) returned the same alert with the same
  `effective`. Lag from CAP publication to API availability was under five minutes.
- **Format**: flat JSON. One request per place, ~200 bytes when there is nothing to report:

  ```json
  {"alerts":[],"location":{"warn_cell_id":801054056,"name":"Stadt Husum",
   "name_short":"Stadt Husum","district":"Nordfriesland",
   "state":"Schleswig-Holstein","state_short":"SH"}}
  ```

- **It preserves the closed vocabulary.** A live alert returns `"event_code": 51`,
  `"event_de": "WINDBÖEN"`, `"event_en": "wind gusts"`, `"severity": "minor"`, `"urgency":
  "immediate"`, `"certainty": "likely"`, `"response_type": "prepare"`, `"category": "met"`,
  `"status": "actual"`. `event_code` is the CAP `<eventCode><valueName>II</valueName>` value read
  straight out of the XML
  ([`dwdparse` `CAPParser._parse_event_code`](https://github.com/jdemaeyer/dwdparse/blob/master/dwdparse/parsers.py)),
  and `event_de`/`event_en` are DWD's own `<event>` strings from the German and English CAP files —
  Bright Sky does not invent labels. **This is the single most important property for this
  project**: the Frisian table can be keyed on a stable integer, not on a German string.
- **Parameters**: `lat`+`lon`, or `warn_cell_id`, plus `tz`. Municipality cells only; district cell
  IDs are rejected with `{"detail":"Unknown warn_cell_id, please use commune (Gemeinden), not
  district (Landkreis) ids"}` (verified against `501000005`).
- **Licence of the software**: MIT (`openapi.json` → `info.license`). The *data* stays DWD's; the
  OpenAPI intro states "the DWD's Terms of Use apply to all data you retrieve through the API".
- **Cost/keys**: "The public instance at `https://api.brightsky.dev/` is free-to-use for all
  purposes, **no API key required**". No rate-limiting middleware exists in the web application
  source.
- **Risk**: a single volunteer maintainer (Jakob de Maeyer) in the critical path of a page whose
  whole point is safety-relevant warnings. This is real and is addressed in §8.

### 3.4 Candidate 4 — DWD warnapp JSON (not in the ticket; the fallback)

`https://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json`

This deserves to be on the list because the ticket's framing of "official but awkward" vs
"convenient but undocumented" has a third case. This endpoint is **listed as an official DWD product**
in section 2 ("JSON — Hochaktueller Landkreis-Status ohne Geometrien") of the
[Produktüberblick DWD Warnungen](https://www.dwd.de/DE/leistungen/opendata/help/warnungen/dwd_warnings_products_overview_de_pdf.pdf?__blob=publicationFile&v=7),
*and* it sends `Access-Control-Allow-Origin: *`.

- **Freshness**: two samples 13 minutes apart were each fresh to within ~2 minutes of the request
  (`Last-Modified: …16:18:40` with payload `time` 16:18:36; `Last-Modified: …16:31:45` with payload
  `time` 16:31:41).
- **Format wart**: it is JSONP, not JSON, despite `Content-Type: application/json`. The body is
  `warnWetter.loadWarnings({…})`. A browser must fetch it as text and strip the wrapper.
- **Size**: 190 KB — all of Germany, every load.
- **Grain**: districts, not municipalities. Keys observed were type-1 (Landkreise, e.g.
  `108326000`), type-9 (district aggregations, e.g. `909671999` "Kreis und Stadt Aschaffenburg") and
  type-2 (lakes). **Coarser than Bright Sky.**
- **Same defect as candidate 2**: `type`/`level` only, no CAP `ii` event code.
- **Attribution**: the payload carries `"copyright": "Copyright Deutscher Wetterdienst"`.
- A municipality-grain sibling exists at
  `https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde.json` (also
  `Access-Control-Allow-Origin: *`, 191 KB, same JSONP wrapper). It is **not** in the product
  overview, so it has the documentation status of candidate 2 with the hosting of candidate 4.

---

## 4. How a warning is scoped to a place

### 4.1 The WarnCellID scheme

Warnings are scoped by **WarnCellID**, carried in CAP as
`<area><geocode><valueName>WARNCELLID</valueName>`. Section 3.6 of the
[CAP DWD profile v2.1.13](https://www.dwd.de/DE/leistungen/opendata/help/warnungen/cap_dwd_profile_de_pdf_2_1_13.pdf?__blob=publicationFile&v=3)
defines the structure as:

```
<WarncellID-Typ Präfix><achtstelliger Amtlicher Gemeindeschlüssel (AGS)>
```

That is: one type-prefix digit followed by the 8-digit German official municipality key. Documented
types (profile §3.6.1):

| Prefix | Meaning | Profile's own example |
|--------|---------|------------------------|
| 1 | Landkreise (LAND) | `109187000` Kreis Rosenheim |
| 2 | Seen (LAKE), Seenzusammenfassungen (LAKE-SUM) | `208438000` Bodensee – Mitte |
| 3 | — | — |
| 4 | Seegebiete (SEA) | `401000003` Südwestliche Nordsee |
| 5 | Küstengebiete (COAST) | `501000002` Helgoland |
| 6 | Kundenspezifische Objekte (OBJECT) | `614729000` Obstland Liptitz-Grauschwitz |
| 7 | Stadt-Unterteilungen (QUARTER) | `706412102` Frankfurt-Süd |
| 8 | **Gemeinden (COMMUNE)** | `807232134` Gemeinde Wiersdorf |
| 9 | Bundesländer (STATE), Zusammenfassungen (AGGREGATION/DISTRICTAREA), Landkreis-Unterteilungen (REGION), … | **`901054001` Kreis Nordfriesland – Binnenland** |

The profile's own worked example for a type-9 REGION cell is Nordfriesland's inland half. Its
counterpart `901054002` is "Kreis Nordfriesland – Küste".

The full catalogue is a DWD CSV,
[`cap_warncellids_csv.csv`](https://www.dwd.de/DE/leistungen/opendata/help/warnungen/cap_warncellids_csv.csv?__blob=publicationFile&v=3)
(581 KB, `WARNCELLID;NAME;KURZNAME;CCC;BL`, 11,828 rows). Counted by prefix: 401 type-1, 25 type-2,
20 type-4, 8 type-5, 245 type-7, **10,997 type-8**, 132 type-9. Nordfriesland alone has 133
municipality cells, plus `101054000` (Kreis) and the two type-9 halves.

Geometry, if ever needed, is on the DWD GeoServer — and it too is CORS-open
(`Access-Control-Allow-Origin: *` verified):

```
https://maps.dwd.de/geoserver/wfs?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature
  &TYPENAMES=Warngebiete_Gemeinden&OUTPUTFORMAT=json
```

### 4.2 Mapping a curated place to its key

Bright Sky resolves lat/lon to a municipality cell server-side, so the pairing can be done **once,
by hand, at build time** — exactly the model already used for BSH tide gauges in #1. Each curated
place gets a hard-coded `warn_cell_id` in its config; the runtime call is then
`GET /alerts?warn_cell_id=…`, which avoids depending on Bright Sky's point-in-polygon lookup at
request time.

Verified resolutions (live, 2026-08-09):

| Place | Query | Resolved cell | `name` |
|-------|-------|---------------|--------|
| Husum | `lat=54.4858&lon=9.0576` | `801054056` | Stadt Husum |
| Amrum (south) | `lat=54.6303&lon=8.3833` | `801054160` | Gemeinde Wittdün auf Amrum |
| Amrum (north) | `lat=54.6919&lon=8.3167` | `801054089` | Gemeinde Norddorf auf Amrum |

**An island is not one cell.** Amrum is three municipalities (Wittdün, Nebel, Norddorf); Sylt is
five (`801054046` Hörnum, `801054061` Kampen, `801054078` List, `801054149`
Wenningstedt-Braderup, `801054168` Sylt). Föhr, Pellworm (`801054103`), Nordstrand
(`801054091`), Hallig Hooge (`801054050`) and Sankt Peter-Ording (`801054113`) are likewise
separate cells. For each curated place the owner must pick **which** municipality is meant — that is
a curation decision, not a lookup. In practice DWD warnings for wind cover a whole island at once,
so one representative cell per place is a defensible simplification, but it should be a recorded
choice rather than an accident.

### 4.3 What the municipality product does *not* contain

This matters for a coastal audience. The `COMMUNEUNION` product carries land cells only. Inspecting
the 16:30 UTC snapshot, all 5,183 WarnCellID references were prefix 8 (5,084), prefix 7 (94) or
prefix 2 (5). **No prefix-5 coastal cells, no prefix-4 sea areas.** Bright Sky rejects them outright.

Consequence: the page will show land warnings for the town — including `57 STARKWIND` and
`58 STURM`, which *are* in the land list and were observed live — but it will **not** show the
separate **Küsten-Warnungen** (`11 BÖEN`, `12 WIND`, `13 STURM`) issued for `501000005`
"Nordfriesische Küste", nor Hochsee warnings for the Deutsche Bucht. For a page aimed at people
deciding what to do on the coast today, this is a real gap, and it is a gap in *all four
candidates*, since none of the JSON feeds carries prefix-5 cells either. Worth a follow-up ticket;
it does not change the choice of source.

---

## 5. Storm surge (*Sturmflut*) — not DWD

**DWD does not issue storm surge warnings.** The proof is the event list itself (§6 below): across
all 52 warning codes, 7 pre-alert codes, 3 coastal codes, 3 high-seas codes and 3
medical-meteorological codes, there is no water-level event of any kind. DWD's coastal codes are
wind only.

Storm surge is the **BSH** (Bundesamt für Seeschifffahrt und Hydrographie), acting under
**Seeaufgabengesetz § 1 Absatz 9**
([bsh.de](https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/wasserstand_und_gezeiten_node.html)).
Its published North Sea classes
([bsh.de → Sturmfluten](https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/Sturmfluten/sturmfluten_node.html)):

| Class | Threshold |
|-------|-----------|
| **Sturmflut** | 1,5 bis 2,5 m über mittlerem Hochwasser (MHW) |
| **Schwere Sturmflut** | 2,5 bis 3,5 m über MHW |
| **Sehr schwere Sturmflut** | mehr als 3,5 m über MHW |

These three strings, plus the two low-water counterparts visible in BSH's own asset names
(`station-niedrigwasser`, `station-schweres-niedrigwasser`,
`station-sehr-schweres-niedrigwasser`, `station-niedriger-wasserstand`,
`station-erhoehter-wasserstand` on `wasserstand.bsh.de`), are a **second closed list** that will
need translating. They belong to the water-level ticket, not this one, but they should not be
forgotten.

Useful detail for that ticket, gathered in passing: BSH's own front-end reads
`https://wasserstand.bsh.de/data/nordsee/map.json` — which sends **no** CORS header — but the
payload's own `information_text` points automated consumers at the official API
`https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast`, and **that one does** send
`Access-Control-Allow-Origin: *`. The `map.json` payload also carries a `global_warning` field
(currently `"Wasserstandsvorhersage"`) which is where a storm-surge headline would appear.

---

## 6. The closed lists — literal and complete

Source for everything in this section: **CAP DWD Profil v2.1.13, 12.09.2022**, sections 3.1 and
2.2.2.6 —
<https://www.dwd.de/DE/leistungen/opendata/help/warnungen/cap_dwd_profile_de_pdf_2_1_13.pdf?__blob=publicationFile&v=3>

> These are DWD's German strings, reproduced verbatim, including capitalisation. **No Frisian
> translation is attempted here** — per #1 the repo owner writes and owns the Mooring text.
>
> The list is not frozen for all time. Between v2.1.12 and v2.1.13 DWD *removed* `24 GERINGFÜGIGE
> GLÄTTE`, *added* `86 EXTREMES GLATTEIS`, and *renamed* both `84` (GLÄTTE → GERINGE GLÄTTE) and
> `87` (VERBREITET GLÄTTE → GLÄTTE). A translation keyed on `event_code` must therefore tolerate an
> unknown code, and the fallback for an unknown code must not be silence.

### 6.1 Warnereignisse — Warnungen (profile §3.1.1)

52 codes.

| ii | `<event>` |
|----|-----------|
| 22 | FROST |
| 31 | GEWITTER |
| 33 | STARKES GEWITTER |
| 34 | STARKES GEWITTER |
| 36 | STARKES GEWITTER |
| 38 | STARKES GEWITTER |
| 40 | SCHWERES GEWITTER mit ORKANBÖEN |
| 41 | SCHWERES GEWITTER mit EXTREMEN ORKANBÖEN |
| 42 | SCHWERES GEWITTER mit HEFTIGEM STARKREGEN |
| 44 | SCHWERES GEWITTER mit ORKANBÖEN und HEFTIGEM STARKREGEN |
| 45 | SCHWERES GEWITTER mit EXTREMEN ORKANBÖEN und HEFTIGEM STARKREGEN |
| 46 | SCHWERES GEWITTER mit HEFTIGEM STARKREGEN und HAGEL |
| 48 | SCHWERES GEWITTER mit ORKANBÖEN, HEFTIGEM STARKREGEN und HAGEL |
| 49 | SCHWERES GEWITTER mit EXTREMEN ORKANBÖEN, HEFTIGEM STARKREGEN und HAGEL |
| 51 | WINDBÖEN |
| 52 | STURMBÖEN |
| 53 | SCHWERE STURMBÖEN |
| 54 | ORKANARTIGE BÖEN |
| 55 | ORKANBÖEN |
| 56 | EXTREME ORKANBÖEN |
| 57 | STARKWIND |
| 58 | STURM |
| 59 | NEBEL |
| 61 | STARKREGEN |
| 62 | HEFTIGER STARKREGEN |
| 63 | DAUERREGEN |
| 64 | ERGIEBIGER DAUERREGEN |
| 65 | EXTREM ERGIEBIGER DAUERREGEN |
| 66 | EXTREM HEFTIGER STARKREGEN |
| 70 | LEICHTER SCHNEEFALL |
| 71 | SCHNEEFALL |
| 72 | STARKER SCHNEEFALL |
| 73 | EXTREM STARKER SCHNEEFALL |
| 74 | SCHNEEVERWEHUNG |
| 75 | STARKE SCHNEEVERWEHUNG |
| 76 | EXTREM STARKE SCHNEEVERWEHUNG |
| 79 | LEITERSEILSCHWINGUNGEN |
| 82 | STRENGER FROST |
| 84 | GERINGE GLÄTTE |
| 85 | GLATTEIS |
| 86 | EXTREMES GLATTEIS |
| 87 | GLÄTTE |
| 88 | TAUWETTER |
| 89 | STARKES TAUWETTER |
| 90 | GEWITTER |
| 91 | STARKES GEWITTER |
| 92 | SCHWERES GEWITTER |
| 93 | EXTREMES GEWITTER |
| 95 | SCHWERES GEWITTER mit EXTREM HEFTIGEM STARKREGEN und HAGEL |
| 96 | EXTREMES GEWITTER mit ORKANBÖEN, EXTREM HEFTIGEM STARKREGEN und HAGEL |
| 98 | TEST-WARNUNG |
| 99 | TEST-UNWETTERWARNUNG |

### 6.2 Vorabinformation Unwetter (profile §3.1.2)

7 codes. Note these **reuse** ii values from §6.1 — `40`, `55`, `65`, `75`, `85`, `89`, `99` — with
different text. They are distinguished by `<urgency>Future</urgency>`, **not** by the code. Any
lookup keyed on `event_code` alone will mislabel a pre-alert unless it also reads `urgency`.

| ii | `<event>` |
|----|-----------|
| 40 | VORABINFORMATION SCHWERES GEWITTER |
| 55 | VORABINFORMATION ORKANBÖEN |
| 65 | VORABINFORMATION HEFTIGER / ERGIEBIGER REGEN |
| 75 | VORABINFORMATION STARKER SCHNEEFALL / SCHNEEVERWEHUNG |
| 85 | VORABINFORMATION GLATTEIS |
| 89 | VORABINFORMATION STARKES TAUWETTER |
| 99 | TEST-VORABINFORMATION UNWETTER |

### 6.3 Küsten-Warnungen (profile §3.1.3)

| ii | `<event>` |
|----|-----------|
| 11 | BÖEN |
| 12 | WIND |
| 13 | STURM |

### 6.4 Hochsee-Warnungen (profile §3.1.4)

Reproduced with the profile's own (inconsistent) lower-case spelling.

| ii | `<event>` |
|----|-----------|
| 14 | Starkwind |
| 15 | Sturm |
| 16 | schwerer Sturm |

### 6.5 Medizin-Meteorologische Warnungen (profile §3.1.5)

These arrive with `<category>Health</category>` and `<senderName>Zentrum für
Medizin-Meteorologische Forschung</senderName>`.

| ii | `<event>` |
|----|-----------|
| 246 | UV-INDEX |
| 247 | STARKE HITZE |
| 248 | EXTREME HITZE |

### 6.6 Severity — the warning tiers (profile §2.2.2.6 and §3.5)

CAP `<severity>` is an enumerated **string**, not a number. Four values, and DWD's profile gives the
German tier name and colour for each:

| `<severity>` | Bright Sky value | German tier name (profile §2.2.2.6) | Colour (§3.5) | RGB |
|--------------|------------------|--------------------------------------|---------------|-----|
| `Minor` | `minor` | Wetterwarnung | Gelb | 255, 235, 59 |
| `Moderate` | `moderate` | Markante Wetterwarnung | Orange | 251, 140, 0 |
| `Severe` | `severe` | Unwetterwarnung | Rot | 229, 57, 53 |
| `Extreme` | `extreme` | Extreme Unwetterwarnung | Violett | 136, 14, 79 |

DWD's own map shows a **fifth visual tier**, *Vorabinformation* (§3.5: "Rosa schraffiert", CAP RGB
`255, 128, 128`), and a "Keine" state (Grün, 197, 229, 102). Vorabinformation is not a severity —
it is `urgency = Future`. If the page shows a tier badge, it needs five labels plus a no-warnings
state, not four.

There are **no numeric severity codes in CAP**. The `level` integers in candidates 2 and 4 are an
undocumented DWD-app invention; observed values on 2026-08-09 were `2` (WINDBÖEN/GEWITTER), `3`
(STURM/STARKES GEWITTER) and `50` (STARKE HITZE). Do not build a translation table on them.

### 6.7 The other closed vocabularies

Small, and all four are enumerated in the profile and re-exported by Bright Sky's OpenAPI schema.
Whether they need Frisian text depends on how much the page surfaces.

| Field | Values | German meaning (profile) |
|-------|--------|--------------------------|
| `<urgency>` §2.2.2.5 | `Immediate` / `Future` | Warnung / Vorabinformation |
| `<certainty>` §2.2.2.7 | `Observed` / `Likely` | Beobachtung / Vorhersage, Auftreten wahrscheinlich (p > ~50%) |
| `<category>` §2.2.2.2 | `Met` / `Health` | Meteorologische Meldung / Medizin-Meteorologische Meldung |
| `<responseType>` §2.2.2.4 | `Prepare` / `AllClear` / `None` / `Monitor` | Meldung mit Zusatzanweisungen / Aktualisierung, keine Gefahr mehr / Meldung ohne Zusatztext / Testmeldung, kann ignoriert werden |
| `<status>` | `Actual` / `Test` | — |

### 6.8 Headline patterns (profile §2.2.2.13)

`<headline>` is generated, not enumerated, but it follows four documented shapes:

- `Amtliche WARNUNG vor ...`
- `Amtliche UNWETTERWARNUNG vor ...`
- `VORABINFORMATION UNWETTER: ...`
- `AUFHEBUNG der UNWETTERWARNUNG vor ...`

### 6.9 What is *not* closed — read this before scoping the translation

`<description>` and `<instruction>` are **free-form generated German prose** and are unbounded. Live
example from 2026-08-09:

> "Es treten Windböen mit Geschwindigkeiten um 60 km/h (17 m/s, 33 kn, Bft 7) aus westlicher
> Richtung auf. In Schauernähe sowie in exponierten Lagen muss mit Sturmböen um 70 km/h (20 m/s, 38
> kn, Bft 8) gerechnet werden."

They are assembled from the per-`ii` parameter table (profile §3.2: `gusts`, `wind direction`,
`precipitation`, `visibility`, `snowfall`, `cause`, `occurrence`, …) with numbers substituted in.
There is **no** finite set of sentences.

So the honest scope of the Frisian translation work is:

1. **~47 distinct event names** (52 codes, but `33/34/36/38` all read "STARKES GEWITTER", `31`/`90`
   both "GEWITTER", etc. — deduplicated it is 47 strings) + 7 pre-alert + 3 coastal + 3 high-seas +
   3 medical = **60 distinct German event strings**, minus the 5 test strings if tests are filtered
   out.
2. **5 tier labels** + a no-warnings state.
3. Optionally the small vocabularies in §6.7 and the four headline shapes in §6.8.
4. **Not** the description/instruction prose. Those must either be shown in German, summarised into
   a hand-written Frisian sentence per event type, or omitted — a product decision this research
   cannot make. Given #1's "no computed verdicts" and "never imply *no warnings* when it only means
   *don't know*", the safest shape is: Frisian event name + Frisian tier + times, with the German
   detail text available but clearly marked as German.

---

## 7. Licence and attribution

**The map's assumption in #1 is out of date and should be corrected.** #1 records DWD as "GeoNutzV /
amended DWD Act". DWD's current
[Rechtliche Hinweise](https://www.dwd.de/DE/service/rechtliche_hinweise/rechtliche_hinweise.html)
state:

> "Alle frei zugänglichen Geodaten und Geodatendienste sowie die als hochwertige Datensätze / high
> value datasets (HVD) festgelegten Leistungen des DWD dürfen unter den Bedingungen der Lizenz
> Creative Commons BY 4.0 (CC BY 4.0) unter Beigabe eines Quellenvermerks weiterverwendet werden."

So: **CC BY 4.0**, with the attribution obligation resting on **§ 7 DWD-Gesetz**.

The exact required wording is fixed by DWD in
[Vorgaben für die Gestaltung des DWD-Quellenvermerks](https://www.dwd.de/DE/service/rechtliche_hinweise/vorlagen_quellenangabe.html):

> "In Textform: **Quelle: Deutscher Wetterdienst**"
> "In grafischer Form: durch Darstellung des DWD-Logos"

Placement rule, verbatim: *"Er ist unmittelbar an der verwendeten DWD-Information zu platzieren"* —
immediately adjacent to the DWD information used, not only in a footer. A `Quellenvermerk` may link
to DWD pages.

### 7.1 The clause that directly affects this project

Same page, and this is the one to design around:

> "**Wenn vom DWD ausgegebene amtliche Wetterwarnungen verändert werden, ist der beigegebene
> Quellvermerk zu löschen.**"
> ("If official weather warnings issued by DWD are altered, the accompanying source attribution must
> be deleted.")

Translating a DWD warning into Mooring **is** an alteration. The rule therefore says: a Frisian
rendering of a warning must **not** carry "Quelle: Deutscher Wetterdienst" attached to it as though
DWD had issued that text. What is required instead, per the same page, is:

> "Bei weitergehenden Veränderungen, Bearbeitungen, Neugestaltungen oder sonstigen Abwandlungen
> erwartet der DWD mindestens eine Nennung des DWD in zentralen Quellenverzeichnissen oder im
> Impressum."

with a modification note of the documented form, e.g. *"Datenbasis: Deutscher Wetterdienst, eigene
Elemente ergänzt"*.

Concretely, for this page:

- If a warning is shown **verbatim in German**: label it `Quelle: Deutscher Wetterdienst`, right
  next to it.
- If a warning is shown **translated into Mooring**: do *not* use `Quelle: Deutscher Wetterdienst`
  on it. Use a modification-style note near the warning and name DWD in the Impressum / central
  credits. Suggested, following DWD's own template pattern:
  `Datenbasis: Deutscher Wetterdienst — auersaat efter Mooring` (owner's wording to decide),
  plus `Quelle: Deutscher Wetterdienst` in the Impressum.
- Bright Sky itself imposes no additional attribution requirement (its MIT licence covers the
  software, not the data), but crediting it is courteous and cheap.

### 7.2 Bright Sky's own terms

From `https://api.brightsky.dev/openapi.json`:

> "The public instance at `https://api.brightsky.dev/` is free-to-use for all purposes, **no API key
> required**! Please note that the [DWD's Terms of Use](https://www.dwd.de/EN/service/legal_notice/legal_notice.html)
> apply to all data you retrieve through the API."

Software licence: MIT.

---

## 8. Recommendation, and what breaks if it disappears

### Recommendation

**Use Bright Sky `/alerts`, called from the browser with a hand-mapped `warn_cell_id` per curated
place.**

It wins on the two things that actually decide this:

1. **It is browser-fetchable** (`Access-Control-Allow-Origin: *`, verified, and deliberate in the
   source), which the official CAP archive is not — and it is one small JSON request per place
   rather than a 290 KB nationwide ZIP or a 114–190 KB nationwide JSON blob.
2. **It preserves `event_code`**, the CAP `ii`. Both DWD JSON feeds throw that away and leave only
   an undocumented `type`/`level` pair. Since the deliverable of this ticket is a translation table
   keyed to a closed vocabulary, a source that discards the vocabulary's identifiers is
   disqualified regardless of its other merits.

It also loses nothing on provenance: it serves `COMMUNEUNION_DWD_STAT` — the same official
municipality product — with an observed end-to-end lag under five minutes against a source that
republishes every ~10.6 minutes.

### What breaks if Bright Sky disappears

Bright Sky is one volunteer's project in the critical path of safety-relevant content. If
`api.brightsky.dev` goes away or degrades:

- **The page does not go blank and must not.** #1 already locked the correct behaviour: on fetch
  failure, show the link-out to DWD, never an empty space, because "the page must never imply *no
  warnings* when it only means *don't know*". Implement that first; it is what converts this risk
  from an outage into a degradation.
- **The event-code translation table survives the outage.** It is keyed to DWD's CAP `ii`, which is
  DWD's vocabulary, not Bright Sky's. Nothing hand-written by the owner is wasted.
- **The migration is a fetch-and-shape change, not a redesign.** Ranked fallbacks:
  1. **Self-host Bright Sky.** It is MIT-licensed with a published
     [infrastructure repository](https://github.com/jdemaeyer/brightsky-infrastructure). Same API,
     same fields, same cell IDs — a base-URL change. This is the cheapest true replacement and the
     reason the volunteer risk is tolerable.
  2. **DWD `warnapp_gemeinden` JSON** (`Access-Control-Allow-Origin: *`, municipality grain). Keeps
     warnings client-side. Costs: strip the JSONP wrapper, download ~191 KB nationwide per load, and
     **lose `event_code`** — the translation table would have to fall back to matching the German
     `event` string, which is exactly the brittleness this recommendation avoids.
  3. **Move to the scheduled job** and parse `COMMUNEUNION_DWD_STAT` CAP directly (which is what
     Bright Sky does). Fully official, keeps `event_code`, and the ~10.6-minute republish cadence
     fits a 15–30 minute job — but it reopens the "a gale warning cannot be 30 minutes stale"
     decision from #1, and is the option to avoid unless forced.
- **Cell IDs do not need re-mapping** in any of the three fallbacks: WarnCellID is DWD's identifier,
  not Bright Sky's, and the catalogue CSV is a DWD download.

The one thing that would genuinely hurt is losing Bright Sky *without* having built the link-out
failure path — the page would be silently warning-free during exactly the weather that makes it
worth visiting.

---

## Appendix: primary sources

- CAP DWD Profil v2.1.13 (12.09.2022) — <https://www.dwd.de/DE/leistungen/opendata/help/warnungen/cap_dwd_profile_de_pdf_2_1_13.pdf?__blob=publicationFile&v=3>
- CAP DWD Profil v2.1.12 (for the changed-events comparison) — <https://www.dwd.de/DE/leistungen/opendata/help/warnungen/cap_dwd_profile_de_pdf_1_12.pdf?__blob=publicationFile&v=4>
- Verarbeitungshinweise zu DWD-CAP-Produkten — <https://www.dwd.de/DE/leistungen/opendata/help/warnungen/cap_dwd_implementation_notes_de_pdf.pdf?__blob=publicationFile&v=5>
- Produktüberblick DWD Warnungen — <https://www.dwd.de/DE/leistungen/opendata/help/warnungen/dwd_warnings_products_overview_de_pdf.pdf?__blob=publicationFile&v=7>
- WarnCellID catalogue CSV — <https://www.dwd.de/DE/leistungen/opendata/help/warnungen/cap_warncellids_csv.csv?__blob=publicationFile&v=3>
- DWD Rechtliche Hinweise — <https://www.dwd.de/DE/service/rechtliche_hinweise/rechtliche_hinweise.html>
- DWD Quellenvermerk-Vorgaben — <https://www.dwd.de/DE/service/rechtliche_hinweise/vorlagen_quellenangabe.html>
- DWD Open Data alerts tree — <https://opendata.dwd.de/weather/alerts/cap/>
- DWD warnapp JSON — <https://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json>
- DWD GeoServer WFS (warn area geometry) — <https://maps.dwd.de/geoserver/wfs>
- Bright Sky OpenAPI specification — <https://api.brightsky.dev/openapi.json>
- Bright Sky source (`polling.py`, `web/app.py`) — <https://github.com/jdemaeyer/brightsky>
- `dwdparse` CAP parser — <https://github.com/jdemaeyer/dwdparse/blob/master/dwdparse/parsers.py>
- BSH Wasserstand und Gezeiten (legal mandate) — <https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/wasserstand_und_gezeiten_node.html>
- BSH Sturmfluten (classes and thresholds) — <https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/Sturmfluten/sturmfluten_node.html>
- BSH water level forecast API — <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast>
