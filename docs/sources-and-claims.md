<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Sources and claims ledger

Specification for Earthmania's single provenance ledger in `data/`. Both written
prose in `src/` and quantitative models in `models/` draw from it, so a page and
a model can never disagree about the same number. This is the only document
that describes the ledger's file layout; other documents refer to "the ledger
(`data/`)".

Binding editorial rules: [`EDITORIAL.md`](../EDITORIAL.md). Writing rules:
[`_guidelines.md`](../_guidelines.md).

## Core rules

1. **One ledger for everything.** Every number, date, quote or checkable fact
   used in `src/` or `models/` is one claim in the ledger, and every claim
   belongs to exactly one source.
2. **Never from memory.** Every entry comes from a source opened in the same
   session. Unsourced claims never merge.
3. **Only what the source says.** The ledger records source-stated facts, values
   and uncertainties only. A one-sided value ("> 84") is stored as printed, with
   `bound`, never closed with a number the source did not print. A figure the
   source gives without a year is recorded as `"undated"`, never given a year.
   Author-assumed uncertainties belong on model flows in `models/`, never in
   `data/`.
4. **Verification does not live in the ledger.** No file has a `verified` or
   `status` field. Human verification is recorded in each page's or model's
   status line and pull-request text, and by the fact-checker's `APPROVED` reply
   listing the checked claim IDs.
5. **Honest precision.** Quantitative values are stored as **normalised decimal
   strings** (preserving significant figures, without thousands separators or
   decimal commas); the verbatim formatting as printed lives in `quote`. Ranges
   stay ranges.
6. **Disagreements stay visible.** Never hide conflicting sources in a
   multi-source list on one claim. Record one claim per source value and link
   them, in both directions, with `alternatives`.
7. **IDs are permanent.** Once merged, a source ID or claim ID is never renamed,
   reused or deleted. A wrong claim is retired and, where needed, replaced by a
   new claim with a new ID (see **Retiring a claim**).

---

## Layout

```text
data/
  sources/
    <source-id>.toml    one file per source: the source and every claim taken from it
```

- **One file per primary source.** The file name without `.toml` is the source
  ID; the file holds no separate `id` key, so the two cannot disagree.
- **Contents, in this order:** `schema_version`, one `[source]` table, then zero
  or more `[claims.<claim-id>]` tables. Nothing else.
- **A claim belongs to the source of its file.** Claims have no `source` field.
- **A new edition is a new source.** Next year's statistic or a revised report
  gets its own file; it may name the edition it follows with `supersedes`. The
  older file stays as it is.
- **Claims are never moved between files.** A claim found to belong to a
  different source is retired, and a new claim with a new ID is added to the
  right file.
- **References use IDs, never paths.** Pages, models and other claims refer to
  sources and claims by ID only, so files can later move into subfolders at no
  cost.

## IDs

All IDs are lowercase. This is enforced, not a style choice: mdBook matches a
footnote reference to its definition by exact text, so a case difference
silently breaks the footnote.

**Source ID** (= file name):

- Pattern `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`, at most 32 characters.
- Form `<organisation>-<short-title>-<edition>`; the edition is mandatory. The short title is in the
  source's own language, transliterated to ASCII (`ä`→`ae`, `ö`→`oe`, `ü`→`ue`,
  `ß`→`ss`, other accents dropped), so it matches the document when you open
  it.
- The last part is the edition: the year printed in the title; for a law, the
  year of the consolidated version; otherwise the `published` year. If two
  editions would still get the same ID, the month is added (`-2022-12`).
- Examples: `bafu-getraenkeverpackungen-2024`, `prs-geschaeftsbericht-2024`,
  `fedlex-vgv-2022`.

**Claim ID**:

- Form `<source-id>--<what>`: the file's source ID, a double hyphen, then
  `<what>`. The prefix must equal the file name.
