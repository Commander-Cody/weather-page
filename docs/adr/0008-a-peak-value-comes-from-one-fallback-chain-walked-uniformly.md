# A peak value comes from one fallback chain, walked uniformly

BSH publishes the height of a single high or low water through **three** different series, and they
do not cover the same gauges or the same horizon:

| Series | Reach | North Frisian gauges carrying it |
| --- | --- | --- |
| `forecast_value` — official, human-made | ~17–18 h, exactly 4 events | **all 23** |
| `mos_forecast_r0…r5_value` — automated MOS peaks | ~130–136 h | 6 |
| `automated_curve_forecast` — automated MOS curve | ~136 h | 9 |

So the 18-hour limit is the **official human forecast** running out, and it runs out at every gauge
on the coast, curve or not. Three gauges — `dagebuell`, `hoernum_hafen`, `buesum_schleuse` — have a
curve but no MOS peak series at all. Taken literally that is three tiers of place, not two.

**A peak value is resolved by walking one chain, and every gauge walks the same one:**

1. `forecast_value` — the official forecast, for the next 4 events
2. `mos_forecast_r0_value`, falling through `r1`…`r5` only where the preceding one is absent
3. the maximum of the `automated_curve_forecast` series at that event
4. no number

Steps 1–2 are BSH's own fallback chain — the r0–r5 order is documented in Tab. 3 of BSH's parameter
documentation as a defined degradation sequence. Extending it by one step is BSH's idiom rather than
an invention of ours. Gauges are not special-cased; they simply fall to different depths in an
identical chain.

Step 3 was the contested one. It means that at 6 gauges the page prefers its own reading of BSH's
curve over `mos_forecast_r0_value`, a figure BSH publishes for the same event — and the two come
from different runs, so they will disagree by a few centimetres. It was rejected for exactly that
reason: relaying an authority's number beats recomputing it. Step 3 survives only as the step below,
reached at the 3 gauges that publish a curve and no peaks, where the alternative is no number for a
peak sitting on a solid line the chart is already drawing.

## Consequences

- **The chain's depth is invisible to the reader.** The only boundary on screen is a deviation number
  or no deviation number (ADR-0007). Steps 1–3 are all surge-corrected and all BSH-derived; exposing
  which one was reached would be noise.
- **The boundary is a peaks-only phenomenon.** The chain runs out around hour 18 at the 14 peaks-only
  gauges, and nowhere inside 48 hours at the 9 curve gauges. "Numbers stop at hour 18" is the wrong
  rule — numbers stop when the chain runs out.
- **A single chart's peak numbers can come from up to three different model runs**: the first four
  from the human forecast, later ones from a MOS run made hours apart. BSH's own published product
  has the same property, so this is not a defect we introduce — but the fetch job must carry
  **provenance per value** rather than one run time for the whole water lane, and ADR-0001's
  staleness threshold has to be applied against the right one.
- **The header leads with the next high water, not the current level** — `11.00 +39`. This reverses
  #6, and it is forced rather than preferred: `measurement` lives inside the `curve` object, so at
  the 14 peaks-only gauges **there is no current water level at all** — absent, not stale. Leading
  with a figure that exists at 10 of 20 places would either put two header shapes on one site or a
  hole in the page's most prominent number. The next high water is always within about six hours,
  so it is always at **chain depth 1** at every gauge: the header is the one water figure that is
  uniformly official and surge-corrected everywhere, and the boundary never touches it.
- **`mean_high_water` is present on all 23 North Frisian gauges**, so a high-water deviation is
  buildable everywhere — which is what makes the header and the high-water-only day cards safe.
  `mean_low_water` is present on only 128 of 136 features collection-wide and has not been checked
  per gauge; low water deviations inside the chart depend on it, and the fetch job must handle its
  absence.
- **The page makes no surge claim beyond 48 hours anywhere.** The day cards carry high water *times*
  only, so the entire surge story lives inside the chart. A MOS deviation a hundred hours out is not
  a claim worth printing on a card, and this keeps the day strip identical at all 20 places.
- **The current water level is wanted and not yet available.** `measurement_url` points at
  Pegelonline, which may publish current levels for the peaks-only gauges — a fourth source and a
  fifth credit line, which #31 already refused once for BKG. Tracked separately; the header decision
  does not wait on it.
