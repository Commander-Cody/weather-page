# North Frisian weather & water-level page

A public, Mooring-Frisian-only weather and water-level page for a curated set of North
Frisian places. Its defining feature is wind, rain and water level fused onto one time
axis, so the good window is visible at a glance.

## Language

### Freshness

**Data age**:
How old the numbers themselves are — the time since the model run they come from was
initialised, or since the last measurement. Never zero, even when everything is healthy.
This is the quantity that decides whether something is stale.
_Avoid_: age, staleness, lag

**Fetch age**:
The time since the scheduled job last successfully retrieved a source. Grows without
bound when the job fails, but stays near zero when a source is reachable yet frozen.
Shown to the reader on a healthy page; never used to decide staleness.
_Avoid_: last updated, refresh age

**Staleness threshold**:
The data age past which a source stops presenting itself as current. One per source, set
at that source's normal worst-case data age plus one missed publication.
_Avoid_: timeout, expiry, TTL

**Stale**:
A source whose data age has crossed its staleness threshold. Its data is still on the
page unless it is unsafe to show; it simply no longer claims to be current.
_Avoid_: expired, out of date

**Implausible**:
A value a source returned successfully that cannot be true — a sea temperature for a
point that is dry land. Treated as missing, never as stale, and never reaches the page.
_Avoid_: invalid, bad data

**Last good**:
The most recent successfully fetched data for a source, kept on disk and served when a
later fetch fails. The page degrades by ageing its last good data, not by emptying.
_Avoid_: cache, fallback

### Water level

**Astronomical tide**:
The tide predicted from the moon and sun alone. A calculation, not a measurement, so it
never goes stale — a series fetched hours ago is still exactly right for days ahead.
Mooring: `astronoomsche tide`.
_Avoid_: predicted tide, tide table

**Surge-corrected forecast**:
The water level actually expected, astronomical tide plus the weather-driven surge. The
gap between it and the astronomical tide is what the page exists to show. Unlike the
astronomical tide, it goes stale quickly. Mooring: `korigiird (wååderpäägel)forütseeding`.
_Avoid_: real tide, actual level

**Deviation**:
How far a high or low water sits above or below its normal — mean high water at highs,
mean low water at lows. Every height on the page is a deviation; absolute centimetres
above gauge zero appear nowhere.
_Avoid_: height, level, absolute height

### Places and gauges

**Place**:
One of the curated locations the page covers, with its own URL and its own page. A row in
the place registry, not a design decision — adding one costs a row and a Frisian name.
_Avoid_: location, station, city

**Own gauge**:
The tide gauge at the place itself. Always preferred, even when it carries only peaks.
_Avoid_: local station, home gauge

**Borrowed gauge**:
Another place's gauge, adopted only where a place has no gauge of its own. Named on the
page like any other, so a borrow is never silent.
_Avoid_: fallback gauge, substitute

**Curve gauge**:
A gauge publishing a water level every 10 minutes across the whole forecast window, so
the surge is visible for about 5.7 days. Nine of the 23 gauges on this coast.
_Avoid_: full gauge, good gauge

**Peaks-only gauge**:
A gauge publishing high and low water times and heights but no curve. Same 5.7-day peak
horizon as a curve gauge, but the surge correction reaches only about 18 hours — after
which its astronomical curve is interpolated by us from the peaks.
_Avoid_: partial gauge, degraded gauge

**Land point**:
The coordinates a place's wind, rain and temperature forecast is read at. The settlement
itself.
_Avoid_: coordinates, position

**Sea point**:
A separate water coordinate a place's sea temperature is read at, kept apart from the
land point because the Marine API returns a value for land too. Validated by comparing
the coordinates requested against the coordinates returned.
_Avoid_: marine coordinates, water position

### Variety and translation

**Variety**:
One of the North Frisian varieties the page can be read in. A property of the reader, not
of the place — a Fering reader sees Fering on every page, including mainland ones. Mooring
at launch, Fering planned.
_Avoid_: locale, dialect, language

**Built variety**:
A variety named in the Astro config and therefore rendered, linked and published. A
variety whose column is incomplete is simply not built; only a built variety can fail the
build for a missing string.
_Avoid_: enabled language, active locale, supported language

**Native name**:
What a place is called on its own coast, recorded together with the variety that name
belongs to. It is the label every reader sees unless their own variety overrides it.
_Avoid_: default name, local name, endonym

**Variety override**:
A per-variety form of a place name, replacing the native name for readers of that variety.
Absent by default — a variety carries an override only where it genuinely differs, or to
record that a fluent speaker confirmed it does not.
_Avoid_: translation, per-locale name, localised name

**Unresolved name**:
A place whose native name is in a variety other than the reader's and which that variety
has not overridden. It still shows the native name; the state exists to raise a question
for a fluent speaker, never to change the page.
_Avoid_: missing name, untranslated place

**Batch list**:
The generated list of open language questions for a fluent speaker: empty cells in a built
variety, unresolved names, and strings whose wording is written but unverified. Derived
from the language file, never kept by hand.
_Avoid_: todo list, translation queue
