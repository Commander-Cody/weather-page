# A weaker water claim is shown by removing, not by relabelling

Half the roster reads a peaks-only gauge (ADR-0002), and at those gauges the surge correction
reaches only about 18 hours. So on a 48-hour chart the page has an expected water level for the
first 18 hours and nothing but astronomy for the remaining 30. The obvious move is to draw the
boundary — a rule, a tick, a hatched edge, a word at the crossing — so the reader can see where
the claim changed. We do not do that.

**Where the page's water claim weakens, things are taken off the chart. Nothing is added, and
nothing already on it changes meaning.**

At the boundary the solid expected line and the surge shading stop. That is the whole visual
event. The dashed astronomical line continues unchanged — it does not thicken, darken, or go
solid when it becomes the only line in the lane. Dashed permanently means *this is a calculation,
not a forecast of the actual water*, which is true of that line everywhere on the chart and at
every gauge, and the interpolated curve at a peaks-only place (#9) is doubly entitled to it.

Promotion would also destroy the signal. Solid becoming solid is no transition at all, so the one
thing that tells the reader something changed would disappear exactly when the lane starts making
a weaker statement.

## Why an undrawn boundary is honest

Two things make this work rather than merely cheap.

The boundary is **self-announcing when it matters**. #6 found the surge gap is invisible except in
a storm. In calm weather the expected and astronomical lines nearly coincide, so the transition is
faint — but there is also nothing behind it to know, because the astronomical tide is very nearly
the right answer. In a storm the shading is fat and its disappearance is unmissable.

And the boundary is **stated in words, to the minute**. The always-visible freshness line carries
one sentence naming the time the surge-corrected forecast ends — meaning *"surge-corrected forecast
only until 11.00"*. It carries a computed time rather than a fixed number, because the measured
reach runs from 15.6 to 18.5 hours across gauges and shrinks as a run ages: BSH anchors the
forecast window to an absolute end timestamp, so a hard "18 hours" in the string would be wrong
part of the time. A reader who wants to know where the claim changes can find out exactly. The
chart stays clean and nothing is concealed.

## Consequences

- **This is the same visual state as stale water, deliberately.** ADR-0001 already sheds the
  expected line and the surge gap while keeping the astronomical tide and the high and low water
  times. A peaks-only place looks like that past the boundary. **One code path, not two** — the
  two states differ only in wording.
- **The deviation numbers go with it.** A deviation number means the page has a surge-corrected
  value (ADR-0008); its absence means the page fell through to astronomy. This is not squeamishness
  about a weaker number: the deviation is measured against mean high water, so an astronomical
  deviation and a surge-corrected one look identical and can differ in **sign** — a neap tide reads
  −15 while the water will actually reach +50. The high and low water *times* are kept, since
  astronomy never goes stale.
- **No word in the lane gutter for this state.** ADR-0001's gutter word flags a temporary
  condition next to the muted data. This is a permanent property of the place, and a permanent
  gutter word becomes furniture the reader stops seeing. It would also overstate: its scope is the
  whole lane, while the condition covers only part of one. The gauge is already named under the
  water lane by ADR-0002.
- **The whole word cost is one string with a time slot**, built from the owner's existing
  `korigiird (wååderpäägel)forütseeding` rather than a new coinage.
- **When a peaks-only place also goes stale, the stale sentence replaces the peaks-only sentence**
  and ADR-0001's gutter word appears as normal. One sentence at a time. Once the entire lane is
  astronomical, saying where the surge ended adds nothing.
- **The dash means "beyond our data" and nothing else.** #6 gives a day past the water horizon a
  dash instead of a high-water time. A calendar day holding only one high water — which happens
  roughly fortnightly, since the tidal day is 24 h 50 min — is **not** missing data, so that slot
  **collapses** rather than dashing. Two marks for two different absences, never one for both.
- **The chart is 48 hours at every place.** A shorter chart at peaks-only places would discard 30
  hours of good wind and rain to hide a limitation in one lane, and a water lane that stopped early
  would break the single shared time axis that makes the fusion readable at all.
- **The 3-hour past window follows the same rule with no extra decision.** `measurement` lives
  inside the `curve` object, so peaks-only gauges have none; their past window shows the
  interpolated astronomical line alone. Removal, again, rather than a substitute.
