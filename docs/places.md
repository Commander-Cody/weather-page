# Place registry

The list of places the page covers, and the tide gauge each one takes its water level
from. This is **data, not design** — adding or removing a place is a row in this table
plus a Frisian name. It needs no design session.

Resolved by [issue #9](https://github.com/Commander-Cody/weather-page/issues/9).

## The pairing rule

**A place uses the gauge at the place, if one exists — even when that gauge carries only
peaks and no curve. Another place's data is adopted only where there is no local data at
all.**

The rejected alternative was to prefer a curve gauge and borrow it from up to ~20 km
away, so that every place could draw the same chart. That was rejected because the page's
job is to be right, not uniform. Recorded as [ADR-0002](adr/0002-local-gauge-data-wins-over-a-borrowed-curve.md).

Where a place has no gauge, the nearest gauge is the starting point, but the final choice
is a judgement about which stretch of coast the place actually belongs to — see the notes
under the table.

## Fields

Each place carries:

| Field | Meaning |
| --- | --- |
| `key` | Stable slug. Appears in the URL. Never changes once published. |
| `name_frisian` | The **native name** — what the place is called on its own coast. The label every reader sees unless their own variety overrides it. |
| `variety` | **Only** which variety `name_frisian` is in. Provenance, not a judgement about any other variety. See below. |
| `name_german` | Shown smaller, alongside. |
| `coords_land` | Forecast point for wind, rain, temperature. The settlement itself. |
| `coords_sea` | Separate point for sea temperature — see below. |
| `gauge` | BSH station id in the `WaterLevelForecast` collection. |
| `gauge_kind` | `curve` or `peaks`. Decides which water lane the place gets. |
| `gauge_origin` | `own` or `borrowed`. |
| `gauge_distance_km` | Distance from `coords_land` to the gauge. |
| `gauge_hw_offset_min` | Measured high-water offset against the alternative that was
  not chosen. A number, not prose — it is what makes the choice auditable. Empty where
  no alternative was in contention. |
| `notes` | Anything a reader or a later session needs to know. |

`coords_sea` is separate because Open-Meteo's Marine API **returns a value even for a
land point**, so a village coordinate silently yields a meaningless sea temperature. The
guard is to compare the coordinates requested against the coordinates returned. Nudging
the land point seaward instead would quietly degrade the wind and rain forecast.

## Seed roster

Twenty places, in two tables that join on `key`. **Names** is the table the repo owner
fills in. **Gauges** is measured, and should not be hand-edited without re-measuring.

### Names

**No agent may invent these.** Fill in the Mooring form where one exists and the local
variety otherwise, and set `variety` to say which. Where you are unsure, put the German
name in `name_frisian` and leave `variety` empty.

| `key` | `name_frisian` | `variety` | `name_german` |
| --- | --- | --- | --- |
| `list` | List | Sölring | List auf Sylt |
| `westerland` | Weesterlönj | Mooring | Westerland |
| `hoernum` | Hörnem | Sölring | Hörnum |
| `wyk` | e Wik | Mooring | Wyk auf Föhr |
| `wittduen` | Witdöön | Mooring | Wittdün |
| `hooge` | e Huuge | Mooring | Hallig Hooge |
| `hamburger-hallig` | Hamborjer Håli | Mooring | Hamburger Hallig |
| `pellworm` | Pelweerm | Mooring | Pellworm |
| `nordstrand` | e Strönj | Mooring | Nordstrand |
| `husum` | Hüsem | Mooring | Husum |
| `dagebuell` | Doogebel | Mooring | Dagebüll |
| `helgoland` | Hålilönj | Mooring | Helgoland |
| `klanxbuell` | Klångsbel | Mooring | Klanxbüll |
| `emmelsbuell-horsbuell` | Ämesbel-Horbel | Mooring | Emmelsbüll-Horsbüll |
| `neukirchen` | Naischöspel | Mooring | Neukirchen |
| `niebuell` | Naibel | Mooring | Niebüll |
| `risum-lindholm` | Risem-Lunham | Mooring | Risum-Lindholm |
| `langenhorn` | e Horne | Mooring | Langenhorn |
| `bredstedt` | Bräist | Mooring | Bredstedt |
| `toenning` | Taning | Mooring | Tönning |

Expected varieties, as a starting point only: Söl'ring on Sylt (`list`, `westerland`,
`hoernum`), Fering on Föhr (`wyk`), Öömrang on Amrum (`wittduen`), Halligfriesisch on
`hooge` and `hamburger-hallig`, Wiedingharder on `klanxbuell`, `emmelsbuell-horsbuell`
and `neukirchen`, Mooring on the rest. Halunder on `helgoland` is its own case. Any of
these is overridden by a Mooring form where one exists.

