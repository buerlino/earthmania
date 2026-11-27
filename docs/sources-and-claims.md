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
3. **Only what the source says.** The ledger records source-stated facts, values
   and uncertainties only. Author-assumed uncertainties belong on model flows in
   `models/`, never in `data/`.
4. **Verification does not live in the ledger.** Neither file has a `verified`
   or `status` field. Human verification is recorded in each page's or model's
   status line and pull-request text, and by the fact-checker's `APPROVED` reply
   listing the checked claim IDs.
5. **Honest precision.** Quantitative values are stored as **normalised decimal
   strings** (preserving significant figures, without thousands separators or
   decimal commas); the verbatim formatting as printed lives in `quote`. Ranges
   stay ranges.
6. **Disagreements stay visible.** Never hide conflicting sources in a
   multi-source list on one claim. Record one claim per source value and link
   them with `alternatives`.

---

## `data/sources.toml`

One table per primary source: `[sources.<source-id>]`. Source IDs are lowercase,
hyphenated slugs (for example `example-agency-report`).

### Fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `title` | string | yes | Exact title as shown on the source page (T in TASL). |
| `author` | string or array of strings | yes | Person or organisation that produced the source (A in TASL). |
| `publisher` | string | no | Publishing organisation if distinct from `author`. |
| `tier` | `"A" \| "B" \| "C" \| "D"` | yes | Source tier per `EDITORIAL.md`. Tier `"D"` cannot be the `source` of a quantitative claim; credit aggregators via `via`. |
| `interest` | string | if `tier = "C"` | Names the commercial, industry or advocacy interest (e.g. `"industry-association"`, `"advocacy-ngo"`). |
| `url` | string | yes | Direct URL of the primary source (S in TASL). |
| `archive` | string | yes | Wayback Machine snapshot URL with the full 14-digit timestamp (`https://web.archive.org/web/<YYYYMMDDhhmmss>/<url>`), copied from a snapshot that exists, never built by hand. Required on every source per `EDITORIAL.md`. `scripts/source-text` rejects shorter timestamps and fails if Wayback redirects to another capture. |
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

[sources.example-source-id]
title = "{{title as shown on the page}}"
author = "{{person or organisation}}"
publisher = "{{publisher, if different}}"
tier = "B" # "A" | "B" | "C" | "D"
# interest = "{{required if tier = 'C'}}"
url = "https://example.org/{{primary-source-path}}"
archive = "https://web.archive.org/web/{{14-digit timestamp}}/https://example.org/{{primary-source-path}}"
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
are lowercase, hyphenated slugs (for example `example-claim-id`).

### Fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `basis` | `"quoted" \| "estimate"` | yes | How the claim is grounded. `"derived"` is deferred until prose needs it (model-level `share_of` and `residual` are computed in `models/`). `"unsourced"` never merges. |
| `kind` | `"quantity" \| "statement"` | yes | `"quantity"` for numeric claims (usable by both `src/` and `models/`); `"statement"` for qualitative claims (prose and reaction species definitions). |
| `value` | string | if `kind = "quantity"` and no `range` | **Normalised decimal string** (ASCII digits, optional `.` decimal point, optional leading `-`, no thousands separators or decimal commas), preserving the source's significant figures. The verbatim printed form lives in `quote`. |
| `range` | `[string, string]` | if source gives a range (or `basis = "estimate"` without `value`) | Lower and upper bounds as normalised decimal strings (`["lo", "hi"]`). |
| `unit` | string | if `kind = "quantity"` | Unit as measured. Model-usable v0.1 mass-per-period and ratio units: `"kg"`, `"t"`, `"kt"`, `"%"`, `"1"`. Descriptive units are allowed for prose-only quantities. |
| `uncertainty` | inline table | no | **Source-stated** uncertainty only (`{ rel = "<decimal>" }`, `{ abs = "<decimal>" }`, or `{ range = ["lo", "hi"] }`). Never put author-assumed uncertainty in the ledger; when the source states no uncertainty, omit this field. |
| `region` | string | if `kind = "quantity"` (optional for `"statement"`) | Geographic scope (`"CH"`, `"EU-27"`, `"global"`, etc.). |
| `data_year` | string | if `kind = "quantity"` (optional for `"statement"`) | Calendar year or period the quantity describes (`"YYYY"` or `"YYYY-YYYY"`). |
| `scope` | string | yes | Exact definition of what is measured or stated. |
| `source` | string | yes | Key in `data/sources.toml`. Exactly one source per claim. |
| `locator` | string | yes | Exact location in the source: page number, section heading, table or figure identifier. |
| `quote` | string | if `basis = "quoted"` | Exact short span copied unchanged from the output of `scripts/source-text` (see **Quote text** below), **maximum 300 characters**. Kept strictly for verification (covered by the `LICENSE` Section 3 exception); never copied into prose from NC, ND or all-rights-reserved sources. |
| `match` | `"auto" \| "manual"` | no (defaults to `"auto"`) | `"auto"` means the quote-match check verifies `quote` against the archived source text. Use `"manual"` only when no usable text can be extracted (paywall, scan, chart-only). |
| `match_reason` | string | if `match = "manual"` | Concrete reason automatic quote matching cannot run; listed by lint for human review. |
| `by` | string | if `basis = "estimate"` | Who produced the estimate (source ID or explicit attribution). |
| `note` | string | if `basis = "estimate"` | Basis and caveats of the estimate. |
| `alternatives` | array of strings | no | Claim IDs in `data/claims.toml` from other good sources that give a different value for the same quantity. |
| `disagreement_note` | string | if `alternatives` is non-empty | Brief explanation of why the sources differ (scope, year, method). |

