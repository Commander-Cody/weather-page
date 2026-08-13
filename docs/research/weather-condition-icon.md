# The weather condition icon: where the code comes from, and which icons the page needs

Research for [issue #11](https://github.com/Commander-Cody/weather-page/issues/11). Everything below comes
either from Open-Meteo's own documentation, from Open-Meteo's AGPLv3 server source, or from live calls made
against the free API on **2026-08-13**. Every claim carries its source. Where documentation and observed
behaviour disagree, both are given.

Two data sets underlie the numbers:

| Set | What | Size |
| --- | --- | --- |
| **Live 7-day** | All 20 places from [`docs/places.md`](../places.md), `best_match`, 2026-08-13 → 2026-08-19 | 20 × 168 h = 3 360 hourly codes, 140 daily codes |
| **One year** | Husum, Hörnum, Helgoland, List via the Historical Forecast API, 2025-08-01 → 2026-07-31 | 4 × 8 760 h = 35 040 hourly codes, 4 × 365 daily codes |

The one-year set is drawn from `historical-forecast-api.open-meteo.com`, which archives the *forecasts
Open-Meteo actually served* — not a reanalysis. It is therefore the closest available answer to "what would
this page have shown last year". Source: <https://open-meteo.com/en/docs/historical-forecast-api>.

---

## 1. Verdict up front

**Take `weather_code` as an hourly variable. Do not take it as a daily variable. Do not derive it.**

- `weather_code` is available hourly **and** daily on `best_match` across the whole 7-day horizon, with no
  nulls at any of the 20 places (§2).
- **Adding hourly `weather_code` costs exactly 0.1 of a call per place per refresh** — the request goes from
  10 variables to 11, weight 1.0 → 1.1. At 20 places × 8 refreshes/day that is 176 units/day against a 10 000
  limit, 1.8 % (§5).
- **Deriving the condition from the locked variables cannot work**, and this is not an argument — it is
  measured. Open-Meteo already does exactly that derivation for models that carry no native code, and the
  result at Husum over one year is **0 hours of fog, 0 of thunderstorm, 0 of showers**, against 226, 29 and
  286 hours from the native DWD code at the same point and year (§6).
- **Do not take the daily `weather_code`.** Its aggregation is a plain numeric `max` over the 24 hourly codes
  — confirmed in the server source and on 870/870 day-place pairs. On 37 % of days at Husum the code the day
  card would carry is true for **two hours or fewer out of 24** (§4). The day card needs its own rule,
  computed in the fetch job from the hourly array it already slices. That also costs nothing.
- **`is_day` is redundant.** It is pure solar geometry — no data is read — and it reproduces from the
  already-locked `sunrise`/`sunset` on 100 % of steps once a minute-rounding artefact at the sunset hour is
  handled (§7). Skip it and save the 0.1.

**And one finding the ticket did not anticipate, which is the most important thing in this document:**

> **`best_match` is not ICON at every place. Three of the twenty — List, Westerland and Neukirchen — are
> served by MET Norway Nordic, whose weather codes come from a different generator and use a visibly
> different vocabulary.** Over a full year, List records **667 hours of drizzle and zero hours of fog,
> showers or thunderstorm**, while Hörnum 25 km down the same island records **10 hours of drizzle, 134 of
> fog, 311 of showers and 25 of thunderstorm** (§3). Two places on Sylt will show different icon families for
> the same weather. This complicates, but does not overturn, the §5 finding of [the #3
> research](open-meteo-api.md).

---

## 2. `weather_code` on Open-Meteo

### 2.1 It exists, hourly and daily, and it is documented

From the "Hourly Parameter Definition" and "Daily Parameter Definition" tables at
<https://open-meteo.com/en/docs>:

> Hourly `weather_code` — "Weather condition as a numeric code. Follow WMO weather interpretation codes."
>
> Daily `weather_code` — "The most severe weather condition on a given day"

The response labels the unit `"wmo code"`. Live at Husum:

```
GET https://api.open-meteo.com/v1/forecast?latitude=54.4764&longitude=9.0514
    &timezone=Europe%2FBerlin&forecast_days=2&hourly=weather_code,is_day&daily=weather_code

"hourly_units": {"time":"iso8601","weather_code":"wmo code","is_day":""}
"hourly":  {"weather_code":[0,0,0,0,0,1,0,1,1,0,2,0,1,1,0,0,0,0,0,0,0,0,0,0, ...]}
"daily_units": {"time":"iso8601","weather_code":"wmo code"}
"daily":   {"time":["2026-08-13","2026-08-14"],"weather_code":[2,3]}
```

**Note the daily description already contradicts the implementation.** "The most severe weather condition"
is not what the code does — see §4.

### 2.2 Coverage across the horizon: no gaps

Requested all 20 places, `forecast_days=7`, `best_match`. **Zero nulls in 3 360 hourly steps and 140 daily
rows.** The ICON-D2 → ICON-EU → ICON Global handover leaves no hole in `weather_code`, exactly as it leaves
none in `temperature_2m` (verified at Husum, List and Helgoland; last non-null ICON-D2 hour
2026-08-15T18:00, last non-null ICON-EU hour 2026-08-18T12:00, `best_match` non-null throughout).

### 2.3 The closed list Open-Meteo can emit — 28 values

This is the authoritative list, from the server source rather than the general WMO table. `WeatherCode` is a
Swift `enum … : Int`, so **no value outside it can ever be returned**:

```swift
enum WeatherCode: Int {
    case clearSky = 0
    case mainlyClear = 1
    case partlyCloudy = 2
    case overcast = 3
    case fog = 45
    case depositingRimeFog = 48
    case lightDrizzle = 51
    case moderateDrizzle = 53
    case denseDrizzle = 55
    case lightFreezingDrizzle = 56
    case moderateOrDenseFreezingDrizzle = 57
    case lightRain = 61
    case moderateRain = 63
    case heavyRain = 65
    case lightFreezingRain = 66
    case moderateOrHeavyFreezingRain = 67
    case slightSnowfall = 71
    case moderateSnowfall = 73
    case heavySnowfall = 75
    case snowGrains = 77
    case slightRainShowers = 80
    case moderateRainShowers = 81
    case heavyRainShowers = 82
    case slightSnowShowers = 85
    case heavySnowShowers = 86
    case thunderstormSlightOrModerate = 95
    case thunderstormStrong = 96
    case thunderstormHeavy = 99
}
```

Source: `Sources/App/Helper/WeatherCode.swift`,
<https://github.com/open-meteo/open-meteo/blob/main/Sources/App/Helper/WeatherCode.swift>.

**28 values.** The general WMO 4677 table has 100. Everything in the 4x, 5x, 6x, 7x, 8x, 9x decades that is
not in this enum — 46, 47, 49, 52, 54, 58, 59, 62, 64, 68, 69, 70, 72, 74, 76, 78, 79, 83, 84, 87–94, 97, 98
— **cannot occur**. The docs table at <https://open-meteo.com/en/docs> lists exactly these 28 and no others,
and adds one restriction:

> *Note: Thunderstorm forecasts with hail are only available in Central Europe*

which matches §3: the MET Norway places never produce 95/96 at all.

### 2.4 Where the code comes from is model-dependent — this is the root of §3

There are two distinct provenances, and it matters which one a place gets:

1. **DWD ICON supplies a native significant-weather field** (`ww`). Open-Meteo post-corrects it rather than
   computing it. The correction function is explicit about the model's quirks:

   ```swift
   /// DWD ICON weather codes show rain although precipitation is 0
   /// Similar for snow at +2°C or more
   func correctDwdIconWeatherCode(temperature_2m: Float, precipitation: Float, snowfallHeightAboveGrid: Bool) -> WeatherCode {
       if precipitation <= 0 && self.isPrecipitationEvent {
           // Weather code shows drizzle, but no precipitation, demote to overcast
           return .overcast
       }
       …
   ```

2. **Models with no native code get one computed** by `WeatherCode.calculate(…)` from cloud cover,
   precipitation, convective precipitation, snowfall, gusts, CAPE, lifted index, convective inhibition,
   boundary-layer height, visibility and categorical freezing rain. That function is reproduced in §6 — it is
   the single most useful primary source in this whole investigation, because it is Open-Meteo's own answer
   to "derive it from what you already have".

MET Norway Nordic falls in category 2: `Sources/App/MetNo/MetNoDomain.swift`
(<https://github.com/open-meteo/open-meteo/blob/main/Sources/App/MetNo/MetNoDomain.swift>) contains **no
weather-code variable at all** — the string `weather` does not appear in the file.

---

## 3. `best_match` is not ICON everywhere — three places are MET Norway

### 3.1 What was observed

Requested `weather_code` and `temperature_2m` for eleven places with no `models` parameter, then again with
`models=icon_d2,icon_eu,icon_global,metno_nordic,knmi_harmonie_arome_europe,ecmwf_ifs025,dmi_harmonie_arome_europe,ukmo_uk_deterministic_2km`,
and asked which model's temperature matches `best_match` **bit for bit** over the first 48 hours:

| Place | Lat | `best_match` == `icon_d2` | `best_match` == `metno_nordic` |
| --- | --- | --- | --- |
| `list` | 55.0189 | 0/48 | **48/48** |
| `neukirchen` | 54.9139 | 2/48 | **48/48** |
| `westerland` | 54.9079 | 1/48 | **48/48** |
| `klanxbuell` | 54.8578 | **48/48** | 3/48 |
| `hoernum` | 54.7561 | **48/48** | 3/48 |
| `dagebuell` | 54.7278 | **48/48** | 2/48 |
| `wyk` | 54.6906 | **48/48** | 1/48 |
| `hooge` | 54.5747 | **48/48** | 3/48 |
| `husum` | 54.4764 | **48/48** | 8/48 |
| `toenning` | 54.3167 | **48/48** | 0/48 |
| `helgoland` | 54.1825 | **48/48** | 5/48 |

The switch is a clean latitude cut, independent of longitude. Scanned at four longitudes (8.30, 8.44, 8.74,
9.05) in 0.005° steps:

```
lat 54.8900 (returned cell 54.88)      d2=24/24  metno= 0/24  -> icon_d2
lat 54.8950 (returned cell 54.88)      d2=24/24  metno= 1/24  -> icon_d2
lat 54.9000 (returned cell 54.89677)   d2= 1/24  metno=24/24  -> metno_nordic
lat 54.9050 (returned cell 54.90564)   d2= 0/24  metno=24/24  -> metno_nordic
```

**The boundary is at 54.90 N**, and the returned coordinate is the tell: below it the response echoes a
multiple of 0.02° (the ICON-D2 lattice); above it a Lambert-conformal cell centre such as 54.89677. The
MET Nordic grid is `PROJCRS["Lambert Conic Conformal" … BBOX[52.302723,1.918457,72.18527,41.764282]]`
(<https://api.open-meteo.com/data/metno_nordic_pp/static/meta.json>), so the domain reaches far south of the
cut; the cut is Open-Meteo's own preference ordering, not the grid edge.

This is **not transient**. Re-checked against the archive for January 2026 at List: `best_match` temperature
equals `metno_nordic` on **744/744 hours** and `icon_d2` on 89/744.

### 3.2 What it does to the icons

The vocabularies barely overlap. One year, same coast:

| Code group | List (metno) | Hörnum (ICON) | Husum (ICON) | Helgoland (ICON) |
| --- | --- | --- | --- | --- |
| 45/48 fog | **0 h** | 134 h | 226 h | 123 h |
| 51/53/55 drizzle | **933 h** | 16 h | 25 h | 16 h |
| 61/63/65 rain | 158 h | 872 h | 857 h | 897 h |
| 80/81/82 rain showers | **0 h** | 317 h | 286 h | 307 h |
| 85/86 snow showers | **0 h** | 31 h | 19 h | 19 h |
| 95/96 thunderstorm | **0 h** | 25 h | 29 h | 36 h |
| 71/73/75/77 snow | 89 h | 125 h | 181 h | 142 h |

And in the live 7-day sample the two families sit side by side on the same island, same days:

```
place                     daily codes 2026-08-13 .. 2026-08-19   model
westerland                [2, 3, 3, 51, 51, 53, 55]              metno_nordic
list                      [2, 3, 3, 51, 53, 55, 55]              metno_nordic
hoernum                   [2, 3, 61, 80, 61, 80, 61]             icon_d2 -> eu -> global
wittduen                  [2, 3, 61,  3, 61, 80, 61]             icon_d2 -> eu -> global
```

Westerland and Hörnum are **17 km apart on Sylt**. For 2026-08-16 one says *dense drizzle* and the other says
*slight rain showers*. A reader comparing two Sylt pages sees a difference that is an artefact of model
selection, not weather.

The mechanism is visible in `WeatherCode.calculate`: with no native code, precipitation of 0.01–0.5 mm/h maps
to `lightDrizzle` (51) and only ≥1.3 mm/h reaches `lightRain` (61). ICON's native `ww` uses DWD's own,
different thresholds. So the MET Norway places are systematically shifted one intensity band "down" into
drizzle.

**This does not mean pass `models=icon_d2`.** [The #3 research](open-meteo-api.md) proved `best_match` is
byte-for-byte the best available model at Husum, and it explicitly flagged *"Whether `best_match` behaves
identically outside Germany"* as undetermined. It turns out not to. But forcing ICON at List would trade a
consistent vocabulary for a worse forecast, and ICON-D2 only reaches 49 h anyway. The honest options are in
§9.4 and the decision belongs to a human.

---

## 4. The daily `weather_code` is a numeric `max`, and it is often wrong for a day card

### 4.1 Primary source

`Sources/App/Controllers/VariableDaily.swift`
(<https://github.com/open-meteo/open-meteo/blob/main/Sources/App/Controllers/VariableDaily.swift>):

```swift
case .weathercode, .weather_code:
    return .max(.surface(.init(.weathercode, 0)))
```

and `Sources/App/Helper/GenericDailyCalculator.swift`
(<https://github.com/open-meteo/open-meteo/blob/main/Sources/App/Helper/GenericDailyCalculator.swift>):

```swift
/// Max/Min require sampling to 1h data
let time1h = timeDaily.with(dtSeconds: 3600)
…
case .max(let variable):
    guard let data = try await reader.get(variable: variable, time: time1h) else { return nil }
    return DataAndUnit(data.data.max(by: 24), data.unit)
```

So: **resample to hourly, take the arithmetic maximum of the 24 numbers.** Not most-severe, not weighted, not
duration-aware. Confirmed empirically on **140/140** live day-place pairs and **365/365** archived days at
each of Husum and List.

The documented description — *"The most severe weather condition on a given day"* — is therefore inaccurate.
Numeric order is not severity order. Within the 28-value list the inversions include:

| Ranks above | …despite being less severe than |
| --- | --- |
| 77 snow grains | 75 heavy snowfall |
| 80 slight rain showers | 65 heavy rain, 67 freezing rain, 75 heavy snowfall |
| 85 slight snow showers | 82 heavy rain showers |
| 51 light drizzle | 48 depositing rime fog |

The one that bites on this coast is **80 over 61–65**: a day of steady rain with one hour of showers in it
reports "slight rain showers".

### 4.2 How thin the daily code actually is

Hours out of 24 that actually carry the daily code:

| | live, 20 places × 7 d | Husum, 365 d | List, 365 d |
| --- | --- | --- | --- |
| median | 3 | 4 | 3 |
| code true for ≤ 2 h of 24 | 25/140 (18 %) | **136/365 (37 %)** | **161/365 (44 %)** |
| code true for ≤ 4 h of 24 | 76/140 (54 %) | 198/365 (54 %) | 215/365 (59 %) |
| code true for exactly 1 h | 13/140 (9 %) | — | — |

Worked examples from the live set:

```
pellworm  2026-08-17  daily=80 "slight rain showers"
          hourly = {2:3, 3:3, 61:12, 80:6}, day total 10.8 mm, of which only 1.8 mm fell in the code-80 hours
husum     2026-08-18  daily=95 "thunderstorm"
          hourly = {2:3, 3:9, 61:6, 80:3, 95:3}  -> thunderstorm is 3 hours of 24
westerland 2026-08-13 daily=2  "partly cloudy"
          hourly = 23 h of code 0/1, one single hour of code 2
```

Across a year at Husum the daily code says *thunderstorm* on 17 days and *showers* on 88. Those are real wet
days (median 6 and 5 wet hours respectively), but a duration-aware rule reclassifies **23 of the 88 shower
days and 13 of the 64 rain days as merely overcast**, because the precipitation lasted under three hours.

### 4.3 What to do instead

Take the hourly array — the fetch job already slices it for the 48-hour lane — and compute the day card's
state in our own code. A candidate rule, tested against the year:

> Collapse each hourly code to its icon state (§9). Take the **most severe state that occupies at least 3 of
> the 24 hours**; if no state reaches 3 hours, take the most severe state present.

Agreement with Open-Meteo's daily max: 221/365 days at Husum (61 %), 251/365 at List (69 %). The differences
are all in the intended direction — see the table in §4.2. This is a *candidate*, not a decision: the 3-hour
threshold, the severity order, and whether to weight daylight hours more heavily are all open (see Open
question 4).

This is also the answer to the ticket's question about whether one icon set serves both rows. **The set is
the same; the aggregation is not.** The hourly row shows the code for that hour. The day card shows a
summary we compute.

---

## 5. The cost, precisely

### 5.1 What counts as a variable

`Sources/App/Controllers/ForecastapiController.swift`
(<https://github.com/open-meteo/open-meteo/blob/main/Sources/App/Controllers/ForecastapiController.swift>):

```swift
let nVariables = (nParamsHourly + nParamsMinutely + nParamsCurrent + nParamsDaily)
                 * domains.reduce(0, { $0 + $1.countEnsembleMember }) + nVariableNonEnsemble
```

It is a **count of requested parameter names**. It does not matter whether a variable is a stored model field
or computed on the fly — `is_day`, which reads no data at all (§7), still counts as one. Hourly and daily
parameters are summed into the same total, so hourly `weather_code` and daily `weather_code` are two
variables, not one.

Fed into `calculateQueryWeight()` in `Sources/App/Helper/Writer/ForecastApiResult.swift`
(<https://github.com/open-meteo/open-meteo/blob/main/Sources/App/Helper/Writer/ForecastApiResult.swift>),
quoted in full by [the #3 research §9.3](open-meteo-api.md):

```
weight per location = max(1, max(variables/10, variables/10 × days/14))
```

At 7 days the time term is 0.5 and never binds, so **weight = variables / 10**, floored at 1.

### 5.2 The arithmetic

| Request | Variables | Weight/place | Response bytes (Husum, measured) |
| --- | --- | --- | --- |
| Locked list, §4.1 of the #3 research | 10 | **1.0** | 9 742 |
| **+ hourly `weather_code`** | **11** | **1.1** | **10 149** |
| + daily `weather_code` as well | 12 | 1.2 | 10 210 |
| + `is_day` as well | 13 | 1.3 | 10 564 |

### 5.3 Budget at the real roster

20 places (not the 12 the #3 research assumed), 8 refreshes/day at the 3-hour ICON-D2 floor:

| | Units/day | Units/month (31 d) | % of 10 000/day | % of 300 000/month |
| --- | --- | --- | --- | --- |
| 10 variables | 160 | 4 960 | 1.6 % | 1.7 % |
| **11 variables (recommended)** | **176** | **5 456** | **1.8 %** | **1.8 %** |
| 13 variables | 208 | 6 448 | 2.1 % | 2.1 % |
| + marine SST, 1 var, 1 refresh/day | +20 | +620 | | |

**The eleventh variable costs 16 units a day.** The ticket's concern that "adding a variable has a cost" is
correct in principle and negligible in this instance — the binding constraint is nowhere near. The reason to
still stop at 11 rather than 13 is not quota, it is that the other two variables are things we can compute
better ourselves (§4.3, §7).

Peak minute load is unchanged at 20 units, 3.3 % of the 600/min limit.

---

## 6. The derive-it alternative, measured

### 6.1 Open-Meteo's own derivation is the primary source

`WeatherCode.calculate(…)` in `Sources/App/Helper/WeatherCode.swift` is precisely the function the ticket's
second option proposes to write. Its signature is the finding:

```swift
public static func calculate(cloudcover: Float, precipitation: Float, convectivePrecipitation: Float?,
    snowfallCentimeters: Float, gusts: Float?, cape: Float?, liftedIndex: Float?,
    convectiveInhibition: Float?, pblHeight: Float?, visibilityMeters: Float?,
    categoricalFreezingRain: Float?, modelDtSeconds: Int, latitude: Float) -> WeatherCode?
```

and its body, in order of precedence:

```swift
if let cape {
    let thunderstroms = calculateThunderstormProbability(convectivePrecipitation:…, cape:…,
                            liftedIndex:…, convectiveInhibition:…, pblHeight:…, gusts:…)
    if thunderstroms > 85 { return .thunderstormStrong }
    if thunderstroms > 60 { return .thunderstormSlightOrModerate }
}
if let categoricalFreezingRain, categoricalFreezingRain >= 1 { … }   // 56/57/66/67
if (convectivePrecipitation ?? 0) > 0 || (cape ?? 0) >= 800 { … }    // 80/81/82, 85/86
switch snowfallCentimeters / modelDtHours { … }                      // 71/73/75
switch precipitation / modelDtHours {
case 0.01..<0.5:  return .lightDrizzle       // 51
case 0.5..<1.0:   return .moderateDrizzle    // 53
case 1.0..<1.3:   return .denseDrizzle       // 55
case 1.3..<2.5:   return .lightRain          // 61
case 2.5..<7.6:   return .moderateRain       // 63
case 7.6...:      return .heavyRain          // 65
default: break }
if let visibilityMeters, visibilityMeters <= 1000 { return .fog }    // 45
switch cloudcover {
case 0..<20:  return .clearSky        // 0
case 20..<50: return .mainlyClear     // 1
case 50..<80: return .partlyCloudy    // 2
case 80...:   return .overcast        // 3
default: break }
```

Read against the locked variable list, this says plainly:

- **Cloud cover alone gives codes 0/1/2/3 and nothing else.** The thresholds 20/50/80 are Open-Meteo's, and
  they are the only part of the derivation the locked variables can reproduce.
- **Fog needs `visibility`.** There is no cloud-cover proxy — see §6.3.
- **Thunderstorm needs `cape`, and ideally `lifted_index`, `convective_inhibition`, `boundary_layer_height`.**
- **Showers vs rain needs `showers`** (convective precipitation) or CAPE ≥ 800.
- **Snow needs `snowfall`**, in centimetres, not `precipitation` in mm.
- **Freezing precipitation needs a categorical freezing-rain field.**

Those extra fields are available on the API — verified live, all non-null at Husum for 168 h:
`visibility` (m), `cape` (J/kg), `lifted_index`, `convective_inhibition` (J/kg), `boundary_layer_height` (m),
`snowfall` (cm), `showers` (mm), `freezing_level_height` (m). **But at List, `lifted_index` and
`freezing_level_height` come back `"undefined"` and all-null** — the MET Norway domain does not carry them.

So a faithful derivation needs **six to eight extra variables** where taking the code needs one. That is
weight 1.7–1.9 per place against 1.1. **Deriving is strictly more expensive than not deriving**, before any
question of whether our thresholds are defensible.

### 6.2 What a degraded derivation actually produces — the decisive measurement

We do not have to speculate about what happens if we derive from cloud cover and precipitation only, because
Open-Meteo runs that experiment for us. The ERA5 archive carries no native weather code and no visibility,
CAPE or convective-precipitation fields on that path, so `archive-api` codes are computed from cloud cover,
precipitation and snowfall — almost exactly the ticket's proposal.

**Husum, the same point, the same year, the two sources side by side:**

| Group | DWD native `ww` (via `best_match`) | Open-Meteo derived (ERA5) |
| --- | --- | --- |
| 45/48 fog | **226 h** | **0 h** |
| 51–57 drizzle | 25 h | **1 528 h** |
| 61–67 rain | 861 h | 155 h |
| 71–77 snow | 181 h | 182 h |
| 80–82 rain showers | **286 h** | **0 h** |
| 85/86 snow showers | 19 h | **0 h** |
| 95–99 thunderstorm | **29 h** | **0 h** |
| 0–3 dry | 7 133 h | 6 895 h |

Derivation from the locked variables **loses fog, showers, snow showers and thunderstorm entirely**, and
converts five sixths of the rain into drizzle. It keeps snow, because snowfall is in the mix there and would
not be in ours. The three states an icon most needs to communicate wordlessly on this coast — fog,
thunderstorm, and "showers, so it will pass" — are exactly the three that vanish.

### 6.3 Why the individual distinctions fail, from the sampled data

**Fog is not high cloud cover.** Husum, one year:

| | n | cloud cover p10 / median / p90 | RH p10 / median | wind median |
| --- | --- | --- | --- | --- |
| 45/48 fog | 226 h | 49 / 100 / 100 % | 96 / 99 % | 1.5 m/s |
| 3 overcast | 4 055 h | 87 / 100 / 100 % | 64 / 83 % | 4.5 m/s |

**58 of the 226 fog hours have cloud cover below 80 %** — a cloud-cover rule would render them "partly
cloudy" or "clear". Humidity plus low wind separates the bulk of the rest, but relative humidity is on the
locked list and wind is too, so a *fog-ish* heuristic is buildable; it would just be ours to defend, and it
would disagree with the model's own visibility field roughly a quarter of the time at the boundary.

**Thunderstorm is not heavy rain.** Husum, one year:

| | n | precipitation p10 / median / p90 mm/h | cloud p10 / median | gusts median |
| --- | --- | --- | --- | --- |
| 95/96 thunderstorm | 29 h | 0.10 / 3.40 / 11.00 | 91 / 100 % | 10.4 m/s |
| 61 light rain | 824 h | 0.10 / 0.30 / 1.20 | 98 / 100 % | 10.6 m/s |
| 80 slight showers | 283 h | 0.00 / 0.10 / 0.60 | 79 / 98 % | 11.9 m/s |

Thunderstorm hours are wetter on average but the p10 is 0.10 mm/h — identical to light rain — and the gust
distribution is *lower* than showers. There is no threshold in precipitation, cloud or wind that isolates
them. In the live 7-day sample the overlap is total:

```
cloud 80-100 %, precip 0.5-1.0 mm/h -> codes {3: 9, 53: 15, 61: 93, 80: 39, 95: 6}
cloud 80-100 %, precip 1.0-1.3 mm/h -> codes {55: 18, 61: 43, 80: 12, 95: 7}
cloud 80-100 %, precip 0.0-0.5 mm/h -> codes {2: 12, 3: 125, 51: 51, 61: 124, 80: 66}
```

Five different codes come out of one (cloud, precipitation) cell. The full table is in the appendix.

**Showers vs rain is not separable at all** from the locked variables — 80 and 61 overlap in cloud,
precipitation and wind. This matters more than it sounds on a page whose purpose is finding the good window:
"showers" means the gap is coming, "rain" means it is not.

**Snow vs rain is the one derivation that would work.** Husum, one year: snow codes span −7.1 to +0.9 °C,
rain codes +0.3 to +28.1 °C. Only 39 of 1 143 rain hours fall at ≤2 °C and **no** snow hour is above 2 °C. A
temperature cut near 1 °C separates them cleanly — but only *given* that precipitation is happening, which is
the part that needs the code.

### 6.4 A caution the code carries into the fused chart

The code and the precipitation amount are **independently sourced and do not always agree**. Husum, one year:

- **193 of 1 372 precipitating-code hours (14.1 %) report 0.0 mm** in the same hour.
- 28 of 7 388 dry-code hours (0.4 %) report more than 0 mm.
- Overall the two disagree on **221 of 8 760 hours (2.5 %)**.

This is not a one-hour alignment artefact — testing the same comparison with the code shifted ±1 hour makes
it worse, not better (42 → 86 or 116 mismatches in the live sample), so it is not the interval-vs-instant
semantics the #3 research flagged for gusts and rain. It is genuine disagreement between DWD's `ww` field and
DWD's precipitation field, which Open-Meteo only partly patches over (`correctDwdIconWeatherCode` demotes to
overcast when precipitation is exactly zero, and evidently the rounding lets some through).

**On the overview screen this is visible.** An hour can carry a rain icon above an empty rain bar. Whether to
suppress the icon, suppress the bar, or let them disagree is a design decision that did not exist before the
icon did (Open question 6).

---

## 7. Day and night variants, and `is_day`

### 7.1 `is_day` reads no data

`Sources/App/Controllers/ForecastapiController.swift`:

```swift
case .is_day:
    let isDay = Zensun.calculateIsDay(timeRange: timeHourlyRead, lat: readerHourly.modelLat, lon: readerHourly.modelLon)
    return .init(variable: variable, unit: .dimensionlessInteger, variables: [ApiArray.float(isDay)])
```

and `Sources/App/Helper/Solar/SunRiseSet.swift`
(<https://github.com/open-meteo/open-meteo/blob/main/Sources/App/Helper/Solar/SunRiseSet.swift>):

```swift
public static func calculateIsDay(timeRange: TimerangeDt, lat: Float, lon: Float) -> [Float] {
    …
    case .transit(rise: let rise, set: let set):
        let secondsSinceMidnight = time.add(universalUtcOffsetSeconds).secondsSinceMidnight
        return secondsSinceMidnight > (rise + universalUtcOffsetSeconds) && secondsSinceMidnight < (set + universalUtcOffsetSeconds) ? 1 : 0
```

It calls `calculateSunTransit` — **the same function that produces the `sunrise` and `sunset` daily
variables** we already request. Documented as *"1 if the current time step has daylight, 0 at night."*
(<https://open-meteo.com/en/docs>).

### 7.2 It is redundant, verified

Reconstructing `is_day` as `sunrise < t < sunset` from the already-locked daily variables reproduces it on
**3 350 of 3 360** hourly steps (99.70 %) across the 20 places. All 10 mismatches are the same artefact:

```
('husum',      '2026-08-13T21:00', is_day=1, derived=0, sunrise='2026-08-13T05:56', sunset='2026-08-13T21:00')
('list',       '2026-08-15T21:00', is_day=1, derived=0, sunrise='2026-08-15T06:01', sunset='2026-08-15T21:00')
```

The `sunset` string is truncated to the minute, so a true sunset of 21:00:38 is published as `21:00` and a
strict `<` comparison flips the 21:00 step. **Treating the boundary hour as day makes the reconstruction
exact.** `is_day` costs 0.1 of a call and buys nothing.

### 7.3 Which states actually need a night form

Husum, one year, split by `is_day`:

| Code | Day h | Night h | Needs a night form? |
| --- | --- | --- | --- |
| 0 clear sky | 517 | 490 | **yes** — a sun at 02:00 is wrong |
| 1 mainly clear | 441 | 295 | **yes** |
| 2 partly cloudy | 798 | 537 | **yes** |
| 3 overcast | 2 020 | 2 035 | no — no sun in the mark |
| 45/48 fog | 83 | 143 | optional; fog is commoner at night |
| 51–55 drizzle | 7 | 18 | no |
| 61–65 rain | 374 | 483 | no |
| 71–77 snow | 85 | 96 | no |
| 80/81 showers | 160 | 126 | optional — the usual mark has a sun behind the cloud |
| 85/86 snow showers | 6 | 13 | optional |
| 95/96 thunderstorm | 15 | 14 | optional |

**Night hours are 4 254 of 8 760 — 49 % of the year.** Day/night is not a nicety here; at this latitude in
December the hourly row for "today" is majority dark.

Three states strictly require it (0, 1, 2). Four more have a conventional night form (fog, showers, snow
showers, thunderstorm) because the standard drawing puts a sun behind the cloud. **The day card never needs a
night form** — a day card summarises a whole day.

---

## 8. Which codes actually occur here

### 8.1 One year, hourly, four points

| Code | Meaning | Husum | Hörnum | Helgoland | List |
| --- | --- | --- | --- | --- | --- |
| 0 | clear sky | 1 007 | 969 | 967 | 1 295 |
| 1 | mainly clear | 736 | 817 | 882 | 710 |
| 2 | partly cloudy | 1 335 | 1 399 | 1 289 | 1 001 |
| 3 | overcast | 4 055 | 4 055 | 4 082 | 4 574 |
| 45 | fog | 220 | 134 | 123 | – |
| 48 | depositing rime fog | 6 | – | – | – |
| 51 | light drizzle | 11 | 10 | 13 | 667 |
| 53 | moderate drizzle | 11 | 3 | 2 | 207 |
| 55 | dense drizzle | 3 | 3 | 1 | 59 |
| 61 | light rain | 824 | 839 | 860 | 102 |
| 63 | moderate rain | 33 | 32 | 37 | 51 |
| 65 | heavy rain | – | 1 | – | 5 |
| 66 | light freezing rain | 4 | – | – | – |
| 71 | slight snowfall | 146 | 111 | 99 | 61 |
| 73 | moderate snowfall | 13 | 7 | 8 | 24 |
| 75 | heavy snowfall | – | – | – | 4 |
| 77 | snow grains | 22 | 7 | 35 | – |
| 80 | slight rain showers | 283 | 311 | 304 | – |
| 81 | moderate rain showers | 3 | 6 | 3 | – |
| 85 | slight snow showers | 18 | 29 | 18 | – |
| 86 | heavy snow showers | 1 | 2 | 1 | – |
| 95 | thunderstorm | 20 | 19 | 26 | – |
| 96 | thunderstorm, slight hail | 9 | 6 | 10 | – |
| | **distinct codes** | **21** | **20** | **19** | **13** |

**23 of the 28 possible codes occur on this coast in a year.** Never observed at any of the four points:
**56, 57** (freezing drizzle), **67** (heavy freezing rain), **82** (violent rain showers), **99**
(thunderstorm with heavy hail). Rare but real: 48 (6 h), 65 (6 h), 66 (4 h), 75 (4 h), 86 (4 h), 81 (12 h).

Nothing here can be treated as impossible — an icon set still needs a fallback for the five unobserved codes,
because a single unusually cold winter would produce 56 or 67.

### 8.2 How much a set of N states buys

Cumulative share of all 35 040 hourly codes, adding codes in frequency order:

| After adding | Cumulative |
| --- | --- |
| 3 overcast | 47.85 % |
| + 2 partly cloudy | 62.19 % |
| + 0 clear sky | 74.28 % |
| + 1 mainly clear | 83.26 % |
| + 61 light rain | **90.75 %** |
| + 80 slight rain showers | 93.31 % |
| + 51 light drizzle | 95.31 % |
| + 45 fog | 96.67 % |
| + 71 slight snowfall | **97.86 %** |
| + 53, 63, 55, 95, 85, 77, 73 | 99.83 % |
| + 96, 81, 48, 65, 66, 86, 75 | 100.00 % |

**Five codes cover 91 % of all hours, nine cover 98 %.** The long tail is the interesting half: fog,
thunderstorm, snow and heavy rain are 3 % of hours and close to 100 % of the reasons someone checks a weather
page before going out on this coast.

### 8.3 Churn

Husum, one year, adjacent hourly steps: the raw code changes on **35.4 %** of steps. Collapsed to a seven-state
grouping it still changes on **29.3 %**. The hourly row will look busy; a set with fewer states does not fix
that much, because the churn is mostly clear ↔ partly ↔ overcast, which no useful set merges.

Seven-state shares at Husum over the year: overcast 46.3 %, clear 19.9 %, partly cloudy 15.2 %, any rain
13.4 %, fog 2.6 %, snow 2.3 %, thunderstorm 0.3 %.

---

## 9. Icon set options

Three candidates at different granularities, each with a complete mapping of all 28 codes. **All three are
proposals for a human to choose between**, not a decision.

Every option needs a **fallback mark** for a code outside its table — the enum cannot produce one today, but
the enum is theirs, not ours.

### 9.1 Option A — six states, three with a night form (9 files)

| State | Codes |
| --- | --- |
| clear | 0, 1 |
| partly cloudy | 2 |
| cloudy | 3, 45, 48 |
| rain | 51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82 |
| snow | 71, 73, 75, 77, 85, 86 |
| thunderstorm | 95, 96, 99 |

Night forms: clear, partly cloudy, thunderstorm.

**Loses:** fog, folded into cloudy — 477 h/year on this coast, and the state most likely to cancel a ferry.
Loses drizzle vs rain vs showers entirely, so the MET Norway/ICON split in §3 becomes invisible, which is
either the best or the worst thing about this option. Loses all intensity.

**Gains:** nine drawings. If the set has to be drawn from scratch rather than adopted, this is the only
option that is realistic to draw well.

### 9.2 Option B — ten states, six with a night form (16 files) — recommended starting point

| State | Codes | Night form |
| --- | --- | --- |
| clear | 0 | yes |
| mainly clear | 1 | yes |
| partly cloudy | 2 | yes |
| overcast | 3 | no |
| fog | 45, 48 | yes |
| drizzle | 51, 53, 55, 56, 57 | no |
| rain | 61, 63, 65, 66, 67 | no |
| showers | 80, 81, 82 | yes |
| snow | 71, 73, 75, 77, 85, 86 | yes |
| thunderstorm | 95, 96, 99 | yes |

Covers 100 % of the 35 040 sampled hours with a distinct mark for every state that occurred.

**Loses:** intensity within each band — light rain and heavy rain share a mark, as do slight and heavy
snowfall. Loses freezing precipitation (56/57/66/67 fold into drizzle and rain), which on a coast where black
ice on the dyke roads matters is a real omission; it is also 4 observed hours in a year. Loses hail (96/99
fold into thunderstorm).

**Why this one:** it is the smallest set in which fog, showers and thunderstorm each have their own mark, and
those are the three states §6 showed cannot be derived and §8.2 showed are the reason the icon earns its
place. It also maps one-to-one onto Meteocons file names (§9.5), so it can be adopted rather than drawn.

### 9.3 Option C — fourteen states (22 files)

Option B plus:

| Added state | Codes | Taken from |
| --- | --- | --- |
| heavy rain | 65, 82 | rain, showers |
| freezing | 56, 57, 66, 67 | drizzle, rain |
| sleet | — (see note) | — |
| hail | 96, 99 | thunderstorm |

**Loses:** almost nothing meteorologically. Costs 22 drawings, and adds three states that between them
occurred **22 hours in 35 040** on this coast. The freezing mark in particular would be shown a handful of
hours a winter, which is exactly when it matters most and exactly when nobody will have checked that it looks
right.

**Note on sleet:** Open-Meteo's enum has no sleet code. Mixed precipitation is expressed as snow codes at
temperatures near zero. If a sleet mark is wanted it must be derived from `weather_code ∈ snow` plus
`temperature_2m` near 0 °C — the one derivation §6.3 showed is sound. That is a deliberate local rule, not a
code lookup.

### 9.4 What none of the options fix

The §3 model split is upstream of the icon set. Under Option B, on 2026-08-16 Westerland shows the **drizzle**
mark and Hörnum shows the **showers** mark. Options:

1. **Accept it.** Each place shows its best available forecast. Defensible, and invisible unless a reader
   compares two Sylt pages.
2. **Collapse drizzle into rain** in the mapping — Option B with nine states. Hides most of the artefact,
   since the metno places' vocabulary is 933 h drizzle vs the ICON places' 16 h. Costs the drizzle/rain
   distinction everywhere.
3. **Pass `models=icon_seamless`** for the three northern places so the whole coast shares a vocabulary. Buys
   consistency, loses the better local model at those points, and reintroduces the `models=` parameter the #3
   research argued against. It would also need re-testing: ICON-D2 reaches only 49 h and the fallback chain
   changes.

**Option 2 is the cheapest and 3 is the most honest-looking but least honest.** This needs a human decision.

### 9.5 Freely licensed icon sets — licences checked at source

| Set | Licence | Verified from | Fit |
| --- | --- | --- | --- |
| **Meteocons** (`basmilius/weather-icons`, npm `@bybas/weather-icons` 2.0.0) | **MIT** | `LICENSE` file: *"MIT License / Copyright (c) 2020-present Bas Milius"*; npm metadata `"license": "MIT"`; LICENSE bundled in the tarball | **Best.** 122 SVGs, fill and line variants, day/night pairs, and it happens to also ship `wind-beaufort-0…12` and `windsock`, which this project wants anyway |
| `Makin-Things/weather-icons` | **MIT** | `LICENSE` file | 53 states, static + animated SVG, explicit `_night` variants. Named for the Australian BOM's categories, so every mapping is a judgement call |
| `erikflowers/weather-icons` | Icons **SIL OFL 1.1**, code MIT, docs CC BY 3.0 | README "Licensing" section (no `LICENSE` file in the repo — the GitHub API returns 404 for it) | 222 glyphs in a **font**, with day/night variants. Ships `wi-wmo4680-*` classes — **but that is WMO table 4680, not the table Open-Meteo's codes come from**; the numbering is not interchangeable and must be re-mapped by hand (see Open question 8) |
| `OGCMetOceanDWG/WorldWeatherSymbols` | **CC BY 4.0** | `LICENSE.md`: *"released under the Creative Commons Attribution 4.0 International (CC BY 4.0) license"* | Official WMO chart symbology — station-model glyphs for meteorologists. Complete and authoritative, and completely wrong for a public page |
| `roe-dl/weathericons` | **GPL-3.0** | GitHub licence metadata | Copyleft. Avoid for a static site's assets unless the implications are understood |
| `meshosk/weather-icons` | Apache-2.0 | GitHub licence metadata | Explicitly built for WMO weather codes, but a one-star repo with no provenance for the artwork |

**Meteocons maps onto Option B essentially one-to-one**, using the `production/{fill,line}/all/` names from
the npm package:

| Option B state | Day file | Night file |
| --- | --- | --- |
| clear | `clear-day.svg` | `clear-night.svg` |
| mainly clear | `partly-cloudy-day.svg` | `partly-cloudy-night.svg` |
| partly cloudy | `overcast-day.svg` | `overcast-night.svg` |
| overcast | `overcast.svg` | — |
| fog | `fog-day.svg` | `fog-night.svg` |
| drizzle | `drizzle.svg` | — |
| rain | `rain.svg` | — |
| showers | `partly-cloudy-day-rain.svg` | `partly-cloudy-night-rain.svg` |
| snow | `snow.svg` | — |
| thunderstorm | `thunderstorms-day-rain.svg` | `thunderstorms-night-rain.svg` |

Note the deliberate shift: Meteocons' `partly-cloudy-day` is a light-cloud mark, so it reads better for code 1
than for code 2, and `overcast-day` (sun behind full cloud) reads better for code 2. Verify against the real
artwork before locking the table.

**Attribution:** MIT requires the copyright notice and permission text to be retained. For a static site that
means shipping the `LICENSE` text alongside the assets, or a credit line naming Meteocons and Bas Milius. It
does **not** require a visible on-page credit the way [Open-Meteo's CC BY 4.0 does](open-meteo-api.md).

### 9.6 The Frisian gap this opens

An icon needs no translation, which is the ticket's point and it holds. But three things around it are text,
and **all three need Mooring terms that this research cannot supply**:

1. **The icon's accessible label.** An `alt` / `aria-label` for each of the ~10 states. A wordless page still
   needs these for screen readers. Named in English: *clear, mainly clear, partly cloudy, overcast, fog,
   drizzle, rain, showers, snow, thunderstorm.*
2. **A legend**, if the set has more than about six states. Option C almost certainly needs one; Option A
   probably does not.
3. **The day card's day-of-week label**, which already existed but now sits next to a mark that changes its
   reading.

A Frisian term is needed for each of the ten state names. **No agent may invent these** — see
[`docs/places.md`](../places.md).

---

## 10. What this contradicts or complicates

1. **[#3 research §5.1](open-meteo-api.md), "`best_match` is byte-for-byte ICON-D2 → ICON-EU → ICON Global".**
   True at Husum, false at three of the twenty places. That research explicitly listed *"Whether `best_match`
   behaves identically outside Germany"* as undetermined, and it does not. §3 above. **Everything else in the
   #3 research survives**, including the recommendation not to pass `models=`.

2. **The #3 budget assumed 12 places.** The roster resolved by [#9](https://github.com/Commander-Cody/weather-page/issues/9)
   is 20. Recomputed in §5.3 — still under 2 % of quota, but the numbers in the older document are stale.

3. **The locked variable list is now the *only* thing on the request that is free.** At 10 variables the
   request sat exactly on the weight-1.0 boundary. It no longer does. Any future variable is now unambiguously
   a cost decision rather than a free one, and there is no longer a round number to defend.

4. **The overview screen's day card cannot use an API field.** Issue #6's prototype implies one icon per day
   card; §4 shows the API's daily field is unfit for it. The day-card state is a computed value that has to
   live in the fetch job's output JSON, which means the JSON schema for the scheduled job now needs a
   `condition` per day as well as per hour.

5. **The icon and the rain bar can disagree in the same hour** (§6.4, 2.5 % of hours). The fused time axis is
   this page's defining feature; putting a rain icon over an empty rain bar undercuts it. This is a new design
   problem created by adopting the code.

6. **`data age` is unaffected.** `weather_code` rides on the same model run as everything else, so
   [ADR-0001](../adr/0001-staleness-is-data-age-not-fetch-age.md) needs no change. But note the three MET
   Norway places now have a *different* data age from the rest of the coast: `metno_nordic_pp` reports
   `update_interval_seconds: 3600` against ICON-D2's `10800`
   (<https://api.open-meteo.com/data/metno_nordic_pp/static/meta.json>,
   <https://api.open-meteo.com/data/dwd_icon_d2/static/meta.json>). Under ADR-0001 the staleness threshold is
   per source, and there are now two atmospheric sources, not one.

---

## 11. What could not be determined from primary sources

- **The rule that picks MET Norway over ICON-D2 at 54.90 N.** The behaviour is reproducible and sharp, but
  the domain-preference ordering for `best_match` was not locatable in the repository tree — there is no
  `MultiDomains.swift` at the path the older `ForecastapiController` implies, and GitHub code search requires
  authentication. The boundary is therefore an empirical finding, and **it could move without notice**. It
  should be re-checked whenever a place is added north of ~54.85 N.
- **Whether `historical-forecast-api` used the same `best_match` preference a year ago as today.** The
  vocabulary evidence is strong and the January 2026 spot check matched `metno_nordic` on 744/744 hours, but
  Open-Meteo does not publish a changelog of domain-preference changes.
- **Which WMO code table Open-Meteo's values are drawn from.** The docs say "WMO weather interpretation codes
  (WW)" without a table number. The published registry at `codes.wmo.int` returned HTTP 404 for `/306`,
  `/306/4677` and `/306/_ww` during this research, so the 4677-vs-4680 question could not be settled from the
  authoritative source. This matters only for reusing an icon set that keys on a table number (§9.5).
- **Why `weather_code` and `precipitation` disagree on 2.5 % of hours** (§6.4). The `correctDwdIconWeatherCode`
  demotion is clearly meant to prevent it and clearly does not fully. Whether the residue is output rounding
  or a deeper mismatch could not be established.
- **Whether Meteocons' artwork is safe to restyle.** MIT permits modification, but the icons are also sold as
  a design product on <https://meteocons.com/>; the repository licence is unambiguous and the npm package
  bundles it, so this is a comfort question rather than a legal one.

---

## Appendix A: separability table (live 7-day set, 20 places, 3 360 hours)

Which codes appear in each (cloud cover, precipitation) cell. **A cell with more than one code is a cell a
derivation cannot resolve.**

| Cloud cover | Precipitation mm/h | Codes observed |
| --- | --- | --- |
| 0–20 % | 0 | `{0: 635, 1: 95, 2: 3, 3: 1}` |
| 0–20 % | 0–0.5 | `{51: 2}` |
| 20–50 % | 0 | `{0: 2, 1: 190, 2: 43, 3: 5}` |
| 20–50 % | 0–0.5 | `{51: 26}` |
| 50–80 % | 0 | `{1: 17, 2: 418, 3: 36}` |
| 50–80 % | 0–0.5 | `{2: 18, 3: 6, 51: 19, 80: 16}` |
| 50–80 % | 0.5–1 | `{53: 1, 80: 7}` |
| 50–80 % | 1–1.3 | `{80: 9}` |
| 80–100 % | 0 | `{1: 2, 2: 84, 3: 1001, 61: 42}` |
| 80–100 % | 0–0.5 | `{2: 12, 3: 125, 51: 51, 61: 124, 80: 66}` |
| 80–100 % | 0.5–1 | `{3: 9, 53: 15, 61: 93, 80: 39, 95: 6}` |
| 80–100 % | 1–1.3 | `{55: 18, 61: 43, 80: 12, 95: 7}` |
| 80–100 % | 1.3–2.5 | `{61: 59}` |
| 80–100 % | 2.5–7.6 | `{63: 3}` |

The bucket edges are `WeatherCode.calculate`'s own thresholds (§6.1). Even on its home ground the mapping is
many-to-one only in the dry cells.

## Appendix B: live 7-day sample, all 20 places

Hourly code counts, `best_match`, 2026-08-13 → 2026-08-19, 168 h each.

| Place | 0 | 1 | 2 | 3 | 51 | 53 | 55 | 61 | 63 | 80 | 95 | Source model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `list` | 34 | 12 | 9 | 70 | 32 | 2 | 9 | – | – | – | – | metno |
| `westerland` | 34 | 18 | 10 | 63 | 31 | 3 | 9 | – | – | – | – | metno |
| `neukirchen` | 33 | 11 | 16 | 62 | 35 | 11 | – | – | – | – | – | metno |
| `hoernum` | 32 | 15 | 32 | 57 | – | – | – | 21 | – | 11 | – | ICON |
| `wyk` | 31 | 12 | 39 | 55 | – | – | – | 25 | – | 6 | – | ICON |
| `wittduen` | 35 | 12 | 36 | 54 | – | – | – | 22 | – | 9 | – | ICON |
| `hooge` | 34 | 15 | 35 | 54 | – | – | – | 21 | – | 9 | – | ICON |
| `hamburger-hallig` | 33 | 17 | 29 | 59 | – | – | – | 21 | – | 9 | – | ICON |
| `pellworm` | 32 | 16 | 24 | 63 | – | – | – | 17 | – | 16 | – | ICON |
| `nordstrand` | 32 | 16 | 30 | 61 | – | – | – | 23 | – | 3 | 3 | ICON |
| `husum` | 33 | 15 | 31 | 60 | – | – | – | 23 | – | 3 | 3 | ICON |
| `dagebuell` | 27 | 19 | 38 | 54 | – | – | – | 21 | – | 9 | – | ICON |
| `helgoland` | 37 | 11 | 32 | 47 | – | – | – | 15 | 3 | 22 | 1 | ICON |
| `klanxbuell` | 28 | 13 | 34 | 63 | – | – | – | 21 | – | 6 | 3 | ICON |
| `emmelsbuell-horsbuell` | 28 | 19 | 34 | 57 | – | – | – | 21 | – | 9 | – | ICON |
| `niebuell` | 26 | 17 | 33 | 62 | – | – | – | 21 | – | 9 | – | ICON |
| `risum-lindholm` | 27 | 19 | 36 | 53 | – | – | – | 24 | – | 9 | – | ICON |
| `langenhorn` | 30 | 19 | 25 | 62 | – | – | – | 23 | – | 9 | – | ICON |
| `bredstedt` | 32 | 18 | 32 | 54 | – | – | – | 23 | – | 6 | 3 | ICON |
| `toenning` | 39 | 10 | 23 | 73 | – | – | – | 19 | – | 4 | – | ICON |

Totals: `{0: 637, 1: 304, 2: 578, 3: 1183, 51: 98, 53: 16, 55: 18, 61: 361, 63: 3, 80: 149, 95: 13}`.

Daily codes for the same window are in §3.2 and §4.2.

## Appendix C: reproducible commands

```bash
# 1. The recommended request: locked 10 variables + hourly weather_code = 11, weight 1.1
curl "https://api.open-meteo.com/v1/forecast?latitude=54.4764&longitude=9.0514\
&timezone=Europe%2FBerlin&forecast_days=7&wind_speed_unit=ms\
&hourly=temperature_2m,relative_humidity_2m,precipitation,precipitation_probability,\
cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m,weather_code&daily=sunrise,sunset"

# 2. Proof that daily weather_code == max(hourly weather_code)
curl "https://api.open-meteo.com/v1/forecast?latitude=54.4764&longitude=9.0514\
&timezone=Europe%2FBerlin&forecast_days=7&hourly=weather_code&daily=weather_code"

# 3. The model split: Westerland is MET Norway, Hoernum 17 km away is ICON-D2
curl "https://api.open-meteo.com/v1/forecast?latitude=54.9079,54.7561&longitude=8.3050,8.2953\
&timezone=UTC&forecast_days=2&hourly=temperature_2m,weather_code&models=icon_d2,metno_nordic"

# 4. The 54.90 N boundary, in 0.005 deg steps
curl "https://api.open-meteo.com/v1/forecast\
?latitude=54.8850,54.8900,54.8950,54.9000,54.9050&longitude=8.44,8.44,8.44,8.44,8.44\
&timezone=UTC&forecast_days=2&hourly=temperature_2m&models=icon_d2,metno_nordic"
# compare each against the same request with no models= parameter;
# note the returned latitude: 54.88 is the ICON-D2 lattice, 54.89677 is MET Nordic's Lambert grid

# 5. One year of archived best_match forecasts (what the page would have shown)
curl "https://historical-forecast-api.open-meteo.com/v1/forecast?latitude=54.4764&longitude=9.0514\
&timezone=Europe%2FBerlin&start_date=2025-08-01&end_date=2026-07-31&wind_speed_unit=ms\
&hourly=weather_code,cloud_cover,precipitation,wind_speed_10m,wind_gusts_10m,is_day,\
temperature_2m,relative_humidity_2m&daily=weather_code"

# 6. The same year with the code DERIVED rather than native (ERA5) - the §6.2 comparison
curl "https://archive-api.open-meteo.com/v1/archive?latitude=54.4764&longitude=9.0514\
&timezone=Europe%2FBerlin&start_date=2025-08-01&end_date=2026-07-31&hourly=weather_code"

# 7. Do the inputs a real derivation needs exist? (they do at Husum; two are null at List)
curl "https://api.open-meteo.com/v1/forecast?latitude=54.4764&longitude=9.0514\
&timezone=Europe%2FBerlin&forecast_days=7\
&hourly=visibility,cape,lifted_index,convective_inhibition,boundary_layer_height,\
snowfall,showers,freezing_level_height"

# 8. Response size per variable count (§5.2)
curl -s -o /dev/null -w "%{size_download}\n" "<request 1 without weather_code>"   # 9742
curl -s -o /dev/null -w "%{size_download}\n" "<request 1>"                        # 10149
```

---

## Open questions

1. **Which of the three icon sets in §9?** Option B is the recommendation, but Option A is the one that can
   realistically be drawn from scratch, and that trade depends on whether an existing set is adopted.

2. **Adopt Meteocons, or draw a set?** Meteocons is MIT, complete, and includes the Beaufort marks this
   project wants elsewhere. Drawing a set makes the page's visual language its own and avoids looking like
   every other weather app. This is a design call, not a technical one.

3. **What to do about the MET Norway / ICON vocabulary split (§9.4)?** Accept it, collapse drizzle into rain,
   or force `icon_seamless` at the three northern places. The first is honest and visibly inconsistent; the
   third is consistent and quietly worse.

4. **What is the day card's aggregation rule?** §4.3 proposes "most severe state lasting ≥ 3 h, else most
   severe present" and shows it disagrees with Open-Meteo's `max` on ~35 % of days. The threshold, the
   severity ordering, and whether daylight hours should count double are all unchosen.

5. **Does the hourly row show every hour's icon, or only when it changes?** The code changes on 29–35 % of
   hourly steps (§8.3). Twenty-four marks in a row, a third of them different from their neighbour, may read
   as noise on the fused axis.

6. **What happens when the icon and the rain bar disagree** (§6.4, 2.5 % of hours)? Suppress the icon,
   suppress the bar, trust the code, or let them contradict each other.

7. **Do the three MET Norway places get a different staleness threshold?** Their model publishes hourly, not
   three-hourly (§10.6). ADR-0001 sets thresholds per source, and there are now two atmospheric sources.

8. **If `erikflowers/weather-icons` is ever considered, which WMO table do its `wi-wmo4680-*` classes use, and
   does it match Open-Meteo's?** Unresolved in §11 because the WMO registry was unreachable.

9. **Who supplies the ten Mooring state names** (§9.6), and does the set need a legend at all? A legend is
   itself text that needs translating, which argues for the smallest set that works.

---

*Researched 2026-08-13 against <https://open-meteo.com> documentation, the
<https://github.com/open-meteo/open-meteo> server source at `main`, live calls to the free forecast, archive
and historical-forecast APIs, and the licence files of six icon repositories.*
