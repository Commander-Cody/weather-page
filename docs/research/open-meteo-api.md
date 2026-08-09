# Open-Meteo: endpoints, parameters and terms for the North Frisian coast

Research for [issue #3](https://github.com/Commander-Cody/weather-page/issues/3). Everything below comes
either from Open-Meteo's own documentation pages, from Open-Meteo's open-source server code, or from live
calls made against the API on **2026-08-09** at coordinates on the North Frisian coast. Every claim carries
its source. Where a live observation and the documentation disagree, both are given.

Test coordinates used throughout:

| Place | Lat | Lon |
| --- | --- | --- |
| Husum | 54.4858 | 9.0517 |
| Hörnum (Sylt) | 54.7566 | 8.2960 |
| List (Sylt) | 54.9010 | 8.3390 |
| Hallig Hooge | 54.5747 | 8.5497 |
| Nordstrand | 54.5330 | 8.9414 |
| Wadden tidal flat E of Föhr | 54.6883 | 8.5750 |
| Wadden tidal flat S of Hooge | 54.5000 | 8.5500 |

---

## 1. Summary of what to build

- **One request per place**, to `https://api.open-meteo.com/v1/forecast`, covers every atmospheric variable
  on the locked list including sunrise/sunset. Hourly and daily blocks come back in the **same** response.
- **Do not pass `models=`.** The default `best_match` already resolves to ICON-D2 (~2 km) for the first
  ~2 days here, then ICON-EU, then ICON Global. Verified empirically (§5).
- **Sea temperature needs a second endpoint**, `https://marine-api.open-meteo.com/v1/marine`. It refreshes
  only **once a day** and its grid does not resolve the Wadden Sea (§6). It also returns plausible-looking
  numbers for points that are dry land, which is a trap (§6.3).
- **Refresh floor is 3 hours**, not 15–30 minutes — that is how often ICON-D2 publishes (§7). Sea
  temperature's floor is 24 hours.
- **Keep the request at 10 variables or fewer.** Open-Meteo's call cost is weighted by variable count;
  10 variables over 7 days is exactly 1.0 calls, 15 variables is 1.5 (§9).
- Limits are **per source IP** (or per Cloudflare Worker), confirmed in the server source (§9).
- A free, ad-free public page is **explicitly listed** by Open-Meteo as qualifying non-commercial use (§8).

---

## 2. Endpoints

| Purpose | Endpoint | Source |
| --- | --- | --- |
| Atmospheric forecast | `https://api.open-meteo.com/v1/forecast` | <https://open-meteo.com/en/docs> |
| Sea surface temperature, waves | `https://marine-api.open-meteo.com/v1/marine` | <https://open-meteo.com/en/docs/marine-weather-api> |
| Model run metadata (free, uncounted) | `https://api.open-meteo.com/data/<model>/static/meta.json` | <https://open-meteo.com/en/docs/model-updates> |

The commercial endpoint is `customer-api.open-meteo.com` with an `apikey` parameter; the free endpoints take
no key. Source: <https://open-meteo.com/en/pricing>.

The model-updates page states: *"Note that API calls to the metadata API are not counted toward daily or
monthly request limits."* (<https://open-meteo.com/en/docs/model-updates>). That makes the metadata endpoint
a free way to detect whether a new model run exists before spending quota on a refetch.

---

## 3. Parameters and units for the locked variable list

All from the "Hourly Parameter Definition" and "Daily Parameter Definition" tables at
<https://open-meteo.com/en/docs>, and confirmed against the `hourly_units` / `daily_units` blocks in the live
responses recorded in §4.

### 3.1 Hourly

| Our variable | API parameter | Valid time (per docs) | Default unit |
| --- | --- | --- | --- |
| Temperature | `temperature_2m` | Instant | `°C` |
| Relative humidity | `relative_humidity_2m` | Instant | `%` |
| Precipitation amount | `precipitation` | Preceding hour sum | `mm` |
| Precipitation probability | `precipitation_probability` | Preceding hour probability | `%` |
| Cloud cover | `cloud_cover` | Instant | `%` |
| Wind speed | `wind_speed_10m` | Instant | `km/h` |
| Wind direction | `wind_direction_10m` | Instant | `°` |
| Wind gusts | `wind_gusts_10m` | **Preceding hour max** | `km/h` |

Two semantics worth carrying into the domain model:

- `wind_gusts_10m` is documented as *"Gusts at 10 meters above ground as a maximum of the preceding hour"*
  and `precipitation` as *"Total precipitation (rain, showers, snow) sum of the preceding hour"*, whereas
  wind speed, direction, temperature, humidity and cloud cover are instantaneous at the stamped hour. On a
  fused time axis, the gust and rain bars belong to the hour *before* their timestamp; the wind arrow belongs
  *at* it. Source: <https://open-meteo.com/en/docs>.
- `precipitation_probability` is **not** at model resolution. The docs say: *"Probability of precipitation
  with more than 0.1 mm of the preceding hour. Probability is based on ensemble weather models with 0.25°
  (~27 km) resolution. 30 different simulations are computed…"* A 27 km cell spans the whole width of the
  North Frisian Wadden Sea, so probability will not distinguish Sylt from the mainland even though wind and
  rain amount (2 km ICON-D2) will. Source: <https://open-meteo.com/en/docs>.

### 3.2 Daily

| Our variable | API parameter | Unit |
| --- | --- | --- |
| Sunrise | `sunrise` | `iso8601` |
| Sunset | `sunset` | `iso8601` |

The docs state that *"If daily weather variables are specified, parameter `timezone` is required."*
(<https://open-meteo.com/en/docs>). In practice the API does **not** reject a daily request without a
timezone — it silently returns GMT days. Observed live:

```
GET https://api.open-meteo.com/v1/forecast?latitude=54.4858&longitude=9.0517&daily=sunrise,sunset&forecast_days=2
{"timezone":"GMT","utc_offset_seconds":0,
 "daily":{"time":["2026-08-09","2026-08-10"],
          "sunrise":["2026-08-09T03:49","2026-08-10T03:51"],
          "sunset":["2026-08-09T19:09","2026-08-10T19:06"]}}
```

Sunrise 03:49 is the GMT rendering of 05:49 local. **Always send `timezone=Europe/Berlin`** — it fixes both
the sunrise/sunset wall-clock values and the midnight boundaries the daily block aggregates over.

### 3.3 Unit and time overrides

From the parameter table at <https://open-meteo.com/en/docs>:

| Parameter | Default | Options |
| --- | --- | --- |
| `temperature_unit` | `celsius` | `fahrenheit` |
| `wind_speed_unit` | `kmh` | `ms`, `mph`, `kn` |
| `precipitation_unit` | `mm` | `inch` |
| `timeformat` | `iso8601` | `unixtime` |
| `timezone` | `GMT` | any IANA name, or `auto` |
| `forecast_days` | `7` | 0–16 |
| `past_days` | `0` | 0–92 |
| `forecast_hours` / `past_hours` | – | integer, anchored on the **current hour** |
| `models` | `auto` | see §5 |
| `cell_selection` | `land` | `sea`, `nearest` |

`wind_speed_unit` applies to gusts as well as mean wind — confirmed live, the response reported
`"wind_speed_10m":"m/s"` **and** `"wind_gusts_10m":"m/s"` from a single `wind_speed_unit=ms`.

`cell_selection` defaults to `land`, which *"finds a suitable grid-cell on land with similar elevation to the
requested coordinates using a 90-meter digital elevation model"* (<https://open-meteo.com/en/docs>). That is
the right default for our places — a Hallig or a harbour should read the land cell, not an offshore one.

---

## 4. The request, and the real response shape

### 4.1 Recommended request (exactly 10 variables → weight 1.0, see §9)

```
https://api.open-meteo.com/v1/forecast
  ?latitude=54.4858&longitude=9.0517
  &timezone=Europe%2FBerlin
  &forecast_days=7
  &wind_speed_unit=ms
  &hourly=temperature_2m,relative_humidity_2m,precipitation,precipitation_probability,cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m
  &daily=sunrise,sunset
```

Live result for Husum on 2026-08-09: HTTP 200, `generationtime_ms` 0.56, **9 654 bytes** of JSON. At ~12
places that is roughly 116 KB of raw JSON per refresh cycle.

### 4.2 Response shape (trimmed, real)

```json
{
  "latitude": 54.48,
  "longitude": 9.059999,
  "generationtime_ms": 1.639,
  "utc_offset_seconds": 7200,
  "timezone": "Europe/Berlin",
  "timezone_abbreviation": "GMT+2",
  "elevation": 10.0,
  "hourly_units": {
    "time": "iso8601", "temperature_2m": "°C", "relative_humidity_2m": "%",
    "precipitation": "mm", "precipitation_probability": "%", "cloud_cover": "%",
    "wind_speed_10m": "m/s", "wind_direction_10m": "°", "wind_gusts_10m": "m/s"
  },
  "hourly": {
    "time":                      ["2026-08-09T00:00", "2026-08-09T01:00", "2026-08-09T02:00", ...168 entries],
    "temperature_2m":            [14.5, 14.1, 13.4, ...],
    "relative_humidity_2m":      [86, 88, 88, ...],
    "precipitation":             [0.0, 0.0, 0.0, ...],
    "precipitation_probability": [0, 0, 0, ...],
    "cloud_cover":               [100, 85, 46, ...],
    "wind_speed_10m":            [2.16, 2.51, 2.42, ...],
    "wind_direction_10m":        [103, 119, 120, ...],
    "wind_gusts_10m":            [4.4, 4.9, 5.9, ...]
  },
  "daily_units": { "time": "iso8601", "sunrise": "iso8601", "sunset": "iso8601" },
  "daily": {
    "time":    ["2026-08-09", "2026-08-10", "2026-08-11", "2026-08-12", "2026-08-13", "2026-08-14", "2026-08-15"],
    "sunrise": ["2026-08-09T05:49", "2026-08-10T05:51", ... 7 entries],
    "sunset":  ["2026-08-09T21:09", "2026-08-10T21:06", ...]
  }
}
```

The layout is **columnar**: one `time` array plus one parallel array per variable, in both the `hourly` and
`daily` objects, with a matching `*_units` object. Documented at <https://open-meteo.com/en/docs> ("JSON
Return Object") and confirmed live.

Note `"latitude": 54.48, "longitude": 9.059999` — the response echoes *the centre of the grid cell used*, not
what you asked for. The docs are explicit: *"WGS84 of the center of the weather grid-cell which was used to
generate this forecast. This coordinate might be a few kilometres away from the requested coordinate."*
This is a useful sanity check to log per place.

### 4.3 Does the hourly/daily split force two requests? No.

One request returns both blocks. `forecast_days=7` gives **168 hourly steps and 7 daily rows** in a single
response — verified live (array lengths 168 and 7).

There is no way to ask for "48 h hourly + 7 days daily" in the natural sense, because `forecast_hours` is
anchored on the *current hour*, not local midnight. Verified live with
`&forecast_days=7&forecast_hours=48` issued at 16:17 UTC:

```
hourly: 48 entries, 2026-08-09T18:00 … 2026-08-11T17:00     <- starts "now", not midnight
daily:  7 entries,  2026-08-09 … 2026-08-15                 <- unaffected
```

Since the page wants "hour-by-hour for today and tomorrow", the simplest correct thing is to request the full
7 days of hourly (which is anchored at 00:00 local when `timezone` is set) and **slice the first 48 entries**
client-side or in the fetch job. Fetching all 168 hours costs nothing extra: the call weight is driven by
variable count and by days, and at 7 days the days term does not bite (§9).

### 4.4 Multiple locations in one HTTP request

Both APIs accept comma-separated coordinate lists and then return a **JSON array** instead of an object:
*"Multiple coordinates can be comma separated… To return data for multiple locations the JSON output changes
to a list of structures."* (<https://open-meteo.com/en/docs/marine-weather-api>). Verified live with 2
locations and again with 200 locations (HTTP 200, array of 200).

This does **not** save quota — the call weight sums per location (§9) — but it does collapse ~12 HTTP
round-trips into one, which matters inside a GitHub Actions job. Whether to use it is a build decision, not a
constraint.

---

## 5. Model choice: don't choose

Documented model table for the DWD provider (<https://open-meteo.com/en/docs/dwd-api>):

| Model | Region | Spatial resolution | Temporal resolution | Forecast length | Update frequency |
| --- | --- | --- | --- | --- | --- |
| ICON Global | Global | 0.1° (~11 km) | Hourly, 3-hourly after 78 h | 7.5 days | Every 6 hours |
| ICON Europe | Europe | 0.0625° (~7 km) | Hourly, 3-hourly after 78 h | 5 days | Every 3 hours |
| ICON D2 | Central Europe | 0.02° (~2 km) | 15-minutely | 2 days | Every 3 hours |

North Frisia is comfortably inside the ICON-D2 domain. The `meta.json` for `dwd_icon_d2` reports a grid
bounding box of `BBOX[43.18, -3.94, 58.08, 20.34]` (lat 43.18–58.08 N, lon 3.94 W–20.34 E), and our
northernmost test point (List, 54.90 N) is ~3.2° inside the northern edge.
Source: <https://api.open-meteo.com/data/dwd_icon_d2/static/meta.json>.

### 5.1 The seamless default already does the right thing — proved

Requesting `temperature_2m` for Husum with no `models` parameter, and separately with
`models=icon_d2,icon_eu,icon_global`, and comparing value by value (UTC, 7 days):

```
2026-08-09T00:00  best=13.4   d2=13.4  ✓   eu=14.1      gl=13.9
2026-08-10T12:00  best=19.8   d2=19.8  ✓   eu=20.5      gl=20.6
2026-08-11T12:00  best=17.8   d2=17.8  ✓   eu=17.9      gl=17.8
2026-08-11T18:00  best=15.9   d2=null      eu=15.9  ✓   gl=16.0
2026-08-13T12:00  best=27.2   d2=null      eu=27.2  ✓   gl=27.3
2026-08-14T18:00  best=26.4   d2=null      eu=null      gl=26.4  ✓
2026-08-15T12:00  best=21.0   d2=null      eu=null      gl=21.0  ✓
```

`best_match` is byte-for-byte ICON-D2 while ICON-D2 has data, then ICON-EU, then ICON Global. **Passing
`models=` would only ever make this worse.** Requested via <https://api.open-meteo.com/v1/forecast>.

Confirmed live that all of `icon_d2`, `icon_eu`, `icon_global`, `icon_seamless` and the longer aliases
(`dwd_icon_d2` etc.) are accepted values. When more than one model is requested the response keys gain a
suffix: `temperature_2m_icon_d2`, `temperature_2m_icon_eu`, … Useful for debugging, not for production.

### 5.2 Observed forecast lengths at Husum (2026-08-09, `forecast_days=16`)

| `models=` | Grid cell returned | Last non-null hour (local) | Non-null hours |
| --- | --- | --- | --- |
| `icon_d2` | 54.48 / 9.0600 | 2026-08-11T12:00 | 61 |
| `icon_eu` | 54.50 / 9.0625 | 2026-08-14T12:00 | 133 |
| `icon_global` | 54.50 / 9.0000 | 2026-08-17T00:00 | 193 |
| `icon_seamless` | 54.48 / 9.0600 | 2026-08-17T00:00 | 193 |

The returned grid cells match the documented resolutions: 0.02° for D2, 0.0625° for EU. The locked horizon
(today + six days = 168 h) sits inside ICON Global's reach and is served by ICON-D2 → EU → Global with no
gaps.

---

## 6. Sea surface temperature and the Wadden Sea

### 6.1 Endpoint and variable

`sea_surface_temperature`, *"The sea surface temperature close to the water surface"*, unit **Celsius**,
valid time **Instant**, on `https://marine-api.open-meteo.com/v1/marine`.
Source: <https://open-meteo.com/en/docs/marine-weather-api>.

Example:

```
https://marine-api.open-meteo.com/v1/marine
  ?latitude=54.7566&longitude=8.2960
  &hourly=sea_surface_temperature
  &timezone=Europe%2FBerlin&forecast_days=2
```

```json
{"latitude":54.791664,"longitude":8.291672,"utc_offset_seconds":7200,
 "timezone":"Europe/Berlin","elevation":0.0,
 "hourly_units":{"time":"iso8601","sea_surface_temperature":"°C"},
 "hourly":{"time":["2026-08-09T00:00","2026-08-09T01:00", ...],
           "sea_surface_temperature":[19.7,19.7,19.6,19.6,19.6,19.5,19.5,19.5, ...]}}
```

### 6.2 Which model actually provides it

The marine docs data-source table lists **"MeteoFrance Sea Surface Temperature — Global — 0.08° (~8 km) —
6-hourly — January 2022 with 10 day forecast — Every 24 hours"**
(<https://open-meteo.com/en/docs/marine-weather-api>).

Probed live which `models=` value carries the field:

| `models=` | `sea_surface_temperature` |
| --- | --- |
| `meteofrance_currents` | **`"°C"`, real values** |
| `meteofrance_wave` | `"undefined"`, all null |
| `ecmwf_wam` | `"undefined"`, all null |
| `dwd_ewam` | `"undefined"`, all null |

So SST rides on the MeteoFrance ocean domain, **not** on any wave model. DWD's higher-resolution EWAM (0.05°,
Europe) gives waves but no SST — there is no finer SST source available on this API.

The observed grid confirms 0.08°: returned cell centres are always on the lattice `k × 0.083333 + 0.041667`,
i.e. 1/12° ≈ 9.3 km in latitude, ~5.4 km in longitude at 54.6 N.

### 6.3 Behaviour over the Wadden Sea and over tidal flats — tested

Requested marine data for real North Frisian places and measured how far the answer's grid cell sits from the
point asked for (`cell_selection` left at the marine default):

| Place | Requested | Returned cell | Shift | `elevation` | SST | `wave_height` |
| --- | --- | --- | --- | --- | --- | --- |
| Hörnum (Sylt) | 54.7566 / 8.2960 | 54.7917 / 8.2917 | 3.9 km | 0 m | 19.7 | 0.54 |
| List (Sylt) | 54.9010 / 8.3390 | 54.8750 / 8.3750 | 3.7 km | 5 m | 19.7 | 0.52 |
| Hallig Hooge | 54.5747 / 8.5497 | 54.5417 / 8.5417 | 3.7 km | 1 m | 20.3 | 0.46 |
| Flat E of Föhr | 54.6883 / 8.5750 | 54.7083 / 8.5417 | 3.1 km | 0 m | 19.9 | 0.34 |
| Nordstrand | 54.5330 / 8.9414 | 54.5417 / 8.7917 | **9.7 km** | −1 m | 20.0 | 0.36 |
| Bredstedt / Wadden edge | 54.6270 / 8.8032 | 54.6250 / 8.7917 | 0.8 km | 0 m | 20.0 | 0.32 |
| **Husum** | 54.4858 / 9.0517 | 54.4583 / 9.0417 | 3.1 km | 10 m | **20.2** | **null** |

Findings:

1. **The whole North Frisian Wadden Sea is one to two grid cells wide.** At 0.08° there is no representation
   of individual tidal basins, priels, or the difference between a flat and a channel. Across a west→east
   transect at 54.60 N the SST moved only 19.4 → 20.1 °C between the open North Sea at 7.8 E and the Wadden
   edge at 8.8 E, with every intermediate cell inside 0.2 K of its neighbours.

2. **There is no wetting and drying.** The underlying models have no tidal flat that falls dry. A point in
   the middle of the flats south of Hooge (54.50 / 8.55) returns a perfectly smooth diurnal SST curve
   interpolated up from the 6-hourly native product:

   ```
   00:00 20.3   01:00 20.2   02:00 20.1   03:00 20.1   04:00 20.0   05:00 20.0
   06:00 19.9   07:00 19.9   08:00 19.9   09:00 19.9   10:00 20.0   11:00 20.0   12:00 20.1
   ```

   Nothing in the response signals that this location is dry for several hours around every low water. The
   number is "the temperature of the nearest 8 km patch of modelled sea", which is the honest way to label
   it. It is **not** "the water temperature at the flats".

3. **Null is not a water mask — this is the trap.** Husum sits ~5 km inland behind the dyke with a DEM
   elevation of 10 m, and the marine API still returns `sea_surface_temperature: 20.2` for it, while
   `wave_height` correctly comes back `null`. Pushing further inland:

   | Point | Elevation | SST | Wave |
   | --- | --- | --- | --- |
   | 54.4583 / 9.2083 (~20 km inland) | 20 m | **20.1** | null |
   | 54.5417 / 9.5417 (Schleswig, ~40 km inland) | 28 m | null | null |
   | 52.5417 / 13.3750 (Berlin) | 37 m | null | null |

   SST keeps answering for tens of kilometres of dry land before it finally gives up. If a place's
   coordinates are ever set slightly wrong, or if a future place is genuinely inland, the page will show a
   confident sea temperature that means nothing. **Guard on the returned `latitude`/`longitude` vs the
   requested pair** (the response always tells you which cell it used) and refuse to display SST beyond a
   chosen distance — the marine API will not refuse for you.

4. **`cell_selection` changes how far it reaches.** The marine parameter table gives the default as `sea`
   (<https://open-meteo.com/en/docs/marine-weather-api>), which *"prefers grid-cells on sea"*. Comparing
   `cell_selection=sea` against `cell_selection=nearest` along the 54.60 N transect: at 54.60 / 9.00 (15 m
   elevation, inland) `sea` silently pulled `wave_height` from the cell at 8.7917 — about 11 km west — while
   `nearest` correctly returned `null`. If the fetch job wants honest nulls rather than nearest-sea
   substitutes, pass `cell_selection=nearest` explicitly.

5. **Coastal accuracy is disclaimed by Open-Meteo itself**: *"Tides and ocean currents are computed at 0.08°
   (~8 km) resolution using numerical models. Accuracy at coastal areas is limited. This is not suitable for
   coastal navigation and does not replace your nautical almanac. Use with caution!"*
   (<https://open-meteo.com/en/docs/marine-weather-api>). The page should label sea temperature as an
   approximate regional value, not a bathing-water reading.

### 6.4 A second, undocumented SST source that must not be used

`sea_surface_temperature` is *also* accepted by the plain weather API and returns values:

```
GET https://api.open-meteo.com/v1/forecast?latitude=54.7566&longitude=8.2960&hourly=sea_surface_temperature
{"latitude":54.760002,"longitude":8.299999,"elevation":0.0,
 "hourly_units":{"sea_surface_temperature":"°C"},
 "hourly":{"sea_surface_temperature":[17.4,17.4,17.6,17.6, ...]}}
```

Two reasons to stay away:

- It **disagrees with the marine API by 2.3 K** at the same point and hour (17.4 °C vs 19.7 °C at Hörnum on
  2026-08-09T00:00 local).
- The string `sea_surface_temperature` **does not appear anywhere** in the HTML of
  <https://open-meteo.com/en/docs> (checked by fetching and searching the page). It is undocumented on that
  endpoint and could change or vanish without notice.

Use the marine endpoint, which documents the field and its provenance.

---

## 7. Publication cadence, and the refresh floor

Documented update frequencies (<https://open-meteo.com/en/docs/dwd-api>,
<https://open-meteo.com/en/docs/marine-weather-api>): ICON-D2 every 3 h, ICON-EU every 3 h, ICON Global every
6 h, MeteoFrance SST every 24 h, MeteoFrance MFWAM every 12 h, DWD EWAM every 12 h.

These are confirmed by the machine-readable metadata endpoints. Snapshot taken 2026-08-09 ~16:26 UTC:

| Model | metadata URL | `update_interval_seconds` | Last run init | Available on API | Latency | Lead time |
| --- | --- | --- | --- | --- | --- | --- |
| ICON-D2 | `/data/dwd_icon_d2/static/meta.json` | 10800 (3 h) | 2026-08-09 15:00 UTC | 16:25 UTC | **85 min** | 49 h |
| ICON-EU | `/data/dwd_icon_eu/static/meta.json` | 10800 (3 h) | 2026-08-09 12:00 UTC | 15:46 UTC | 227 min | 121 h |
| ICON Global | `/data/dwd_icon/static/meta.json` | 21600 (6 h) | 2026-08-09 12:00 UTC | 15:44 UTC | 224 min | 181 h |
| MeteoFrance currents + SST | `/data/meteofrance_currents/static/meta.json` (marine host) | **86400 (24 h)** | 2026-08-09 00:00 UTC | 12:06 UTC | 727 min | 240 h |
| MeteoFrance MFWAM | `/data/meteofrance_wave/static/meta.json` (marine host) | 43200 (12 h) | 2026-08-09 00:00 UTC | 12:05 UTC | 725 min | 243 h |
| DWD EWAM | `/data/dwd_ewam/static/meta.json` (marine host) | 43200 (12 h) | 2026-08-09 12:00 UTC | 15:47 UTC | 227 min | 79 h |

Lead times are `data_end_time − last_run_initialisation_time` and match the documented forecast lengths
(ICON-EU 121 h ≈ "5 days", ICON Global 181 h ≈ "7.5 days"; ICON-D2's 49 h is the documented "2 days").

**Implications for the scheduled job:**

- The fastest-moving thing we consume is **ICON-D2 at every 3 hours**. Open-Meteo additionally advises
  *"wait an additional 10 minutes after the forecast update has been applied"* because its servers are only
  eventually consistent (<https://open-meteo.com/en/docs/model-updates>). So the earliest a refresh can
  return genuinely new atmospheric numbers is roughly every 3 h, at run time + ~95 min.
- A 15–30 min cron is therefore **6 to 12 times more often than the data changes**. It is not harmful — the
  quota is nowhere near strained (§9) — but nothing is gained past ~30 min, and the honest floor is 3 h.
- **Sea temperature must not drive the refresh rate at all.** It publishes once per day with ~12 h latency.
  Fetching it every 30 min is 48 identical responses per day.
- Cheapest correct design: poll `meta.json` (free, uncounted) and only spend quota on a real fetch when
  `last_run_availability_time` has moved. This also gives the page an honest "data from run X" stamp.
- Note that the free and commercial tiers *"operate on different servers, leading to slight variations in
  update times"* (<https://open-meteo.com/en/docs/model-updates>) — the metadata above is from the free host,
  which is the one we use.

---

## 8. Terms, licence and attribution

### 8.1 The non-commercial condition, verbatim

From <https://open-meteo.com/en/terms>, section "Non-Commercial Use" — *"By using the Free API for
non-commercial use you agree to following terms:"*

> - Less than 10'000 API calls per day, 5'000 per hour and 600 per minute.
> - You may only use the free API services for non-commercial purposes.
> - You accept to the CC-BY 4.0 licence, as specified in the licence conditions.
> - We reserve the right to block applications and IP addresses that misuse our service without prior notice.

The same page defines non-commercial *"as elaborated by creative commons"* and then gives examples.
Qualifying as non-commercial:

> - Using our service for private or non-profit websites or apps that do not have subscriptions or advertising.
> - Utilizing our service for personal home automation purposes.
> - Using our service for public research conducted at public institutions.
> - Incorporating our service into educational content.

Counting as commercial:

> - Operating websites or apps that have subscriptions or display advertisements.
> - Integrating our service into commercial products or promotional activities.
> - Conducting undisclosed research at commercial entities.

### 8.2 Is a free public information page unambiguously inside the terms?

**Yes, provided it stays free of advertising, subscriptions and promotion.** The first qualifying example —
"private or non-profit websites… that do not have subscriptions or advertising" — describes this project
exactly: a public page, no accounts, no payment, no ads. Being publicly reachable is not what makes something
commercial in Open-Meteo's framing; monetisation is. The three things that would flip it, per the same list,
are: adding advertising, adding subscriptions, or using the page to promote a commercial product or service.

One nuance worth recording as a constraint rather than a risk: the terms bind the *operator* of the free API
usage. Our architecture already puts every Open-Meteo call in a scheduled server-side job, so the traffic
comes from one identifiable party under one set of terms, rather than from every visitor's browser. That
keeps the non-commercial undertaking clean and, per §9, keeps the quota accounting predictable.

### 8.3 Licence and the exact attribution wording

From <https://open-meteo.com/en/licence>:

> API data are offered under **Attribution 4.0 International (CC BY 4.0)**
>
> You are free to **share**: copy and redistribute the material in any medium or format and **adapt**: remix,
> transform, and build upon the material.
>
> **Attribution:** You must give appropriate credit, provide a link to the licence, and indicate if changes
> were made. …
>
> You must include a link next to any location Open-Meteo data are displayed, for example:

```html
<a href="https://open-meteo.com/">
	Weather data by Open-Meteo.com
</a>
```

That snippet is the wording Open-Meteo itself publishes. Three practical consequences:

- **"next to any location Open-Meteo data are displayed"** is stronger than a single footer line on the
  homepage. Every place page that shows a forecast needs the credit reachable on that page.
- **"indicate if changes were made"** applies to us. Slicing to 48 hours, converting km/h to m/s, and
  re-serving as static JSON are modifications; the credit line should say the data was processed, not
  present it as an untouched feed.
- **"provide a link to the licence"** — the CC BY 4.0 deed, in addition to the Open-Meteo link.

### 8.4 DWD attribution on top of the Open-Meteo credit

The licence page lists the upstream sources and their licences, including *"Atmospheric, ensemble and wave
forecasts from Deutscher Wetterdienst DWD (CC-BY Licence)"* (<https://open-meteo.com/en/licence>).

The marine API docs carry an explicit "Citation & Acknowledgement" block:

> Generated using ICON Wave forecast from the German Weather Service DWD. All users of Open-Meteo data must
> provide a clear attribution to DWD as well as a reference to Open-Meteo.

Source: <https://open-meteo.com/en/docs/marine-weather-api>.

This lines up with the map's plan of a DWD credit line — and note that the DWD credit is now doing double
duty, since the *forecast* we display is ICON, and the *warnings* come from DWD directly. Two caveats:

- That acknowledgement text names ICON Wave because it is rendered on the DWD tab of the marine docs. Our
  actual marine data comes from **MeteoFrance** (§6.2), whose licence is listed separately on the licence
  page. If we display sea temperature, MeteoFrance is the upstream to credit for it, not DWD.
- The licence page mandates only the Open-Meteo link as the displayed attribution; the per-provider credits
  follow from each provider's own licence, which the licence page links out to. The map's three-credit-line
  plan (Open-Meteo, BSH, DWD) is sound; the Open-Meteo line should mention DWD ICON, and MeteoFrance if sea
  temperature ships.

### 8.5 Other terms worth knowing

- Governed by **Swiss law**, operated by OpenMeteo GmbH, Bürglen (UR), Switzerland.
- No warranty of accuracy, completeness or availability; all liability disclaimed.
- Terms can change at any time, effective on posting, but *"All changes are transparently tracked on GitHub."*
- Open-Meteo's own free service *"may collect non-personal information, such as IP addresses"* and keeps web
  server logs, *"which may contain sensitive information such as geographical coordinates"*, deleted after 90
  days. Because our fetch happens server-side, no visitor coordinates ever reach Open-Meteo — a real privacy
  advantage of the scheduled-job architecture, and an argument against the geolocation button ever calling
  Open-Meteo directly from the browser.

All from <https://open-meteo.com/en/terms>.

---

## 9. Rate limits: the numbers, and what they are keyed on

### 9.1 Confirmed limits

<https://open-meteo.com/en/terms> and <https://open-meteo.com/en/pricing> both publish the same table for the
Free / Open-Access tier:

| Window | Free tier limit |
| --- | --- |
| Per minute | 600 calls |
| Per hour | 5 000 calls |
| Per day | 10 000 calls |
| **Per month** | **300 000 calls** |

The 10k/5k/600 figures in the issue are confirmed. **There is a fourth limit the map does not mention: 300 000
calls per month.** At the planned 12 places × 48 refreshes = 576/day, a 31-day month is ~17 900 calls — about
6 % of the monthly allowance. No risk, but it should be written down.

### 9.2 Per-IP, not per-application — confirmed in the source

Open-Meteo's server is open source (AGPLv3, <https://open-meteo.com/en/licence>). The rate limiter is
`Sources/App/Helper/Vapor/RateLimiter.swift`
(<https://github.com/open-meteo/open-meteo/blob/main/Sources/App/Helper/Vapor/RateLimiter.swift>), whose
doc-comment states plainly:

> Limit API request rate for the free API.
> Count how many calls have been made by a **given IP address**.

The defaults are exactly the published ones, overridable by environment variable:

```swift
private static let limitDaily    = Float(Environment.get("CALL_LIMIT_DAILY").flatMap(Int.init)    ?? 10_000)
static        let limitHourly    = Float(Environment.get("CALL_LIMIT_HOURLY").flatMap(Int.init)   ??  5_000)
private static let limitMinutely = Float(Environment.get("CALL_LIMIT_MINUTELY").flatMap(Int.init) ??    600)
static let concurrencyLimit     = Environment.get("CONCURRENCY_LIMIT").flatMap(Int.init)      ?? 1
static let concurrencyLimitHard = Environment.get("CONCURRENCY_LIMIT_HARD").flatMap(Int.init) ?? 5
```

Counters are held per IPv4 address (exact) and per hashed IPv6 address, and are cleared on minute, hour and
day boundaries. There is **no API key and no application identity on the free tier**, so there is nothing
else it could key on.

**One important exception, directly relevant to the map's Cloudflare escape hatch.** In
`Sources/App/Helper/Vapor/ApiKeyManager.swift`
(<https://github.com/open-meteo/open-meteo/blob/main/Sources/App/Helper/Vapor/ApiKeyManager.swift>):

```swift
/// For CloudFlare worker applications, use the `CF-Worker` header for rate limiting instead of IP address
let isCFWorker = RateLimiter.cloudFlareWorkerIPs.contains(address)
…
if isCFWorker, let cfHash = self.headers["CF-Worker"].first?.hashValue { slot = cfHash }
else { slot = address.rateLimitSlot }
```

So if the scheduled job moves to **Cloudflare Workers**, the quota is keyed on the Worker's zone
(`CF-Worker` header), *not* on Cloudflare's shared egress IPs. That is the behaviour we want — running on
Cloudflare will not put us in a bucket with every other Cloudflare Worker. Worth capturing before that swap
is made.

Also from the same file: a request whose weight exceeds the hourly limit is rejected outright with
*"Your API call requests too much data. Please reduce the number of variables, locations and/or weather
models."*, and **failed requests still increment the counter by 1** (*"Some users do infinite retries on
errors!"*). A retry storm in the fetch job burns quota even when every call fails.

### 9.3 A "call" is weighted — this changes how we shape the request

The pricing FAQ says: *"Requests for data covering more than 10 weather variables or extending over a period
of more than 2 weeks for a single location are considered multiple API calls. To calculate the number of API
calls accurately, fractional counts are used. For example, a request for 2 weeks of data with 15 weather
variables will be calculated as 1.5 API calls"* (<https://open-meteo.com/en/pricing>).

The exact formula is in `Sources/App/Helper/Writer/ForecastApiResult.swift`
(<https://github.com/open-meteo/open-meteo/blob/main/Sources/App/Helper/Writer/ForecastApiResult.swift>):

```swift
/// - 14 days of data are considered a weight of 1
/// - 10 weather variables are a weight of 1
/// `weight = max(variables / 10, variables / 10 * days / 14) * locations`
func calculateQueryWeight() -> Float {
    let referenceDays = 14
    let referenceVariables = 10
    return results.reduce(0, {
        let nDays = $1.time.range.durationSeconds / 86400
        let timeFraction = Float(nDays) / Float(referenceDays)
        let variablesFraction = Float(nVariablesTimesDomains) / Float(referenceVariables)
        let weight = max(variablesFraction, timeFraction * variablesFraction)
        return $0 + max(1, weight)
    })
}
```

Reading it out:

- The floor is **1.0 per location**, so nothing is ever cheaper than one call per place.
- Below 14 days the time factor never reduces cost (the `max` keeps `variablesFraction`), so **the horizon is
  free but the variable count is not**. 7 days costs the same as 1 day.
- The variable count is `nVariablesTimesDomains` — **variables × models**. Requesting three ICON models
  triples the cost.
- Locations **sum**, so batching 12 places into one HTTP request costs the same 12 units as 12 requests.

Applied to our design:

| Request | Variables | Weight |
| --- | --- | --- |
| Recommended §4.1 (8 hourly + 2 daily, 7 days) | 10 | **1.0** |
| Same plus 5 daily aggregates | 15 | 1.5 |
| Marine SST only | 1 | 1.0 |

So the recommended shape sits exactly on the free boundary — **adding an eleventh variable starts costing
fractionally more**. The locked variable list fits in 10 with sunrise and sunset if the daily block is kept
to those two and everything else is derived from the hourly arrays in our own job. That is worth doing
anyway, since we control the aggregation semantics that way.

Budget at 12 places, 48 refreshes/day: 576 weather units + 12–48 marine units ≈ 590–620/day against 10 000.
Roughly 6 % of the daily allowance, and the hourly peak (12 units in one minute) is 2 % of the 600/min limit.
Rate limiting genuinely stops being a concern, as the map assumed.

### 9.4 No rate-limit headers

Live responses carry no `X-RateLimit-*` headers of any kind (checked with `curl -D -` against
`api.open-meteo.com/v1/forecast`; the response headers were only `Date`, `Content-Type`,
`Transfer-Encoding`, `Connection`). The fetch job cannot read remaining quota from the response — it must
track its own budget, and treat HTTP 429 as the only signal.

---

## 10. What could not be determined from primary sources

- **Whether rate-limit counters are shared across Open-Meteo's redundant API servers.** The limiter is an
  in-process `actor` holding dictionaries in memory, which implies per-server counting, and the model-updates
  page confirms multiple redundant servers exist. But nothing documents whether a load balancer pins a client
  to one server. Treat the published limits as the binding ones and do not rely on any multiplier.
- **The maximum number of locations per free-tier request.** 200 coordinates were accepted live. The server
  passes an `OpenMeteo.numberOfLocationsMaximum` into each request, but that constant's value was not locatable
  in the repository tree, and GitHub code search was unavailable during this research.
- **Whether the 300 000/month free limit is enforced.** The pricing FAQ says *"A usage statistics portal is
  under development. Until it is available, monthly limits are not enforced"* — but that sentence sits in the
  paid-plan section, so it is unclear whether it also covers the free tier's monthly cap.
- **The native temporal resolution of the SST product.** The marine docs table says the MeteoFrance SST
  product is 6-hourly, but `meteofrance_currents/static/meta.json` reports
  `temporal_resolution_seconds: 3600`. The two could not be reconciled; either way the API serves hourly
  values and Open-Meteo interpolates, so the practical effect is only that sub-6-hourly SST detail is not
  real signal.
- **Which model backs `sea_surface_temperature` on the plain weather API** (§6.4). It is not `icon_d2`,
  `icon_eu` or `ecmwf_ifs025` — all three return `"undefined"` for the field — and the variable is
  undocumented there, so its provenance could not be established. Another reason to use the marine endpoint.
- **Whether `best_match` behaves identically outside Germany.** The ICON-D2 → EU → Global chain was proved at
  Husum only; that is the location that matters here, but the result should not be generalised.

---

## Appendix: reproducible commands

```bash
# 1. The recommended per-place request
curl "https://api.open-meteo.com/v1/forecast?latitude=54.4858&longitude=9.0517\
&timezone=Europe%2FBerlin&forecast_days=7&wind_speed_unit=ms\
&hourly=temperature_2m,relative_humidity_2m,precipitation,precipitation_probability,\
cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=sunrise,sunset"

# 2. Proof that best_match == ICON-D2 -> ICON-EU -> ICON Global
curl "https://api.open-meteo.com/v1/forecast?latitude=54.4858&longitude=9.0517\
&hourly=temperature_2m&forecast_days=7&timezone=UTC"
curl "https://api.open-meteo.com/v1/forecast?latitude=54.4858&longitude=9.0517\
&hourly=temperature_2m&forecast_days=7&timezone=UTC&models=icon_d2,icon_eu,icon_global"

# 3. Sea surface temperature at Hoernum
curl "https://marine-api.open-meteo.com/v1/marine?latitude=54.7566&longitude=8.2960\
&hourly=sea_surface_temperature&timezone=Europe%2FBerlin&forecast_days=2"

# 4. The land-point trap: Husum returns an SST but no waves
curl "https://marine-api.open-meteo.com/v1/marine?latitude=54.4858&longitude=9.0517\
&hourly=sea_surface_temperature,wave_height&forecast_days=1"

# 5. Wadden transect, honest nulls vs nearest-sea substitution
curl "https://marine-api.open-meteo.com/v1/marine?latitude=54.6,54.6,54.6,54.6\
&longitude=8.6,8.8,9.0,9.2&hourly=sea_surface_temperature,wave_height\
&forecast_days=1&cell_selection=nearest"

# 6. Model run timings (free, not counted against quota)
curl "https://api.open-meteo.com/data/dwd_icon_d2/static/meta.json"
curl "https://api.open-meteo.com/data/dwd_icon_eu/static/meta.json"
curl "https://api.open-meteo.com/data/dwd_icon/static/meta.json"
curl "https://marine-api.open-meteo.com/data/meteofrance_currents/static/meta.json"
```

---

*Researched 2026-08-09 against <https://open-meteo.com> documentation, the
<https://github.com/open-meteo/open-meteo> server source, and live calls to the free API.*