### Names across varieties

A place has **one** name here, and a variety overrides it only where its own form genuinely
differs. Per-variety overrides do **not** live in this file — they live in the language CSV,
alongside everything else a translator writes. Recorded as
[ADR-0003](adr/0003-place-names-are-a-native-name-plus-per-variety-overrides.md).

So `variety` says nothing about any variety other than the one it names. `list` is tagged
Sölring because that is what the name is; it does not claim Mooring has no form of its own,
and it does not claim Mooring uses this one. That question is **derived**, not stored — a
name is unresolved for a reader when its `variety` is not the reader's variety and that
variety has no override. Today that is `list` and `hoernum`.

The batch list is generated from this and from the language CSV. It is not kept by hand.

### Gauges

`coords_sea` is not in this table yet — none have been picked. See the gap list.

| `key` | `coords_land` | `gauge` | kind | origin | distance |
| --- | --- | --- | --- | --- | --- |
| `list` | 55.0189, 8.4408 | `list_hafen` | curve | own | 0.2 km |
| `westerland` | 54.9079, 8.3050 | `westerland` | peaks | own | 2.2 km |
| `hoernum` | 54.7561, 8.2953 | `hoernum_hafen` | curve | own | 0.2 km |
| `wyk` | 54.6906, 8.5678 | `wyk` | peaks | own | 0.6 km |
| `wittduen` | 54.6314, 8.3856 | `wittduen_hafen` | curve | own | 0.1 km |
| `hooge` | 54.5747, 8.5461 | `hooge_anleger` | curve | own | 0.8 km |
| `hamburger-hallig` | 54.6053, 8.7872 | `der_strand_hamburger_hallig` | peaks | own | 0.0 km |
| `pellworm` | 54.5222, 8.6472 | `pellworm_anleger` | peaks | own | 4.3 km |
| `nordstrand` | 54.4747, 8.8408 | `strucklahnungshoern` | peaks | own | 3.5 km |
| `husum` | 54.4764, 9.0514 | `husum_schleuse` | curve | own | 1.8 km |
| `dagebuell` | 54.7278, 8.6889 | `dagebuell` | curve | own | 0.3 km |
| `helgoland` | 54.1825, 7.8869 | `helgoland_binnenhafen` | curve | own | 0.4 km |
| `klanxbuell` | 54.8578, 8.6789 | `osterley` | peaks | borrowed | 7.9 km |
| `emmelsbuell-horsbuell` | 54.8514, 8.7194 | `osterley` | peaks | borrowed | 10.5 km |
| `neukirchen` | 54.9139, 8.7431 | `osterley` | peaks | borrowed | 14.0 km |
| `niebuell` | 54.7869, 8.8283 | `dagebuell` | curve | borrowed | 11.0 km |
| `risum-lindholm` | 54.7583, 8.8722 | `dagebuell` | curve | borrowed | 12.3 km |
| `langenhorn` | 54.6944, 8.9000 | `schluettsiel` | peaks | borrowed | 9.4 km |
| `bredstedt` | 54.6208, 8.9789 | `der_strand_hamburger_hallig` | peaks | borrowed | 12.5 km |
| `toenning` | 54.3167, 8.9444 | `eider-sperrwerk_aussenpegel` | curve | borrowed | 8.7 km |

**Twelve places have their own gauge, eight borrow. Ten get a curve, ten get peaks only.**
That last split is the important one: under this rule the peaks-only water lane is not an
edge case, it is half the site.

