<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- status: draft -->
# World4 model schema (v0.1 draft)

Draft specification for declarative mass-flow models under `models/` and the
standalone chemical atom-balance registry `models/reactions.toml`.

This document defines the schema before any Rust code is written. Rust
implementation (`crates/w4-core` and `crates/w4-cli`) begins only after
backlog steps 1–3 complete (ledger format plus one verified PET section).

Provenance ledger specification: [`docs/sources-and-claims.md`](./sources-and-claims.md).
Binding editorial policy: [`EDITORIAL.md`](../EDITORIAL.md).

---

## Core principles (v0.1)

1. **No sourced literals in models.** Model files define topology, scopes,
   relationships and `sorry` holes — never typed empirical numbers. Every
   sourced quantity references a claim ID in `data/claims.toml`.
2. **Plain `mdBook` integration (`w4 export` + `{{#include}}`).** No custom
   mdBook preprocessor. `w4 export` writes a committed Markdown fragment under
   `src/_generated/<model-id>.md` (starting with a generator comment naming
   `w4 export` and the source model file, and emitting `[^c-<claim-id>]`
   footnotes). Chapters include it via stock `{{#include ../_generated/<model-id>.md}}`.
   `w4 export --check` in PR CI fails if a committed fragment is stale.
3. **Publication gate.** Any chapter listed in `src/SUMMARY.md` (`stub` or
   `verified`) may include only models with zero open `sorry` holes and all
   referenced claims verified through the editorial workflow.
4. **Goods-level mass by default (`total_mass`).** Real waste and industrial
   statistics report *goods* (bales with caps, labels, residual liquid,
   moisture), not chemically pure polymer. v0.1 checks mass conservation in
   `kg`, `t`, `kt` (and annual rates `kg/yr`, `t/yr`, `kt/yr`) at goods level,
   with per-flow `scope` making material definitions explicit.
5. **Interval closure (`[lo, hi]`), never arbitrary tolerances.** Every quantity
   normalises to an interval `[lo, hi]` and propagates through each node.
   - **Conserved:** `0` lies inside `sum(inflows) - sum(outflows)` (or
     `sum(inflows) - sum(outflows) - delta` for a 1-period stock).
   - **Closed by residual:** when independent sources do not close and the
     author declares an explicit `residual` flow (at most one per node, with a
     mandatory `reason`), `w4` computes the residual interval, fails if it is
     wholly negative, and labels the node **"closed by residual"** (never
     "conserved"). Sourced values are never silently adjusted.
   - **Not evaluated (open sorry):** any node incident to a `sorry` flow is
     marked **"not evaluated (open sorry)"**, and `w4` prints the **implied
     interval `[lo, hi]`** the `sorry` hole must fall into for closure.
6. **Year-mismatch warning.** Whenever a referenced claim's `data_year` differs
   from `model.reference_year`, `w4` emits a visible warning in CLI output and
   in the exported Markdown fragment.

---

## Model file schema (`models/<kind>/<slug>.toml`)

### Top-level metadata (`[model]`)

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | `"0.1"` |
| `id` | string | yes | Unique model slug (e.g. `"pet_bottles_ch"`). |
| `title` | string | yes | Human-readable title. |
| `region` | string | yes | Primary geographic boundary (e.g. `"CH"`). |
| `reference_year` | string | yes | Target calendar year of the model (e.g. `"2023"` or `"tbd"` while all flows are `sorry`). |
| `period` | string | yes | Time basis of the boundary (e.g. `"1 yr"`). |
| `steady_state_note` | string | no | Explicit statement when in-use stock change is assumed negligible over `period`. |
| `description` | string | yes | Concise boundary definition. |

### Nodes (flat unique ID namespace)

Every node ID must be unique across `[sources]`, `[processes]`, `[stocks]` and
`[sinks]`. Flows reference bare node IDs (`from = "virgin_resin"`).

- **`[sources.<id>]`**: external inflows entering the system boundary.
  Topology rule: **no incoming flows** allowed.
- **`[processes.<id>]`**: transformation or routing nodes obeying interval mass
  balance (`sum(in) - sum(out)`). Fields: `label`, optional `conservation`
  (defaults to `"total_mass"`).
- **`[stocks.<id>]`** *(optional 1-period storage)*: reservoirs where
  `sum(in) - sum(out) == delta` over `period`. Fields: `label`, `delta`
  (either `{ claim = "..." }`, `{ residual = true, reason = "..." }`, or
  `{ sorry = true, reason = "...", research_question = "..." }`).