- `<what>` follows the source-ID pattern, at most 32 characters, as
  `<slug>[-<year>][-r<n>]`:
  - `<slug>` says briefly what is measured or stated (`pet-recycled-mass`).
  - `<year>` is required when the claim's `data_year` is a single year, and
    must equal it (`2024`). A claim whose `data_year` is a period, `"undated"`
    or absent has no year suffix, and its `<slug>` may not end in a four-digit
    part (write `iso9001`, not `iso-9001`).
  - `-r<n>` (`n` ≥ 2) marks a replacement that states the same thing as a
    retired claim: it is allowed only when the same ID without it (or with the
    previous `n`) exists in the same file and is retired. No other `<what>` may
    end in a part of the form `r` plus digits (write `r32-refrigerant`, not
    `refrigerant-r32`). A replacement that
    states something different (for example, the year was wrong) gets a fresh
    `<what>` instead. Either way, the retired claim names it in `replaced_by`.
- Examples: `bafu-getraenkeverpackungen-2024--pet-recycled-mass-2024`,
  `prs-geschaeftsbericht-2025--rate-eu-method-2024`,
  `prs-geschaeftsbericht-2025--rate-eu-method-2024-r2`,
  `fedlex-vgv-2022--art8-rate-definition`.

The double hyphen appears only as the separator. The prefix makes a claim ID
unique whenever file names are, shows which file holds it, and keeps two
editions that restate the same year apart.

---

## The `[source]` table

### Three kinds of source

| Kind | Required identifiers | Claims |
|---|---|---|
| Web page, report, dataset or paper | `url`, `archive` (papers also `doi` where one exists) | `match = "auto"` unless no text can be extracted |
| Printed book with an openly available full text | `isbn`, `edition`, `url`, `archive` (of the open text) | as for web sources |
| Printed book with no openly available full text | `isbn`, `edition`; no `url` or `archive` | all `match = "manual"`, quote transcribed by a person from the copy |

An open full text that exists but has no snapshot yet is archived first; it
never makes a book a source without a web copy.

A book with no open full text can be cited for its title, year and contents
through its library catalogue record, which is a web source (first row). Worked
example: `data/sources/loc-lccn-2004000125-2016.toml`, cited in `src/intro.md`.

Whenever a source has `archive`, its licence was seen on a web page:
`licence_seen_at` is that page's URL and `licence_archive` is required.

### Fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `title` | string | yes | Exact title as shown on the source (T in TASL). |
| `author` | string or array of strings | yes | Person or organisation that produced the source (A in TASL). |
| `publisher` | string | no | Publishing organisation if distinct from `author`. |
| `tier` | `"A" \| "B" \| "C" \| "D"` | yes | Source tier per `EDITORIAL.md`. A tier `"D"` source cannot hold a quantitative claim; credit aggregators via `via`. |
| `interest` | string | if `tier = "C"` | Names the commercial, industry or advocacy interest (e.g. `"industry-association"`, `"advocacy-ngo"`). |
| `url` | string | see **Three kinds of source** | Direct URL of the primary source (S in TASL). |
| `archive` | string | see **Three kinds of source** | Wayback Machine snapshot URL with the full 14-digit timestamp (`https://web.archive.org/web/<YYYYMMDDhhmmss>/<url>`), copied from a snapshot that exists, never built by hand. `scripts/source-text` rejects shorter timestamps and fails if Wayback redirects to another capture. |
| `isbn` | string | for printed books | ISBN as printed in the copy consulted. It identifies one edition in one format. |
| `edition` | string | with `isbn` | Edition as printed in the copy consulted (e.g. `"2nd edition"`). |
| `doi` | string | for papers, where one exists | A persistent name, not a copy of the text: it never replaces `archive`. |
| `published` | string | yes | Publication or dataset release date (`"YYYY-MM-DD"` or `"YYYY"`), or `"unknown"`. |
| `accessed` | string | yes | ISO date (`"YYYY-MM-DD"`) when the source was opened. |
| `licence` | string | yes | Licence stated on the source itself (L in TASL), e.g. `"CC-BY-4.0"`, `"CC0-1.0"`, `"public-domain"`, `"all-rights-reserved"`. `"none-stated"` when the source states no licence at all (e.g. a library catalogue record); treated like `"all-rights-reserved"`, so `use = "cite"`. |
| `licence_seen_at` | string | yes | Exact URL where that licence statement was seen (always a URL when the source has `archive`); for a book without `archive`, the place in the copy (e.g. `"copyright page"`). |
| `licence_archive` | string | if the source has `archive` | Wayback snapshot of the `licence_seen_at` page, full 14-digit timestamp, copied from an existing snapshot. Several sources may share one. |
| `use` | `"cite" \| "adapted" \| "copied"` | yes | `"adapted"` and `"copied"` are allowed **only** for `CC0`, `public-domain`, `CC-BY` or `CC-BY-SA`. NC, ND and `all-rights-reserved` sources must use `"cite"`. |
| `via` | string | no | URL (or source ID) of an aggregator or secondary route (e.g. Our World in Data, Wikipedia) used to locate the primary source. |
| `supersedes` | string | no | Source ID of the earlier edition this source follows. Lets the freshness check report claims still cited from the older edition. |
| `notes` | string | no | Brief provenance notes (language, errata). |

