# BSH storm surge warnings: is there a feed, and what is the closed list?

Research for [issue #26](https://github.com/Commander-Cody/weather-page/issues/26). Investigated
against primary sources only: the live BSH API, BSH's own PDFs, BSH's own XML warning product and
its stylesheet, and archived snapshots of that product taken during real storm surges.

All live measurements were taken on **2026-08-15 between 23:05 and 23:25 UTC** (2026-08-16,
01:05–01:25 CEST). Every header quoted below is copied from a real response, made with `curl` and an
`Origin:` request header set to a foreign origin (`https://weather.example.org`). Values move; the
*shapes* are what matter.

**A note on language.** This document contains no Mooring. Where the page will need a Frisian
string, the gap is named and left open — see [§10](#10-what-this-leaves-for-the-owner-to-write).
German source strings are reproduced verbatim, including BSH's own spelling inconsistencies.

---

## 1. Verdict up front

**Yes. A machine-readable BSH storm surge warning exists, it is browser-fetchable, and it is
already inside a product this project has researched** — it is a field on the
`WaterLevelForecast` features from [#2](https://github.com/Commander-Cody/weather-page/issues/2),
not a separate service.

| Question | Answer |
| --- | --- |
| **Is there a machine-readable product?** | Yes — `official_warning_level_region` on every coastal feature of the `WaterLevelForecast` collection. Also a standalone XML product, `sturmflut_aktuell.xml`. |
| **Can a browser fetch it?** | **Yes, the API can** — `Access-Control-Allow-Origin: *`. **But only if the request carries a `lang` parameter**; without it the request 301-redirects and the redirect has no CORS header. The standalone XML **cannot** — no CORS header at all. |
| **How is it scoped?** | The official warning is scoped to **the entire German North Sea coast** — one value for all 20 places. Coarser than a coastal section. Two *automated* fields are finer (per gauge, per tide event). |
| **Three classes, or finer?** | **Three warning classes plus an explicit no-warning default**, for the North Sea. Table 5 of BSH's parameter PDF lists nine values in total, but five of them are Baltic-only. |
| **Freshness** | Official forecast 4×/day, round the clock during a surge. The no-warning state is a **positive value**, not an absent field. |
| **Licence** | **CC BY 4.0** — the #2 instrument, stated in-band. The #12 tide-calculator instrument does **not** apply. |

**The single most consequential finding is about granularity, not availability.** The official
warning is one headline for the whole German North Sea coast, and during the surge of 2022-01-30 that
headline read `Schwere Sturmflut` while BSH's own prose in the same document put the North Frisian
coast a full class lower. See [§5](#5-scoping-the-finding-that-should-drive-the-decision). This is a
decision for a human, and this document does not make it.

**Three things contradict assumptions recorded elsewhere in the project** — see
[§9](#9-what-this-contradicts-elsewhere-in-the-project). The sharpest is that DWD and BSH impose
*opposite* attribution rules on the same warning slot.

---

## 2. CORS, verified empirically

### 2.1 The API — open, with a trap

```
$ curl -s -D - -o /dev/null -H "Origin: https://weather.example.org" \
    "https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/collections/waterlevelforecastdata/items/husum_schleuse?lang=en&f=json"
HTTP/1.1 200 OK
Content-Type: application/geo+json
ETag: "a5181b2fbe8c38832a566c48e8226d53"
Vary: Accept,Accept-Language,Accept-Encoding
Content-Language: en
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Expose-Headers: Link, Content-Crs, OATiles-hint, Prefer, ETag
Access-Control-Allow-Headers: X-Requested-With,Origin,Content-Type,Accept
Access-Control-Allow-Methods: GET, POST
```

**The same URL without `lang` does not work from a browser:**

```
$ curl -s -D - -o /dev/null -H "Origin: https://weather.example.org" \
    "https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/collections/waterlevelforecastdata/items/husum_schleuse?f=json"
HTTP/1.1 301 Moved Permanently
Server: Apache/2.4.67 (Debian)
Location: https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/collections/waterlevelforecastdata/items/husum_schleuse?lang=en&f=json
Content-Length: 459
Content-Type: text/html; charset=iso-8859-1
            <- no Access-Control-Allow-Origin anywhere in the response
```

Apache rewrites the request to append `lang=en`, and **that redirect response carries no CORS
header**. Under the Fetch standard a cross-origin redirect must itself pass the CORS check
([Fetch, §4.4 "HTTP-redirect fetch"](https://fetch.spec.whatwg.org/#http-redirect-fetch)), so the
browser aborts before it ever sees the 200. `curl -L` hides this completely — which is exactly why
this had to be checked with the redirect unfollowed.

The trigger is a literal `lang` substring in the query string. Verified three ways:

| Query string contains | Result |
| --- | --- |
| `?f=json` | **301**, no CORS |
| `?f=json&lang=de` | **200**, `Access-Control-Allow-Origin: *`, `Content-Language: de` |
| `?f=json&lang=en` | **200**, `Access-Control-Allow-Origin: *`, `Content-Language: en` |
| `?f=json&filter-lang=cql2-text` | **200**, `Access-Control-Allow-Origin: *` (the substring alone satisfies the rewrite) |

**This also resolves the open caveat in #2.** That document reported "an explicit `OPTIONS`
preflight 301-redirects, so keep requests CORS-simple". The preflight was not the problem — the
missing `lang` was:

```
$ curl -s -D - -o /dev/null -X OPTIONS -H "Origin: https://weather.example.org" \
    -H "Access-Control-Request-Method: GET" \
    "…/items/husum_schleuse?f=json"
HTTP/1.1 301 Moved Permanently
Location: …/items/husum_schleuse?lang=en&f=json

$ curl -s -D - -o /dev/null -X OPTIONS -H "Origin: https://weather.example.org" \
    -H "Access-Control-Request-Method: GET" \
    "…/items/husum_schleuse?f=json&lang=de"
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: X-Requested-With,Origin,Content-Type,Accept
```

With `lang` present the preflight is clean. Requests do **not** have to be CORS-simple; they have to
carry `lang`. #2's write-up should be corrected on this point.

### 2.2 The standalone XML — closed

```
$ curl -s -D - -H "Origin: https://weather.example.org" \
    https://www2.bsh.de/aktdat/wvd/sturm/sturmflut_aktuell.xml
HTTP/1.1 200 OK
Server: Apache/2.4.59 (Debian)
Last-Modified: Sat, 15 Aug 2026 23:01:02 GMT
ETag: "585-6591de9396532"
Content-Length: 1413
Content-Type: application/xml
            <- no Access-Control-Allow-Origin anywhere in the response
```

Not browser-fetchable. It is still the more *interesting* document — see §4 — but it can only be
read by the scheduled job.

### 2.3 The federal warning relay (NINA / MoWaS) — closed, and empty

Checked because storm surge warnings are also disseminated through the BBK's public warning system,
which would in principle offer district-level scoping:

```
$ curl -s -D - -o /dev/null -H "Origin: https://weather.example.org" \
    https://warnung.bund.de/api31/dashboard/010540000000.json
HTTP/1.1 200 OK
Server: myracloud
Content-Type: application/json
ETag: "1786043661284"
Last-Modified: Thu, 06 Aug 2026 19:14:21 GMT
cache-control: max-age=10
            <- no Access-Control-Allow-Origin anywhere in the response
```

Body was `[]` (no active warnings for Kreis Nordfriesland, AGS `01054`). No CORS, it is a relay
rather than the issuing authority, and it carries only warnings that have been escalated to the
population-warning system — which a routine `Sturmflut` need not be. Not a candidate.

### 2.4 Keys, robots

All endpoints above are keyless — no registration, no token. Neither BSH host publishes a
`robots.txt`:

```
$ curl -s -o /dev/null -w "%{http_code}\n" https://gdi.bsh.de/robots.txt
404
$ curl -s -o /dev/null -w "%{http_code}\n" https://www2.bsh.de/robots.txt
404
```

This is worth recording because it *differs* from `filebox.bsh.de`, where
[#12](https://github.com/Commander-Cody/weather-page/issues/12) found `User-agent: * / Disallow: /`.
The robots question raised there does not extend to these two hosts.

---

## 3. The product: three warning fields, not one

The `WaterLevelForecast` collection carries **three** distinct warning-level fields. They differ in
scope and in authorship, and conflating them would be a serious error. All three are documented in
BSH's own parameter reference, [`parameter_documentation.pdf`](https://www2.bsh.de/aktdat/wvd/api/parameter_documentation.pdf)
(dated 27.05.2026), which is the authoritative field reference.

| Field | Where | BSH's own description (verbatim, English PDF) | Scope | Human or automated |
| --- | --- | --- | --- | --- |
| `official_warning_level_region` | feature `properties` | "Official warning level for the North Sea or Baltic Sea (see Tab. 5)" | **Whole sea** | **Official / human** |
| `automated_gauge_warning` | feature `properties` | "Automatically generated warning level for this gauge station" | **One gauge** | Automated |
| `forecast_automated_event_warning` | each `high_water_low_water` entry | "Automated warning level of the event" | **One tide event at one gauge** | Automated |

The PDF is explicit that the official one is not a station-level statement:

> "Depending on the current or expected water level on the German North Sea and Baltic Sea coasts,
> official information or warnings are published. The threshold water levels differ between the
> North Sea and the Baltic Sea. The respective category is given in the
> `official_warning_level_region` parameter (see Tab. 1). **Please note that the warning level does
> not apply specifically to a particular gauge station.**"
>
> — `parameter_documentation.pdf`, p. 4 (emphasis in the original is absent; the sentence is verbatim)

### 3.1 Live values, whole collection

Fetched all 136 features in one request:

```
GET https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/collections/waterlevelforecastdata/items
    ?f=json&limit=200&lang=de
→ numberMatched: 136, numberReturned: 136
```

| Field | `north_sea` | `baltic_sea` |
| --- | --- | --- |
| `official_warning_level_region` | `"Wasserstandsvorhersage"` ×75, **absent ×7** | `"Wasserstandsvorhersage"` ×54 |
| `automated_gauge_warning` | `"Wasserstandsvorhersage"` ×82 | **absent ×54** |

Two structural facts fall out of that table:

- **`automated_gauge_warning` is a North Sea–only field.** It is present on all 82 North Sea
  features and on none of the 54 Baltic ones. Irrelevant to this project directly, but it tells you
  the field is a product of the North Sea MOS chain, not a general facility.
- **The 7 North Sea features without an official warning level are all river gauges**, not coastal
  ones: `bremen_wilhelm-kaisen-bruecke`, `elsfleth_ohrt`, `geesthacht_wehr_unterpegel`,
  `hamburg_zollenspieker`, `leerort`, `oldenburg_drielake`, `papenburg` — areas `Weser`, `Elbe`,
  `Ems`. So **an absent field means "not a coastal station", never "no warning"**. All 23 North
  Frisian gauges carry all three fields; verified individually, 23/23.

### 3.2 The per-event field only covers the official window

`forecast_automated_event_warning` is populated only on the events that also carry an official
forecast — the next four. Live, `husum_schleuse`, 22 events in `high_water_low_water`:

| index | `event_timestamp` | official `forecast_value`? | `forecast_automated_event_warning` |
| --- | --- | --- | --- |
| 0 | `2026-08-16 05:11:00+02:00` | yes | `"Wasserstandsvorhersage"` |
| 1 | `2026-08-16 11:26:00+02:00` | yes | `"Wasserstandsvorhersage"` |
| 2 | `2026-08-16 17:22:00+02:00` | yes | `"Wasserstandsvorhersage"` |
| 3 | `2026-08-16 23:58:00+02:00` | yes | `"Wasserstandsvorhersage"` |
| 4–21 | `2026-08-17 …` to `2026-08-21 13:39:00+02:00` | no | **key absent** |

So the per-event warning reaches roughly **19 hours**, matching the ~17 h official peak horizon #2
measured — not the 5.7-day curve horizon. Two features in the whole collection returned an **empty
string** rather than an absent key for this field, so a consumer must treat `""` and absent alike.

### 3.3 The strings are not localised

This matters for the translation table, so it was checked directly:

```
$ …/items/husum_schleuse?f=json&lang=de → official_warning_level_region = 'Wasserstandsvorhersage'
$ …/items/husum_schleuse?f=json&lang=en → official_warning_level_region = 'Wasserstandsvorhersage'
```

`lang` switches `forecast_text`, `copyright`, `information_text` and the `Link` titles, but **the
warning level strings stay German in both**. There is **no numeric code anywhere** — not in the API,
not in the PDF, not in the XML. **The German string is the identifier.** See §9 for why that cuts
against #4's stated reason for choosing Bright Sky.

---

## 4. The standalone warning product, and what it reveals

BSH runs a dedicated *Sturmflutwarndienst* page at <https://www2.bsh.de/aktdat/wvd/sturm/>. It is a
shell whose entire content is an `<iframe src="sturmflut_aktuell.xml">`. That XML is the actual
warning document, and it is the thing the API field is derived from.

**Live, at 2026-08-15 23:09 UTC** (verbatim, whitespace as returned):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="sturmflut.xsl"?>
<BLOCK>
	<CREATIONDATE>16.08.2026, 00:10</CREATIONDATE>
	<AUTHOR>Bundesamt für Seeschifffahrt und Hydrographie</AUTHOR>
	<REGIONAL>Deutsche Nordseeküste</REGIONAL>
	<SHORTTITLE>Wasserstandsvorhersage</SHORTTITLE>
	<VORHERSAGETEXT>Am Sonntag werden das Morgen-Hochwasser an der deutschen Nordseeküste und in Emden sowie das Vormittag-Hochwasser in Bremen und Hamburg <b>nicht wesentlich</b> vom mittleren Hochwasser abweichen.</VORHERSAGETEXT>
	<FORECAST_TEXT>On Sunday, the morning high water along the German North Sea coast and in Emden, Bremen and Hamburg will <b>not deviate significantly</b> from the Mean High Water.</FORECAST_TEXT>
	<DISCLAIMER>The English translation of the official German forecast is provided for convenience only and is not legally binding.</DISCLAIMER>
	<ZUSATZ></ZUSATZ>
	<ADDITION></ADDITION>
	<TIME_HW_CUX>16.08.2026, 04:24</TIME_HW_CUX>
	<TIME_HW_HH>16.08.2026, 07:54</TIME_HW_HH>
	<TEL>040-3190 3190</TEL>
	<URL>https://wasserstand-nordsee.bsh.de</URL>
<BLOCKOST>
<AUTHOR>Bundesamt für Seeschifffahrt und Hydrographie Rostock</AUTHOR>
<REGIONAL>DOK</REGIONAL>
<SHORTTITLE>ENTWARNUNG</SHORTTITLE>
<WARNTEXT>
Zurzeit liegt keine Sturmflutwarnung für die deutsche Ostseeküste vor.
</WARNTEXT>
<VALID_FROM>2026-08-15T13:22</VALID_FROM>
<URL>http://www.bsh.de</URL>
</BLOCKOST>
</BLOCK>
```

Three things to take from this:

1. **`BLOCK/SHORTTITLE` is the same value as the API's `official_warning_level_region`**, and
   `BLOCK/VORHERSAGETEXT` is byte-for-byte the API's `forecast_text.de` for every North Sea station.
   Confirmed against `husum_schleuse` fetched in the same minute. The API field is this document,
   republished with CORS.
2. **The Baltic block uses a value the API's closed list does not contain** — `ENTWARNUNG`. The XML
   and the API do not share one vocabulary. Only the North Sea `BLOCK` matters for this project, but
   do not assume the two products are interchangeable.
3. `<REGIONAL>Deutsche Nordseeküste</REGIONAL>` — the scope, stated in band. The whole coast.

### 4.1 The stylesheet is a primary source for the closed list

[`sturmflut.xsl`](https://www2.bsh.de/aktdat/wvd/sturm/sturmflut.xsl) (`Last-Modified: Mon, 30 Jun
2025`) branches on `BLOCK/SHORTTITLE`. Its `xsl:when` tests are an exhaustive enumeration of the
values BSH's own renderer expects for the North Sea, and the sentence each produces:

| `BLOCK/SHORTTITLE` | Sentence rendered (verbatim) |
| --- | --- |
| `Sturmflut` | `Für die deutsche Nordseeküste besteht die Gefahr einer Sturmflut.` |
| `Schwere Sturmflut` | `Für die deutsche Nordseeküste besteht die Gefahr einer schweren Sturmflut.` |
| `Sehr schwere Sturmflut` | `Für die deutsche Nordseeküste besteht die Gefahr einer sehr schweren Sturmflut.` |
| *(`ZUSATZ` non-empty)* | renders the free-text `ZUSATZ` — not a class |
| *(otherwise)* | `Zurzeit liegt keine Sturmflutwarnung für die deutsche Nordseeküste vor.` |

All three warning branches also render:

> `Die Sturmflutgefahr besteht bis etwa <TIME_HW_HH>. Bitte informieren Sie sich regelmäßig!`

— note that the end-of-danger time BSH publishes is **Hamburg's** high water, which on the North
Frisian coast is roughly three and a half hours *after* the local peak. It is not a per-place
validity time.

**`Erhoehter Wasserstand` does not appear in the North Sea branches at all**, which independently
corroborates Table 5's blank North Sea cell (§5.1).

---

## 5. Scoping: the finding that should drive the decision

### 5.1 The official warning is one value for the entire German North Sea coast

Not a coastal section. Not a gauge. One string, `Deutsche Nordseeküste`, covering everything from
the Dutch border to the Danish border. **All 20 places would display the identical warning.**

### 5.2 And it is the maximum over that coast, which over-warns North Frisia

This is not a theoretical worry. The Wayback Machine holds snapshots of `sturmflut_aktuell.xml`
taken during real surges. From **2022-01-30**, during storm *Nadia*
([snapshot `20220130085106`](https://web.archive.org/web/20220130085106id_/https://www2.bsh.de/aktdat/wvd/sturm/sturmflut_aktuell.xml)):

```xml
	<CREATIONDATE>30.01.2022, 08:13</CREATIONDATE>
	<REGIONAL>Deutsche Nordseeküste</REGIONAL>
	<SHORTTITLE>Schwere Sturmflut</SHORTTITLE>
	<VORHERSAGETEXT>Am Sonntag werden das Vormittag-Hochwasser bzw. das Nachmittag-Hochwasser an der ostfriesischen Küste, im Weser- und Elbegebiet 2 bis 2,5 m höher als das mittlere Hochwasser eintreten, an der nordfriesischen Küste 1,5 bis 2 m höher als das mittlere Hochwasser eintreten und im Hamburger Elbegebiet 2,5 bis 3 m höher als das mittlere Hochwasser eintreten.</VORHERSAGETEXT>
```

Read the two together. The machine-readable headline says **`Schwere Sturmflut`**. BSH's own prose
in the same document says the North Frisian coast is getting **1,5 bis 2 m über MHW** — which is
plainly a `Sturmflut`, one class down. The `Schwere Sturmflut` headline is earned by Hamburg and the
Elbe, 150 km away.

So a page that renders `official_warning_level_region` for Husum on that day would have shown a
North Frisian reader a class higher than BSH's own text said applied to them. Given that
[ADR-0004](https://github.com/Commander-Cody/weather-page/blob/decide/warnings-presentation/docs/adr/0004-the-page-relays-warnings-it-never-authors-them.md)
exists precisely because
"a page that names a *sehr schwere Sturmflut* on its own authority is making a safety claim it
cannot stand behind", relaying an overstated class deserves the same scrutiny. The page would not be
authoring it — but it would be presenting a coast-wide maximum as though it were local.

**The regional detail exists only as prose.** `VORHERSAGETEXT` is free text; it is not a closed list
and cannot be translated as one, exactly as #4 concluded for CAP `description`/`instruction`.

### 5.3 The automated fields do map onto the gauges we already pair

`automated_gauge_warning` is per gauge, and since
[ADR-0002](https://github.com/Commander-Cody/weather-page/blob/main/docs/adr/0002-local-gauge-data-wins-over-a-borrowed-curve.md)
every place already has a
gauge, it maps onto the existing pairing with no new curation. All 15 distinct gauges behind the 20
places carry the field:

| gauge | places served |
| --- | --- |
| `list_hafen` | `list` |
| `westerland` | `westerland` |
| `hoernum_hafen` | `hoernum` |
| `wyk` | `wyk` |
| `wittduen_hafen` | `wittduen` |
| `hooge_anleger` | `hooge` |
| `der_strand_hamburger_hallig` | `hamburger-hallig`, `bredstedt` |
| `pellworm_anleger` | `pellworm` |
| `strucklahnungshoern` | `nordstrand` |
| `husum_schleuse` | `husum` |
| `dagebuell` | `dagebuell`, `niebuell`, `risum-lindholm` |
| `helgoland_binnenhafen` | `helgoland` |
| `osterley` | `klanxbuell`, `emmelsbuell-horsbuell`, `neukirchen` |
| `schluettsiel` | `langenhorn` |
| `eider-sperrwerk_aussenpegel` | `toenning` |

15 gauges, 20 places, all present. Note the consequence of borrowing: `niebuell` and
`risum-lindholm` are 11–12 km inland and would show `dagebuell`'s surge warning. That is the same
trade ADR-0002 already accepted for water level, so it is not a new cost — but a *warning* borrowed
inland reads differently from a *tide curve* borrowed inland, and that is worth a moment's thought.

### 5.4 The trade-off, stated plainly

| | `official_warning_level_region` | `automated_gauge_warning` |
| --- | --- | --- |
| Authority | **Official**, human forecaster, `Amtliche Wasserstandsvorhersage des Bundes gemäß §1 SeeAufG` | Automated MOS output, published by BSH |
| Scope | Whole German North Sea coast | The place's own (or borrowed) gauge |
| Accuracy for North Frisia | Can overstate by a class (§5.2) | Local by construction |
| Documented closed list | **Yes** — Table 5, plus the XSL | **No** — PDF says only "Automatically generated warning level" |
| Satisfies ADR-0004? | Yes, unambiguously | Yes on the letter — BSH classifies, the page does not — but it is not the *amtliche* warning |

**This document does not choose.** Both are BSH-published, so ADR-0004's bar is cleared either way,
and the choice is an editorial one about whether "official but coast-wide" beats "local but
automated". It belongs in the decision ticket, not in research.

---

## 6. The closed list, literal and complete

From `parameter_documentation.pdf`, **Tab. 5 "Overview of the official warning level categories"**,
reproduced exactly as printed — including `Erhoehter` spelled without the umlaut, which is how BSH
writes it:

| warning level categories | North Sea (relative to MHW) | Baltic Sea (relative to NHN) |
| --- | --- | --- |
| `"Wasserstandsvorhersage"` | Default | Default |
| `"Erhoehter Wasserstand"` | — | +0.75 m |
| `"Sturmflut"` | **+1.5 m** | +1.0 m |
| `"Schwere Sturmflut"` | **+2.5 m** | +1.5 m |
| `"Sehr schwere Sturmflut"` | **+3.5 m** | +2.0 m |
| `"Niedriger Wasserstand"` | — | −0.75 m |
| `"Niedrigwasser"` | — | −1.0 m |
| `"Schweres Niedrigwasser"` | — | −1.5 m |
| `"Sehr schweres Niedrigwasser"` | — | −2.0 m |

**Nine values exist; four can appear on the North Sea.** The five with an em dash have a genuinely
blank cell in BSH's table, not a different threshold.

### 6.1 So the list this project must translate is four strings

```
Wasserstandsvorhersage      ← the no-warning state
Sturmflut                   ← rank 2
Schwere Sturmflut           ← rank 3
Sehr schwere Sturmflut      ← rank 4
```

Exactly three warning classes, which is exactly what
[#10](https://github.com/Commander-Cody/weather-page/issues/10) assumed when it placed surge classes
at ranks 2/3/4. **#10's shape survives unchanged.**

### 6.2 Triangulated three ways

The list is not taken on the PDF's word alone.

**The XSL** (§4.1) branches on exactly those three warning values and nothing else.

**BSH's public flyer**, *Wasserstandsvorhersage- und Sturmflutwarndienst für die deutsche
Nordseeküste* ([PDF](https://www.bsh.de/DE/PUBLIKATIONEN/_Anlagen/Downloads/BSH-Informationen/BSH-Flyer/Wasserstandsvorhersage_dt.pdf?__blob=publicationFile&v=9),
`M14_002 Stand 07/20`), p. 2, verbatim:

> „Bei zu erwartendem extremen Hoch- oder Niedrigwasser warnen wir frühzeitig die Öffentlichkeit und
> insbesondere die Schifffahrt, Häfen, Unternehmen und die an der Küste und den tideabhängigen
> Flüssen lebenden Menschen. **Ab einem Wasserstand höher als 1,5 m über mittlerem Hochwasser (MHW)
> werden Sturmflutwarnungen herausgegeben.**
> • Ab 1,5 m über MHW = Sturmflut
> • Ab 2,5 m über MHW = schwere Sturmflut
> • Ab 3,5 m über MHW = sehr schwere Sturmflut"

**An archived real observation.** On 2024-12-17 the water was forecast at ¾–1 m above MHW — above
the Baltic's `Erhoehter Wasserstand` threshold — and the North Sea headline was still the default
([snapshot `20241217013203`](https://web.archive.org/web/20241217013203id_/https://www2.bsh.de/aktdat/wvd/sturm/sturmflut_aktuell.xml)):

```xml
	<SHORTTITLE>Wasserstandsvorhersage</SHORTTITLE>
	<VORHERSAGETEXT>In der Nacht von Montag zu Dienstag wird das Hochwasser an der deutschen Nordseeküste, in Emden, Bremen und Hamburg 3/4 bis 1 m höher als das mittlere Hochwasser eintreten.</VORHERSAGETEXT>
```

That is direct evidence that there is **no intermediate public tier below 1.5 m on the North Sea**.

### 6.3 Why the 0.75 m tier is not public — and it is not free

The flyer explains the gap, and the answer is commercial:

> „Über das System FACT 24 können Interessierte **kostenpflichtige** Warnungen bereits ab einem
> Wasserstand von 0,75 m über MHW bzw. 0,75 m unter MNW per Telefon oder Fax bestellen."

A paid telephone/fax subscription. Not a feed, not free, not relevant — but it explains why
`Erhoehter Wasserstand` exists as a category while never appearing on the public North Sea product.

### 6.4 One inconsistency in BSH's own material

BSH's [Sturmfluten page](https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/Sturmfluten/sturmfluten_node.html)
lists **four** Baltic classes, including `Mittlere Sturmflut` (1,25–1,49 m über NHN), which does not
appear in the API's Table 5 at all. Baltic-only, so it costs this project nothing — but it is a
reminder that BSH's web copy and its API vocabulary are not maintained together. **Key on the API's
Table 5, not on the website.**

### 6.5 The legal basis, and a small correction

#4 and #26 both record the basis as "Seeaufgabengesetz § 1 Abs. 9". The flyer quotes the statute
directly, and the structure is slightly different:

> „Gesetz über die Aufgaben des Bundes auf dem Gebiet der Seeschifffahrt (Seeaufgabengesetz –
> SeeAufgG): **§ 1** Dem Bund obliegt auf dem Gebiet der Seeschifffahrt […] **9.** die nautischen
> und hydrographischen Dienste, insbesondere […] **b) der Gezeiten-, Wasserstands- und
> Sturmflutwarndienst** […]"

So it is **§ 1 Nr. 9 lit. b SeeAufgG** — a numbered item and a letter, not a paragraph (`Absatz`).
The API's own `copyright` field abbreviates it as `gemäß §1 SeeAufG`, dropping the second `g` from
the standard abbreviation `SeeAufgG`. Cosmetic, but if the Impressum quotes a statute it should
quote it correctly.

---

## 7. Freshness and failure

### 7.1 Publication cadence

The flyer states the official rhythm:

> „Viermal am Tag, gegen 00.30, 08.00, 14.00 und 20.00 Uhr, werden Vorhersagen für die kommenden
> zwei Hoch- und zwei Niedrigwasser an festgelegten Pegelorten erstellt und mit den jeweiligen
> Eintrittszeiten herausgegeben."

and, for staffing during an event:

> „Telefonische Erreichbarkeit / Mo–Fr: 06.30–20.30 Uhr / Sa–So: 06.30–13.30 Uhr und 18.00–20.30 Uhr
> / **Bei Sturmflut: Rund um die Uhr**"

Consistent with the live `forecast_timestamp` of `2026-08-16 00:07:39+02:00` — the ~00:30 run.

### 7.2 Measured, over 20 minutes

Sampled every 30 s across 26 samples, 23:11:59 to 23:24:45 UTC:

- **`sturmflut_aktuell.xml` is rewritten every 10 minutes on the minute**, regardless of whether
  anything changed: `Last-Modified` moved `23:01:02` → `23:11:01` → `23:21:01`. Content was
  unchanged across all of it — still 1413 bytes, still `<CREATIONDATE>16.08.2026, 00:10</CREATIONDATE>`,
  and two fetches after the final rewrite hashed identically (`md5 6562784f006a7eb8b6415961d43b36af`)
  to the body quoted in §4. **So the file's mtime is not evidence that the warning changed.**
- `official_warning_level_region` and `automated_gauge_warning` held steady at
  `Wasserstandsvorhersage` at every sample; `forecast_timestamp` held at the 00:07 run;
  `automated_curveforecast_timestamp` advanced `01:04:38` → `01:11:28` → `01:19:14`, gaps of 6 m 50 s
  and 7 m 46 s — the ~7–8 min automated cadence #2 measured.

**A caching consequence.** The XML's `ETag` is Apache's default `hexsize-hexmtime` form —
`"585-6591de9396532"`, where `0x585` = 1413 = the byte length. It changes with mtime, so it tracks
*rewrites*, not content. The API's `ETag` is a content hash (`"a5181b2fbe8c38832a566c48e8226d53"`).
Both honour `If-None-Match` with a clean `304` and zero body — but only the API's 304 actually means
"nothing changed":

```
$ curl -o /dev/null -w "%{http_code} %{size_download}\n" \
    -H 'If-None-Match: "89494bcc8fb1abe72026aa12230d8cb4"' \
    "…/items/husum_schleuse?f=json&lang=de"
304 0
```

### 7.3 What absence means — and it is good news

**The no-warning state is a positive value, not an empty response.** When nothing is happening the
field reads `"Wasserstandsvorhersage"`. This is materially better than DWD's `alerts: []`, because
the page can distinguish three states rather than two:

| Observed | Meaning |
| --- | --- |
| `"Wasserstandsvorhersage"` | BSH says: no surge warning. A **positive statement**. |
| `"Sturmflut"` / `"Schwere Sturmflut"` / `"Sehr schwere Sturmflut"` | An active warning. |
| Field **absent** | Not a coastal station (the 7 river gauges). **Never** means "no warning". |
| Fetch fails | The page knows nothing. |

This lines up cleanly with [#7](https://github.com/Commander-Cody/weather-page/issues/7)'s rule that
an empty warning area means "the sources say nothing" — here the source says something, explicitly.

**No staleness threshold applies.** Per #7, a live browser fetch has only success or failure. The
`forecast_timestamp` is nonetheless worth reading, because it dates the *human* forecast and will be
up to ~6 hours old in calm weather by design — that is normal, not stale, and it must not be
displayed as a fetch age.

### 7.4 Payload cost, and the awkward part

The field cannot be requested on its own. Both `properties` (projection) forms are rejected:

```
$ …/items/husum_schleuse?f=json&lang=de&properties=official_warning_level_region
HTTP/1.1 400 Bad Request
{"status":400,"title":"Bad Request","detail":"The following query parameters are rejected:
 properties. Valid parameters for this request are: access_token, crs, f, lang"}
```

So a warning fetch pulls the whole feature — **10,616 B gzipped, 106,273 B raw** for one station,
almost all of it the 10-minute curve.

There is one cheap trick. The 400 on the *collection* endpoint enumerates the queryables, and
`official_warning_level_region` and `automated_gauge_warning` are both among them. Combined with
`result-type=hitsOnly` that gives a count-only response:

```
GET …/items?f=json&lang=de&result-type=hitsOnly
    &filter=area LIKE 'Nordfriesland%' AND official_warning_level_region <> 'Wasserstandsvorhersage'
    &filter-lang=cql2-text
Origin: https://weather.example.org

HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Content-Length: 412            (gzipped)

{"type":"FeatureCollection","numberReturned":0,"numberMatched":0,
 "timeStamp":"2026-08-15T23:17:46Z","features":[],"links":[…]}
```

**412 bytes on the wire to answer "is there a surge warning right now?"** — and because the official
level is coast-wide, that one request answers it for all 20 places at once. Narrowing to *which*
class costs at most two more such requests, since the list is three long. Note `result-type=hits` is
rejected; the enum value is `hitsOnly`.

### 7.5 The structural problem this creates

**The surge warning is not a separate product — it is a field on the feature the scheduled job
already fetches for water level.** That cuts across the fetch-model split:

- #1/#4 put **warnings client-side and live**.
- #2 put **water level in the scheduled job**.
- The surge warning is *both*, in one payload.

So there are three shapes, and the ticket's worry was aimed at the wrong risk. CORS is fine; the
coupling is the issue:

1. **Live client-side, hitsOnly** — 412 B, genuinely live, but only the coast-wide official level,
   and it needs 1–3 requests to resolve the class.
2. **Live client-side, full feature** — 10.6 KB per place, gives every field including
   `automated_gauge_warning`, but re-downloads a curve the scheduled job already has.
3. **Ride along in the scheduled job** — free, since the job already fetches these exact features,
   but the warning inherits the job's cadence and therefore acquires a staleness threshold, which
   #7 says a live warning does not have.

Option 3 is free and wrong; option 1 is live and thin; option 2 is live and wasteful. That is a real
decision and it is not this document's to make.

---

## 8. Licence and attribution — for #19

**CC BY 4.0 applies. The #12 tide-calculator instrument does not.**

The licence is stated in band, per feature:

```json
"licence": "CC BY 4.0",
"copyright": {
  "de": "@Bundesamt für Seeschifffahrt und Hydrographie (BSH). Das BSH übernimmt für die angegebenen Informationen keine Gewähr. Amtliche Wasserstandsvorhersage des Bundes gemäß §1 SeeAufG.",
  "en": "@Federal Maritime and Hydrographic Agency (BSH). The BSH accepts no liability for the information provided here. Official water level forecast of the federal government according to §1 SeeAufG."
}
```

and on the service landing page (<https://gdi.bsh.de/ldproxy/rest/services?f=json>):

> "BSH's open data is provided under the 'Creative Commons license CC BY 4.0'. […] **Attribution**:
> You must provide an appropriate source citation, link to the license, and indicate whether any
> changes have been made. **The form is freely selectable**, but must not give the impression that
> the licensor supports or recommends you or your use."

### 8.1 The finding that simplifies #19

**The surge warning adds no new credit line.** It is not merely the same licence as the water level
data from #2 — it is *the same bytes*. The warning field and the tide curve arrive in one response,
under one `licence` field and one `copyright` field. Whatever line #19 settles on for BSH water
level already covers the surge warning, with no second obligation and no second attribution string.

#12 counted four credit lines. On this evidence it is three: BSH tide calculator is genuinely
separate (prescribed form, no licence to link), but BSH water level and BSH surge warning are one.

### 8.2 The finding that complicates #19 — and it is the sharp one

**Inside one warning slot, the two agencies' attribution rules point in opposite directions.**

[ADR-0005](https://github.com/Commander-Cody/weather-page/blob/decide/warnings-presentation/docs/adr/0005-a-translated-warning-carries-no-dwd-source-attribution.md)
has already decided the DWD half: a translated DWD warning carries **no** source note,
because *„Wenn vom DWD ausgegebene amtliche Wetterwarnungen verändert werden, ist der beigegebene
Quellvermerk zu löschen"*, and it settles on "a Mooring label carrying the German proper name",
attached once to the slot. It explicitly leaves the cross-source arrangement to #19.

This research supplies the other half, and the two do not have the same shape:

| | DWD warning (ADR-0005) | BSH surge warning (this document) |
| --- | --- | --- |
| On translation, attribution must be… | **removed** | **kept** |
| Licence link required? | No — the note's wording is unprescribed | **Yes** — CC BY 4.0 requires a link to the licence |
| Change indication required? | Expected, wording free | **Yes**, explicitly |

ADR-0004 puts both on **one ladder in one warning area**, so a single component must apply opposite
rules depending on which agency issued the warning — and which agency that is, is the one thing the
reader is not told directly, since ADR-0004 says "the event name is what tells a reader which body
issued it".

The concrete consequence for #19: **ADR-0005's chosen shape is not sufficient for the BSH half.** A
Mooring label plus an untranslated proper name satisfies DWD, but CC BY 4.0 additionally requires a
licence link and a modification indication. Either the slot carries a slightly richer BSH credit than
DWD credit — visibly asymmetric, and ADR-0005 already warns that a future reader will be tempted to
"fix" exactly that kind of asymmetry — or the BSH obligations are met once at slot level in a way
that also covers the surge class. That is a decision, and §8.1 at least makes it cheaper: there is
one BSH water-level credit line, not two.

---

## 9. What this contradicts elsewhere in the project

**1. #4's decisive argument for Bright Sky does not transfer, and cannot.** #4 chose Bright Sky
`/alerts` because it "is the only candidate that preserves the CAP `event_code`", calling a table
keyed on German strings "a maintenance trap worth avoiding". For BSH surge warnings **there is no
integer to key on** — no numeric code exists in the API, the PDF, or the XML, and the strings stay
German under `lang=en` (§3.3). The Mooring lookup for the surge half of the warning slot **must** key
on the German string. This is not a bad choice among alternatives; it is the only representation BSH
publishes. Mitigating factors: the list is four strings rather than sixty, it is documented in a
dated PDF, and it is corroborated by a stylesheet and a flyer.

**2. #2's CORS caveat is wrong in its diagnosis.** "An explicit `OPTIONS` preflight 301-redirects, so
keep requests CORS-simple" — the preflight is fine; the missing `lang` was the cause (§2.1). The
correct rule is *always send `lang`*, and with it non-simple requests work too. #2's `docs/research/bsh-water-level-api.md`
should be amended, because "keep requests CORS-simple" is a constraint the build session would
otherwise design around for no reason. It also means #2's own recommended scheduled-job request —
which happens to include `filter-lang` — works by accident.

**3. #26 anticipated the wrong failure mode.** The ticket reasoned that absent CORS "would force
surge warnings into the scheduled job and split the warning slot across two fetch models". CORS is
present, so that specific fear is void — but the split arrives anyway, by a different route: the
warning is welded to the water-level payload the scheduled job already fetches (§7.5). The decision
is still needed; the reason changed.

**Not a contradiction, worth noting as confirmed:** #10's placement of three surge classes at ranks
2/3/4 is exactly right (§6.1), and ADR-0004's rule that the page must never derive a class is
satisfiable — BSH publishes the classification, in two granularities.

---

## 10. What this leaves for the owner to write

**No Frisian appears in this document, and none should be inferred from it.**

The strings the page will need, in the project's own terms
([`CONTEXT.md`](https://github.com/Commander-Cody/weather-page/blob/main/CONTEXT.md) → *Batch list*),
are **four cells in the language file**:

| Needed for | German source string |
| --- | --- |
| The no-warning state | `Wasserstandsvorhersage` |
| Rank 2 | `Sturmflut` |
| Rank 3 | `Schwere Sturmflut` |
| Rank 4 | `Sehr schwere Sturmflut` |

`CONTEXT.md` currently carries Mooring for *astronomical tide* and *surge-corrected forecast*, but
**nothing for a storm surge or for a warning**. That is a real gap in the glossary, not just in the
language file — the domain has no term yet for the thing the whole warning slot is about. Naming it
is the owner's, and only the owner's.

Two further points a fluent speaker should rule on, which are editorial rather than lexical:

- Whether the no-warning state is rendered as a *phrase* at all, or as an empty warning area. #7 and
  ADR-0004 imply the latter, in which case only three cells are needed.
- Whether the three class names should be built compositionally from one root plus intensifiers, the
  way German does (`Sturmflut` → `Schwere …` → `Sehr schwere …`). That is a question about Mooring's
  own morphology and it is not one an agent should answer.

The scope caveat from §5.2 may also need a sentence of its own — if the official coast-wide level is
what gets rendered, an honest page arguably has to say that the warning covers the whole coast
rather than this place. That sentence does not exist in any language yet.

---

## 11. The *Küsten-Warnungen* hole is not BSH's to fill

#26 asks whether this source covers the gap #4 found, where DWD's municipality product carries no
coastal warning cells for "Nordfriesische Küste". **It does not, and no BSH product ever will.**

The two are different phenomena. The missing DWD warnings are **wind**: `11 BÖEN`, `12 WIND`,
`13 STURM`. BSH's statutory remit is **water level** — `der Gezeiten-, Wasserstands- und
Sturmflutwarndienst` (§ 1 Nr. 9 lit. b SeeAufgG, §6.5). BSH issues no wind warning of any kind;
there is no wind field anywhere in the `WaterLevelForecast` collection, and the *Sturmflutwarndienst*
product contains nothing but water levels.

So the hole stays open, and it stays a **DWD** problem. Nothing in this research changes #4's
conclusion that the fix must come from a DWD product carrying coastal cells, or not at all. It is
worth noting that the two gaps are correlated in practice — the weather that produces a
`Sturmflut` is the weather that produces a coastal storm warning — so on the days the wind hole is
most visible, the BSH surge warning will often be the thing that fires. That mitigates the hole
somewhat. It does not close it.

---

## 12. What I could not settle

Listed so a later session does not mistake inference for measurement.

1. **The live vocabulary of `automated_gauge_warning` and `forecast_automated_event_warning` is
   unverified.** Both read `Wasserstandsvorhersage` at every station throughout the observation
   window — August, calm. The PDF documents neither against Table 5, and the XSL does not touch
   them. I am *assuming* they share Table 5's vocabulary because they share its default value. **A
   session working during an actual surge should capture these fields**, because if the automated
   route is chosen, this assumption becomes load-bearing. There is no archive of the API to check
   against retrospectively — the API is new, and the Wayback Machine has no snapshots of it.
2. **Whether `official_warning_level_region` in the API tracks `SHORTTITLE` during an event.** They
   are identical now and `forecast_text.de` is byte-identical to `VORHERSAGETEXT`, which is strong
   evidence of a shared origin, but I could only observe the pair in the default state. The archived
   `Schwere Sturmflut` example (§5.2) predates the API.
3. **Whether a `Sehr schwere Sturmflut` has ever been published on this product.** The Wayback
   Machine's coverage of `sturmflut_aktuell.xml` starts in 2019 and is sparse; of 31 distinct
   snapshots between 2021-12 and 2026-01 I sampled several and found one `Schwere Sturmflut`
   (2022-01-30) and defaults otherwise. The class is documented in three independent BSH sources, so
   its existence is not in doubt — only an observed instance is missing.
4. **The `ZUSATZ` / `ADDITION` free-text branch.** The XSL renders it as a warning-styled panel when
   non-empty, but it was empty in every snapshot I read. Its content is unknown, and it is *not* a
   class — if the page consumes the XML at all it would need a policy for it. It has no counterpart
   in the API (`forecast_text_additional` was documented in the PDF but `null` everywhere, the same
   observation #2 made).
5. **The exact rewrite cadence of the XML beyond ~10 minutes**, and whether it tightens during an
   event. Observed across three rewrites only.
6. **Whether BSH would consider the `hitsOnly` filter trick (§7.4) acceptable use.** It is plainly
   within the API's documented capabilities and there is no rate limit documented or observed, but a
   per-page-load count query is a usage pattern BSH has not blessed explicitly.

---

## 13. Sources

Primary, all fetched 2026-08-15:

- API landing page and service list — <https://gdi.bsh.de/ldproxy/rest/services?f=json>
- Collection items — `https://gdi.bsh.de/ldproxy/rest/services/WaterLevelForecast/collections/waterlevelforecastdata/items?f=json&lang=de`
- **Parameter documentation (authoritative field reference, Tab. 5)** — <https://www2.bsh.de/aktdat/wvd/api/parameter_documentation.pdf> (27.05.2026)
- **Sturmflutwarndienst product** — <https://www2.bsh.de/aktdat/wvd/sturm/sturmflut_aktuell.xml>
- **Its stylesheet** — <https://www2.bsh.de/aktdat/wvd/sturm/sturmflut.xsl> (30.06.2025)
- BSH flyer *Wasserstandsvorhersage- und Sturmflutwarndienst für die deutsche Nordseeküste* — [PDF](https://www.bsh.de/DE/PUBLIKATIONEN/_Anlagen/Downloads/BSH-Informationen/BSH-Flyer/Wasserstandsvorhersage_dt.pdf?__blob=publicationFile&v=9) (`M14_002 Stand 07/20`)
- BSH *Sturmfluten* topic page — <https://www.bsh.de/DE/THEMEN/Wasserstand_und_Gezeiten/Sturmfluten/sturmfluten_node.html>
- BBK warning API — `https://warnung.bund.de/api31/dashboard/010540000000.json`
- Archived warning snapshots — Wayback Machine, `20220130085106`, `20230203025748`, `20241217013203`, `20251107060333`
- Fetch standard, HTTP-redirect fetch — <https://fetch.spec.whatwg.org/#http-redirect-fetch>

Project documents referenced:

- [ADR-0002 — local gauge data wins over a borrowed curve](https://github.com/Commander-Cody/weather-page/blob/main/docs/adr/0002-local-gauge-data-wins-over-a-borrowed-curve.md) (`main`)
- [ADR-0004 — the page relays warnings, it never authors them](https://github.com/Commander-Cody/weather-page/blob/decide/warnings-presentation/docs/adr/0004-the-page-relays-warnings-it-never-authors-them.md) (`decide/warnings-presentation`)
- [ADR-0005 — a translated warning carries no DWD source attribution](https://github.com/Commander-Cody/weather-page/blob/decide/warnings-presentation/docs/adr/0005-a-translated-warning-carries-no-dwd-source-attribution.md) (`decide/warnings-presentation`)
- [`CONTEXT.md`](https://github.com/Commander-Cody/weather-page/blob/main/CONTEXT.md) and [`docs/places.md`](https://github.com/Commander-Cody/weather-page/blob/main/docs/places.md) (`main`)
- [`docs/research/bsh-water-level-api.md`](https://github.com/Commander-Cody/weather-page/blob/research/bsh-water-level-api/docs/research/bsh-water-level-api.md) and [`docs/research/dwd-warnings.md`](https://github.com/Commander-Cody/weather-page/blob/research/dwd-warnings/docs/research/dwd-warnings.md)
- Issues #1, #2, #4, #7, #10, #12, #19, #26
