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
- Fetch age is still recorded and is what the healthy page displays, because "aktualisiird
  09.14" is what a reader understands. It just never decides anything.