A merged `[source]` table may be corrected (for example a new `archive` after a
snapshot disappears); every claim in its file is then re-checked. A different
document is always a new source.

---

## Claim tables `[claims.<claim-id>]`

One table per checkable number or statement taken from the file's source.

### Fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `basis` | `"quoted" \| "estimate"` | yes | How the claim is grounded. `"derived"` is deferred until prose needs it (model-level `share_of` and `residual` are computed in `models/`). `"unsourced"` never merges. |
| `kind` | `"quantity" \| "statement"` | yes | `"quantity"` for numeric claims (usable by both `src/` and `models/`); `"statement"` for qualitative claims (prose and reaction species definitions). |
| `value` | string | if `kind = "quantity"` and no `range` | **Normalised decimal string** (ASCII digits, optional `.` decimal point, optional leading `-`, no thousands separators or decimal commas), preserving the source's significant figures. The verbatim printed form lives in `quote`. |
| `printed` | string, or `[string, string]` with `range` | if `kind = "quantity"` and the claim has a `quote` | The number exactly as it stands in `quote`, nothing else: `"40’792"`, `"1,3"`, `"84"` (not `"> 84"`). Allowed characters: ASCII digits `0`–`9`, at most one leading sign (`-`, `−`, `+`), and otherwise only the declared `decimal_mark` (at most once) and the declared `group_mark`. Every other character after the sign — including every `.` or `,` — must be one of the two declared marks. For a `range`, one string per end. |
| `decimal_mark` | `"." \| ","` | when `printed` has a decimal mark | Which character is the decimal mark in `printed`. Declared by the person who reads the source, never guessed. |
| `group_mark` | `"'" \| "’" \| " " \| "." \| ","` | when `printed` has a grouping mark | The thousands-grouping character in `printed`; never the same as `decimal_mark`. |
| `bound` | `"lower" \| "upper"` | see rule | Set when the source prints **this claim's own value** as a one-sided limit ("> 84 Prozent" for the rate itself). Only with `value`; never with `range` or `uncertainty`. A limit that is part of what the claim states — a legal minimum, a target — is a point value without `bound` ("mindestens 75 Prozent" as the legal minimum is the value 75). The limit is visible in `quote`; a person sets `bound` and the fact-checker confirms it. No check reads words, in any language. The other end is never stored: the model tool closes it by rule (`docs/model-schema.md`, principle 6). `>` and `≥` are not distinguished, because published limits are usually rounded. |
| `range` | `[string, string]` | if source gives a range (or `basis = "estimate"` without `value`) | Lower and upper bounds as normalised decimal strings (`["lo", "hi"]`). |
| `unit` | string | if `kind = "quantity"` | Unit as measured. Model-usable v0.1 mass-per-period and ratio units: `"kg"`, `"t"`, `"kt"`, `"%"`, `"1"`. Descriptive units are allowed for prose-only quantities. |
| `uncertainty` | inline table | no | **Source-stated** uncertainty only (`{ rel = "<decimal>" }`, `{ abs = "<decimal>" }`, or `{ range = ["lo", "hi"] }`). Never put author-assumed uncertainty in the ledger; when the source states no uncertainty, omit this field. |
| `region` | string | if `kind = "quantity"` (optional for `"statement"`) | Geographic scope (`"CH"`, `"EU-27"`, `"global"`, etc.). |
| `data_year` | string | if `kind = "quantity"` (optional for `"statement"`) | Calendar year or period the quantity describes (`"YYYY"` or `"YYYY-YYYY"`), or `"undated"` when the source gives the figure without a year (e.g. "every year about …"). An `"undated"` claim says so in `scope`, may be cited in prose without implying a year, and may not be used by a model. |
| `scope` | string | yes | Exact definition of what is measured or stated. |
| `locator` | string | yes | Exact location in the source: page number, section heading, table or figure identifier. |
| `quote` | string | if `basis = "quoted"` | Exact short span copied unchanged from the output of `scripts/source-text` (see **Quote text** below), **maximum 300 characters**. For a claim with `match = "manual"`, the text a person transcribed from the source (for a chart, the label and value as printed on it). Kept strictly for verification (covered by the `LICENSE` Section 3 exception); never copied into prose from NC, ND or all-rights-reserved sources. |
| `match` | `"auto" \| "manual"` | no (defaults to `"auto"`) | `"auto"` means the quote-match check verifies `quote` against the archived source text. Use `"manual"` only when no usable text can be extracted (paywall, scan, chart-only, printed book). |
| `match_reason` | string | if `match = "manual"` | Concrete reason automatic quote matching cannot run; listed by lint for human review. |
| `by` | string | if `basis = "estimate"` | Who produced the estimate (source ID or explicit attribution). |
| `note` | string | if `basis = "estimate"` | Basis and caveats of the estimate. |
| `alternatives` | array of strings | no | Claim IDs from other sources (or another place in the same source) that give a different value for the same quantity. Listed in **both** directions: if A lists B, B lists A. |
| `disagreement_note` | string | if `alternatives` is non-empty | Brief explanation of why the values differ (scope, year, method, definition). |
| `retired` | string | no | Reason the claim must no longer be cited. See **Retiring a claim**. |
| `replaced_by` | string | only with `retired` | Claim ID of the claim that replaces it. |

