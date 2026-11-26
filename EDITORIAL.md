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
| Roles | **The owner writes every page.** AI is a research assistant and fact-checker only: a research agent proposes ledger entries (never prose); a fresh, read-only fact-checker session advises on each pull request. AI never supplies facts, numbers or citations from memory, and no agent runs unattended. |
| Verification | **A human checks every claim** against its source before content becomes `verified`. Recorded in the page's status line (date, by whom, PR number) and in the pull request text; not in the ledger. |
| What a claim is | **Every sentence containing a digit (years included) carries a claim footnote** in that sentence, and **every paragraph of prose carries at least one footnote**. Names containing digits (CO2, PM2.5, nylon 6,6, standard numbers) are on an allowlist. Vague quantifiers ("most", "rarely") are checked by the fact-checker. |
| Provenance | **Sources registry + claims ledger.** `data/sources.yaml` lists each source once; `data/claims.yaml` lists each claim with its source, location and supporting quote. Neither appears on the site. |
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
- Every source has an access date and an archive link (web.archive.org).
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
2. **Research.** The research agent returns a source dossier: proposed entries
   for `data/sources.yaml` and `data/claims.yaml`, with exact quotes, locations,
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
