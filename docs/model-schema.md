<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- status: draft -->
# Model schema (v0.1 draft)

Draft specification for declarative mass-flow models under `models/` and the
standalone chemical atom-balance registry `models/reactions.toml`.

This document defines the schema before any Rust code is written. Rust
implementation (`crates/earthmania-core` and `crates/earthmania-cli`) begins only after
backlog steps 1–3 complete (owner-verified claims for the first flows, plus
the ledger checks).

Provenance ledger specification: [`docs/sources-and-claims.md`](./sources-and-claims.md).
Binding editorial policy: [`EDITORIAL.md`](../EDITORIAL.md).

---

## Core principles (v0.1)

1. **No sourced literals in models.** Model files define topology, relationships
   and `sorry` holes — never typed empirical numbers or ungrounded formulas.
   Every sourced quantity references a claim ID in `data/claims.toml`; every
   chemical species formula in `models/reactions.toml` references a statement
   claim ID in `data/claims.toml`.
2. **Model verification status line.** Line 1 of every model file carries the
   same status convention as pages in `_guidelines.md`:
   ```toml
   # status: draft
   # status: verified · verified: YYYY-MM-DD by <github-handle> (PR #n)
   ```
   Any chapter listed in `src/SUMMARY.md` (`stub` or `verified`) may include
   only `verified` models with zero open `sorry` holes. The gate is enforced at
   export: `earthmania export` refuses to write a fragment for a model that is
   not `verified` or still has a `sorry` hole, so a committed fragment always
   comes from a verified model. Editing a verified model resets its status line
   to `draft` until it is verified again.
3. **Plain `mdBook` integration (`earthmania export` + `{{#include}}`).** No custom
   mdBook preprocessor. `earthmania export` writes a committed **tables-only** Markdown
   fragment (never prose) outside `src/` under `models/generated/<model-id>.md`
   (starting with a generator comment naming `earthmania export` and the source model
   file). Keeping fragments outside `src/` prevents an empty directory in the
   published `book/` output. Chapters include fragments via stock
   `{{#include ../../models/generated/<model-id>.md}}`. Fragments emit footnote
   **references** (`[^c-<claim-id>]`) only; footnote definitions stay
   hand-written in `## Sources` on the host page. `earthmania export --check` in PR CI
   fails if a committed fragment is stale.
4. **No unsourced prose via model fields.** Node `label` fields are short names
   only (never claims or explanations). Free-text metadata fields
   (`description`, `steady_state_note`, `scope`, `reason`, `research_question`)
   are internal documentation for editors and are **not exported** into rendered
   page fragments unless backed by a `claim` ID.
5. **Goods-level mass per period (`kg`, `t`, `kt`).** Every process in v0.1 uses
   goods-level total-mass balance over `[model].period` (mass per period only:
   `"kg"`, `"t"`, `"kt"`, plus dimensionless `"%"` and `"1"` for `share_of`
   rates). Steady-state over `period` is assumed in v0.1; stock nodes are
   deferred to v0.2.
6. **Interval closure (`[lo, hi]`), never arbitrary tolerances.** Every quantity
   normalises to an interval `[lo, hi]` (from source-stated `range` /
   `uncertainty` in `data/claims.toml`, or optional flow-level
   `assumed_uncertainty`) and propagates through each process.
   - **Conserved:** `0` lies inside `sum(inflows) - sum(outflows)`.
   - **Closed by residual:** when independent sources do not close and the
     author declares an explicit `residual` flow (at most one per process, with
     a mandatory `reason`), `earthmania` computes the residual interval, fails if it is
     wholly negative, and labels the process **"closed by residual"** (never
     "conserved"). Sourced values are never silently adjusted.
   - **Not evaluated (open sorry):** any process incident to a `sorry` flow is
     marked **"not evaluated (open sorry)"**. When that `sorry` is the process's
     only unknown (no other `sorry` and no `residual` on the same process),
     `earthmania` prints the **implied interval `[lo, hi]`** the hole must fall
     into for closure; with two or more unknowns it prints none.
   - **Order of evaluation:** `share_of` flows are computed first, then each
     `residual`. A `residual` whose process also depends on another process's
     `residual` is an error in v0.1, not something to solve.
7. **Year-mismatch warning.** Whenever a referenced claim's `data_year` differs
   from `model.reference_year`, `earthmania` emits a visible warning in CLI output and
   in the exported table fragment.

---

## Model file schema (`models/<kind>/<slug>.toml`)

File names, model IDs, node IDs and flow IDs are **lowercase and hyphenated**
(matching `_guidelines.md` and claim IDs, e.g. `pet-bottles-ch`).

