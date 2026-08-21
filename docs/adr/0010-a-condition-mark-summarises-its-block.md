# A condition mark summarises its block: backgrounds by frequency, events by severity

The overview screen's top lane is condition icons, sharing its x-axis with temperature, wind, rain
and water ([#6](https://github.com/Commander-Cody/weather-page/issues/6)). Those four lanes are
hourly. **This one is not, and cannot be.**

The chart runs at **15 pixels per hour** and the mark is **22 pixels wide**. Marks every hour
overlap. Marks on change overlap too — the code changes on 29–35 % of hourly steps
([#11](https://github.com/Commander-Cody/weather-page/issues/11) §8.3), so two changes an hour apart
are routine. Three-hourly spacing is forced by geometry already locked, and it matches the wind
lane's direction arrows.

That leaves a question the spacing does not answer: **what does one mark mean?**

## The two failures

**Sampling** — drawing the code at 00:00, 03:00, 06:00 and ignoring the hours between — shows a
one-hour state **at best one time in three**. That is arithmetic, not a claim about the weather. And
the short-lived states are exactly fog, showers and thunderstorm, which #11 §8.2 showed are the
entire reason the icon earns its place. A page that samples away two thirds of its thunderstorms
shows fair weather during a thunderstorm.

**A single severity ordering over all eleven states** — taking the worst of the block — fails the
other way. #11 §8.3 found the churn is mostly clear ↔ partly cloudy ↔ overcast, so a block of
`[clear, clear, overcast]` would show overcast, and since clear is 19.9 % of hours at Husum the lane
would show clear only when all three hours are clear. A broken-sky afternoon reads as solid grey.
That is the same error as
[#29](https://github.com/Commander-Cody/weather-page/issues/29)'s coast-wide surge warning:
overstating the bad weather to exactly the readers who will act on it.

## The distinction that resolves it

The eleven states are not one kind of thing.

- **Sky states** — clear, mainly clear, partly cloudy, overcast — are a *background*. The sky is
  always doing one of them.
- **Weather states** — fog, drizzle, rain, downpour, showers, snow, thunderstorm — are *events*.
  They happen, or they do not.

You summarise a background by asking **what it mostly was**. You summarise an event by asking
**whether it happened**. Applying one rule to both is what causes both failures above.

**The rule:**

> If any hour in the block carries a weather state, the mark is the most severe weather state in the
> block. Otherwise the mark is the commonest sky state.

Severity, most severe first:
**thunderstorm → downpour → showers → snow → rain → fog → drizzle.**

Ours, not the enum's. #11 established that Open-Meteo's numeric order is not severity order — 80
*slight showers* outranks 65 *heavy rain* — so an ordering had to be written rather than inherited.
It only fires when two *different* weather states share one block, which is uncommon; the ranks that
get exercised in practice are showers/rain, rain/drizzle and thunderstorm/showers.

The mark is drawn at the **block's midpoint**, because it describes the block rather than an instant.

## What this costs

The condition lane stops being a direct read of `weather_code` at a given hour, while every lane
beside it stays hourly. On a page whose defining feature is that you read down a vertical slice and
see everything at one moment, that looks like a contradiction.

It is not, because **the slice property was already gone for this lane**. At three-hourly spacing
there is no mark at 14:00 under any rule. The choice was only ever about what the sparse marks mean,
and a summary loses less than a sample.

A second consequence: fog is hidden whenever it shares a block with rain or worse. It still outranks
drizzle, so the mizzle-fog combination common on this coast shows fog.

And the header icon, which means *now*, shows the **current hour's** condition with no summarising.
So the header can read clear while the first block reads rain, when rain starts two hours out. Both
are correct; they answer different questions.

## Where the work happens

In the scheduled fetch job, not the page — the same place #11 put the day card's condition, and for
the same reason. The output JSON carries a resolved condition per block.

## Related

- [ADR-0004](0004-the-page-relays-warnings-it-never-authors-them.md) — the page relays. A
  precipitating mark over a 0.0 mm rain bar therefore **stands**: `weather_code` says what the
  weather is doing, precipitation says how much water fell, and rain that fails to register a tenth
  of a millimetre is real. Correcting one source field with another would be authoring.
- [`docs/condition-icons.md`](../condition-icons.md) — the eleven states and their marks.
- [ADR-0011](0011-a-day-card-is-summarised-by-water-not-by-hours.md) — the day card summarises 24
  codes, not 3, and **does not reuse this rule**. It could not: at three hours "it happened" means a
  third of the block, at twenty-four it means 4 %, so one drizzly hour would mark a clear day. The
  day card is gated on how much water fell instead, and its sky half comes from mean cloud cover
  rather than from the commonest sky code. Same eleven states, different aggregation
  ([#16](https://github.com/Commander-Cody/weather-page/issues/16)).
