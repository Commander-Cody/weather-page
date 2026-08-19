# Staleness is measured by data age, not fetch age

The page is fed by a scheduled job, so the obvious way to detect stale data is to record
when each fetch last succeeded and warn once that gets old. We do not do that. A source
can keep answering while serving a model run that stopped advancing — Open-Meteo returns
a valid response either way — and in that case the fetch age stays near zero while the
numbers on the page get steadily older. Fetch age would report the page as healthy at
exactly the moment it is lying.

So each source carries its **data age** — time since its model run was initialised, or
since its last measurement — and that is what the staleness threshold is measured
against. It catches both failure modes with one mechanism: a fetch that never happened
and a publication that never happened both show up as data that has not advanced.

## Consequences

- Every source has a **non-zero normal data age**, so thresholds are set relative to that
  baseline rather than to zero: ICON-D2 weather is routinely 4.5 h old, sea temperature
  36 h. Thresholds are that baseline plus one missed publication — 8 h, 2 h for water,
  60 h for sea temperature.
- Weather data age is not in the forecast response. It comes from
  `api.open-meteo.com/data/dwd_icon_d2/static/meta.json`, which is free and does not count
  against the API quota. `generationtime_ms` in the forecast response is server processing
  time and is not a run time.

## Amendment: the weather source is three models, not one (ADR-0009)

The 8 h weather threshold above is ICON-D2's number, and it was only ever right for the first
48 hours of the forecast. `icon_seamless` is a chain of three models with three different
publication cadences, and the "one threshold per source" rule applies to each of them:

| Covers | Model | Publishes every | Threshold |
| --- | --- | --- | --- |
| hours 0–48 — the fused chart | ICON-D2 | 3 h | 8 h |
| beyond 48 h — the day cards | ICON-EU, then ICON Global | 3 h / 6 h | ~16 h |

ICON Global's 6-hourly cadence plus roughly 3.5 h between initialisation and availability puts
its honest threshold at about double D2's. Applying D2's 8 h to the whole horizon would report
an age the page has reason to know is wrong for days 3–7 — measured on 2026-08-19, ICON-EU's
run was **6 h older** than the D2 run whose `meta.json` was being read. That is precisely the
"answering while serving a frozen run" failure this ADR exists to catch, so the three metas are
read and each horizon segment is aged against its own.

This is not a special case bolted onto the rule. It is the rule — *per source* — applied to
three sources that happened to share an alias.

**Consequence:** the page can be fresh in the chart and stale in the day cards at the same
time, so the freshness line needs wording that can say two things at once. That is a string
question, not a design one.
- Fetch age is still recorded and is what the healthy page displays, because "aktualisiird
  09.14" is what a reader understands. It just never decides anything.
