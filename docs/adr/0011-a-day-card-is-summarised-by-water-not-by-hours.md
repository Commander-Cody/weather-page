# A day card is summarised by water, not by hours

The day strip below the fused chart carries one condition mark per day
([#6](https://github.com/Commander-Cody/weather-page/issues/6)). One mark for 24 hourly codes.

Open-Meteo publishes a daily `weather_code`, and it cannot be used: it is a plain numeric `max`
over the 24 hourly values, and numeric order is not severity order — code 80 *slight rain showers*
outranks 65 *heavy rain*. On **37 % of days at Husum** the code it reports is true for two hours or
fewer out of twenty-four
([#11](https://github.com/Commander-Cody/weather-page/issues/11) §4). So the day state is computed
in the fetch job, and this ADR is the rule it computes.

## The rule

```
1.  any thunderstorm hour                    -> thunderstorm
2.  total precipitation >= 0.5 mm
      snow codes carry > half the mm         -> snow
      otherwise                              -> the wet state with the most mm
3.  >= 6 hours of fog                        -> fog
4.  otherwise, from mean cloud cover:
      < 10 %  clear          < 45 %  mainly clear
      < 85 %  partly cloudy   else   overcast
```

All 24 hours of the calendar day, with no daylight weighting. Beside the mark, the card carries the
day's **total precipitation in mm**: the icon says what kind of weather, the number says how much of
it.

The strip runs **tomorrow through +6 — six cards, and no card for today.** Today is partly in the
past by the time anyone reads it, so its card would either mean something different from the other
six or describe weather that has already happened. The 48-hour chart above covers today in full.

## Why not ADR-0010's rule

One lane above, the three-hour blocks run a different rule: *any* weather state in the block wins on
severity, and only a block with no weather at all falls through to the commonest sky state
([ADR-0010](0010-a-condition-mark-summarises-its-block.md)). Reusing it here was the obvious move
and it does not survive the change of scale. At three hours, "it happened" means at least a third of
the block. At twenty-four it means 4 %, so a single drizzly hour at 04:00 would beat twenty-three
hours of clear sky, and every card in the strip would show rain.

The candidate on #11 — *most severe state lasting at least 3 h* — fails the other way. Measured over
a year under the pinned `icon_seamless`:

| state | days it occurs at Husum | median hours | days surviving a 3 h bar |
| --- | --- | --- | --- |
| thunderstorm | 17 | **1** | **2** |
| drizzle | 15 | 1 | 0 |
| showers | 102 | 2 | 44 |
| fog | 49 | 3 | 23 |
| snow | 30 | 7 | 23 |
| rain | 163 | 4 | 76 |

A three-hour bar **erases thunderstorm from the day card** — two days a year at Husum, one at List.
Thunderstorm is also the only state a threshold can erase outright, since nothing outranks it, so
every one of those losses is the threshold and not a worse state winning. #11 took `weather_code` at
all because fog, showers and thunderstorm are what a derived condition loses; a duration bar hands
one of the three straight back. The same rule also made `overcast` the commonest mark of the year at
118 days of 365.

## What the rule rests on

**Duration is the wrong instrument.** A day is summarised by how much weather it had, not by how many
hours carried a label. That is why thunderstorm needs no threshold — it is a hazard whatever its
duration — and why everything else is gated on water rather than on hours.

**0.5 mm is a judgement call and is recorded as one.** The climatological wet-day definition is
1.0 mm in 24 hours (the WMO's ETCCDI indices); 0.5 mm was chosen instead because it is the setting
at which the showers mark survives on the day card at all — 14 days a year rather than 8. It is a
better-informed guess than the three hours it replaces, not a borrowed standard.

**The cloud-cover cuts are calibrated, not picked.** 10 / 45 / 85 % reproduce ICON's own sky coding
on **86 %** of 14 334 sky hours across both measured places.

**Six hours of fog is a quarter of the day.** Fog is only reached on a day under 0.5 mm, so rain
suppresses it, a foggy day that also rains being a rainy day. A clock rule was considered — fog at
Husum peaks 03:00–09:00, and 20 of 38 dry foggy days have no fog after 10:00 — and rejected: at List
the pattern is flat and peaks at 10:00, because that is sea fog rather than radiation fog, so a rule
tuned on the mainland would misfire on Sylt. A six-hour bar removes most brief morning fog anyway,
leaving 5 pure-morning days a year at Husum, each of which genuinely had six hours of fog.

**Intensity cannot come from an average.** Mean intensity over a day never reaches the WMO
heavy-rain line of 7.6 mm/h anywhere in the measured year — the maximum is 4.30 mm/h at Husum and
3.66 at List, because a single violent hour averages down against the light ones around it. Only the
daily total separates a wet day from a soaking, and a total belongs in a number rather than in a mark
with two rungs. Hence the mm figure on the card.

## What this costs

**Millimetres overrule the code, on 60 of 197 code-wet days at Husum (30 %) and 64 of 203 at List.**
ADR-0010 explicitly let the icon and the rain bar contradict each other, on the grounds that
correcting one source field with another is authoring, which
[ADR-0004](0004-the-page-relays-warnings-it-never-authors-them.md) forbids. Two things separate the
day card. There is no source field to relay — #11 established that the day state is ours to compute,
so it is authored by construction. And the veto is **one-directional**: across the measured year,
**zero days** carry 1 mm or more without a precipitating code. Millimetres can take rain away; they
can never invent it.

**The sky words now carry two definitions.** In the chart lane, *partly cloudy* means code 2. On the
day card it means a mean cloud cover of 45–85 %. The cuts are calibrated so the two agree on 86 % of
hours, but they are not the same definition and a future reader will find the seam.

**The day card can never show drizzle or downpour**, so it draws on 9 of the 11 states. Drizzle never
carries the most millimetres on a wet day — it overlaps almost entirely with slight rain, maxing at
0.9 mm/h against slight rain's 0.3 mm/h median, so it is a character rather than a weak intensity.
Downpour's codes (65, 82) fired **0 hours in 17 520** at both places under the ICON pin.

**It amends the day card a second time.**
[#13](https://github.com/Commander-Cody/weather-page/issues/13) took the surge deviations off it and
gave it two high-water slots; this adds a precipitation total and removes today's card.

## What it does not cost

**No new API variables.** `precipitation` and `cloud_cover` are both already on the locked list, so
the request weight stays at 1.1 and the budget stays at 1.8 % of quota. Snow-versus-rain share needs
no `snowfall` either — it is `precipitation` summed over the snow-coded hours.

**No new Mooring strings.** The mark needs no translation and `mm` is an SI unit.

**#11's prohibition is intact.** It ruled out *deriving the condition* from cloud cover and
precipitation, because a derivation cannot produce fog, showers or thunderstorm. All three come from
`weather_code` here. Cloud cover only summarises the background the sky was against, which is the one
thing it measures directly.

## Where the work happens

In the scheduled fetch job, like the block condition and for the same reason. The output JSON gains a
condition and a precipitation total per day.

## Related

- [ADR-0010](0010-a-condition-mark-summarises-its-block.md) — the three-hour block rule this one
  deliberately does not reuse.
- [`docs/condition-icons.md`](../condition-icons.md) — the eleven states and their marks. The set is
  the same at both grains; only the aggregation differs.
- [#16](https://github.com/Commander-Cody/weather-page/issues/16) — the ticket.
