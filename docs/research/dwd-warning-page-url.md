# The DWD warning page URL for a place's own area

Research for [issue #27](https://github.com/Commander-Cody/weather-page/issues/27). Every URL below was
fetched live on **2026-08-15** between 22:55 and 23:30 UTC. HTTP statuses come from real requests.
Because the scoping on these pages is done entirely in the browser, statuses alone prove nothing —
so every claim about *what the reader actually sees* was also checked by loading the URL in a real
browser and reading the resulting DOM. Both kinds of evidence are quoted below.

Per [#1](https://github.com/Commander-Cody/weather-page/issues/1) and
[#10](https://github.com/Commander-Cody/weather-page/issues/10), no Mooring wording is proposed
anywhere in this document. The link's Frisian label is the owner's, and #10 already fixed it.

---

## 1. Verdict up front

**There is a working per-municipality DWD warning URL, it is documented by DWD, and it has been
stable for seven and a half years. But it is keyed on a municipality *name string* that we do not
hold and cannot derive, and it fails silently when the string is wrong.**

Recommended pattern:

```
https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnkarten/warnWetter_shh_node.html
    ?bundesland=shh
    &ort=<municipality name, exactly as DWD spells it>
    [&lk=<Kreis …>]        # only where the name is not unique nationwide
```

Worked examples, both verified live (HTTP 200, and confirmed in-browser to select the place, fill
the search field and render that place's warning state):

| Place | URL |
|---|---|
| **Husum** (mainland) | `https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnkarten/warnWetter_shh_node.html?bundesland=shh&ort=Husum&lk=Kreis%20Nordfriesland` |
| **List auf Sylt** (island) | `https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnkarten/warnWetter_shh_node.html?bundesland=shh&ort=List%20auf%20Sylt` |

With Husum selected and no warning current, the panel beside the map reads `Husum` / `Keine
Warnungen` — so the no-warnings case is answered for the reader's own place, not left blank. With a
warning current, the same panel carries the full German headline, validity window and description
(§2.4).

Three things about this recommendation are load-bearing:

- **`bundesland=shh` is not decoration.** It is what makes the failure mode survivable. If `ort`
  ever stops matching, the reader still lands on the Schleswig-Holstein and Hamburg warning map
  rather than on a map of all of Germany. Verified: §2.5.
- **The `ort` value is a hand-paired identifier**, unrelated to the WarnCellID or AGS from
  [#4](https://github.com/Commander-Cody/weather-page/issues/4). Twenty pairings, done once. Same
  shape as the BSH gauges under ADR-0002. Full table in §3.3.
- **`lk` is undocumented.** It works, and two of our twenty places need it, but DWD has never
  written it down. §3.2.

Two answers the ticket asked for that came back negative:

- **There is no WarnWetter web view to compare against.** WarnWetter is an app only. §5.3.
- **An English page exists at a predictable URL and takes the same parameters — but the warning
  prose stays German on it.** §6.

---

## 2. What the URL actually does

### 2.1 The server ignores it entirely

`warnWetter_node.html?ort=Husum` and `warnWetter_node.html?ort=Zzzzzznotaplace` return **byte-identical
HTML** apart from the parameter being echoed back into the canonical link and the three skip-nav
anchors. Diffed after normalising the session id:

```
$ curl -s ".../warnWetter_node.html?ort=Husum"            -o a.html   # 200
$ curl -s ".../warnWetter_node.html?ort=Zzzzzznotaplace"  -o b.html   # 200
   14 differing fragments, all of the form
   -  <link rel="canonical" href="…?ort=Husum"/>
   +  <link rel="canonical" href="…?ort=Zzzzzznotaplace"/>
```

So an HTTP 200 on one of these URLs carries **no information** about whether the link works. Anything
that only checks status codes will pass a broken link. This is the single most important operational
fact in this document.

### 2.2 The scoping is one function in a minified bundle

All of it happens in `SiteGlobals/Functions/JavaScript_Optimierung2/__everything_warnWetter.js` (798 KB,
loaded by every warning page). De-minified, the whole contract is:

```js
getGemeindeFromURL: function () {
  var ort, lk, q = location.search.substring(1);
  if (q && q.length > 0) {
    q = q.replace(/amp;/g, "");
    for (var parts = q.split("&"), i = 0; i < parts.length; i++)
      if (parts[i].indexOf("=") > 0) {
        var kv = parts[i].split("=");
        if (kv[0] === "ort")     ort = decodeURI(kv[1]).toLowerCase();
        else if (kv[0] === "lk") lk  = decodeURI(kv[1]).toLowerCase();
      }
  }
  if (ort)
    for (i = 0; i < gemeinden.length; i++) {
      var g = gemeinden[i];
      if (g.name.toLowerCase() === ort) {
        if (!lk) return g;              // first array match wins
        if (g.lk.toLowerCase() === lk) return g;
      }
    }
}
```

Consequences worth writing down:

- The match is an **exact full-string comparison**, case-insensitive. No prefix match, no fuzzy match,
  no trimming. `Westerland` does not match `Sylt`; `Husum ` with a trailing space matches nothing.
- **`decodeURI`, not `decodeURIComponent`.** Percent-encoded UTF-8 for umlauts and `ß` decodes
  correctly (verified against `Reußenköge`, §2.3). Spaces must be `%20`; a `+` would not be decoded.
- Without `lk`, a duplicated name resolves to **whichever entry happens to come first in the array**.
  That is an ordering accident, not a guarantee.

The sibling function `parseBundeslandFromURL()` is stricter — it whitelists thirteen literal values
(`all`, `baw`, `bay`, `bbb`, `hes`, `mvp`, `nib`, `nrw`, `rps`, `sac`, `saa`, `shh`, `thu`) and returns
`all` for anything else. So `bundesland` cannot break the page, only fail to narrow it.

The call site fires 200 ms after the SVG map initialises: it selects the municipality, zooms the map
to it, and fills the search field with the resolved name.

### 2.3 Verified in a real browser

Loaded in a browser and read back through `UTILS.getGemeindeFromURL()` and the DOM:

| URL query | Resolved | Search field |
|---|---|---|
| `?ort=Husum&lk=Kreis%20Nordfriesland` | `{name: "Husum", lk: "Kreis Nordfriesland", state: "shh"}` | `Husum` |
| `?ort=Sylt` | `{name: "Sylt", state: "shh"}` | `Sylt` |
| `?ort=List%20auf%20Sylt` | `{name: "List auf Sylt", state: "shh"}` | `List auf Sylt` |
| `?ort=H%C3%B6rnum%20(Sylt)` | `{name: "Hörnum (Sylt)", state: "shh"}` | `Hörnum (Sylt)` |
| `?ort=Reu%C3%9Fenk%C3%B6ge` | `{name: "Reußenköge", state: "shh"}` | `Reußenköge` |
| `?ort=Neukirchen` | `{… lk: "Kreis Nordfriesland"}` | `Neukirchen` |
| `?ort=Neukirchen&lk=Kreis%20Ostholstein` | `{… lk: "Kreis Ostholstein"}` | `Neukirchen` |
| **`?ort=Westerland`** | **`undefined` — no match** | **empty** |

The last row is the failure mode: HTTP 200, page renders perfectly, nothing selected, no error
anywhere. Westerland has not been a municipality since it merged into Gemeinde Sylt, so DWD's
catalogue has no such entry — and the link degrades to a general warning map without saying so.

### 2.4 What the reader sees when a warning exists

Checked against Gemeinde Barleben, which had a live thunderstorm warning during the session. The
deep-link path renders a detail box beside the map:

> Amtliche WARNUNG vor GEWITTER · So, 16. Aug, 01:00 – 02:00 Uhr · Es treten Gewitter auf. …

That is the unbounded German prose #27 describes, which is exactly why #10 sends the reader here
rather than rendering it inline.

*Method note, so this is reproducible:* the rendering step runs inside `requestAnimationFrame`, and
animation frames do not fire in a browser pane that is not compositing. On a first pass this looked
like a DWD defect — the panel stayed empty even for a warned municipality. It is not. Patching
`requestAnimationFrame` to a `setTimeout` and re-running the same selection callback produced the
detail box above. Anyone re-checking this in headless automation will hit the same false negative.

### 2.5 The failure mode is chosen by the base URL

| Base URL | `ort` matches | `ort` does not match |
|---|---|---|
| `warnungen_gemeinden/warnWetter_node.html` | the place, selected | **map of all Germany** |
| `warnungen_gemeinden/warnkarten/warnWetter_shh_node.html?bundesland=shh` | the place, selected | **map of Schleswig-Holstein and Hamburg** |

Verified: `warnWetter_shh_node.html?bundesland=shh&ort=Westerland` → HTTP 200,
`getGemeindeFromURL()` returns nothing, `parseBundeslandFromURL()` still returns `shh`, and the page
title stays *Warnkarte Schleswig-Holstein und Hamburg*.

For a static site that bakes the link in and may not notice a break for months, the second row is
worth the extra parameter.

---

## 3. The identifier, and whether we already hold it

### 3.1 No — and there is no transform that would get us there

`ort` is matched against `https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/viewer/gemeinden.js`
(714 KB, `Access-Control-Allow-Origin: *`, `Last-Modified: Fri, 25 Mar 2022 16:17:12 GMT`). It holds
11,214 entries shaped like:

```js
var gemeinden = [ …,
  {"name":"Husum", "x": 1963, "y":1273, "state": "shh", "lk": "Kreis Nordfriesland"},
  {"name":"Wittdün auf Amrum", "x": 1874, "y":1248, "state": "shh"}, … ]
```

**There is no AGS and no WarnCellID in this file.** Name, two map pixel coordinates, a Bundesland
code, and a Kreis only where the name is duplicated. So the `ort` value cannot be computed from the
`warn_cell_id` #4 established, nor from the AGS inside it, nor from anything else in the place
registry.

Worse, the same municipality carries **five different name forms** across DWD's own products. Husum
and its neighbours:

| Where it appears | Husum | Wittdün | Emmelsbüll-Horsbüll | Neukirchen (NF) |
|---|---|---|---|---|
| `gemeinden.js` `name` — **the `ort` value** | `Husum` | `Wittdün auf Amrum` | `Emmelsbüll-Horsbüll` | `Neukirchen` |
| WarnCellID catalogue `NAME` | `Stadt Husum` | `Gemeinde Wittdün auf Amrum` | `Gemeinde Emmelsbüll-Horsbüll` | `Gemeinde Neukirchen` |
| WarnCellID catalogue `KURZNAME` | `Stadt Husum` | `Wittdün/Amrum` | `Emmelsb.-Horsb.` | `Neukirchen (NF)` |
| Bright Sky `location.name_short` | `Stadt Husum` | `Wittdün/Amrum` | `Emmelsb.-Horsb.` | `Neukirchen (NF)` |
| Warning-table HTML anchor id | *(prefixed form — see note)* | | | |

The last row could not be observed for our places: Schleswig-Holstein had no warnings during the
session, so none of them appeared in the table. It was observed for warned municipalities elsewhere
— `Gemeinde Barleben`, `Gemeinde Altenhausen`, `Stadt …`, `Mitgliedsgemeinde …`,
`gemeindefreies Gebiet …` — which is the prefixed form, not the `ort` form. That is enough to reject
the anchors (§5.2) without pinning each of our twenty.

The `ort` form is the only one without a `Stadt`/`Gemeinde` prefix, and the abbreviations in
`KURZNAME` (`Emmelsb.-Horsb.`) are not derivable in either direction. Any attempt to generate `ort`
from the identifiers we hold would be a string-mangling heuristic that fails silently per §2.1.

### 3.2 Cost of pairing: twenty rows, once

Exactly the hand-pairing shape the ticket anticipated, and the same shape as the BSH gauges under
ADR-0002. The pairing is done below (§3.3), so the remaining cost is storing it: one new field per
place in the place registry, holding the `ort` string, plus an optional second field for `lk`.

Only **two of the twenty** need `lk`:

| Place | Why | `lk` value |
|---|---|---|
| `husum` | `Husum` also exists in Kreis Nienburg (Weser), Niedersachsen | `Kreis Nordfriesland` |
| `neukirchen` | `Neukirchen` exists four times: Nordfriesland, Ostholstein, Schwalm-Eder, Straubing-Bogen | `Kreis Nordfriesland` |

Both currently resolve correctly *without* `lk`, because the Nordfriesland entry happens to sort
first. Do not rely on that — §2.2. Send `lk`.

`lk` is not mentioned in any DWD documentation, in the current Homepagewetter page or in its 2019
archived copy. It is real, verified behaviour on an undocumented parameter.

### 3.3 The twenty places, paired

Every URL below was fetched: **all twenty returned HTTP 200, and all twenty resolve** under a
faithful port of `getGemeindeFromURL` run against the live catalogue. Cell ids are from DWD's
WarnCellID catalogue CSV and agree with #4 where they overlap.

Base for all of them:
`https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnkarten/warnWetter_shh_node.html?bundesland=shh`

| `key` | `ort` (raw) | `lk` | WarnCellID | Query string to append |
|---|---|---|---|---|
| `list` | List auf Sylt | — | 801054078 | `&ort=List%20auf%20Sylt` |
| `westerland` | Sylt | — | 801054168 | `&ort=Sylt` |
| `hoernum` | Hörnum (Sylt) | — | 801054046 | `&ort=H%C3%B6rnum%20(Sylt)` |
| `wyk` | Wyk auf Föhr | — | 801054164 | `&ort=Wyk%20auf%20F%C3%B6hr` |
| `wittduen` | Wittdün auf Amrum | — | 801054160 | `&ort=Wittd%C3%BCn%20auf%20Amrum` |
| `hooge` | Hallig Hooge | — | 801054050 | `&ort=Hallig%20Hooge` |
| `hamburger-hallig` | Reußenköge | — | 801054108 | `&ort=Reu%C3%9Fenk%C3%B6ge` |
| `pellworm` | Pellworm | — | 801054103 | `&ort=Pellworm` |
| `nordstrand` | Nordstrand | — | 801054091 | `&ort=Nordstrand` |
| `husum` | Husum | Kreis Nordfriesland | 801054056 | `&ort=Husum&lk=Kreis%20Nordfriesland` |
| `dagebuell` | Dagebüll | — | 801054022 | `&ort=Dageb%C3%BCll` |
| `helgoland` | Helgoland | — | 801056025 | `&ort=Helgoland` |
| `klanxbuell` | Klanxbüll | — | 801054065 | `&ort=Klanxb%C3%BCll` |
| `emmelsbuell-horsbuell` | Emmelsbüll-Horsbüll | — | 801054166 | `&ort=Emmelsb%C3%BCll-Horsb%C3%BCll` |
| `neukirchen` | Neukirchen | Kreis Nordfriesland | 801054086 | `&ort=Neukirchen&lk=Kreis%20Nordfriesland` |
| `niebuell` | Niebüll | — | 801054088 | `&ort=Nieb%C3%BCll` |
| `risum-lindholm` | Risum-Lindholm | — | 801054109 | `&ort=Risum-Lindholm` |
| `langenhorn` | Langenhorn | — | 801054075 | `&ort=Langenhorn` |
| `bredstedt` | Bredstedt | — | 801054019 | `&ort=Bredstedt` |
| `toenning` | Tönning | — | 801054138 | `&ort=T%C3%B6nning` |

**Two of these are curation decisions, not lookups**, and the owner should confirm them:

- **`westerland` → `Sylt`.** Westerland is not a municipality; it merged into Gemeinde Sylt. `Sylt` is
  the cell that contains it (confirmed: the Westerland town coordinate resolves to `801054168`
  Gemeinde Sylt). This is the same "an island is several municipalities" problem #4 flagged — Sylt
  is five cells, and Westerland's warnings arrive on the one named after the whole island.
- **`hamburger-hallig` → `Reußenköge`.** The Hamburger Hallig is not its own municipality. Reußenköge
  is the municipality on the mainland shore it belongs to and is the only defensible candidate in
  the catalogue, but this is a local judgement of the kind places.md already makes for gauges.

### 3.4 Two registry problems found in passing

Not this ticket's job, but they surfaced while resolving coordinates and should not be lost:

- **`emmelsbuell-horsbuell`'s stored `coords_land` (54.8514, 8.7194) resolves to the wrong
  municipality** — Bright Sky returns `801054086` Gemeinde **Neukirchen** for it, not Emmelsbüll-Horsbüll.
- **`neukirchen`'s stored `coords_land` (54.9139, 8.7431) resolves to no municipality cell at all**
  (HTTP 404 from Bright Sky).

`docs/places.md` already warns that the Wiedingharde coordinates are estimates. These two are
concrete instances. They do not affect the table above, which is paired by name, not by coordinate.

Related and worth knowing before anyone builds on point lookups: **Bright Sky's lat/lon → cell
resolution has holes in exactly our region.** Coordinates for Reußenköge village, the Hamburger
Hallig and Neukirchen all returned 404, despite all three municipalities existing in both DWD
catalogues. Automating this pairing from coordinates would silently drop places. Pair by name.

---

## 4. Stability

**Verdict: the path is genuinely old and stable; the mechanism behind it is explicitly disclaimed by
DWD and has already lost one per-place product.** Bake it in, but bake in the graceful-degradation
form, and treat the link as something to re-verify rather than something that cannot break.

### 4.1 What argues for stability

- **The URL is DWD-documented, on DWD's own page for exactly this use case** — *Ihr Homepagewetter*
  (`…/warnungen_aktuell/objekt_einbindung/objekteinbindung_node.html`, page's own date stamp
  13.04.2021). It states that a link may be set directly onto a municipality, that the address fills
  the search field and the application then shows that municipality's warning situation, and gives
  `…/warnWetter_node.html?ort=Miesbach` as the worked example. It also explicitly invites linking to
  the DWD site, including the per-Bundesland warning pages, with
  `…/warnkarten/warnWetter_bay_node.html?bundesland=bay` as its example — which is the other half of
  the recommended pattern.
- **That documentation is unchanged since at least January 2019.** The 2019-01-31 Wayback capture
  carries the same two sentences and the same Miesbach example, word for word, as the page served
  today. Seven and a half years of an unchanged documented contract.
- **The paths archive clean over nine years.** Wayback CDX, HTTP 200 throughout:
  | Path | Snapshots | First | Last |
  |---|---|---|---|
  | `…/warnungen_gemeinden/warnWetter_node.html` | 97 | 2017-06-06 | 2026-08-01 |
  | `…/warnkarten/warnWetter_bay_node.html` | 22 | 2017-08-04 | 2026-07-18 |
  | `…/warnapp_gemeinden/viewer/gemeinden.js` | 56 | 2016-11-02 | 2026-08-01 |
- **`www.dwd.de/warnungen` is a maintained permanent redirect** (HTTP 301 →
  `/DE/wetter/warnungen/warnWetter_node.html`), which suggests DWD manages redirects when it moves
  these pages rather than dropping them.

### 4.2 What argues against it

- **DWD disclaims the whole thing.** The same Homepagewetter page states there is no entitlement to
  the service's availability, and that products, product names and paths may be changed by DWD at
  any time. That is DWD's own framing of every URL in this document.
- **DWD has already withdrawn the per-place product.** The section of that page headed *HTML-File
  (pro Kreis bzw Gemeinde)* now reads, in full: "Können nicht mehr angeboten werden." Per-district
  and per-municipality warning files used to exist and were discontinued — already gone by the
  January 2019 capture. There is direct precedent for DWD killing a per-place URL surface.
- **DWD calls its own web artefacts by-products.** The same page notes about the JSONP files that
  they are by-products of the website's warning application and could be changed or switched off at
  any time. `gemeinden.js` is a sibling of those files, and the `ort` mechanism depends on it.
- **The behaviour lives in a minified bundle, not in a contract.** `__everything_warnWetter.js`
  carries a `?v=5` cache-buster; a site relaunch that replaces this application replaces
  `getGemeindeFromURL` with it. Nothing server-side would need to change for every `ort` link on our
  site to go quietly inert.
- **The catalogue is four years stale.** `gemeinden.js` has not been modified since 2022-03-25. That
  is stability today, but it also means municipal mergers since then are not reflected — and a future
  refresh could rename entries under us. Westerland is the cautionary example of what a merged
  municipality does to a name-keyed link.
- **`lk` is undocumented** (§3.2), so two of our twenty links rest on behaviour DWD never promised.

### 4.3 The coarser fallback, if that is judged too fragile

Named as the ticket asks. In descending order of precision:

1. `…/warnkarten/warnWetter_shh_node.html?bundesland=shh` — no `ort` at all. The Schleswig-Holstein
   and Hamburg warning map at municipality grain. Documented, one parameter, whitelisted server-side
   against a fixed list of thirteen, and cannot fail silently in the way `ort` can: the worst case is
   an ignored parameter and a map of Germany. Verified: HTTP 200.
2. `https://www.dwd.de/warnungen` — DWD's own short link for the national warning page, HTTP 301 to
   the canonical path. The most stable target on the site, and the least useful to a reader in Husum.

Option 1 is the honest coarse target. It costs the reader one interaction — finding their own place
on a map of two Bundesländer — and it costs us nothing to maintain, because it has no per-place
component at all. If the twenty pairings are ever judged not worth their upkeep, this is where to
retreat to, and the recommended pattern already degrades to exactly it.

---

## 5. Is there a better destination?

### 5.1 The comparison the ticket asked for

Measured as: how many actions between the reader arriving and seeing the warning detail for *their*
place.

| Destination | Actions to the reader's own detail | Grain | Fails silently? |
|---|---|---|---|
| **`warnWetter_shh_node.html?bundesland=shh&ort=…&lk=…`** (recommended) | **0** — arrives selected | municipality | yes, if `ort` breaks — but degrades to row below |
| `warnWetter_shh_node.html?bundesland=shh` | 1 — find the place on the SH/HH map | municipality | no |
| `warnungen_gemeinden/warnWetter_node.html?ort=…` | 0 | municipality | yes, and degrades to all of Germany |
| `warnungen_landkreise/warnWetter_node.html?ort=…` | 0 | **district** | yes |
| `www.dwd.de/warnungen` | 2 — narrow to SH, then find the place | municipality | no |
| Warning table anchor, `warnings_gemeinde_shh.html#Stadt Husum` | 0 when warned, **broken when not** | municipality | see §5.2 |

### 5.2 Two destinations that look attractive and are not

**The district page.** `warnungen_landkreise/warnWetter_node.html` accepts the same `ort` and `lk`
parameters — verified, `?ort=Husum&lk=Kreis%20Nordfriesland` selects correctly. But its inline config
sets `GEMEINDE_WARNUNGEN = false`, so it draws **district-grain** warnings. Our page's own warnings
come from Bright Sky's municipality product (#4). Linking to the district page would send the reader
from a Frisian list of municipality warnings to an official page showing a different, coarser set —
and the two can disagree. Reject it for that reason, not for its usability, which is identical.

**The warning-table anchors.** DWD documents deep anchors into a per-Bundesland HTML table, e.g.
`…/warnapp_gemeinden/json/warnings_gemeinde_shh.html#Gemeinde Miesbach`. It is tempting: static file,
no JavaScript, no map. It is unusable here for three reasons, all verified:

1. **The table only contains municipalities that currently have a warning.** DWD says so, and says
   the reader is left at the top of the table otherwise. On a page whose normal state is *no
   warnings*, the normal outcome is a broken anchor.
2. **It was empty for our whole region during this session.** `warnings_gemeinde_shh.html` returned
   **301 bytes**, no rows. The nationwide file listed 2,012 warned municipalities across seven
   Bundesländer, none of them Schleswig-Holstein.
3. **The anchor uses a sixth name form** — `Stadt Husum`, `Gemeinde Barleben`, `Mitgliedsgemeinde …`,
   `gemeindefreies Gebiet …` — different again from the `ort` value, and DWD's own note admits the
   name may need to be read out of the page source.

### 5.3 There is no WarnWetter web view

The ticket asks to compare against one. It does not exist.

- `warnwetter.de` and `www.warnwetter.de` have **no address record** — DNS resolves the name but
  returns no host. Only `app-prod-static.warnwetter.de` resolves, and that is the app's data bucket
  identified in #4, not a web page.
- DWD's own WarnWetter page (`…/leistungen/warnwetterapp/warnwetterapp.html`, HTTP 200) offers the
  App Store and Google Play only. The one `warnwetterapp.de` domain it links to serves four legal
  pages — accessibility, privacy, disclaimer, the civil-protection version — and no application.

The warning application on `www.dwd.de` **is** the web equivalent of WarnWetter, which is why the
recommendation targets it.

---

## 6. Language, and the English page

**The German page declares its language correctly.** `<html xml:lang="de" lang="de">`, plus
`<body class="… lang-de">`. A Mooring page linking out to it is linking to something honestly marked
as German, which is what #10's signposting relies on.

**An English page exists at a predictable URL and takes the same parameters.** Verified live:

```
https://www.dwd.de/EN/weather/warnings/warnings_node.html?ort=Husum&lk=Kreis%20Nordfriesland   → 200
```

It declares `<html xml:lang="en" lang="en">`, loads the same `gemeinden.js` and the same
`GEMEINDE_WARNUNGEN = true` municipality product, and `getGemeindeFromURL()` resolved Husum on it
exactly as on the German page.

**But it is not an English destination in the sense that matters.** Checked by selecting a warned
municipality on the English page: the detail box rendered the identical German text —
`Amtliche WARNUNG vor GEWITTER … Es treten Gewitter auf …`. Only the page chrome is translated
(*Automatic updating*, *Warnings of extreme weather (Level 4)*, *No severe weather*), and even that
is partial — the timestamp line and the "select a place" prompt beside the map are still German.

So the English page translates the furniture and not the content. It does not change #10's decision,
which is what the ticket predicted; recorded here because it was cheap to establish. Note also that
the EN path is `EN/weather/warnings/warnings_node.html` — **not** a mechanical `DE`→`EN` rewrite of
the German path, and it has no `warnkarten` per-Bundesland node, so the graceful-degradation form of
§2.5 is not available in English.

---

## 7. Open questions for the owner

1. **Confirm `westerland` → `Sylt` and `hamburger-hallig` → `Reußenköge`** (§3.3). Both are local
   judgements, not lookups, and both should be recorded as choices in the place registry rather than
   inherited silently from this document.
2. **Decide whether the link is worth twenty stored strings**, or whether the coarse
   `?bundesland=shh` target from §4.3 is enough. The recommendation assumes yes, because #10 made this
   link the only route to the warning detail.
3. **Decide how a broken `ort` is noticed.** Nothing about §2.1 fails loudly. If the pairing lives in
   the place registry, a build-time check that each `ort` value still appears in `gemeinden.js` would
   turn a silent break into a failed build — which matches how this project already prefers to fail.
   That check is cheap: the catalogue is a single CORS-open file.
4. **The coastal-warning gap from #4 is untouched by this.** These links show municipality warnings.
   The *Küsten-Warnungen* for Nordfriesische Küste still appear nowhere, on our page or on the page we
   link to at this grain.

---

## Appendix: primary sources

All fetched 2026-08-15, 22:55–23:30 UTC.

- DWD *Ihr Homepagewetter* — the document that specifies `?ort=` and the per-Bundesland links, and
  that disclaims availability — <https://www.dwd.de/DE/wetter/warnungen_aktuell/objekt_einbindung/objekteinbindung_node.html>
- Archived copy of the same page, 2019-01-31, used to date the contract — <http://web.archive.org/web/20190131003548/https://www.dwd.de/DE/wetter/warnungen_aktuell/objekt_einbindung/objekteinbindung_node.html>
- Municipality warning application (national node) — <https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnWetter_node.html>
- Municipality warning application (Schleswig-Holstein / Hamburg node, the recommended base) — <https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnkarten/warnWetter_shh_node.html?bundesland=shh>
- District warning application, rejected in §5.2 — <https://www.dwd.de/DE/wetter/warnungen_landkreise/warnWetter_node.html>
- English warning application — <https://www.dwd.de/EN/weather/warnings/warnings_node.html>
- DWD short link for national warnings (HTTP 301) — <https://www.dwd.de/warnungen>
- `gemeinden.js` — the catalogue the `ort` value is matched against — <https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/viewer/gemeinden.js>
- `__everything_warnWetter.js` — the bundle containing `getGemeindeFromURL` and
  `parseBundeslandFromURL` — <https://www.dwd.de/SiteGlobals/Functions/JavaScript_Optimierung2/__everything_warnWetter.js>
- Per-Bundesland warned-municipality HTML table, evaluated in §5.2 — <https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde_shh.html>
- Municipality warnings JSONP, used to find a warned municipality for the render test — <https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde.json>
- DWD WarnCellID catalogue CSV, for the cell ids and the `NAME`/`KURZNAME` forms — <https://www.dwd.de/DE/leistungen/opendata/help/warnungen/cap_warncellids_csv.csv?__blob=publicationFile&v=3>
- DWD WarnWetter app page, establishing that there is no web view — <https://www.dwd.de/DE/leistungen/warnwetterapp/warnwetterapp.html>
- Bright Sky `/alerts`, used for coordinate → cell resolution — <https://api.brightsky.dev/alerts>
- Wayback CDX index, used for the stability figures — <http://web.archive.org/cdx/search/cdx>
