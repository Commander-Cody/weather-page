# The page relays warnings, it never authors them

Warnings are the one thing on this page that carry the authority of an official body, so the page
takes a strict editorial stance: it shows everything an authority warns about, ranks it, and adds
nothing of its own. Concretely — no severity is filtered out, no category is filtered out, an
unknown event code degrades to a generic name rather than vanishing, and the page never derives a
warning class from its own numbers.

That last one is the surprising part. BSH's storm surge classes are defined as height above mean
high water (1.5–2.5 m, 2.5–3.5 m, over 3.5 m), and since ADR-0002 every height this page holds is
already a deviation from mean high water. The page could classify a surge itself, with no extra
source. It must not: the forecast can sit either side of a threshold by a few centimetres, and a
page that names a *sehr schwere Sturmflut* on its own authority is making a safety claim it cannot
stand behind. Surge warnings come from BSH as published warnings or they do not appear.

Filtering is rejected for a related reason. A severity filter looked attractive because a yellow
wind warning is close to the baseline condition on this coast in winter — but #7 already locked
that an empty warning area means "the sources say nothing", and a filter would make that sentence
false. Prominence, not inclusion, is the lever: severity is carried by an ordered count of marks,
so a routine warning can be quiet without being hidden.

## Consequences

- **One ladder of four ranks serves two agencies.** DWD's four severities occupy ranks 1–4; BSH's
  three surge classes occupy 2, 3 and 4. An ordered count is only meaningful if there is a single
  ladder, so the two scales had to be placed on it deliberately. The cost: a Sturmflut renders
  mid-ladder alongside a Markante Wetterwarnung, and a BSH warning borrows a DWD tier colour. The
  event name is what tells a reader which body issued it.
- **Severity is encoded three times over** — count, colour, word. Colour alone was rejected because
  it fails silently, and DWD's yellow → orange → red run is hardest to separate for exactly the
  most common kinds of colour blindness. The count is the channel that survives greyscale and needs
  no language, which matters more here than on a page whose words every reader can read.
- **Vorabinformation is not a rank.** It is `urgency = future`, so the page organises warnings by
  onset — running now, or starting at a stated time — and a pre-alert is simply the far end of
  that. This keeps DWD's fifth hatched map tier out of the ladder, and means the translation lookup
  must key on **event code plus urgency**: seven codes carry two different meanings.
