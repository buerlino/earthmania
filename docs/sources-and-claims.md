<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Sources and claims ledger

Specification for Earthmania's single provenance ledger: `data/sources.toml` and
`data/claims.toml`. Both written prose in `src/` and quantitative models in
`models/` draw from these two files so a page and a model can never disagree
about the same number.

Binding editorial rules: [`EDITORIAL.md`](../EDITORIAL.md). Writing rules:
[`_guidelines.md`](../_guidelines.md).

## Core rules

1. **One ledger for everything.** Every number, date, quote or checkable fact
   used in `src/` or `models/` has one entry in `data/claims.toml` pointing to
   one entry in `data/sources.toml`.
2. **Never from memory.** Every entry comes from a source opened in the same
   session. Unsourced claims never merge.
3. **Verification does not live in the ledger.** Neither file has a `verified`
   or `status` field. Human verification is recorded in each page's status line
   and pull-request text, and by the fact-checker's `APPROVED` reply listing the
   checked claim IDs.
4. **Honest precision.** Quantitative values are stored as **strings exactly as
   printed** by the source so significant figures are never altered by floating-point
   formatting. Ranges stay ranges.
5. **Disagreements stay visible.** Never hide conflicting sources in a multi-source
   list on one claim. Record one claim per source value and link them with
   `alternatives`.

---

## `data/sources.toml`

One table per primary source: `[sources.<source-id>]`. Source IDs are lowercase,
hyphenated slugs (for example `bafu-abfallstatistik-2023`).

### Fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `title` | string | yes | Exact title as shown on the source page (T in TASL). |
| `author` | string or array of strings | yes | Person or organisation that produced the source (A in TASL). |
| `publisher` | string | no | Publishing organisation if distinct from `author`. |
| `tier` | `"A" \| "B" \| "C" \| "D"` | yes | Source tier per `EDITORIAL.md`. Tier `"D"` cannot be the `source` of a quantitative claim; credit aggregators via `via`. |
| `interest` | string | if `tier = "C"` | Names the commercial, industry or advocacy interest (e.g. `"industry-association"`, `"advocacy-ngo"`). |
| `url` | string | yes | Direct URL of the primary source (S in TASL). |
| `archive` | string | yes | Wayback Machine snapshot URL (`https://web.archive.org/web/...`), or `"none"` when archiving is impossible (requires `archive_note`). |
| `archive_note` | string | if `archive = "none"` | Reason no usable archive snapshot exists (e.g. paywall, dynamic portal). |
| `published` | string | yes | Publication or dataset release date (`"YYYY-MM-DD"` or `"YYYY"`), or `"unknown"`. |
| `accessed` | string | yes | ISO date (`"YYYY-MM-DD"`) when the source was opened. |
| `licence` | string | yes | Licence stated on the source's own page (L in TASL), e.g. `"CC-BY-4.0"`, `"CC0-1.0"`, `"public-domain"`, `"all-rights-reserved"`. |
| `licence_seen_at` | string | yes | Exact URL where that licence statement was seen. |
| `use` | `"cite" \| "adapted" \| "copied"` | yes | `"adapted"` and `"copied"` are allowed **only** for `CC0`, `public-domain`, `CC-BY` or `CC-BY-SA`. NC, ND and `all-rights-reserved` sources must use `"cite"`. |
| `via` | string | no | URL (or source ID) of an aggregator or secondary route (e.g. Our World in Data, Wikipedia) used to locate the primary source. |
| `notes` | string | no | Brief provenance notes (edition, language, errata). |

### Template

```toml
schema_version = "0.1"

[sources.example-primary-source]
title = "{{title as shown on the page}}"
author = "{{person or organisation}}"
publisher = "{{publisher, if different}}"
tier = "B" # "A" | "B" | "C" | "D"
# interest = "{{required if tier = 'C'}}"
url = "https://example.org/{{primary-source-path}}"
archive = "https://web.archive.org/web/{{timestamp}}/https://example.org/{{primary-source-path}}"
published = "{{YYYY-MM-DD or YYYY or unknown}}"
accessed = "{{YYYY-MM-DD}}"
licence = "{{exact licence as seen on the source page}}"
licence_seen_at = "https://example.org/{{page-stating-licence}}"
use = "cite" # "cite" | "adapted" | "copied"
# via = "https://ourworldindata.org/{{optional-route}}"
```

---

## `data/claims.toml`

One table per checkable number or statement: `[claims.<claim-id>]`. Claim IDs
are lowercase, hyphenated slugs (for example `pet-collection-rate-ch-2023`).

### Fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `basis` | `"quoted" \| "estimate"` | yes | How the claim is grounded. `"derived"` is deferred until prose needs it (model-level `share_of` and `residual` are computed in `models/`). `"unsourced"` never merges. |
| `kind` | `"quantity" \| "statement"` | yes | `"quantity"` for numeric claims (usable by both `src/` and `models/`); `"statement"` for qualitative claims (prose only). |
| `value` | string | if `kind = "quantity"` and no `range` | Number **as printed** in the source (string, preserving significant figures). |
| `range` | `[string, string]` | if source gives a range (or `basis = "estimate"` without `value`) | Lower and upper bounds as printed (`["lo", "hi"]`). |
| `unit` | string | if `kind = "quantity"` | Unit as measured. Model-usable mass/rate units in v0.1: `"kg"`, `"t"`, `"kt"`, `"kg/yr"`, `"t/yr"`, `"kt/yr"`, `"%"`, `"1"`. |
| `uncertainty` | inline table | no (required if adding bounds beyond printed `range`) | See **Uncertainty** below. Every uncertainty declares whether it came from the source or is an author assumption. |
| `region` | string | yes | Geographic scope (`"CH"`, `"EU-27"`, `"global"`, etc.). |
| `data_year` | string | yes | Calendar year or period the claim describes (`"YYYY"` or `"YYYY-YYYY"`). |
| `scope` | string | yes | Exact definition of what is measured (e.g. beverage bottles only vs. all PET packaging; net polymer vs. gross bales with caps and moisture). |
| `source` | string | yes | Key in `data/sources.toml`. Exactly one source per claim. |
| `locator` | string | yes | Exact location in the source: page number, section heading, table or figure identifier. |
| `quote` | string | if `basis = "quoted"` | Exact short verbatim span from the source, **maximum 300 characters**. Kept strictly for verification (covered by the `LICENSE` Section 3 exception); never copied into prose from NC, ND or all-rights-reserved sources. |
| `match` | `"auto" \| "manual"` | no (defaults to `"auto"`) | `"auto"` means the quote-match check verifies `quote` against the archived source text. Use `"manual"` only when no extractable text exists (paywall, scan, chart-only). |
| `match_reason` | string | if `match = "manual"` | Concrete reason automatic quote matching cannot run; listed by lint for human review. |
| `by` | string | if `basis = "estimate"` | Who produced the estimate (source ID or explicit attribution). |
| `note` | string | if `basis = "estimate"` | Basis and caveats of the estimate. |
| `alternatives` | array of strings | no | Claim IDs in `data/claims.toml` from other good sources that give a different value for the same quantity. |
| `disagreement_note` | string | if `alternatives` is non-empty | Brief explanation of why the sources differ (scope, year, method). |

### Uncertainty table (`uncertainty`)

When a quantity carries an explicit uncertainty beyond a printed `range`:

```toml
uncertainty = { basis = "source", rel = "{{fraction, e.g. 0.05}}" }
# or:
uncertainty = { basis = "source", abs = "{{absolute half-width in claim unit}}" }
# or:
uncertainty = { basis = "author_assumption", range = ["{{lo}}", "{{hi}}"], note = "{{why this interval is assumed}}" }
```

- `basis` is required: `"source"` (stated by the cited source) or `"author_assumption"` (requires `note`).
- Exactly one bound form is set: `range = [lo, hi]`, `abs`, or `rel`.
- When neither `range` nor `uncertainty` is present on a `quoted` quantity, models treat it as a point interval `[value, value]`.

### Templates

```toml
schema_version = "0.1"

# Quoted quantitative claim
[claims.example-quoted-quantity]
basis = "quoted"
kind = "quantity"
value = "{{printed number}}"
unit = "{{t/yr | kt/yr | kg/yr | t | kt | kg | % | 1}}"
region = "{{CH | EU-27 | global}}"
data_year = "{{YYYY}}"
scope = "{{exact physical definition of what is measured}}"
source = "example-primary-source"
locator = "{{page, section, table or chart}}"
quote = "{{exact verbatim span, max 300 characters}}"
match = "auto" # or "manual" with match_reason = "..."

# Quoted qualitative statement (prose only)
[claims.example-quoted-statement]
basis = "quoted"
kind = "statement"
region = "{{region}}"
data_year = "{{YYYY}}"
scope = "{{what the statement applies to}}"
source = "example-primary-source"
locator = "{{page or section}}"
quote = "{{exact verbatim span, max 300 characters}}"

# Estimate claim (always carries a range and attribution)
[claims.example-estimate]
basis = "estimate"
kind = "quantity"
range = ["{{lo}}", "{{hi}}"]
unit = "{{unit}}"
region = "{{region}}"
data_year = "{{YYYY}}"
scope = "{{exact scope}}"
source = "example-primary-source"
locator = "{{page or section}}"
by = "{{who made the estimate}}"
note = "{{method and caveats}}"
```

---

## Using claims in prose and models

- **In `src/` prose:** cite a claim with `[^c-<claim-id>]` per `_guidelines.md`. Every sentence containing a digit carries a claim footnote, and every paragraph carries at least one.
- **In `models/`:** flows hold no sourced numbers — they reference `claim = "<claim-id>"` (or `share_of` + `claim`). Generated Markdown fragments exported by `w4 export` emit the same `[^c-<claim-id>]` footnotes so prose rules apply uniformly.

## Who checks what

- **Deterministic checks (scripts / `w4`):**
  - Schema completeness (required fields, valid tiers, `interest` on Tier C, `licence_seen_at`, `use` compatible with `licence`, `quote` ≤ 300 characters).
  - Referential integrity (every `source` exists in `data/sources.toml`; every `[^c-<id>]` and model `claim` exists in `data/claims.toml`; every `alternatives` ID exists).
  - Quote match against archived text (for changed claims where `match = "auto"`; `match = "manual"` entries are listed explicitly).
  - Licence lint and wording-overlap checks against NC/ND/all-rights-reserved sources.
- **Fact-checker (fresh, read-only session):**
  - Checks overstatement, precision, scope, year, vague quantifiers, licence on the actual page, and primary-source rule. Replies `APPROVED` with checked claim IDs, or `FIX` with at most five findings.
- **Owner:**
  - Opens each source, verifies each claim personally, writes the prose, updates the page's status line, and merges.
