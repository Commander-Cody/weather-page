# Place names are a native name plus per-variety overrides

Place names differ between North Frisian varieties, so the obvious model is a translation
table: one column per variety, every place named in every one of them. We do not do that.

**Each place carries one native name — what it is called on its own coast — tagged with
the variety that name belongs to. A variety carries an override only where its own form
genuinely differs.** Absent an override, the native name is what the reader sees.

The reason is the project's own rule that no agent may invent Frisian vocabulary and that
gaps go to a fluent speaker in a batch. Under a translation table, adding Fering means
producing a Fering name for all twenty places, including mainland ones like Bredstedt and
Niebüll that a Fering speaker may simply have no distinct name for. That would put twenty
new questions on the batch list as the entry price for a second variety — making the
promised Fering extension harder to keep, which is backwards.

Under the override model the same addition costs only the names that actually differ.
Everything else falls through to a name that is already correct.

## What the variety tag means

`variety` records **which variety the native name is in**. Nothing more. It is provenance,
not a judgement about any other variety.

This matters because the field was previously carrying an uncertainty as though it were a
fact. `list` is tagged Sölring — but nobody had established whether Mooring has its own
form for List or whether Mooring speakers use the Sölring one, and the field had no way to
say so.

With the tag narrowed to provenance, that uncertainty becomes **derived** rather than
stored: a name is unresolved for a reader when its native variety is not the reader's
variety and that variety has no override. Today that is exactly two places, `list` and
`hoernum`. Adding Fering starts with all twenty unresolved, which is the honest state and
hands a translator a worklist instead of a blank page.

To record that a fluent speaker checked and the forms really are identical, write the
override out explicitly even though it matches. Without that, a confirmed-same name would
sit on the batch list forever as noise.

## Consequences

- **Overrides live in the language file, not the place registry.** A Fering override is
  translator knowledge, and it belongs where the translator works — so adding a variety
  never requires editing the registry. The cost is that a place's forms are split across
  two artifacts rather than visible on one row.
- **Place names use their own fallback chain, and it is not the general one.** It is
  `override(variety) → native name`, a single step. It must not fall through Mooring on
  the way: a Fering reader with no override for List should see the native `List`, not a
  Mooring form of a Sylt place. General strings fall back to Mooring; place names never
  do. A build session that collapses these into one chain gets it wrong.
- **Missing place overrides never fail the build**, unlike every other missing string. An
  absent override is a correct outcome, not an omission, so it cannot be treated as one.
  Unresolved names surface through the batch list instead.
- **The escape hatch is already open.** If a variety considers a native name actively
  wrong rather than merely foreign, it writes an override. No schema change, no
  migration — that is the mechanism working as designed.
- **Nothing here applies to the interface.** Every string around the name is translated
  normally. Only the name itself is fixed against the reader's variety.
