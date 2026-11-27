# Earthmania Editorial Policy

The project's working agreement: what Earthmania is for, how content is produced,
and the rules every page must meet. Decisions are dated; change them deliberately,
never silently. How to write a page: `_guidelines.md`. Rules for AI sessions: `CLAUDE.md`.

## Main goal

**Build a small, solid, trustworthy knowledge base — not a big one fast.**

Earthmania is a connected map of how materials, industrial processes and systems
actually work: what things physically are, what they transform into, which systems
they touch, and where the real technical bottlenecks sit. Accuracy and trust come
before coverage and speed. Five excellent, fully verified pages are worth more than
a hundred plausible drafts. We are not trying to map everything with AI quickly.

Earthmania is part of a wider ecosystem of open knowledge, not a competitor to it.
Where others do something well (e.g. Our World in Data for data and charts),
we link to them and build on them.

## Principles

1. **Verified or not published.** Only content a human has verified against its
   sources appears on earthmania.org.
2. **Every claim is traceable** to a source that someone opened and recorded in the ledger.
3. **Every number carries context:** region, year, definition, source.
4. **Honest about uncertainty.** Contested figures are shown as ranges with an
   explanation of why sources differ. Unknowns are stated.
5. **Plain and simple.** Stock mdBook and plain Markdown: no custom theme, plugins
   or scripts. The one exception is embedded Our World in Data charts.

## Page status

Every page has exactly one status, recorded in its first line
(`<!-- status: … -->`, see `_guidelines.md`):

| Status | Meaning | On the site? |
|---|---|---|
| `draft` | Work in progress | No (not in `SUMMARY.md`) |
| `stub` | A short definition with no numbers, verified | Yes, marked as a stub |
| `verified` | Every claim checked by a human against its source | Yes |

A page may be published section by section: unverified sections are left out of
the page until verified.

## Decisions (2026-11-26)

| Topic | Decision |
|---|---|
| Roles | **The owner writes every page.** AI is a research assistant and fact-checker only: a research agent proposes ledger entries (never prose); a fresh, read-only fact-checker session advises on each pull request. AI never supplies facts, numbers or citations from memory, and no agent runs unattended. (Extended on 2026-11-27: AI also writes code and model files; see below.) |
| Verification | **A human checks every claim** against its source before content becomes `verified`. Recorded in the page's status line (date, by whom, PR number) and in the pull request text; not in the ledger. |
| What a claim is | **Every sentence containing a digit (years included) carries a claim footnote** in that sentence, and **every paragraph of prose carries at least one footnote**. Names containing digits (CO2, PM2.5, nylon 6,6, standard numbers) are on an allowlist. Vague quantifiers ("most", "rarely") are checked by the fact-checker. |
| Provenance | **Sources registry + claims ledger.** `data/sources.toml` lists each source once; `data/claims.toml` lists each claim with its source, location and supporting quote. Neither appears on the site. |
| Footnotes | **Hand-written** `[^c-<claim-id>]`, checked by a script against the ledger. No preprocessor. |
| Quote source text | **Fetched from the Wayback snapshot at check time** (PDFs via pdftotext). No source text stored in the repo. Where no usable snapshot exists (paywall, scan), the claim is marked `match: manual` with a reason and listed by the lint. |
| Quoting in pages | **None from NC, ND or all-rights-reserved sources:** restate their facts in our own words with a citation. Exact quotes live only in the ledger, kept short. |
| Page structure | **Free-form connected nodes** (replaces the fixed template). Loose flow: physical reality → transformations & flows → impacts & bottlenecks → sources & attribution. Folders: `materials/`, `processes/`, `impacts/`, `systems/`. See `_guidelines.md`. |
| Framing | **Mechanics and bottlenecks, no preaching.** No "X is bad, use Y", no alternatives tables, no advice lists. |
| Stub pages | **Verified mini-stubs.** A short definition with no numbers, verified like any page, may be published as a `stub`. Links to unpublished pages are not links; they are marked as planned (see `_guidelines.md`). |
| Interested parties | **Allowed, always labelled.** Industry associations and advocacy NGOs may be cited, with their interest named in the text; never the sole support for a contested claim. |
| Geography | **Global by default, with regional breakouts** (EU, US, others) where figures differ meaningfully. |
| Our World in Data | **Link, cite the original, embeds allowed.** For data OWID compiled, cite the original producer and credit OWID as the route. OWID charts may be embedded (iframe) with attribution, only where the chart's own page states a licence that allows it. OWID's written text is not adapted. |
| Tooling | **Plain mdBook + repo-side checks.** Checks run in GitHub Actions and never change the site. |
| Automatic checks (planned) | On pull requests: `mdbook build`, claims lint, ledger schema, quote match, licence lint, internal-link check. Later, in order: monthly freshness and dead-link check, cross-page consistency check, attribution check. Today only the deploy workflow exists. |
| Contributions | **Solo author for now, open for issues.** Anyone can report errors or suggest sources via GitHub issues. |
| Handover kit | `docs/pollination/` (from the N62 project) is local reference only, never committed. |

