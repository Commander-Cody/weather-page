# A hand-paired value is verified against the source that consumes it, never against a status code

The place registry holds four values a human chose and no algorithm can derive from anything else
we store — the gauge, the land point, the sea point, and the DWD municipality name. Every one of
them fails **silently** when wrong, because each of the three sources answers a wrong value exactly
as cheerfully as a right one: the forecast API returns weather for any land coordinate, the Marine
API returns a sea temperature for dry land, and DWD's warning page returns byte-identical HTML for
`?ort=Husum` and `?ort=Zzzzzznotaplace`. So the rule is that a hand-paired value is verified against
the source that consumes it, and an HTTP 200 is never accepted as evidence that a value resolved.

The verification has **two implementations**, because the two kinds of source expose different
things:

- **Where the source echoes back what it used**, compare requested against returned. Open-Meteo
  replies with the centre of the grid cell it actually read, so both coordinates are checked this
  way. The land point needs a tolerance that admits normal grid snapping — ICON-D2's grid is 0.02°,
  so a legitimate cell centre sits up to roughly 1.5 km away — while still catching
  `cell_selection=land` relocating the point to a different settlement.
- **Where the source matches against a catalogue**, assert the value is in that catalogue. DWD's
  municipality match is an exact case-insensitive comparison against a JS file that can be fetched
  and read directly.

Alongside the check, every hand-paired value records its **provenance** — what it was confirmed
against, and when. That part is uniform with no per-source variation, and it is what stops a later
session from having to re-establish which values anyone ever actually looked at.

## Consequences

- **The uniform thing is the prohibition, not the mechanism.** Forcing echo-comparison and
  catalogue-membership into one implementation would be uniformity on paper only. A future reader
  should not "unify" them.
- **None of these checks can run at build time.** They all need the network, so they belong in the
  scheduled fetch job or a monitor, failing into ADR-0001's non-zero exit. The build-time Zod schema
  can only check shape, and must not be extended to claim more.
- **Correctness is established once, by a human, and is never re-proven automatically.** These
  checks catch drift and silent relocation. None of them can tell you that a coordinate confirmed
  against the wrong village is wrong. That is what provenance is for.
- **The authority is consulted, not vendored.** BKG's GN250 and VG250 are open under
  Datenlizenz Deutschland Namensnennung 2.0, but their boundaries are generalised at 1:250 000 —
  good enough to catch a several-kilometre error, not good enough to adjudicate a point near a
  boundary. Copying them into the repo would add a fifth credit line requiring two links, for a
  precision the data does not have.