## Notes on individual pairings

**Westerland** is the rule's clearest win. Its own gauge carries no curve, but every curve
gauge on Sylt is **97 to 128 minutes** out of phase with it — the tidal wave has to travel
round the north tip of the island before it reaches List. A borrowed curve there would be
confidently, authoritatively wrong.

**Wyk, Pellworm, Nordstrand and Hamburger Hallig** are the places where the rule costs
something. Each has a good curve gauge nearby — Wyk to `dagebuell` is +13 min, Pellworm to
`hooge_anleger` is −8 min, Nordstrand to `husum_schleuse` is +20 min, Hamburger Hallig to
`husum_schleuse` is **+4 min**. Under the old draft rule all four took the borrowed curve.
They now use their own gauge and get peaks only. Those offsets are recorded here so the
trade can be revisited without re-measuring.

**The Wiedingharde has no gauge on its coast.** Checked against all 136 BSH stations: the
northernmost mainland gauge in North Frisia is Dagebüll. `osterley`, about 5–14 km
offshore in the Wadden Sea, is the nearest thing and is what the three Wiedingharde places
use. It runs only 15 minutes from `dagebuell` at high water, so either would be
defensible — `osterley` wins on being the water those villages actually look at.

**`suedwesthoern` is the preferred Wiedingharde source, but is not available yet.** It
exists on BSH's *other* product, the tide calculator at `gezeiten.bsh.de`, flagged as an
interpolated gauge. That product is not CC BY 4.0 — see the gap list below.

**Langenhorn** takes `schluettsiel` as the nearest gauge, 9.4 km. `der_strand_hamburger_hallig`
at 12.5 km is the alternative if the Hamburger Hallig shore turns out to be the coast
Langenhorn identifies with. A local call, not a technical one.

**Pellworm** has two gauges, `pellworm_anleger` on the south-east side and
`pellworm_hoogerfaehre` on the north. The Anleger is the ferry pier and the busier side.

**Tönning** sits on the Eider, and `eider-sperrwerk_aussenpegel` is the outer gauge,
seaward of the barrage — so it reflects the sea, not the impounded river.

## Known gaps

- **Every Frisian name.** All 20 rows of the Names table are blank. Filled in by the repo
  owner; see the instructions above that table.
- **Every `coords_sea`.** None picked yet. Each needs to be a point Open-Meteo's Marine
  API confirms is water, by returning coordinates close to the ones requested.
- **`coords_land` for the smaller places is provisional.** The Wiedingharde and inland
  coordinates are estimates and should be confirmed. Treat them as approximate: the first
  estimate of Südwesthörn's position in this effort was 8 km out.
- **Sankt Peter-Ording is not in the roster.** It has no gauge in the forecast API at all,
  and was cut as primarily a tourist town. It *does* exist on the tide calculator as
  `st-peter-ording_bad`, so it becomes a candidate if that product turns out to be usable.
- **Places named but not yet placed**: Ockholm, Alkersum, Süderende. Adding them needs a
  gauge decision each and a Frisian name, nothing more.

## The tide calculator, if its licence permits

`gezeiten.bsh.de` carries **39 stations in this region against the forecast API's 23**,
including `suedwesthoern`, `st-peter-ording_bad`, `langeness_nord`, `langeness_hilligenley`,
`rantumdamm`, `list_west`, `hoernum_west`, `nordstrandischmoor`, `holmer_siel` and
`everschopsiel`. It offers a **curve** text file per station, which is exactly what the
peaks-only gauges lack.

It is astronomical only — no surge, no measurement — and it arrives as a per-station,
per-calendar-year download rather than an API, with next year's file appearing around
August. Downloading requires accepting BSH's fee schedule for digital data and separate
usage conditions for tide data, which is a different licence world from the forecast API's
CC BY 4.0.

If those terms permit republishing, the better design is a **local astronomical curve from
the tide calculator paired with a borrowed surge from the nearest forecast gauge** — which
serves the pairing rule above better than either product alone. That question is open.
