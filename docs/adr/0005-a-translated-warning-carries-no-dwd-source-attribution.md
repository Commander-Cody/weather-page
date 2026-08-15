# A warning translated into Mooring carries no DWD source attribution

DWD data is CC BY 4.0 under § 7 DWD-Gesetz, and DWD requires the source note `Quelle: Deutscher
Wetterdienst` immediately adjacent to the data used — not merely in a footer. But the same rules
add a clause that inverts this for warnings specifically: *"Wenn vom DWD ausgegebene amtliche
Wetterwarnungen verändert werden, ist der beigegebene Quellvermerk zu löschen."* Rendering a
warning in Mooring is an alteration, so a Frisian warning must **not** carry that source note, as
that would present DWD as the author of text DWD did not write.

For altered works DWD instead expects at minimum a mention in central credits or the Impressum,
alongside a modification-style note near the data. Crucially, that note's wording is **not**
prescribed, unlike the `Quellenvermerk` itself. So the warning slot carries a Mooring label
followed by the untranslated proper name `Deutscher Wetterdienst`, attached once to the slot rather
than to each warning, and DWD is also named in the Impressum.

## Consequences

- **This is the one place the page credits a source by *not* naming it the usual way.** A future
  reader comparing the warning slot against the Open-Meteo and BSH credit lines will see an
  inconsistency and be tempted to "fix" it by adding `Quelle: Deutscher Wetterdienst`. That would
  breach the licence terms, not satisfy them.
- **The label is Mooring, the institution is not.** A German modification note would put German text
  inline on a page whose defining rule forbids exactly that. Since the wording is unprescribed, a
  Mooring label carrying the German proper name satisfies the obligation without breaking the rule.
- **If a warning were ever shown verbatim in German, the normal rule returns** and it would need
  `Quelle: Deutscher Wetterdienst` next to it. The page does not do this today.
- Where this credit line sits relative to the page's three other credit lines, whose rules conflict
  with each other, is decided separately.
