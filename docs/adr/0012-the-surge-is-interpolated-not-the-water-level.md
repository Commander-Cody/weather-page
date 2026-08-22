# The surge is interpolated, not the water level

Half the roster reads a peaks-only gauge (ADR-0002). Those gauges publish high and low water
but no curve, so both lines in the water lane — the dashed astronomical tide and the solid
expected level — have to be drawn between known points rather than read off a series. The
obvious way is to interpolate each line from its own peaks: the astronomical line from
`tidal_prediction_value`, the expected line from the surge-corrected peak values. We do not
do that.

**At a peaks-only gauge the expected line is the astronomical line plus an interpolated
surge. The expected water level is never interpolated directly.**

The surge is the difference between a surge-corrected peak and its astronomical peak. That
difference is interpolated between peaks with a straight line and added to the astronomical
curve. The astronomical curve itself is interpolated between turning points with a half
cosine — `h = mean + half_range × cos(π × fraction)`.

## Why the obvious way is a trap

Interpolating a tidal curve from its turning points is not very accurate. Measured against
BSH's own astronomical curve at the six North Frisian gauges that publish one, a half-cosine
fit is wrong by **7.4 to 25.6 cm RMS and up to 71 cm at worst** — roughly 10 to 20 % of the
tidal range, largest at the Wadden Sea stations, Husum and Dagebüll. The error is systematic
rather than random: the real tide there floods faster than it ebbs, and a symmetric curve
cannot know that.

That number looks alarming and is mostly harmless, because **the same error appears in both
lines and cancels in the gap between them** — and the gap is the whole point of the lane. The
absolute position of either line is never shown as a figure; every number on the page is a
deviation read at a peak, straight from BSH.

Which means the interpolation error is only tolerable while it is shared. Measured three
ways, on the same six gauges, as error in the gap:

| How the two lines are built | Gap error RMS | Worst |
| --- | --- | --- |
| Both lines interpolated from their own peaks | 3.4–13.5 cm | 40 cm |
| Real astronomical curve, expected line interpolated | **7.4–26.9 cm** | **84 cm** |
| Real astronomical curve, **surge** interpolated | 3.4–13.3 cm | 40 cm |

The middle row is the trap. Making one line exactly right while the other stays interpolated
**roughly doubles the error in the gap** — the page would draw a surge that is not there, of
a size comparable to the everyday surges it exists to show. An improvement in a line the
reader cannot check, paid for with a defect in the thing the reader is looking at.

The third row is the rule above, and it costs nothing: it reproduces today's gap accuracy to
within a tenth of a centimetre while leaving the astronomical line free to come from anywhere.

## Why these two methods

They are not interchangeable, and each matches what is actually known about its signal.

A tide between two turning points has a known shape, so a curve is right. Half-cosine beat
monotone cubic interpolation at **every** station tested — 7.4–25.6 cm RMS against 10.2–28.8,
and 71 cm worst case against 105 cm. A spline overshoots near the turning points because it
is fitting curvature it has no evidence for.

A surge between two peaks six hours apart has no known shape, so a straight line invents the
least. Trying a cosine on the surge as well changed nothing measurable, so the simpler and
more honest method wins.

## The front edge

BSH publishes the surge-corrected peaks four times a day, and the first one falls **0.6 to
2.1 hours after the run**. For that stretch after each new run there is no earlier peak to
interpolate from, so the surge at "now" is unbracketed — about a fifth of the day, at the
most-read end of the chart.

**The first surge residual is held flat back to "now".** A surge barely moves in two hours, so
constant extrapolation is the mildest claim available. The alternative — starting the expected
line at the first peak — would open and close a hole at the front of the chart four times a
day on BSH's schedule, which reads as a fault rather than as honesty. The 3-hour past window
is unaffected: ADR-0007 already gives peaks-only places astronomy alone there.

## Consequences

- **The astronomical line's source stops being load-bearing.** Once the surge is interpolated
  separately, where the dashed line comes from no longer affects the gap. This is what makes
  the next consequence affordable.
- **BSH's tide calculator is not adopted, and the astronomical line stays ours at all ten
  peaks-only places** ([#18](https://github.com/Commander-Cody/weather-page/issues/18)). Its
  full-year astronomical curve is licence-clean and free
  ([#12](https://github.com/Commander-Cody/weather-page/issues/12)) and would give five of the
  ten a real BSH line. With this rule in place, what that buys is the *shape* of an unlabelled
  dashed line and nothing else — no number on the page changes. What it costs is a second BSH
  product under a different legal instrument, a fixed-width Latin-1 parser in metres and
  year-round CET, a yearly ~23 MB fetch with no staleness rule, an archive duty because BSH
  deletes files after two years, an unresolved `robots.txt` conflict, and a fourth credit line
  in prescribed German on a Frisian-only page. It also deletes no code: `osterley` and
  `der_strand_hamburger_hallig` have no curve, so the interpolation is written either way.
  Parked as a possible separate effort, not ruled out forever.
- **We keep a known inaccuracy, deliberately.** The dashed line at every peaks-only place is
  wrong by up to 71 cm against BSH's own curve. It is stated here rather than left for someone
  to discover. What makes it acceptable is that nothing numeric rests on it and the gap is
  unaffected — not that it is small.
- **The tide calculator's high/low-water files offer this project nothing.** Its peaks are the
  same computation the forecast API already serves: compared across all 23 events at
  Westerland, `tidal_prediction_value` and the tide calculator's published peaks agree **to
  the minute and the centimetre**. Only the curve was ever new.
- **The expected line ends at the last surge-corrected peak**, exactly as before — the surge
  horizon is unchanged by this rule and is still read from the data, never hard-coded.
- **This rule is the reason the code looks indirect.** Building an expected line by adding an
  interpolated surge to an interpolated tide invites the simplification of interpolating the
  expected peaks directly. That simplification is the middle row of the table above.

## How this was measured

The six gauges that publish both a real astronomical curve and peaks — `list_hafen`,
`hoernum_hafen`, `dagebuell`, `husum_schleuse`, `buesum_schleuse`, `helgoland_binnenhafen` —
were each treated as if they were peaks-only, and the reconstruction compared against the real
series. Surge-corrected peaks were taken as the extremum of `automated_curve_forecast` near
each event rather than `forecast_value`, so that both sides of every comparison come from one
product and no cross-run disagreement enters the numbers. The magnitudes will not transfer
exactly to a real peaks-only gauge; the ordering of the three rows is the finding.