### Retiring a claim

A merged claim is never renamed, moved or deleted, and its **frozen fields**
never change in place: `basis`, `kind`, `value`, `range`, `printed`,
`decimal_mark`, `group_mark`, `bound`, `unit`, `uncertainty`, `region`,
`data_year`, `scope`, `quote`, `by`, `note`. Only
`locator`, `match`, `match_reason`, `alternatives`, `disagreement_note`,
`retired` and `replaced_by` may be edited.

When a claim turns out to be wrong, or to belong to another source, it gets
`retired = "<reason>"` (and `replaced_by` when a new claim takes its place) and
stays in its file, so its ID is never reused. Pages and models may not cite a
retired claim. Retired claims are skipped by the quote-match and printed-number
checks.

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
`WebFetch`. When a number comes from a PDF table, check its row on the rendered
page before proposing the claim: the extracted text can run neighbouring rows
together (`docs/oddities.md`, 2026-11-27).

---

## Template: `data/sources/<source-id>.toml`

```toml
schema_version = "0.1"

[source]
title = "{{title as shown on the source}}"
author = "{{person or organisation}}"
publisher = "{{publisher, if different}}"
tier = "B" # "A" | "B" | "C" | "D"
# interest = "{{required if tier = 'C'}}"
url = "https://example.org/{{primary-source-path}}"          # not for a book without open text
archive = "https://web.archive.org/web/{{14-digit timestamp}}/https://example.org/{{primary-source-path}}"
# isbn = "{{as printed}}"       # printed books
# edition = "{{as printed}}"    # with isbn
# doi = "{{doi}}"               # papers, in addition to archive
published = "{{YYYY-MM-DD or YYYY or unknown}}"
accessed = "{{YYYY-MM-DD}}"
licence = "{{exact licence as seen on the source}}"
licence_seen_at = "https://example.org/{{page-stating-licence}}"
licence_archive = "https://web.archive.org/web/{{14-digit timestamp}}/https://example.org/{{page-stating-licence}}"
use = "cite" # "cite" | "adapted" | "copied"
# via = "https://ourworldindata.org/{{optional-route}}"
# supersedes = "{{source-id of the previous edition}}"

# Quoted quantitative claim
[claims.example-source-2024--what-is-measured-2024]
basis = "quoted"
kind = "quantity"
value = "{{normalised decimal string, e.g. 12300 or 4.5}}"
printed = "{{the number exactly as in the quote, e.g. 12’300 or 4,5}}"
# decimal_mark = "," # if printed contains . or ,
# group_mark = "’"   # if printed contains digit grouping
# bound = "lower" # only if the source prints this value as a one-sided limit ("> 84")
unit = "{{kg | t | kt | % | 1}}"
# uncertainty = { rel = "{{source-stated fraction}}" } # only if stated by source
region = "{{region}}"
data_year = "2024" # or "undated"
scope = "{{exact physical definition of what is measured}}"
locator = "{{page, section, table or chart}}"
quote = "{{exact span from scripts/source-text output, max 300 characters}}"
match = "auto" # or "manual" with match_reason = "..."

# Quoted qualitative statement (prose and species formulas; region/data_year optional)
[claims.example-source-2024--what-is-stated]
basis = "quoted"
kind = "statement"
scope = "{{what the statement applies to}}"
locator = "{{page or section}}"
quote = "{{exact span from scripts/source-text output, max 300 characters}}"

# Estimate claim (always carries attribution; a range, or a value if the source gives one)
[claims.example-source-2024--what-is-estimated-2024]
basis = "estimate"
kind = "quantity"
range = ["{{lo}}", "{{hi}}"]
unit = "{{unit}}"
region = "{{region}}"
data_year = "2024"
scope = "{{exact scope}}"
locator = "{{page or section}}"
by = "{{who made the estimate}}"
note = "{{method and caveats}}"
```

