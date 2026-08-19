# The page names the forecast model it reads

Open-Meteo's `best_match` picks a model per coordinate and does not tell you which one it
picked. Above **54.90 N** it picks MET Norway Nordic instead of the DWD ICON chain, which put
three of the twenty places — `list`, `westerland`, `neukirchen` — on a weather condition
Open-Meteo **derives** from cloud cover and precipitation, because MET Norway publishes no
native condition field. That derivation is the one this project already measured and rejected
for every other place: it cannot produce fog, showers or thunderstorm at all. So every place
now requests `models=icon_seamless` explicitly, and the fetch job proves the pin held by
checking that the coordinates Open-Meteo echoes back sit on ICON's 0.02° lattice.

This reverses the "never pass `models=`" rule that came out of the Open-Meteo research. That
rule was sound and its evidence was real — it was gathered at Husum, and only at Husum.

## Why the split mattered more than it looked

It reads like a cosmetic disagreement between neighbouring places, and it is not. The three
northern places were structurally incapable of showing three of the states the page has icons
for. Measured over one year, List logged **933 h of drizzle and zero hours of fog, showers or
thunderstorm**; Hörnum, 25 km down the same island on ICON, logged 16 h of drizzle against
134 h of fog, 317 h of showers and 25 h of thunderstorm. Live at List on 2026-08-19 the two
models disagreed on **89 of 163 hours**, and ICON found a thunderstorm where `best_match`
found drizzle.

The defect was therefore *inside* each of those places, not between them and their neighbours.
A reader on Sylt could never have been shown fog.

## Considered options

- **Accept the split.** Each place gets whichever model Open-Meteo prefers there. Rejected:
  it keeps the derived condition, and no amount of per-place honesty makes a page that cannot
  show fog on a foggy coast correct.
- **Collapse drizzle into rain** so the loudest symptom disappears. Rejected: it hides one
  state and leaves fog, showers and thunderstorm still missing, while costing the
  drizzle/rain distinction at the seventeen places where the condition is native and reliable.
  It makes two different things look the same instead of making them the same.
- **Pin only the three northern places.** Rejected: it fixes the instance and leaves the
  mechanism running. The other seventeen would still be choosing a model by latitude, so a
  shift in Open-Meteo's preference — or a corrected coordinate — could still move a place
  between models with no commit on our side.
- **Pin the condition but keep `best_match` for the numbers**, via a second small request for
  `weather_code` alone (about 2.4 quota units a day, genuinely cheap). Rejected on coherence:
  the icon would come from a different model than the rain bar drawn beside it, on the one
  page whose defining feature is fusing them onto a shared axis. The condition and the
  precipitation already disagree on 2.5 % of hours *within* a single model; sourcing them
  from two would make that systematic.

The measured harm was all on the accept-it side and it was categorical. The harm claimed for
pinning — "quietly worse data at the three places furthest from ICON-D2" — turned out to rest
on a false premise: ICON-D2's grid reaches **58.08 N**, so List at 55.02 N sits roughly 340 km
inside it, not at its edge. No accuracy measurement was run, deliberately, because no accuracy
score can outweigh a state that can never appear.

## Consequences

- **The page stops tracking Open-Meteo's model preference.** If a better model over Germany
  appears, twenty places keep asking for ICON until a human changes one value. This is the
  accepted cost: an explicit value that can be verified beats an implicit one that can move
  without notice.
- **The 54.90 N boundary stops being load-bearing.** It was an empirical finding that the
  research could not locate in Open-Meteo's source and warned could move silently. It can now
  move freely without affecting the page. `neukirchen` sits 1.5 km above the line and its land
  point is still being confirmed; that correction is now just a coordinate change.
- **The pinned model is a fifth hand-paired value under ADR-0006**, verified by the same
  coordinate echo the land point and sea point already use — a third instance of an existing
  mechanism, not a new one. It lives as a constant in the fetch job rather than a registry
  field, because it has one instance rather than one per place.
- **There is one atmospheric source again**, so the three northern places need no staleness
  threshold of their own.
- **But `icon_seamless` is three models wearing one name**, and ADR-0001's single 8 h weather
  threshold was only ever right for the first 48 hours. See the amendment there.
- **Drizzle nearly disappears from the roster.** The ICON places log 16–25 h a year against
  List's 933. Any count of "which condition states actually occur here" gathered before this
  decision was counting MET Norway's vocabulary and needs redoing.
- **The Marine API is not covered by this.** Sea temperature comes from a separate endpoint
  that also picks a model by `best_match` and names no model in its response. The same
  question is open there.
