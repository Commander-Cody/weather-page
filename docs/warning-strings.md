# Warning strings to translate into Mooring

Handed over by [#10](https://github.com/Commander-Cody/weather-page/issues/10). Source for every
German string: **CAP DWD Profil v2.1.13**, via the research on
[#4](https://github.com/Commander-Cody/weather-page/issues/4).

**No Frisian is written here.** Every Mooring column below is deliberately empty — the repo owner
writes and owns the Mooring text, and no agent may invent, guess at or extend it.

## What is in scope, and what is not

| Group | Count | In the language file? |
|---|---|---|
| Warning event names (§3.1.1), deduplicated, tests removed | 45 | yes |
| Pre-alert names (§3.1.2), test removed | 6 | yes |
| Medical-meteorological names (§3.1.5) | 3 | yes |
| Tier labels | 4 | yes |
| BSH storm surge classes | 3 | yes, pending the source research |
| Page strings for the warning slot | 4 | yes |
| **Total** | **65** | |
| Coastal warnings (§3.1.3, codes 11–13) | 3 | **no** — unreachable |
| High-seas warnings (§3.1.4, codes 14–16) | 3 | **no** — unreachable |
| Test warnings (codes 98, 99) | 3 | **no** — filtered on `status` |
| `description` / `instruction` prose | unbounded | **no** — never rendered inline |

The coastal and high-seas codes are dropped because #4 established that the municipality product
(`COMMUNEUNION_DWD_STAT`) carries no coastal cells, so they can never arrive through the chosen
source. They are not "skipped for now" — they are unreachable.

All 54 event names, the 4 tier labels and the 4 page strings are **defined keys**, so #8's build
gate applies to them untouched: an empty cell in a built variety fails the build. An unknown code
has no key at all, which is why it falls back at runtime instead.

## Keys

The key scheme below is a proposal, not a decision — #8 owns the language file's shape. What #10
does fix is that **the lookup keys on event code plus urgency**, because seven codes carry two
different meanings depending on whether urgency is `immediate` or `future`.

Several codes share one German string, so the table has one row per distinct string with every code
that maps to it. The code-to-key map lives in the build, not in the language file.

## Warning event names (urgency `immediate`)

| Key | Codes | German | Mooring |
|---|---|---|---|
| `warning.event.frost` | 22 | FROST | |
| `warning.event.gewitter` | 31, 90 | GEWITTER | |
| `warning.event.gewitter_stark` | 33, 34, 36, 38, 91 | STARKES GEWITTER | |
| `warning.event.gewitter_schwer` | 92 | SCHWERES GEWITTER | |
| `warning.event.gewitter_extrem` | 93 | EXTREMES GEWITTER | |
| `warning.event.gewitter_schwer_orkan` | 40 | SCHWERES GEWITTER mit ORKANBÖEN | |
| `warning.event.gewitter_schwer_orkan_extrem` | 41 | SCHWERES GEWITTER mit EXTREMEN ORKANBÖEN | |
| `warning.event.gewitter_schwer_regen` | 42 | SCHWERES GEWITTER mit HEFTIGEM STARKREGEN | |
| `warning.event.gewitter_schwer_orkan_regen` | 44 | SCHWERES GEWITTER mit ORKANBÖEN und HEFTIGEM STARKREGEN | |
| `warning.event.gewitter_schwer_orkan_extrem_regen` | 45 | SCHWERES GEWITTER mit EXTREMEN ORKANBÖEN und HEFTIGEM STARKREGEN | |
| `warning.event.gewitter_schwer_regen_hagel` | 46 | SCHWERES GEWITTER mit HEFTIGEM STARKREGEN und HAGEL | |
| `warning.event.gewitter_schwer_orkan_regen_hagel` | 48 | SCHWERES GEWITTER mit ORKANBÖEN, HEFTIGEM STARKREGEN und HAGEL | |
| `warning.event.gewitter_schwer_orkan_extrem_regen_hagel` | 49 | SCHWERES GEWITTER mit EXTREMEN ORKANBÖEN, HEFTIGEM STARKREGEN und HAGEL | |
| `warning.event.gewitter_schwer_regen_extrem_hagel` | 95 | SCHWERES GEWITTER mit EXTREM HEFTIGEM STARKREGEN und HAGEL | |
| `warning.event.gewitter_extrem_orkan_regen_hagel` | 96 | EXTREMES GEWITTER mit ORKANBÖEN, EXTREM HEFTIGEM STARKREGEN und HAGEL | |
| `warning.event.windboeen` | 51 | WINDBÖEN | |
| `warning.event.sturmboeen` | 52 | STURMBÖEN | |
| `warning.event.sturmboeen_schwer` | 53 | SCHWERE STURMBÖEN | |
| `warning.event.orkanartige_boeen` | 54 | ORKANARTIGE BÖEN | |
| `warning.event.orkanboeen` | 55 | ORKANBÖEN | |
| `warning.event.orkanboeen_extrem` | 56 | EXTREME ORKANBÖEN | |
| `warning.event.starkwind` | 57 | STARKWIND | |
| `warning.event.sturm` | 58 | STURM | |
| `warning.event.nebel` | 59 | NEBEL | |
| `warning.event.starkregen` | 61 | STARKREGEN | |
| `warning.event.starkregen_heftig` | 62 | HEFTIGER STARKREGEN | |
| `warning.event.starkregen_extrem_heftig` | 66 | EXTREM HEFTIGER STARKREGEN | |
| `warning.event.dauerregen` | 63 | DAUERREGEN | |
| `warning.event.dauerregen_ergiebig` | 64 | ERGIEBIGER DAUERREGEN | |
| `warning.event.dauerregen_extrem_ergiebig` | 65 | EXTREM ERGIEBIGER DAUERREGEN | |
| `warning.event.schneefall_leicht` | 70 | LEICHTER SCHNEEFALL | |
| `warning.event.schneefall` | 71 | SCHNEEFALL | |
| `warning.event.schneefall_stark` | 72 | STARKER SCHNEEFALL | |
| `warning.event.schneefall_extrem_stark` | 73 | EXTREM STARKER SCHNEEFALL | |
| `warning.event.schneeverwehung` | 74 | SCHNEEVERWEHUNG | |
| `warning.event.schneeverwehung_stark` | 75 | STARKE SCHNEEVERWEHUNG | |
| `warning.event.schneeverwehung_extrem_stark` | 76 | EXTREM STARKE SCHNEEVERWEHUNG | |
| `warning.event.leiterseilschwingungen` | 79 | LEITERSEILSCHWINGUNGEN | |
| `warning.event.frost_streng` | 82 | STRENGER FROST | |
| `warning.event.glaette_gering` | 84 | GERINGE GLÄTTE | |
| `warning.event.glaette` | 87 | GLÄTTE | |
| `warning.event.glatteis` | 85 | GLATTEIS | |
| `warning.event.glatteis_extrem` | 86 | EXTREMES GLATTEIS | |
| `warning.event.tauwetter` | 88 | TAUWETTER | |
| `warning.event.tauwetter_stark` | 89 | STARKES TAUWETTER | |

45 rows.

`LEITERSEILSCHWINGUNGEN` is power-line galloping — overhead cables oscillating under wind and ice
load. Flagged because it is the one term with no everyday equivalent to reach for.

## Pre-alert names (urgency `future`)

These reuse codes from the table above with different text, which is why the lookup needs urgency.

| Key | Code | German | Mooring |
|---|---|---|---|
| `warning.prealert.gewitter_schwer` | 40 | VORABINFORMATION SCHWERES GEWITTER | |
| `warning.prealert.orkanboeen` | 55 | VORABINFORMATION ORKANBÖEN | |
| `warning.prealert.regen` | 65 | VORABINFORMATION HEFTIGER / ERGIEBIGER REGEN | |
| `warning.prealert.schnee` | 75 | VORABINFORMATION STARKER SCHNEEFALL / SCHNEEVERWEHUNG | |
| `warning.prealert.glatteis` | 85 | VORABINFORMATION GLATTEIS | |
| `warning.prealert.tauwetter_stark` | 89 | VORABINFORMATION STARKES TAUWETTER | |

6 rows.

## Medical-meteorological names

Arrive with `category: health`. Shown like any other warning — #10 rejected filtering by category
for the same reason it rejected filtering by severity.

| Key | Code | German | Mooring |
|---|---|---|---|
| `warning.event.uv_index` | 246 | UV-INDEX | |
| `warning.event.hitze_stark` | 247 | STARKE HITZE | |
| `warning.event.hitze_extrem` | 248 | EXTREME HITZE | |

3 rows.

## Tier labels

The four DWD severities, which are also ranks 1–4 on the single ladder #10 settled on.

| Key | Rank | CAP `severity` | German | Mooring |
|---|---|---|---|---|
| `warning.tier.1` | 1 | `minor` | Wetterwarnung | |
| `warning.tier.2` | 2 | `moderate` | Markante Wetterwarnung | |
| `warning.tier.3` | 3 | `severe` | Unwetterwarnung | |
| `warning.tier.4` | 4 | `extreme` | Extreme Unwetterwarnung | |

4 rows. Note there is **no** fifth tier: Vorabinformation is `urgency = future`, not a severity, and
#10 carries it in the event name instead.

## BSH storm surge classes

Pending the source research. Classes are defined by height above mean high water. They occupy ranks
2, 3 and 4 of the same ladder, so they share the DWD tier colours.

| Key | Rank | Threshold above MHW | German | Mooring |
|---|---|---|---|---|
| `warning.surge.1` | 2 | 1.5–2.5 m | Sturmflut | |
| `warning.surge.2` | 3 | 2.5–3.5 m | schwere Sturmflut | |
| `warning.surge.3` | 4 | over 3.5 m | sehr schwere Sturmflut | |

3 rows.

## Page strings for the warning slot

| Key | Purpose | Mooring |
|---|---|---|
| `warning.unknown` | Generic name for a warning whose code has no string. Must read as a real warning, not as a fault. | |
| `warning.link` | Link to DWD's warning page for this place's area. Names the language: **`tjüsch`** (owner-supplied). | |
| `warning.source` | Data-source label, followed by the untranslated proper name `Deutscher Wetterdienst`. Not `Quelle:` — see the ADR. | |
| `warning.failed` | Shown when the warning fetch fails. Must say the page cannot see the warnings, never that there are none. | |

4 rows.

Once BSH surge warnings land there are two sources and two independent failures, so `warning.failed`
may need to split into one string per source. That waits on the BSH research.

## Terms already supplied by the owner

- **`tjüsch`** — German (the language). Uses the palatal `tj`, verified by #20 as surviving the
  spreadsheet round trip unchanged.