---

## Using claims in prose and models

- **In `src/` prose:** cite a claim with `[^c-<claim-id>]` per `_guidelines.md`. Every sentence containing a digit carries a claim footnote, and every paragraph carries at least one (`src/intro.md` is exempt from the paragraph rule). Footnote definitions are hand-written under `## Sources`.
- **In `models/`:** flows hold no sourced literals — they reference `claim = "<claim-id>"` (or `share_of` + `claim`). Generated Markdown table fragments exported by `earthmania export` emit footnote **references** (`[^c-<claim-id>]`) only; the footnote definitions stay hand-written under `## Sources` on the host page.

## Who checks what

- **Deterministic checks (scripts / `earthmania`):**
  - **Layout:** every file in `data/sources/` has a valid source-ID name and holds only `schema_version`, one `[source]` and `[claims.*]` tables.
  - **IDs:** source and claim IDs follow the patterns and length limits under **IDs**; every claim ID's prefix equals its file name; a single-year `data_year` appears as the year suffix and no other `<slug>` ends in a four-digit part; `-r<n>` only follows a retired claim of the same ID.
  - **Schema:** required fields and the three kinds of source; valid tiers; no quantity claim in the file of a tier D source; `interest` on tier C; `licence_seen_at` a URL and `licence_archive` present whenever `archive` is; `use` compatible with `licence`; 14-digit timestamps; `quote` ≤ 300 characters; normalised decimal syntax for `value`/`range`; `bound` only with `value` and never with `uncertainty`; `replaced_by` only with `retired`; `match = "manual"` on every claim of a source without `archive`; no model uses an `"undated"` claim.
  - **References:** claim IDs are unique across all files (a TOML parser only catches duplicates within one file); every `[^c-<id>]` and model `claim` exists and is not retired; every `alternatives` ID exists and lists the claim back; `replaced_by`, `supersedes` and source-ID `via`/`by` values exist.
  - **Permanence (diff against `main`):** no merged claim or source file is deleted or renamed, and no frozen field of a merged claim changes.
  - **Quote match, per changed file:** when a file changes, every claim in it that has `match = "auto"` and is not retired is re-checked, because a changed `[source]` changes what all its claims are matched against. The check runs `scripts/source-text` on the source's `archive` URL, applies the same normalisation to the ledger quote, and looks for it as a substring. Exit `1` from the script fails the claim; exit `3` (network) is inconclusive, never a pass. `match = "manual"` claims are listed for a person.
  - **Printed number** (every live claim with `printed`). Character rules only; no words and no language are read, and nothing is guessed:
    "Digit" means an ASCII digit `0`–`9` only (a superscript footnote mark is not a digit).
    1. **Characters:** `printed` uses only the allowed characters for its declared marks. Otherwise: fail.
    2. **Whole number:** `printed` occurs in the normalised `quote`, and at each occurrence:
       - the character directly before or after it is not a digit (otherwise that occurrence does not count);
       - a mark directly before or after it (`'`, `’`, `.`, `,` or the declared `group_mark`) counts as continuing the number only when a digit is on its far side; then that occurrence does not count. So `40` cannot stand for `40’792` and `1` cannot stand for `1,3`, while `84.` at the end of a sentence is fine;
       - a space directly before or after it with a digit on its far side makes the occurrence **ambiguous** (space-grouped numbers and neighbouring numbers look alike once spaces are normalised);
       - a sign directly before it (`-`, `−`, `+`), not itself preceded by a digit, must be part of `printed` (otherwise: fail); an en dash `–` in that place makes the occurrence **ambiguous** (minus or dash).

       No counting occurrence: fail.
    3. **Value:** converting `printed` (remove `+` and every `group_mark`, turn `−` into `-`, turn `decimal_mark` into `.`) gives exactly `value` (or each `range` end), character for character, so significant figures and the sign are compared too. Otherwise: fail.
    4. **Ambiguous occurrence:** if `printed` has more than one counting occurrence, or its only one is ambiguous, the check reports **"ambiguous occurrence"**. CI still passes, but the pull request lists the claim, and the fact-checker settles it against `locator`.

    Whether a mark is a decimal or a grouping mark (`34.188` is 34188 in German use) is declared, not checked: the fact-checker confirms `decimal_mark`, `group_mark` and `bound` against the source.
  - **Changed or retired claims:** a pull request that edits or retires a merged claim lists every page and model citing it, because those were verified against the old content.
  - Licence lint and wording-overlap checks against NC/ND/all-rights-reserved sources.
- **Fact-checker (fresh, read-only session):**
  - Checks overstatement, precision, scope, year, vague quantifiers, licence on the actual page, and primary-source rule. Replies `APPROVED` with checked claim IDs (plus an `INCONCLUSIVE:` line for any it could not check because the network failed), or `FIX` with at most five findings.
- **Owner:**
  - Opens each source, verifies each claim personally (for printed books, against the copy), writes the prose, updates the page's or model's status line, and merges.