- **`[sinks.<id>]`**: outflows leaving the system boundary.
  Topology rule: **no outgoing flows** allowed.
- Self-loops (`from == to`) are forbidden. Multi-node cycles (such as closed-loop
  recycling `sorting_and_recycling -> bottle_production`) are allowed.

### Flows (`[[flows]]`)

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Unique flow ID within the model. |
| `from` | string | yes | Source, process or stock node ID. |
| `to` | string | yes | Process, stock or sink node ID. |
| `scope` | string | yes | Physical goods definition of this flow (e.g. caps/labels included vs. net resin). |
| `quantity` | table | yes | Exactly one of the four forms below. |

The four `quantity` forms:

```toml
# 1. Directly cited claim from data/claims.toml
quantity = { claim = "<claim-id>" }

# 2. Computed share/yield of another flow (using a rate/percentage claim from data/claims.toml)
quantity = { share_of = "<flow-id>", claim = "<rate-claim-id>" }

# 3. Explicit unaccounted / balancing flow (max 1 per node; fails if wholly negative)
quantity = { residual = true, reason = "<why an unaccounted residual exists>" }

# 4. Typed open research hole (compiles; node marked "not evaluated" with implied bounds)
quantity = { sorry = true, unit = "t/yr", reason = "<what is missing>", research_question = "<specific question to research>" }
```

Note: `share_of` dependencies must form an acyclic derivation graph even when
the physical material flows form a cycle.

### Assertions (`[[assertions]]`)

v0.1 supports a single assertion kind — `ratio` — which cross-checks a
published rate claim against independently sourced mass flows (no naked
threshold numbers):

```toml
[[assertions]]
id = "collection_rate_cross_check"
kind = "ratio"
numerator = ["bottles_collected"]
denominator = ["bottles_to_market"]
expected_claim = "<published-rate-claim-id>"
description = "Cross-checks separate collection tonnes against the published collection rate."
```

`w4` computes the interval `sum(numerator) / sum(denominator)` and verifies
that it overlaps the interval of `expected_claim` in `data/claims.toml`.

---

## Draft model: `models/materials/pet_bottles_ch.toml`

Switzerland 1-year PET beverage bottle collection and recycling loop.
**Contains `sorry` holes only and zero empirical numbers** until verified Swiss
sources (e.g. BAFU, PET-Recycling Schweiz) pass through the `data/` ledger
workflow.