### Top-level metadata (`[model]`)

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | `"0.1"` |
| `id` | string | yes | Unique hyphenated model slug (e.g. `"pet-bottles-ch"`). |
| `title` | string | yes | Short display title. |
| `region` | string | yes | Primary geographic boundary (e.g. `"CH"`). |
| `reference_year` | string | yes | Target calendar year of the model (`"YYYY"`, or `"tbd"` while all flows are `sorry`). |
| `period` | string | yes | Accounting period for mass flows (e.g. `"1 yr"`). All flow quantities are mass per `period`. |
| `steady_state_note` | string | no | Internal note recording the steady-state assumption (not exported). |
| `description` | string | yes | Internal boundary description (not exported). |

### Nodes (flat unique ID namespace)

Every node ID must be unique across `[inputs]`, `[processes]` and `[outputs]`.
(Boundary nodes are not called "sources": that word is reserved for cited
sources in `data/sources.toml`.)
Flows reference bare node IDs (`from = "virgin-resin"`). Node `label` values
are short names only.

- **`[inputs.<id>]`**: external inflows entering the system boundary.
  Topology rule: **no incoming flows** allowed.
- **`[processes.<id>]`**: transformation or routing nodes obeying goods-level
  total-mass interval balance (`sum(in) - sum(out)`). Field: `label`.
- **`[outputs.<id>]`**: outflows leaving the system boundary.
  Topology rule: **no outgoing flows** allowed.
- Self-loops (`from == to`) are forbidden. Multi-node cycles (such as closed-loop
  recycling `sorting-and-recycling -> bottle-supply`) are allowed.

### Flows (`[[flows]]`)

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Unique hyphenated flow ID within the model. |
| `from` | string | yes | Input or process node ID. |
| `to` | string | yes | Process or output node ID. |
| `scope` | string | yes | Internal note on the physical good measured on this edge (not exported). |
| `quantity` | table | yes | Exactly one of the four forms below. |
| `assumed_uncertainty` | inline table | no | Optional author-assumed interval when the source states none: `{ rel = "<decimal>", note = "..." }` or `{ abs = "<decimal>", note = "..." }`. Flagged as author-assumed in exported tables; never stored in `data/claims.toml`. |

The four `quantity` forms:

```toml
# 1. Directly cited claim from data/claims.toml
quantity = { claim = "<claim-id>" }

# 2. Computed share/yield of another flow (using a rate/percentage claim from data/claims.toml)
quantity = { share_of = "<flow-id>", claim = "<rate-claim-id>" }

# 3. Explicit unaccounted / balancing flow (max 1 per process; fails if wholly negative)
quantity = { residual = true, reason = "<why an unaccounted residual exists>" }

# 4. Typed open research hole (compiles; process marked "not evaluated" with implied bounds)
quantity = { sorry = true, unit = "t", reason = "<what is missing>", research_question = "<specific question to research>" }
```

Note: `share_of` dependencies must form an acyclic derivation graph even when
the physical material flows form a cycle.

### Assertions (`[[assertions]]`)

v0.1 supports a single assertion kind — `ratio` — which cross-checks a
published rate claim against independently sourced mass flows (no naked
threshold numbers):

```toml
[[assertions]]
id = "collection-rate-cross-check"
kind = "ratio"
numerator = ["bottles-collected"]
denominator = ["bottles-to-market"]
expected_claim = "<published-rate-claim-id>"
```

`earthmania` computes the interval `sum(numerator) / sum(denominator)` and verifies
that it overlaps the interval of `expected_claim` in `data/claims.toml`.

---

## Draft model: `models/materials/pet-bottles-ch.toml`

Switzerland 1-year PET beverage bottle collection and recycling loop.
**Contains `sorry` holes only and zero empirical numbers** until verified
primary sources pass through the `data/` ledger workflow.