## Decisions (2026-11-27)

| Topic | Decision |
|---|---|
| Ledger format | **Single TOML ledger (`data/sources.toml` + `data/claims.toml`)** replacing the planned YAML files; specification in `docs/sources-and-claims.md`. Shared by both prose in `src/` and models in `models/`. Holds only what sources state (no author-assumed uncertainty; no verification field). Verification remains in status lines and pull-request text. |
| Quantitative models | **Declarative TOML models (`models/`), zero sourced literals.** Flows reference claim IDs in `data/claims.toml`, `share_of`, explicit `residual` flows (at most one per process, labelled "closed by residual"), or typed `sorry` holes. Processes use goods-level total-mass interval closure `[lo, hi]` (mass per period only) with implied bounds printed for `sorry` holes; author-assumed uncertainty lives on model flows, never in `data/`. Node labels are short names only; free-text notes are not exported unless backed by a claim ID. Standalone `models/reactions.toml` checks integer atom-count balance only in v0.1, with each species formula backed by a statement claim ID. |
| Quote text | **At most 300 characters per ledger quote**, copied unchanged from the output of `scripts/source-text`, which normalises text the same way the quote-match check does (rule in `docs/sources-and-claims.md`). Archive links carry the full 14-digit Wayback timestamp and are copied from an existing snapshot, never built by hand. A network failure makes a check inconclusive, never a pass. |
| Model verification | **Same status line as pages:** line 1 of every model file is `# status: draft` or `# status: verified · verified: YYYY-MM-DD by <github-handle> (PR #n)`. Any chapter listed in `src/SUMMARY.md` (`stub` or `verified`) may include only `verified` models (zero open `sorry` holes); the export tool refuses to write a fragment for any other model. |
| Publishing models | **Plain mdBook only — still no preprocessors.** Planned `earthmania export` (`crates/earthmania-core`, `crates/earthmania-cli`) writes committed **tables-only** Markdown fragments (never prose) outside `src/` under `models/generated/`, pulled into pages via stock `{{#include}}`. Fragments emit footnote **references** (`[^c-<claim-id>]`) only; footnote definitions stay hand-written in `## Sources` on the host page. `earthmania export --check` in PR CI keeps fragments fresh. |
| Roles for models and code | **The owner chooses, verifies and approves; AI researches and builds.** The owner names what to model and its boundary, checks every claim against its source before it enters `data/`, writes all page text, and gives the yes for each commit. AI proposes ledger entries (research agent), writes code and model files (`scripts/`, `crates/`, `models/`, CI), and fact-checks in a fresh session. Model files reference only claims the owner has accepted. Page text stays the owner's; revisit after the first published page. |
| Rules for code | **One concern per change, with three checks:** a test that is seen to fail before the change, a review by a fresh session (not the one that wrote it), and one run against real data before the code is relied on. Workflow oddities are logged in `docs/oddities.md` the day they happen. |
| Sequencing | **Real claims before the tool.** The research trial runs on the first flows of the first model (PET bottles, Switzerland); the owner verifies those claims. Then the ledger checks, then the model tool (checking before export), then the first page. No `Cargo.toml`, `crates/` or CI changes before verified claims exist in `data/` (backlog steps 1–3). |
| Licensing | `models/` follows `data/` under CC BY-SA 4.0; planned `Cargo.toml` and `crates/` follow code under MIT (see `LICENSE`). |
| Ledger layout | **One file per source** (replaces the two-file layout named in "Provenance", "Ledger format" and "Quantitative models" above, decided before any claim was stored). Each source and the claims taken from it share one file; claim IDs stay global. Reason: a claim has exactly one source, and claims are checked source by source. The layout is described only in `docs/sources-and-claims.md`; other documents say "the ledger (`data/`)". |
| Ledger IDs | **Fixed pattern, never renamed, reused or deleted.** Lowercase only. Source ID `<organisation>-<short-title>-<edition>` in the source's own language (transliterated), at most 32 characters, the edition always present: the year in the title; for a law, the year of the consolidated version; otherwise the `published` year; plus the month if two editions would still collide; claim ID `<source-id>--<what>`, with `<what>` at most 32 characters and ending in the claim's data year (before any `-r<n>`) when it has a single data year. A wrong claim is retired and replaced: `-r2`, `-r3` when the replacement states the same thing, a fresh ID when it states something else. A claim found to belong to another source is replaced, not moved; a new edition of a source is a new source. The core fields of a merged claim never change in place. |
| Undated figures | **Recorded as `data_year = "undated"`**, never given a year the source did not state. Pages may cite them without implying a year; models may not use them. |
| Footnote checks | **CI fails on any footnote problem**: a `[^c-…]` reference that is undefined or not in the ledger, and mdBook's warning for an unused footnote definition. (mdBook itself renders a mistyped footnote as plain text without a warning.) |
| Sources without a web copy | **Printed books: ISBN, edition and page instead of an archive link**, checked by a person against the copy (`match = "manual"`). Where an openly available full text exists, it is archived as well. Papers keep an archived copy; their DOI is recorded where there is one. |
| One-sided values | **Stored as printed** (`bound = "lower"` or `"upper"`), never closed with a number the source did not print, and only when the limit is about the claim's own value (a legal minimum is a point value). `>` and `≥` are treated alike. The model tool closes them by fixed rules that depend on use, labels each rule-supplied end, and rejects a lower-bound mass flow. |
| Rounding in cross-checks | **Published values are compared within their printed rounding** (half a unit of the last printed digit), in model assertions only, one-sided values included, and every such pass is labelled. |
| Further ledger checks | Disagreement links (`alternatives`) are checked in both directions; every number claim declares its number exactly as printed in the quote (`printed`, with `decimal_mark` and `group_mark`), and a script checks it by character rules only (no words or languages are matched, nothing is guessed), while people set and confirm `bound` and the marks; an ambiguous occurrence (the number appears twice in its quote, or next to another number) passes CI but is listed in the pull request for the fact-checker; the licence page is archived too (`licence_archive`); every claim in a changed source file is re-checked. |
| Intro page | **`src/intro.md` is exempt from the footnote-per-paragraph rule**: it describes the project, not the world. Its sentences with digits and its factual references are still cited. |
| Numbers on pages | **One house style, ISO style**: decimal point, and numbers of five or more digits grouped in threes with a no-break space (`40&nbsp;792`); never a comma or point as grouping mark; years and numbers of four digits or fewer ungrouped. The planned page check converts each number by this rule and compares it with its claim, without guessing. |
| First model year | **The PET beverage bottle model (Switzerland) uses 2024**, the latest year for which all first flows are archived. BAFU's 2024 rate is printed as "> 84" in its table and "85" in its note; both are recorded as linked claims, and the owner asks BAFU. |

