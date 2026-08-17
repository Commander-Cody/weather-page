# Local gauge data wins over a borrowed curve

Only 9 of the 23 BSH gauges on this coast publish a curve — a water level every 10
minutes across the whole forecast window. The other 14 publish peaks only: the times and
heights of high and low water. The obvious move is to prefer a curve, borrowing one from a
neighbouring gauge where a place's own gauge has none, so that every place draws the same
chart. We do not do that.

**A place uses the gauge at the place, even when that gauge carries only peaks. Another
place's data is adopted only where there is no local data at all.**

The reason is that borrowing is not uniformly cheap, and its cost is invisible on the
page. Measured across all 23 forecast peaks, Wyk's own gauge sits 13 minutes from
Dagebüll's, and Hamburger Hallig's sits 4 minutes from Husum's — borrowing there would
cost almost nothing. But Westerland sits **97 to 128 minutes** from every curve gauge on
Sylt, because the tidal wave has to travel round the north tip of the island before it
reaches List or the Wadden side. A rule that borrows by distance would hand Westerland a
high-water time two hours wrong, rendered in exactly the same confident chart as every
other place.

Choosing per place by measured offset instead would work, but it makes every future
addition a design decision. The local-data rule makes adding a place a data edit.

## What is actually lost

Less than it first appears. Both kinds of gauge publish 23 peaks reaching about 5.7 days
ahead, so the peaks-only places have the same high and low water horizon as the curve
places. And the surge correction on the peak series is only **4 events — roughly 18 hours
— deep at every gauge, curve or not**. The long-range surge exists only inside the curve.

So the real difference is not markers versus a line. It is the surge being visible for
18 hours instead of 5.7 days.

## Consequences

- **Half the roster is peaks-only** — 10 of the 20 seed places. The peaks-only water lane
  is a first-class case to design, not an edge case to tolerate.
- **The astronomical curve has to be interpolated** at peaks-only places, from the 23
  known high and low water points. Interpolating between known turning points is standard
  nautical practice, but the drawn line is ours, not BSH's.
- **The interpolated curve makes the peaks-only screen the same shape as a stale curve
  screen.** [ADR-0001](0001-staleness-is-data-age-not-fetch-age.md) already decided that
  stale water sheds the expected line and the surge gap while keeping the astronomical
  tide and the high/low water times. A peaks-only place looks like that from hour 18
  onward. One behaviour to build, not two.
- **Inside the 48-hour fused chart, a peaks-only place has a surge gap for the first
  ~18 hours and nothing but astronomy for the remaining 30.** How that boundary is shown
  to the reader is settled by
  [ADR-0007](0007-a-weaker-water-claim-is-shown-by-removing-not-relabelling.md): by
  subtraction only, with no mark drawn and the end time stated in words.
- **The gauge is named on every place, borrowed or not.** A label that appears only on
  borrowed places is a warning marker that then needs explaining in Mooring. A constant
  gauge name under the water lane needs no translation and is honest everywhere.
- **The measured high-water offset against the alternative not chosen is recorded per
  place**, as a number. It is what makes each pairing auditable and lets the trade be
  revisited without re-measuring.