### Quote text

A `quote` is compared against what `scripts/source-text` prints, so both sides
use one normalisation, defined in that script (`normalise_text`):

- Unicode NFC. Not NFKC, which would turn `m²` into `m2`.
- No-break and typographic spaces become a plain space; soft hyphens and
  zero-width characters are removed.
- Runs of spaces and tabs collapse to one space; lines are trimmed and blank
  lines dropped.
- When matching, a line break counts as one space, so a quote that runs across
  a line break in the extracted text is written with a single space there.
- Everything else is kept as printed, including the source's digit grouping,
  decimal comma and typographic apostrophes.

Copy a quote from the script's output, never from a browser, a PDF viewer or
`WebFetch`.

### Templates

```toml
schema_version = "0.1"

# Quoted quantitative claim
[claims.example-quoted-quantity]
basis = "quoted"
kind = "quantity"
value = "{{normalised decimal string, e.g. 12300 or 4.5}}"
unit = "{{kg | t | kt | % | 1}}"
# uncertainty = { rel = "{{source-stated fraction}}" } # only if stated by source
region = "{{region}}"
data_year = "{{YYYY}}"
scope = "{{exact physical definition of what is measured}}"
source = "example-source-id"
locator = "{{page, section, table or chart}}"
quote = "{{exact span from scripts/source-text output, max 300 characters}}"
match = "auto" # or "manual" with match_reason = "..."

# Quoted qualitative statement (prose and species formulas; region/data_year optional)
[claims.example-quoted-statement]
basis = "quoted"
kind = "statement"
scope = "{{what the statement applies to}}"
source = "example-source-id"
locator = "{{page or section}}"
quote = "{{exact span from scripts/source-text output, max 300 characters}}"

# Estimate claim (always carries a range and attribution)
[claims.example-estimate]
basis = "estimate"
kind = "quantity"
range = ["{{lo}}", "{{hi}}"]
unit = "{{unit}}"
region = "{{region}}"
data_year = "{{YYYY}}"
scope = "{{exact scope}}"
source = "example-source-id"
locator = "{{page or section}}"
by = "{{who made the estimate}}"
note = "{{method and caveats}}"
```

---

## Using claims in prose and models

- **In `src/` prose:** cite a claim with `[^c-<claim-id>]` per `_guidelines.md`. Every sentence containing a digit carries a claim footnote, and every paragraph carries at least one. Footnote definitions are hand-written under `## Sources`.
- **In `models/`:** flows hold no sourced literals — they reference `claim = "<claim-id>"` (or `share_of` + `claim`). Generated Markdown table fragments exported by `earthmania export` emit footnote **references** (`[^c-<claim-id>]`) only; the footnote definitions stay hand-written under `## Sources` on the host page.

## Who checks what

- **Deterministic checks (scripts / `earthmania`):**
  - Schema completeness (required fields, valid tiers, `interest` on Tier C, `licence_seen_at`, `use` compatible with `licence`, `archive` has a 14-digit timestamp, `quote` ≤ 300 characters, normalised decimal syntax for `value`/`range`).
  - Referential integrity (every `source` exists in `data/sources.toml`; every `[^c-<id>]` and model `claim` exists in `data/claims.toml`; every `alternatives` ID exists).
  - Quote match against archived text (for changed claims where `match = "auto"`; `match = "manual"` entries are listed explicitly). The check runs `scripts/source-text` on the source's `archive` URL, applies the same normalisation to the ledger quote, and looks for it as a substring. Exit `1` from the script fails the claim; exit `3` (network) is inconclusive, never a pass.
  - Licence lint and wording-overlap checks against NC/ND/all-rights-reserved sources.
- **Fact-checker (fresh, read-only session):**
  - Checks overstatement, precision, scope, year, vague quantifiers, licence on the actual page, and primary-source rule. Replies `APPROVED` with checked claim IDs (plus an `INCONCLUSIVE:` line for any it could not check because the network failed), or `FIX` with at most five findings.
- **Owner:**
  - Opens each source, verifies each claim personally, writes the prose, updates the page's or model's status line, and merges.