```toml
schema_version = "0.1"

[model]
id = "pet_bottles_ch"
title = "Switzerland 1-Year PET Beverage Bottle Collection and Recycling Loop"
region = "CH"
reference_year = "tbd"
period = "1 yr"
steady_state_note = "Beverage bottles turn over in weeks; annual in-use stock change is assumed negligible over a 1-year period."
description = "Goods-level mass-flow boundary for PET beverage bottles placed on the Swiss market, separately collected, mechanically recycled, incinerated in municipal waste (KVA), or littered."

# ---------------------------------------------------------------------------
# Boundary sources
# ---------------------------------------------------------------------------
[sources.virgin_resin]
label = "Virgin PET Resin / Imported Preforms and Filled Bottles"

# ---------------------------------------------------------------------------
# Processes (goods-level total_mass interval balance)
# ---------------------------------------------------------------------------
[processes.bottle_production]
label = "Bottle Supply (Manufacturing, Preforms & Net Filled-Bottle Trade)"

[processes.market_consumption]
label = "Swiss Beverage Market (Placed on Market & Post-Consumer Disposal)"

[processes.sorting_and_recycling]
label = "Separate PET Collection, Sorting & Mechanical Recycling"

# ---------------------------------------------------------------------------
# Boundary sinks
# ---------------------------------------------------------------------------
[sinks.open_loop_rpet]
label = "Open-Loop rPET (Fibres, Sheet, Strapping, Non-Bottle Packaging)"

[sinks.municipal_incineration]
label = "Municipal Solid Waste Incineration (KVA)"

[sinks.littered_environment]
label = "Littered PET Bottles in Environment"

# ---------------------------------------------------------------------------
# Directed flows (sorry holes only; replace with `claim` / `share_of` once
# primary Swiss sources are recorded in data/sources.toml & data/claims.toml)
# ---------------------------------------------------------------------------
[[flows]]
id = "virgin_to_production"
from = "virgin_resin"
to = "bottle_production"
scope = "Virgin PET resin and net imported preforms/bottles entering Swiss PET beverage bottle supply."
quantity = { sorry = true, unit = "t/yr", reason = "Primary source not yet recorded in data/claims.toml.", research_question = "How many tonnes per year of virgin PET (or net non-recycled input) enter Swiss PET beverage bottle supply?" }

[[flows]]
id = "rpet_closed_loop"
from = "sorting_and_recycling"
to = "bottle_production"
scope = "Food-grade bottle-to-bottle rPET re-entering Swiss PET beverage bottle production."
quantity = { sorry = true, unit = "t/yr", reason = "Primary source not yet recorded in data/claims.toml.", research_question = "What mass or share of recycled Swiss PET beverage bottles returns into bottle-to-bottle production each year?" }

[[flows]]
id = "bottles_to_market"
from = "bottle_production"
to = "market_consumption"
scope = "PET beverage bottles placed on the Swiss market (confirm with source whether caps and labels are included)."
quantity = { sorry = true, unit = "t/yr", reason = "Primary source not yet recorded in data/claims.toml.", research_question = "What annual tonnage of PET beverage bottles is placed on the Swiss market according to BAFU / PET-Recycling Schweiz, and what is the exact weight definition?" }

[[flows]]
id = "bottles_collected"
from = "market_consumption"
to = "sorting_and_recycling"
scope = "PET beverage bottles collected through separate Swiss collection channels."
quantity = { sorry = true, unit = "t/yr", reason = "Primary source not yet recorded in data/claims.toml.", research_question = "How many tonnes per year (or what collection rate of market supply) of PET beverage bottles are separately collected in Switzerland?" }

[[flows]]
id = "bottles_to_incineration"
from = "market_consumption"
to = "municipal_incineration"
scope = "Uncollected PET beverage bottles disposed of in mixed municipal solid waste sent to Swiss KVAs."
quantity = { sorry = true, unit = "t/yr", reason = "Primary source not yet recorded in data/claims.toml.", research_question = "What tonnage or share of uncollected Swiss PET beverage bottles enters mixed municipal waste incineration (KVA)?" }

[[flows]]
id = "bottles_littered"
from = "market_consumption"
to = "littered_environment"
scope = "PET beverage bottles lost outside collection and municipal waste streams."
quantity = { sorry = true, unit = "t/yr", reason = "Primary source not yet recorded in data/claims.toml.", research_question = "Are there primary Swiss BAFU estimates for the mass or share of PET beverage bottles lost to littering?" }

[[flows]]
id = "rpet_open_loop"
from = "sorting_and_recycling"
to = "open_loop_rpet"
scope = "Recycled PET output leaving the beverage bottle loop for textiles, strapping, trays or sheet."
quantity = { sorry = true, unit = "t/yr", reason = "Primary source not yet recorded in data/claims.toml.", research_question = "What mass or share of Swiss recycled PET beverage bottle output goes into open-loop applications rather than new bottles?" }

[[flows]]
id = "sorting_rejects_to_incineration"
from = "sorting_and_recycling"
to = "municipal_incineration"
scope = "Sorting, washing and extrusion losses/rejects (including non-PET fractions if gross weight is used) sent from recycling plants to incineration."
quantity = { sorry = true, unit = "t/yr", reason = "Primary source not yet recorded in data/claims.toml.", research_question = "What sorting and reprocessing loss rate applies to Swiss PET beverage bottle recycling, and where do the rejects go?" }
```

---

## Standalone stoichiometry registry (`models/reactions.toml`, v0.1)

In v0.1, chemical stoichiometry is kept strictly separate from mass-flow models
and performs **integer atom-count balance verification only** — no hardcoded
atomic-weight table and no stoichiometry-derived mass flows yet.

```toml
schema_version = "0.1"

[species.pet_repeat_unit]
name = "Polyethylene terephthalate (repeat unit)"
formula = "C10H8O4"

[species.o2]
name = "Molecular oxygen"
formula = "O2"

[species.co2]
name = "Carbon dioxide"
formula = "CO2"

[species.h2o]
name = "Water"
formula = "H2O"

[reactions.pet_complete_combustion]
description = "Ideal complete oxidation of the PET repeat unit (atom-count balance only; excludes additives, incomplete combustion and energy recovery)."
reactants = { pet_repeat_unit = 1, o2 = 10 }
products = { co2 = 10, h2o = 4 }
```

`w4-core` parses each chemical formula into element counts and proves that
`sum(reactant_coeff * atoms(species)) == sum(product_coeff * atoms(species))`
for every element (`C`, `H`, `O`, ...). Mass-flow CO2 conversion will be
revisited only when an incineration page needs it and a verified primary source
provides the empirical factor for bottle-grade PET.
