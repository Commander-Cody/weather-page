# BSH `WaterLevelForecast` API — stations, data kinds, forecast horizon, licence

Research for [issue #2](https://github.com/Commander-Cody/weather-page/issues/2). Investigated against
primary sources only: the live API, BSH's own PDFs and web pages, and the OGC API Features conformance
declaration. Every claim below carries the URL of the source that owns it.

All live measurements in this document were taken on **2026-08-09, roughly 18:15–18:35 CEST**
(16:15–16:35 UTC). Values move; the *shapes* are what matter.

---

## TL;DR — the numbers that decide the panel

| Question | Answer | Confidence |
| --- | --- | --- |
| **Forecast horizon (curve)** | **≈ 136 h ≈ 5.7 days** ahead, measured. Ends at a **fixed absolute timestamp per model run**, so it decays between runs. BSH documents the driving model as running "bis zu 7 Tagen". | Measured directly; see [caveat](#the-horizon-caveat-you-must-design-around) |
| **Astronomical line beyond the horizon** | **Does not exist in this API.** The astronomical series ends at the *same* timestamp as the surge-corrected series, at all 39 North Sea curve stations. | Measured, 39/39 stations |
| **North Frisian gauges** | 23 in the `Nordfriesland bis Elbmündung` area — but only **9 have curve data**. The other 14 give peaks only. | Measured |
| **Official (human) peak forecast** | Only the **next 4 events** (~17–19 h). Everything beyond that is automated. | BSH flyer + measured |
| **Update cadence** | Official forecast **4×/day**; automated curve forecast **≈ every 10 min**. | BSH page + measured |
| **CORS** | `Access-Control-Allow-Origin: *`. Browser-callable. | Measured |
| **Licence** | CC BY 4.0, keyless, free, no registration. | API payload + landing page |
| **Rate limits** | None documented, none observed. | Measured |

The single most important consequence: **the map's plan of "solid surge-corrected line to the horizon,
faint astronomical line beyond" cannot be built from this API.** Both lines stop at the same wall. See
[What this means for the water-level panel](#what-this-means-for-the-water-level-panel).

---

## 1. What the service is

An OGC API Features service (ldproxy) with a **single collection**, `waterlevelforecastdata`.

- Landing page: <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast?f=json>
- Collection: <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/collections/waterlevelforecastdata?f=json>
- OpenAPI 3.0: <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/api?f=json>
- Conformance: <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/conformance?f=json>
- **Parameter documentation (PDF, the authoritative field reference)**:
  <https://www2.bsh.de/aktdat/wvd/api/parameter_documentation.pdf> (dated 27.05.2026)

The landing page describes the offering itself:

> "The Federal Maritime and Hydrographic Agency (BSH) provides a standardised interface for automatically
> retrieving official forecasts and tidal predictions, as well as station-based model evaluations of water
> levels, for the German North Sea and Baltic Sea coasts."
>
> — <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast?f=json> (`description`)

It is explicitly published as an EU **high-value dataset**: "the data can be obtained free of charge and
without registration and reused under the 'CC BY 4.0' licence" (same source).

Formats: `f=json` (GeoJSON), `f=fgb` (FlatGeobuf), `f=html`. Declared conformance includes
OGC API Features Parts 1–3 and CQL2
(<https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/conformance?f=json>).

**Collection metadata says `itemCount: 135`; the collection actually returns 136 features.** Minor, but
don't trust `itemCount` for pagination.

---

## 2. Stations in North Frisia

Filter on the `area` property, which for the whole North Frisian coast is the single string
`Nordfriesland bis Elbmündung (inkl. Helgoland)`.

**Real request** (returns all 23 in one call, 94 KB gzipped):

```
GET https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/collections/waterlevelforecastdata/items
    ?filter=area%20LIKE%20'Nordfriesland%25'
    &filter-lang=cql2-text
    &f=json&lang=en&limit=50
Accept-Encoding: gzip
```

→ `numberMatched: 23`, wire 94,602 B, uncompressed 1,007,215 B.

| `id` | `gauge_label` | lat, lon | Curve? | MOS peaks? | PNP rel. NHN | MHW rel. PN |
| --- | --- | --- | :---: | :---: | --- | --- |
| `list_hafen` | List, Sylt, Hafen | 55.0167, 8.4406 | **yes** | yes | −499 cm | 592 cm |
| `munkmarsch` | Munkmarsch, Sylt | 54.9211, 8.3633 | no | no | — | 596 cm |
| `westerland` | Westerland, Sylt | 54.9086, 8.2711 | no | no | — | 594 cm |
| `osterley` | Osterley | 54.8494, 8.5558 | no | no | — | 632 cm |
| `foehrer_ley_nord` | Föhrer Ley, Nord | 54.7964, 8.5600 | no | no | — | 629 cm |
| `hoernum_hafen` | Hörnum, Sylt, Hafen | 54.7581, 8.2961 | **yes** | no | −500 cm | 606 cm |
| `dagebuell` | Dagebüll | 54.7306, 8.6869 | **yes** | no | −501 cm | 643 cm |
| `amrum_odde` | Amrum Odde, Amrum | 54.7067, 8.3397 | no | no | — | 605 cm |
| `wyk` | Wyk, Föhr | 54.6933, 8.5764 | no | no | — | 645 cm |
| `schluettsiel` | Schlüttsiel | 54.6825, 8.7550 | no | no | — | 666 cm |
| `wittduen_hafen` | Wittdün, Amrum, Hafen | 54.6317, 8.3839 | **yes** | yes | −503 cm | 630 cm |
| `groede_anleger` | Gröde, Anleger | 54.6294, 8.7292 | no | no | — | 665 cm |
| `der_strand_hamburger_hallig` | Der Strand, Hamburger Hallig | 54.6053, 8.7872 | no | no | — | 658 cm |
| `hooge_anleger` | Hooge, Anleger | 54.5786, 8.5564 | **yes** | yes | −502 cm | 645 cm |
| `pellworm_hoogerfaehre` | Pellworm, Hoogerfähre | 54.5356, 8.5978 | no | no | — | 648 cm |
| `pellworm_anleger` | Pellworm, Anleger | 54.5008, 8.7019 | no | no | — | 656 cm |
| `strucklahnungshoern` | Strucklahnungshörn, Nordstrand, AP | 54.4989, 8.8064 | no | no | — | 664 cm |
| `husum_schleuse` | Husum, Schleuse | 54.4722, 9.0247 | **yes** | yes | −500 cm | 672 cm |
| `suederoogsand` | Süderoogsand | 54.4200, 8.5192 | no | no | — | 636 cm |
| `eider-sperrwerk_aussenpegel` | Eider-Sperrwerk, Außenpegel | 54.2658, 8.8419 | **yes** | yes | −502 cm | 647 cm |
| `helgoland_binnenhafen` | Helgoland, Binnenhafen | 54.1789, 7.8900 | **yes** | yes | −502 cm | 619 cm |
| `buesum_schleuse` | Büsum, Schleuse | 54.1222, 8.8592 | **yes** | no | −502 cm | 661 cm |
| `meldorf_sperrwerk_aussenpegel` | Meldorf, Sperrwerk, Außenpegel | 54.0922, 8.9492 | no | no | — | 667 cm |

Source: live collection, `properties.area`, `properties.gauge_label`, `properties.latitude/longitude`,
`properties.gaugezero_relative_to_nhn`, `properties.mean_high_water`.

**Identifier**: the OGC feature `id` (e.g. `husum_schleuse`) is the stable key and is what you put in the
item URL. There is also `operator_gauge_id` (the WSV Pegelonline number, e.g. `9530020` for Husum) and
`measurement_url` pointing at Pegelonline — but only on the 9 curve stations.

### The 14 stations without curves are much thinner than they look

They are missing far more than the curve. Live example, `wyk`, complete property set:

```json
{
  "gauge_label": "Wyk, Föhr",
  "official_warning_level_region": "Wasserstandsvorhersage",
  "licence": "CC BY 4.0",
  "area": "Nordfriesland bis Elbmündung (inkl. Helgoland)",
  "region": "north_sea",
  "mean_high_water": 645.0,
  "mean_low_water": 358.0,
  "latitude": 54.693333,
  "longitude": 8.576389,
  "automated_gauge_warning": "Wasserstandsvorhersage",
  "forecast_timestamp": "2026-08-09 13:25:59+02:00"
}
```

No `gaugezero_relative_to_nhn`, no `chartdatum_relative_to_gaugezero`, no `state`, no `measurement_url`,
no `bsh_url_waterlevel`, no `operator_gauge_id`, no `curve`.

**Consequence: at these stations you cannot convert to NHN or chart datum at all** — the conversion
constant simply is not published through this API. You can only show values relative to gauge zero, or
relative to MHW/MNW (which *are* present).

Key frequency across all 136 features, for planning null-handling:

| Property | Present on |
| --- | --- |
| `gauge_label`, `licence`, `copyright`, `area`, `region`, `latitude`, `longitude`, `forecast_timestamp` | 136 |
| `mean_high_water` | 131 |
| `official_warning_level_region`, `forecast_text` | 129 |
| `mean_low_water` | 128 |
| `curve`, `gaugezero_relative_to_nhn`, `chartdatum_relative_to_gaugezero`, `state`, `bsh_url_waterlevel`, `operator_gauge_id`, `automated_curveforecast_timestamp` | 93 |
| `automated_gauge_warning`, `measurement_url`, `high_water_low_water` | 82 |
| `information_text` | 75 |

---

## 3. Data kinds and exact response shapes

A feature is GeoJSON: `type`, `geometry` (Point, `[lon, lat]`), `properties`, `id`. The two time series
live *inside* `properties`, as `high_water_low_water` and `curve`
(<https://www2.bsh.de/aktdat/wvd/api/parameter_documentation.pdf>, structure table p.1).

**Real request:**

```
GET https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/collections/waterlevelforecastdata/items/husum_schleuse?f=json
```

→ 200, 106,781 B uncompressed / 10,178 B gzipped.

### 3a. Station metadata (`properties`)

Trimmed real response:

```json
{
  "gauge_label": "Husum, Schleuse",
  "official_warning_level_region": "Wasserstandsvorhersage",
  "licence": "CC BY 4.0",
  "gaugezero_relative_to_nhn": -500.0,
  "chartdatum_relative_to_gaugezero": 254.0,
  "area": "Nordfriesland bis Elbmündung (inkl. Helgoland)",
  "region": "north_sea",
  "state": "Schleswig-Holstein",
  "mean_high_water": 672.0,
  "mean_low_water": 324.0,
  "latitude": 54.472222,
  "longitude": 9.024722,
  "automated_gauge_warning": "Wasserstandsvorhersage",
  "bsh_url_waterlevel": "https://wasserstand-nordsee.bsh.de/husum_schleuse",
  "measurement_url": "https://www.pegelonline.wsv.de/gast/stammdaten?pegelnr=9530020#...",
  "operator_gauge_id": "9530020",
  "forecast_timestamp": "2026-08-09 13:25:59+02:00",
  "automated_curveforecast_timestamp": "2026-08-09 18:11:20+02:00"
}
```

`forecast_text` and `copyright` are **objects keyed by language**, always containing both `de` and `en`,
regardless of the `lang` query parameter:

```json
"forecast_text": {
  "de": "In der Nacht von Sonntag zu Montag wird das Hochwasser an der deutschen Nordseeküste, in Emden, Bremen und Hamburg <b>nicht wesentlich</b> vom mittleren Hochwasser abweichen.",
  "en": "During the night from Sunday to Monday the high water along the German North Sea coast, in Emden, Bremen and Hamburg will <b>not deviate significantly</b> from the Mean High Water."
}
```

Note the embedded **HTML markup** (`<b>`) inside these strings.

### 3b. Vertical datum — everything is relative to gauge zero

This is the part most likely to be got wrong.

**All water-level values in this API — `tidal_prediction`, `automated_curve_forecast`, `measurement`,
`tidal_prediction_value`, `forecast_value`, `mos_forecast_r*_value`, `mean_high_water`, `mean_low_water`
— are in centimetres relative to the local gauge zero (Pegelnullpunkt, PN/PNP).** Not NHN, not chart
datum. Source: <https://www2.bsh.de/aktdat/wvd/api/parameter_documentation.pdf>, Tab. 1, Tab. 2, Tab. 4.

Two conversion constants are supplied (Tab. 1):

- `gaugezero_relative_to_nhn` — "The height of gauge zero relative to Normalhöhennull (NHN)", cm
- `chartdatum_relative_to_gaugezero` — "The height of chart datum relative to the local gauge zero", cm

So:

```
height_NHN_cm        = value_cm + gaugezero_relative_to_nhn
height_above_SKN_cm  = value_cm − chartdatum_relative_to_gaugezero
height_rel_MHW_cm    = value_cm − mean_high_water
```

Verified against BSH's own official forecast sheet. The API gives Husum
`gaugezero_relative_to_nhn = -500.0`, `mean_high_water = 672.0`, `chartdatum_relative_to_gaugezero = 254.0`;
the official PDF <https://wasserstand.bsh.de/data/nordsee/Wasserstandsvorhersage.pdf> prints for Husum
`PNP -5,00 m`, `MHW 6,72 m`, `SKN 2,54 m`. Exact match. That PDF also defines the terms:

> "NHN = Normalhöhennull, PNP = Pegelnullpunkt bezogen auf NHN, SKN = Seekartennull bezogen auf PNP,
> MHW = Mittleres Hochwasser bezogen auf PNP, MNW = Mittleres Niedrigwasser bezogen auf PNP"

Worked example (Husum, HW on 2026-08-09 23:16): `forecast_value` 662 cm rel. PN → **+1.62 m NHN**, and
662 − 672 = **−0.10 m relative to MHW**, which matches the API's own `forecast_deviation: "-0,1 m"`.

### 3c. Time zone

Timestamps are strings with an **explicit UTC offset**, in German legal time (`+02:00` in summer,
`+01:00` in winter) — *not* UTC, and *not* ISO-8601 `T`-separated:

```
"2026-08-09 05:00:00+02:00"
```

The PDF calls the type "datetime string with explicit UTC offset"
(<https://www2.bsh.de/aktdat/wvd/api/parameter_documentation.pdf>, Tab. 1/2/4). BSH's forecast sheet
labels its times "(gesetzliche Zeit)"
(<https://wasserstand.bsh.de/data/nordsee/Wasserstandsvorhersage.pdf>).

**Parsing hazard**: the space separator instead of `T` means these are *not* valid ISO-8601. JS
`new Date("2026-08-09 05:00:00+02:00")` is not spec-guaranteed (it happens to work in V8). Normalise the
space to `T` before parsing.

### 3d. `high_water_low_water` — peak forecasts

Present on 82 of 136 features (all North Sea stations; no Baltic station has it). Around 22–23 events
per North Frisian station, spanning the same ~136 h window as the curve.

Real entries from `husum_schleuse`:

```json
{
  "event_timestamp": "2026-08-09 16:33:00+02:00",
  "event": "NW",
  "tidal_prediction_value": "338",
  "forecast_value": 354,
  "forecast_uncertainty": 10.0,
  "forecast_deviation": "+0,3 m",
  "forecast_automated_event_warning": "Wasserstandsvorhersage",
  "forecast_event_forecast_timestamp": "2026-08-09 13:25:59+02:00"
}
```

```json
{
  "event_timestamp": "2026-08-15 10:45:00+02:00",
  "event": "NW",
  "tidal_prediction_value": "302",
  "mos_forecast_r0_value": 301,
  "mos_forecast_r0_deviation": "-0,2 m",
  "mos_forecast_r1_value": 309,
  "mos_forecast_r5_value": 305,
  "mos_forecast_event_forecast_timestamp": "2026-08-09 18:00:00+02:00"
}
```

Note the second entry has **no `forecast_value`** — the official forecast has already run out.

Fields (<https://www2.bsh.de/aktdat/wvd/api/parameter_documentation.pdf>, Tab. 2):

| Field | Unit | Meaning |
| --- | --- | --- |
| `event_timestamp` | datetime+offset | time of the peak |
| `event` | — | `"HW"` (high water) or `"NW"` (low water) |
| `tidal_prediction_value` | cm rel. PN | **astronomical** prediction of the peak |
| `forecast_value` | cm rel. PN | **official** (human) forecast of the peak |
| `forecast_uncertainty` | cm | uncertainty of the official forecast |
| `forecast_deviation` | m | deviation from MHW/MNW, **German-formatted string** (`"+0,3 m"`) |
| `forecast_automated_event_warning` | — | automated warning level for this event |
| `forecast_event_forecast_timestamp` | datetime+offset | when the official forecast was made |
| `mos_forecast_r0…r5_value` | cm rel. PN | **automated MOS** peak forecast, r0 = main, r1–r5 fallbacks |
| `mos_forecast_r0…r5_deviation` | m | as above, German-formatted string |
| `mos_forecast_event_forecast_timestamp` | datetime+offset | when the MOS forecast was made |

The r0–r5 fallback chain is documented in Tab. 3 of the same PDF: r0 is the main system; r1 if the
gauge's own measurements are missing; r2 if the upstream gauge's are; r3 without GFS input; r4 if the
numerical model is unavailable; r5 if more than one input is missing. **Use `r0` and fall through r1→r5
only when r0 is absent.**

### 3e. `curve` — the time series

Present on 93 of 136 features: **exactly 39 North Sea** stations and 54 Baltic stations. The 39 matches
BSH's own statement:

> "Neben den Wissenschaftler-Vorhersagen der Einzelereignisse werden für 39 Pegel auch vollständige
> Kurvenvorhersagen aus dem MOS-Verfahren dargestellt."
>
> — <https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/Nordsee/nordsee.html>

Real entries from `husum_schleuse` (920 points):

```json
{"timestamp": "2026-08-09 05:00:00+02:00", "tidal_prediction": "387", "measurement": "381"}
{"timestamp": "2026-08-09 18:00:00+02:00", "tidal_prediction": "398", "measurement": "412"}
{"timestamp": "2026-08-09 18:10:00+02:00", "tidal_prediction": "411", "automated_curve_forecast": "424"}
{"timestamp": "2026-08-15 10:50:00+02:00", "tidal_prediction": "302", "automated_curve_forecast": "302"}
```

| Field | Unit | Meaning |
| --- | --- | --- |
| `timestamp` | datetime+offset | time of the sample |
| `tidal_prediction` | cm rel. PN | **astronomical** tide (no weather) |
| `automated_curve_forecast` | cm rel. PN | **MOS model forecast** — this is the surge-corrected line |
| `measurement` | cm rel. PN | **observed** water level |

Source: <https://www2.bsh.de/aktdat/wvd/api/parameter_documentation.pdf>, Tab. 4.

Structural facts measured live at Husum:

- **Keys are omitted, not null.** A point has `measurement` *or* `automated_curve_forecast`, never both;
  `tidal_prediction` is on essentially every point. Code must treat absence as the signal.
- **`measurement` and `automated_curve_forecast` do not overlap.** Measurements ran
  05:00 → 18:00, the forecast began 18:10. The handover is the "now" line and it is clean.
- **The grid is 10 minutes but not uniform.** Step histogram over 920 points: 879 steps of 600 s, plus 41
  irregular steps of 60–540 s. The irregular points are the **exact HW/NW turning times inserted into the
  series** (e.g. `16:33`, `23:16`, `05:17` — the same values as `event_timestamp` in
  `high_water_low_water`). Do not assume a fixed dt when charting or resampling.
- **Measurement history is short**: ~13 h back only (05:00 → 18:00 on the day of request), ~80 points.
- **Baltic curves are a different product**: uniform 15-minute grid, `measurement` and
  `automated_curve_forecast` only — **no `tidal_prediction`** — and a much shorter window
  (`flensburg`: 2026-08-08 12:00 → 2026-08-12 00:00). Irrelevant here, but don't write code that assumes
  one shape.

### 3f. JSON type inconsistency (real hazard)

Measured across all 136 features:

| Field | Observed JSON types |
| --- | --- |
| `curve.tidal_prediction`, `curve.automated_curve_forecast`, `curve.measurement` | `str` only |
| `high_water_low_water.tidal_prediction_value` | `str` only |
| `high_water_low_water.forecast_value` | **`int` *and* `str`** |
| `high_water_low_water.forecast_uncertainty` | **`float` *and* `str`** |
| `high_water_low_water.mos_forecast_r*_value` | `int` only |

Numeric-looking values are quoted strings in some places and real JSON numbers in others, and
`forecast_value` is *both* depending on the station. Coerce every one of these explicitly. The
`*_deviation` fields are always German-formatted strings with a comma decimal separator (`"+0,3 m"`) —
parse or ignore, never `parseFloat` naively.

### 3g. Documentation drift

Two fields in the PDF's Tab. 1 do not appear in the live payload as documented:

- `information` — the live payload uses **`information_text`** instead (75 features).
- `forecast_text_additional` — not present on any of the 136 features at time of measurement.

The PDF also types `forecast_text` and `copyright` as plain text, but they are language-keyed objects
live. Trust the payload over the PDF for shape; trust the PDF for units and semantics.

---

## 4. The forecast horizon

**This is the number the ticket asked for, so here is exactly what was measured and exactly what was not.**

At response `timeStamp` `2026-08-09T16:18:46Z`, for all 39 North Sea curve stations:

| Series | First | Last | Relative to now |
| --- | --- | --- | --- |
| `measurement` | 2026-08-09 05:00 +02:00 | 2026-08-09 18:00 +02:00 | −13.3 h → −0.3 h |
| `automated_curve_forecast` | 2026-08-09 18:10 +02:00 | **2026-08-15 10:50 +02:00** | −0.1 h → **+136.5 h** |
| `tidal_prediction` | 2026-08-09 05:00 +02:00 | **2026-08-15 10:50 +02:00** | −13.3 h → **+136.5 h** |

**≈ 136.5 hours ≈ 5.7 days.** Identical end timestamp at every North Sea curve station
(only two distinct curve-end values exist across the whole collection: `2026-08-15 10:50+02:00` for the
39 North Sea stations, `2026-08-12 00:00+02:00` for the 54 Baltic ones).

Per-station measured horizons, North Frisia:

| Station | Official peak fc | MOS peak fc | Curve fc |
| --- | --- | --- | --- |
| `husum_schleuse` | +17.6 h | +136.4 h | +136.5 h |
| `dagebuell` | +18.0 h | — | +136.5 h |
| `wittduen_hafen` | +17.2 h | +136.2 h | +136.5 h |
| `list_hafen` | +18.5 h | +131.2 h | +136.5 h |
| `hoernum_hafen` | +18.0 h | — | +136.5 h |
| `hooge_anleger` | +17.2 h | +136.3 h | +136.5 h |
| `buesum_schleuse` | +16.6 h | — | +136.5 h |
| `helgoland_binnenhafen` | +15.6 h | +134.8 h | +136.5 h |
| `eider-sperrwerk_aussenpegel` | +17.1 h | +129.7 h | +136.5 h |
| `wyk`, `pellworm_*`, `schluettsiel`, … (14 stations) | ~+17 h | — | **none** |

### There are three different horizons, not one

1. **Official, human-made peak forecast (`forecast_value`) — the next 4 events only, ~17 h.**
   Every North Frisian station returned exactly 4 events carrying `forecast_value` (except
   `groede_anleger`, which returned 2). BSH documents this precisely:

   > "Viermal am Tag, gegen 00.30, 08.00, 14.00 und 20.00 Uhr, werden Vorhersagen für die kommenden
   > **zwei Hoch- und zwei Niedrigwasser** an festgelegten Pegelorten erstellt und mit den jeweiligen
   > Eintrittszeiten herausgegeben."
   >
   > — <https://www.bsh.de/DE/PUBLIKATIONEN/_Anlagen/Downloads/BSH-Informationen/BSH-Flyer/Wasserstandsvorhersage_dt.pdf>

   Cross-checked directly: the API's last official peak for Husum was `2026-08-10 11:53:00+02:00`, and
   the official sheet <https://wasserstand.bsh.de/data/nordsee/Wasserstandsvorhersage.pdf> ("Erstellt am
   09.08.2026 um 13:25 Uhr") lists Husum's fourth event as `HW 10.08.2026 11:53`. Same number, and the
   sheet's creation time matches the API's `forecast_timestamp` of `2026-08-09 13:25:59+02:00` to the
   minute.

2. **Automated MOS peak forecast (`mos_forecast_r0_value`) — ~130–136 h**, but only at 32 stations
   collection-wide, 6 of which are North Frisian.

3. **Automated MOS curve forecast (`automated_curve_forecast`) — ~136 h**, at 39 North Sea stations,
   9 of which are North Frisian. **This is the series the panel should draw.**

### What BSH documents about the underlying model

> "Für Vorhersagezeiträume von bis zu 7 Tagen bilden die Ergebnisse eine wesentliche Basis für die
> Wasserstandsvorhersagen des BSH."
>
> — <https://www.bsh.de/DE/THEMEN/Modelle/Hydrodynamik/hydrodynamik_node.html>

The same page states the North Sea water level and surge model runs **four times daily**. So the raw
model reaches 7 days; the MOS product exposed here was measured at 5.7 days. BSH does not publish a
stated horizon for the MOS curve product itself — **the 136 h figure is measured, not documented.**

### The horizon caveat you must design around

Across five probes spanning 18:22 → 18:34 CEST — covering **three distinct curve-forecast runs** — the
curve's **end timestamp did not move** (`2026-08-15 10:50+02:00`) while the *start* of the forecast
advanced (18:10 → 18:30) and `measurement` extended (18:00 → 18:10). The window is therefore anchored to
an absolute end that survives across automated runs, and **the usable horizon shrinks as the window
ages**, jumping back up when the end rolls forward.

I could not observe a full run-to-run cycle inside this session, so **I cannot state the minimum horizon
from primary observation.** If the window rolls once daily, the horizon would oscillate roughly between
~136 h and ~112 h. That is an inference, not a measurement, and it is flagged as such.

**Engineering consequence — and this is the robust answer regardless of the cycle: do not hard-code the
horizon.** Read it from the data as the timestamp of the last non-null `automated_curve_forecast`, and
put the seam there. That is correct whatever BSH does with its run schedule.

---

## 5. The finding that changes the panel design

**There is no astronomical tail beyond the forecast horizon.**

Checked at all 39 North Sea curve stations: the number of stations where `tidal_prediction` extends past
`automated_curve_forecast` is **zero**. Both series terminate on the identical timestamp. The same holds
in `high_water_low_water`: the last astronomical peak (`tidal_prediction_value`, Husum
`2026-08-15 10:45`) sits inside the same window as the last curve point (`2026-08-15 10:50`).

The astronomical prediction *does* extend ~13 h further **backwards** than the forecast, covering the
measurement period — that's the only asymmetry.

BSH's separate tide service <https://gezeiten.bsh.de/en> does publish long-range tidal predictions, but
it is **not** part of this CC BY 4.0 offering: "The provision and use of tidal data is subject to the
conditions contained in the user fee regulation for digital data", and it exposes downloads rather than
an API. Treat it as a licensing and integration question of its own, not a drop-in extension.

### What this means for the water-level panel

The map (issue #1) locked: *"show the BSH surge-corrected forecast as the main line with the astronomical
tide faint behind it — the gap between them is the information. Past the forecast horizon, one line only,
with a visible seam."*

Against the real data:

- **The good half holds, and holds better than assumed.** `automated_curve_forecast` (surge-corrected)
  and `tidal_prediction` (astronomical) exist on the *same timestamps* over the *entire* forecast window.
  The gap between them is directly plottable with no interpolation or alignment work — they share a
  point grid. The surge is literally the vertical difference at each point.
- **The seam is not where the map assumed.** There is no "astronomical only" region. The seam at ~+136 h
  is between *data* and *no data*.
- **The page's horizon overshoots the data.** The map locked "today plus six days" (7 days). The water
  data reaches ~5.7 days. **The last ~1.3 days of the page's time axis have no water level at all** —
  neither line. That needs a deliberate design decision, not an empty axis.
- **Place-to-gauge pairing is constrained by curve availability, not by geography.** Only 9 North Frisian
  gauges have curves. For the others there is no line to draw — only up to 23 peak markers, of which just
  the first ~4 are surge-corrected and the rest are pure astronomy. Suggested substitutions:
  Wyk → `dagebuell` or `wittduen_hafen`; Pellworm → `hooge_anleger` or `husum_schleuse`;
  Schlüttsiel → `dagebuell`; Strucklahnungshörn → `husum_schleuse`; Amrum Odde → `wittduen_hafen`;
  Westerland/Munkmarsch → `list_hafen` or `hoernum_hafen`. Hooge is itself a curve station.
- **Height labels are not universally available.** At the 14 non-curve stations you cannot express
  heights in NHN or chart datum, only relative to gauge zero or to MHW. If the page shows heights in a
  single datum everywhere, that constrains pairing further.

---

## 6. Update cadence

**Official forecast — 4×/day.**

> "Die Erstellung der Vorhersage unter Berücksichtigung aller verfügbaren Informationen erfolgt durch den
> diensthabenden Wissenschaftler. Sie erfolgt viermal am Tag – um 1.00, 8.00, 14.00 und 20.00 Uhr."
>
> — <https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/Nordsee/nordsee.html>

BSH's flyer gives the times slightly differently — "gegen 00.30, 08.00, 14.00 und 20.00 Uhr"
(<https://www.bsh.de/DE/PUBLIKATIONEN/_Anlagen/Downloads/BSH-Informationen/BSH-Flyer/Wasserstandsvorhersage_dt.pdf>).
The two BSH sources disagree on the first slot (00.30 vs 1.00); the rest agree. Times are German legal
time. The measured `forecast_timestamp` of `2026-08-09 13:25:59+02:00` sits just before the 14:00 slot,
consistent with both.

**Automated curve forecast — roughly every 7–8 minutes.** Measured by polling `husum_schleuse` every
3 minutes:

| Probe (UTC) | `automated_curveforecast_timestamp` | first forecast point | last `measurement` | curve end |
| --- | --- | --- | --- | --- |
| 16:22:15 | 2026-08-09 18:11:20+02:00 | 18:10 | 18:00 | 2026-08-15 10:50 |
| 16:25:15 | 2026-08-09 **18:19:12**+02:00 | 18:30 | 18:10 | 2026-08-15 10:50 |
| 16:28:16 | 2026-08-09 18:19:12+02:00 | 18:30 | 18:10 | 2026-08-15 10:50 |
| 16:31:16 | 2026-08-09 **18:26:21**+02:00 | 18:30 | 18:10 | 2026-08-15 10:50 |
| 16:34:16 | 2026-08-09 18:26:21+02:00 | 18:30 | 18:10 | 2026-08-15 10:50 |

Three distinct curve-forecast runs in 12 minutes — 18:11:20 → 18:19:12 → 18:26:21, intervals of 7 m 52 s
and 7 m 09 s. `forecast_timestamp` stayed pinned at `13:25:59` and the last official peak at
`2026-08-10 11:53` across all five probes, confirming the official and automated products update on
independent schedules. The curve end never moved.

The probe did not span one of the four official update slots (the next was 20:00 CEST), so the official
cadence rests on BSH's documentation rather than on my own measurement.

**Recommended job cadence**: the map's 15–30 min is well matched to the curve product and comfortably
oversamples the official 4×/day text. Nothing is gained below ~10 min. Use `If-None-Match` (below) so
unchanged polls cost nothing.

---

## 7. CORS

**Allowed, wildcard.** Measured on a real `GET` with an `Origin: https://example.com` header:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: X-Requested-With,Origin,Content-Type,Accept
Access-Control-Expose-Headers: Link, Content-Crs, OATiles-hint, Prefer, ETag
```

A plain `fetch()` with no custom headers is a CORS-simple request and needs no preflight, so this works
from the browser today. One caveat: an explicit `OPTIONS` preflight to the item URL returned **301** (to
`?lang=en&...`) rather than a preflight response, so a request that *does* trigger preflight (custom
headers) may fail. Since the map only needs this informationally — BSH is fetched from the scheduled job
— this is not blocking. Note also that `Access-Control-Allow-Origin: *` together with
`Allow-Credentials: true` is a contradictory combination that browsers reject for credentialed requests;
don't send credentials.

---

## 8. Licence and required attribution

**Licence: CC BY 4.0.** Stated in the payload itself on all 136 features (`"licence": "CC BY 4.0"`) and
on the landing page:

> "BSH's open data is provided under the 'Creative Commons license CC BY 4.0'
> (<https://creativecommons.org/licenses/by/4.0/legalcode.en>). … The following requirements apply when
> using the data: **Attribution**: You must provide an appropriate source citation, link to the license,
> and indicate whether any changes have been made. The form is freely selectable, but must not give the
> impression that the licensor supports or recommends you or your use. **No additional restrictions**: You
> may not impose legal conditions or technical measures that would prevent others from freely using the
> material under the license."
>
> — <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast?f=json> (`description`)

**BSH does not mandate one fixed sentence** — "The form is freely selectable". But it ships its own
attribution string in every feature's `copyright` property, and using that verbatim is the safest choice:

German (`properties.copyright.de`):

> `@Bundesamt für Seeschifffahrt und Hydrographie (BSH). Das BSH übernimmt für die angegebenen Informationen keine Gewähr. Amtliche Wasserstandsvorhersage des Bundes gemäß §1 SeeAufG.`

English (`properties.copyright.en`):

> `@Federal Maritime and Hydrographic Agency (BSH). The BSH accepts no liability for the information provided here. Official water level forecast of the federal government according to §1 SeeAufG.`

To satisfy CC BY 4.0 fully the credit line also needs a **link to the licence** and an **indication that
changes were made** (the page derives, resamples and re-renders the data). Something of the shape:

> Wååterstånd: © Bundesamt für Seeschifffahrt und Hydrographie (BSH) — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — bewerket / bearbeitet.
> Das BSH übernimmt für die angegebenen Informationen keine Gewähr.

(Wording to be authored in Mooring by the repo owner per issue #1; the *elements* required are: BSH named,
licence linked, changes indicated.)

Note the `copyright` value uses `@` rather than `©`, and the field is **present on all 136 features**, so
it can be read from the data rather than hard-coded — which keeps the page correct if BSH changes it.

---

## 9. Reliability, rate limits, no-guarantee clauses

**No-guarantee clauses — three, all primary:**

- In every feature: "Das BSH übernimmt für die angegebenen Informationen keine Gewähr." /
  "The BSH accepts no liability for the information provided here." (`properties.copyright`)
- In the parameter documentation: "**The information provided via the API may be incorrect or out of
  date, and should not be relied upon instead of the officially published forecasts on the website**
  (www.bsh.de)." — <https://www2.bsh.de/aktdat/wvd/api/parameter_documentation.pdf>, p.1
- Same page, on coverage: "Please note that not all categories and parameters are available for every
  station." (amply confirmed above)

Also from the PDF (Tab. 5): the `official_warning_level_region` value "does not apply specifically to a
particular gauge station" — it is a North Sea / Baltic-wide category, not per-gauge. Do **not** render it
as a station-level warning. Per-station there is `automated_gauge_warning` (present on 82 features), and
per-event `forecast_automated_event_warning`. The North Sea thresholds relative to MHW are: Sturmflut
+1.5 m, schwere Sturmflut +2.5 m, sehr schwere Sturmflut +3.5 m — matching the flyer.

**Rate limits: none documented and none observed.** 15 rapid sequential item requests all returned 200 in
0.23–0.30 s with no `X-RateLimit-*`, `Retry-After` or `Quota` headers. `https://gdi.bsh.de/robots.txt`
returns 404. BSH publishes no SLA or uptime commitment for this service that I could find; the landing
page's only operational statement is the free/no-registration one. **Absence of a documented limit is not
permission to hammer it** — the map's 15–30 min cadence is far below any plausible threshold.

**Operational status channel**: `information_text` (present on 75 features) is documented as an
"Informational notice on the operational status, e.g. technical disruptions". At time of measurement it
carried a notice pointing users at this very API. Worth surfacing or at least logging — it is BSH's
in-band channel for telling consumers something is broken.

**Human contact**: Wasserstandsvorhersagedienst Nordsee, `wvd@bsh.de`, +49 40 3190-3190
(<https://www.bsh.de/DE/PUBLIKATIONEN/_Anlagen/Downloads/BSH-Informationen/BSH-Flyer/Wasserstandsvorhersage_dt.pdf>).
The landing page explicitly invites feedback on the API.

---

## 10. Practical recipe for the scheduled job

**One request gets every North Frisian station**, including full curves:

```
GET https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/collections/waterlevelforecastdata/items
    ?filter=area%20LIKE%20'Nordfriesland%25'&filter-lang=cql2-text&f=json&lang=en&limit=50
Accept-Encoding: gzip
If-None-Match: "<etag from last run>"
```

Measured costs:

| Request | Uncompressed | Gzipped | Time |
| --- | --- | --- | --- |
| Single station (`husum_schleuse`) | 106,781 B | 10,178 B | ~0.25 s |
| All 23 North Frisian (CQL2 `area LIKE`) | 1,007,215 B | 94,602 B | ~1 s |
| bbox `8.0,54.3,9.2,55.1` (19 stations) | 690,993 B | 64,662 B | — |
| Whole collection (136) | 5,631,707 B | 503,419 B | ~1.8 s |

- **gzip works** and saves ~10×. Always send `Accept-Encoding: gzip`.
- **`If-None-Match` works** — a conditional GET returned **304** with an empty body. Use it.
- **CQL2 filtering works** (`filter-lang=cql2-text`), e.g. `area LIKE 'Nordfriesland%'` or
  `region='north_sea' AND state='Schleswig-Holstein'`. The bare `area=...` shorthand queryable returned
  `numberMatched: 0` even with the exact string — **use CQL2, not the shorthand.**
- **`datetime` does not subset the curve.** A request with
  `datetime=2026-08-11T00:00:00Z/2026-08-11T12:00:00Z` returned `numberMatched: 136` and full 922-point
  curves. It filters *features*, not the embedded series, and here filters nothing. **There is no way to
  trim the payload by time** — you always get the whole window and must slice client-side.
- There is **no `properties=` selection**, so you cannot ask for metadata without curves.
- Every request 301-redirects to add `?lang=…`; **follow redirects** (`curl -L`). Content negotiation via
  `Accept: application/geo+json` works without `f=`.
- Unknown station → clean `404` JSON problem document:
  `{"status": 404, "title": "Not Found", "detail": "The requested feature does not exist."}`

---

## 11. Open questions not answerable from primary sources

Stated explicitly rather than guessed:

1. **The minimum forecast horizon between model runs.** Measured 136.5 h at one point in the cycle; the
   end timestamp is fixed per run. The roll-forward behaviour was not observed within this session and
   BSH does not document the MOS product's horizon. *Mitigation: derive the seam from the data, never
   hard-code it.*
2. **Whether the 39-station curve set is stable**, or varies with data availability. Measured once.
3. **Any uptime/SLA commitment.** No such statement found on any BSH page or in the API metadata.
4. **Why `itemCount` (135) disagrees with the returned feature count (136).**
5. **Whether `forecast_text_additional` ever appears.** Documented in the PDF, absent from all 136
   features at time of measurement.
6. **The exact provenance of `forecast_value` at the 14 non-curve stations.** They carry official peak
   forecasts despite not being among BSH's 16 manually forecast gauges
   (<https://wasserstand.bsh.de/data/nordsee/Wasserstandsvorhersage.pdf> lists 16, of which 7 are North
   Frisian). The values are presumably derived by applying a base gauge's deviation, but BSH does not
   document the derivation, so their accuracy relative to the manual gauges is unknown.

---

## Sources

Primary, all consulted directly:

- Live API landing page — <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast?f=json>
- Live collection & items — <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/collections/waterlevelforecastdata/items?f=json>
- Conformance declaration — <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/conformance?f=json>
- OpenAPI 3.0 definition — <https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/api?f=json>
- **BSH, "Description of JSON API response parameters", 27.05.2026** — <https://www2.bsh.de/aktdat/wvd/api/parameter_documentation.pdf>
- BSH, official water level forecast sheet — <https://wasserstand.bsh.de/data/nordsee/Wasserstandsvorhersage.pdf>
- BSH, "Wasserstandsvorhersage an der Nordsee" — <https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/Nordsee/nordsee.html>
- BSH, "Hydrodynamik" (operational model) — <https://www.bsh.de/DE/THEMEN/Modelle/Hydrodynamik/hydrodynamik_node.html>
- BSH flyer, "Wasserstandsvorhersage- und Sturmflutwarndienst" — <https://www.bsh.de/DE/PUBLIKATIONEN/_Anlagen/Downloads/BSH-Informationen/BSH-Flyer/Wasserstandsvorhersage_dt.pdf>
- BSH tide service (licensing contrast) — <https://gezeiten.bsh.de/en>
- BSH water level app — <https://wasserstand.bsh.de/>
- CC BY 4.0 legal code — <https://creativecommons.org/licenses/by/4.0/legalcode.en>

Not used as evidence: the Home Assistant integration `EnlightningMan/ha-bsh_tides` was checked as a
pointer per the ticket, but its README documents no endpoints, fields, polling interval or horizon, so
every claim here rests on BSH sources and the live API instead.