## Sources

### Source tiers

| Tier | Kind | Use |
|---|---|---|
| A | Official statistics, primary datasets, peer-reviewed research and reviews, critically reviewed LCAs | Preferred |
| B | Government agencies and intergovernmental bodies | Preferred |
| C | Industry associations, advocacy NGOs, companies | Allowed, interest always named in text |
| D | News, Wikipedia, blogs, aggregators' own text | Leads only: credited as the route ("via …") in the footnote, never as the source of a number |

### Rules

- Never cite a source that was not opened. Never cite from memory (human or AI).
- Every source has an access date and an archive link (web.archive.org). A
  printed book with no open full text has its ISBN and edition instead, and its
  claims are checked by hand against the copy.
- Cite the primary producer of data; credit an aggregator as the route.
- Restate facts in your own words.
- When a source is wrong and a better one shows it, correct the page and report
  the error upstream.

## Licensing

- Earthmania's licences are set out in `LICENSE`.
- Facts and numbers may be restated in our own words with a citation.
- Copied or adapted text, images, charts or data only from **CC0, public domain,
  CC BY or CC BY-SA** sources, credited in TASL format (Title, Author, Source,
  Licence — the *original's* licence, as stated on its own page). Never from NC,
  ND or all-rights-reserved material.
- Prefer redrawing charts from underlying data over copying images.

## Workflow

1. **Pick a section** of a page (one pull request is one section).
2. **Research.** The research agent returns a source dossier: proposed ledger
   entries, one block per source file, with exact quotes, locations,
   data years, licences as seen and archive links, and where sources disagree.
3. **Ledger first.** Review the proposed entries and add the ones you accept.
4. **Write** the section by hand following `_guidelines.md`. Every claim footnote
   uses a claim id from the ledger.
5. **Check.** Open a pull request; the checks must pass. Start a fresh
   fact-checker session; it replies APPROVED or FIX. It advises; you decide.
6. **Verify.** Open each source and check each claim yourself. Update the page's
   status line, and list what you checked in the pull request.
7. **Publish.** Add the page to `SUMMARY.md` if it is new, then merge.
8. **Maintain.** The monthly freshness check opens issues for dead links and old
   data. Corrections are made openly, never silently.
