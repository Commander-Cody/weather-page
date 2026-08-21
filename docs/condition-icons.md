# The condition icon set

Decided on [#15](https://github.com/Commander-Cody/weather-page/issues/15). Sourced from the
research on [#11](https://github.com/Commander-Cody/weather-page/issues/11) and reshaped by
[#14](https://github.com/Commander-Cody/weather-page/issues/14)'s model pin.

**Eleven states, adopted from Meteocons, nothing drawn.** How a mark is *chosen* is a separate
question from what the marks are, and it is answered twice, because the two grains need different
rules:

- **Three-hour chart blocks** — [ADR-0010](adr/0010-a-condition-mark-summarises-its-block.md): any
  weather state in the block wins on severity, otherwise the commonest sky state.
- **Day cards** — [ADR-0011](adr/0011-a-day-card-is-summarised-by-water-not-by-hours.md): gated on
  how much water fell, with the sky half from mean cloud cover. The day card reaches only **9** of
  the eleven states; drizzle and downpour are hourly-only.

## The source

[Meteocons](https://github.com/basmilius/weather-icons) by Bas Milius, **MIT**, verified in the
`LICENSE` file at the repository root and in the npm tarball's metadata. MIT requires the copyright
notice and permission text to be retained; it does **not** require a visible on-page credit. So this
adds **no fourth credit line** to the attribution question on
[#19](https://github.com/Commander-Cody/weather-page/issues/19).

**Vendored from the repository, not installed from npm.** The published
`@bybas/weather-icons@2.0.0` carries **122** icons in `production/fill/all/`; the repository's `v2`
branch carries **236**, and `extreme-rain` — the downpour mark — exists only in the larger set. Ship
the `LICENSE` text alongside the assets. There is no version number to pin, which is the cost of the
choice.

**Variant: `fill`.** Not `monochrome`, which renders `rain` and `extreme-rain` as the same outline
and would silently delete the downpour state. Not `line`, whose strokes are ~26 px on a 1024 px
canvas and so render at roughly half a pixel in a 22 px lane. All three variants use identical file
names in parallel directories, so this is reversible without touching the table below.

## The table

All 28 codes Open-Meteo can emit are placed. Night forms follow one rule: **a state has a night form
if and only if its mark contains the sun.**

| State | Codes | Day mark | Night mark |
|---|---|---|---|
| clear | 0 | `clear-day` | `clear-night` |
| mainly clear | 1 | `partly-cloudy-day` | `partly-cloudy-night` |
| partly cloudy | 2 | `overcast-day` | `overcast-night` |
| overcast | 3 | `overcast` | — |
| fog | 45, 48 | `fog` | — |
| drizzle | 51, 53, 55, 56, 57 | `drizzle` | — |
| rain | 61, 63, 66, 67 | `rain` | — |
| downpour | 65, 82 | `extreme-rain` | — |
| showers | 80, 81 | `partly-cloudy-day-rain` | `partly-cloudy-night-rain` |
| snow | 71, 73, 75, 77, 85, 86 | `snow` | — |
| thunderstorm | 95, 96, 99 | `thunderstorms-rain` | — |
| *unknown* | anything else | `not-available` | — |

**16 files.** Four day/night pairs, seven single marks, one fallback.

The file names are misleading and the artwork was checked rather than trusted:
`partly-cloudy-day` is a sun with **one** white cloud, which reads as *mainly clear*;
`overcast-day` is a sun with a white cloud **and a dark grey one behind it**, which reads as
*partly cloudy*. The shift is deliberate.

Night is derived from the `sunrise`/`sunset` daily variables already locked, with the boundary hour
counted as day — #11 verified this reproduces `is_day` exactly, so `is_day` is not requested.

## What the set cannot say

- **Freezing rain and freezing drizzle** (56, 57, 66, 67) fold into drizzle and rain. **No freely
  licensed set has a freezing-rain mark** — not Meteocons, not Makin-Things. `sleet` means ice
  pellets falling, not rain freezing on contact, so it would be a factual error. On a coast where
  black ice on the dyke roads matters this is the real loss, and it is a gap rather than a
  preference.
- **Hail** (96, 99) folds into thunderstorm. Every hail code in Open-Meteo's enum *is* a
  thunderstorm, and Meteocons' hail marks carry no lightning at any variant. Splitting hail out
  would replace a correct mark with one that hides the more dangerous half.
- **Intensity within rain and snow.** Light and heavy snowfall share a mark. Carried instead by the
  rain lane directly beneath the icon, which says it better than an icon can.

## No legend

The marks stand alone on the overview screen. A legend would hand back the icon's one real advantage
on a Frisian-only page — needing no translation — in the most expensive form, twelve *definitional*
strings. Whether a reference screen behind the menu button carries one is not decided here.

## Mooring strings needed

Twelve, one per state plus the unknown fallback. Each is an `alt` / `aria-label`, so they are written
whether or not they are ever painted on screen. **No agent may invent, guess at or extend these** —
see [`places.md`](places.md).

| Key | English | Mooring |
|---|---|---|
| `condition.clear` | clear | klåår |
| `condition.mainly_clear` | mainly clear | mååst klåår |
| `condition.partly_cloudy` | partly cloudy | wat betäägen |
| `condition.overcast` | overcast | betäägen |
| `condition.fog` | fog | mist |
| `condition.drizzle` | drizzle | språnking |
| `condition.rain` | rain | rin |
| `condition.downpour` | downpour | gootrin |
| `condition.showers` | showers | flåågi |
| `condition.snow` | snow | snii |
| `condition.thunderstorm` | thunderstorm | tunerwääder |
| `condition.unknown` | unknown | ünbekånd |

`condition.downpour` is the one to check first. The state was named *downpour* rather than *heavy
rain* precisely so that codes 65 and 82 — heavy continuous rain and a violent shower — could sit
under one word. If Mooring has no such single word, the state should be renamed *heavy rain* and
code 82 moved to `showers`.