```toml
# status: draft
schema_version = "0.1"

[model]
id = "pet-bottles-ch"
title = "Switzerland 1-Year PET Beverage Bottle Collection and Recycling Loop"
region = "CH"
reference_year = "tbd"
period = "1 yr"
steady_state_note = "Steady-state assumed over the 1-year accounting period; stock deltas are not modeled in v0.1."
description = "Goods-level mass-flow boundary for PET beverage bottles in Switzerland across supply, collection, recycling, incineration and littering."

# ---------------------------------------------------------------------------
# Boundary inputs (labels are short names only)
# ---------------------------------------------------------------------------
[inputs.virgin-resin]
label = "Virgin PET input"

# ---------------------------------------------------------------------------
# Processes (goods-level total-mass interval balance)
# ---------------------------------------------------------------------------
[processes.bottle-supply]
label = "Bottle supply"

[processes.market-consumption]
label = "Market consumption"

[processes.sorting-and-recycling]
label = "Sorting and recycling"

# ---------------------------------------------------------------------------
# Boundary outputs
# ---------------------------------------------------------------------------
[outputs.open-loop-rpet]
label = "Open-loop rPET"

[outputs.incineration]
label = "Incineration"

[outputs.littered]
label = "Littered"

# ---------------------------------------------------------------------------
# Directed flows (sorry holes only; replace with `claim` / `share_of` once
# primary sources are recorded in data/sources.toml & data/claims.toml)
# ---------------------------------------------------------------------------
[[flows]]
id = "virgin-to-supply"
from = "virgin-resin"
to = "bottle-supply"
scope = "Non-recycled PET input entering Swiss PET beverage bottle supply."
quantity = { sorry = true, unit = "t", reason = "Primary source not yet in data/claims.toml.", research_question = "What annual mass of non-recycled PET enters Swiss PET beverage bottle supply?" }

[[flows]]
id = "rpet-closed-loop"
from = "sorting-and-recycling"
to = "bottle-supply"
scope = "Bottle-to-bottle recycled PET re-entering Swiss PET beverage bottle supply."
quantity = { sorry = true, unit = "t", reason = "Primary source not yet in data/claims.toml.", research_question = "What annual mass or share of separately collected Swiss PET beverage bottles returns into bottle-to-bottle production?" }

[[flows]]
id = "bottles-to-market"
from = "bottle-supply"
to = "market-consumption"
scope = "PET beverage bottles placed on the Swiss market (record source weight definition in claim scope)."
quantity = { sorry = true, unit = "t", reason = "Primary source not yet in data/claims.toml.", research_question = "What annual mass of PET beverage bottles is placed on the Swiss market, and what weight definition does the primary source use?" }

[[flows]]
id = "bottles-collected"
from = "market-consumption"
to = "sorting-and-recycling"
scope = "PET beverage bottles collected through separate collection."
quantity = { sorry = true, unit = "t", reason = "Primary source not yet in data/claims.toml.", research_question = "What annual mass or collection rate of Swiss PET beverage bottles is separately collected?" }

[[flows]]
id = "bottles-to-incineration"
from = "market-consumption"
to = "incineration"
scope = "Uncollected PET beverage bottles disposed of into municipal incineration."
quantity = { sorry = true, unit = "t", reason = "Primary source not yet in data/claims.toml.", research_question = "What annual mass or share of uncollected Swiss PET beverage bottles enters municipal incineration?" }

[[flows]]
id = "bottles-littered"
from = "market-consumption"
to = "littered"
scope = "PET beverage bottles lost outside collection and municipal disposal."
quantity = { sorry = true, unit = "t", reason = "Primary source not yet in data/claims.toml.", research_question = "What primary estimates exist for the annual mass or share of Swiss PET beverage bottles lost as litter?" }

[[flows]]
id = "rpet-open-loop"
from = "sorting-and-recycling"
to = "open-loop-rpet"
scope = "Recycled PET leaving the beverage bottle loop into non-bottle uses."
quantity = { sorry = true, unit = "t", reason = "Primary source not yet in data/claims.toml.", research_question = "What annual mass or share of recycled Swiss PET beverage bottles exits into open-loop applications?" }

[[flows]]
id = "sorting-rejects-to-incineration"
from = "sorting-and-recycling"
to = "incineration"
scope = "Sorting and reprocessing rejects sent from recycling to incineration."
quantity = { sorry = true, unit = "t", reason = "Primary source not yet in data/claims.toml.", research_question = "What sorting and reprocessing reject mass or loss rate applies to Swiss PET beverage bottle recycling, and where do the rejects go?" }
```

---

## Standalone stoichiometry registry (`models/reactions.toml`, v0.1)

In v0.1, chemical stoichiometry lives strictly outside mass-flow models and
performs **integer atom-count balance verification only** — no atomic-weight
table and no stoichiometry-derived mass flows yet.

Because a chemical formula is itself a sourced fact (atom counting proves a
reaction balances, not that a formula belongs to a named substance), **every
species entry references a statement claim ID in `data/claims.toml`**.

```toml
# status: draft
schema_version = "0.1"

[species.example-reactant]
label = "{{species name}}"
formula = "{{chemical formula grounded by claim}}"
claim = "{{statement-claim-id-in-data-claims-toml}}"

[species.example-product]
label = "{{species name}}"
formula = "{{chemical formula grounded by claim}}"
claim = "{{statement-claim-id-in-data-claims-toml}}"

[reactions.example-reaction]
reactants = { example-reactant = 1 }
products = { example-product = 1 }
```

`earthmania-core` parses each chemical formula into integer element counts and proves
that `sum(reactant_coeff * atoms(species)) == sum(product_coeff * atoms(species))`
for every element. Mass-flow CO2 conversion will be revisited only when an
incineration page needs it and a verified primary source states the factor for
bottle-grade PET.
