# The 2060 Settlement Atlas — Interactive Map

A speculative worldbuilding project modeling **where humanity could sustainably live by 2060** under a deliberately worst-case scenario: +3 °C warming, AMOC collapse, +0.55 m sea-level rise, no fossil fuels, no synthetic fertilizer, and minimal global trade.

Population is derived from the ground up — climate → water → foodshed → carrying capacity — never assigned top-down. Every piece of current land belongs to exactly one of **160 zones**: settled regions (R), excluded zones (X), and wildlands (W).

## View it

**[→ Open the live map](https://YOURUSERNAME.github.io/2060-settlement-atlas/)**
*(replace `YOURUSERNAME` after you publish — see setup below)*

Or download `index.html` and open it in any browser. It's fully self-contained (one file, ~3 MB) and works offline — the only external dependency is the D3 library from a CDN.

## What you can explore

Toggle layers in the legend (top-right):

- **Zones** — settled (green), excluded (red), wildland-hostile (near-red) and wildland-covenant (green-grey). Click anywhere to identify.
- **Cities** (circles) — 488 cities colored by 2060 fate: viable, defended heat-refuge, heat-stressed, or contracting/excluded.
- **Coastal submergence** — drowned coasts drawn to *regional* sea-level rise (the US East Coast sits at +0.90 m thanks to AMOC pile-up, the Gulf at +1.15 m).
- **National parks** (green hatching) — "Wild-Locked," held through the contraction.
- **Sacred sites** (stars) — 139 across three lenses: human-attested, and two AI-selected sets.
- **Toxic sites** (diamonds) — 14 contaminated exclusions, classed by 2060 decay.
- **Species refugia + greenways** (leaves) — 21 flagship endangered species: present range → 2060 climate refugium, with the corridors we must keep open.
- **Dissolve zones** — collapse the 4,596 base units into 160 clean zone silhouettes.
- **Political borders** — toggle off for a pure zone view.

## Publishing this to GitHub Pages

See [`SETUP.md`](SETUP.md) for click-by-click instructions.

## A note on the data

This is **modeled, not predicted** — a rigorous thought experiment, not a forecast. Some overlays (national-park and species-range boundaries, flood polygons) are curated approximations where authoritative datasets weren't available; they're built to be swapped for precise geometry later. The zone partition itself is exhaustive and verified: every unit of land resolves to exactly one zone, and the total dissolved land area computes to Earth's real land fraction.
