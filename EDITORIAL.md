# Earthmania Editorial Policy

This document is the project's working agreement: what Earthmania is for, how
content is produced, and the rules every page must meet. It applies to every
page in `src/`. Decisions are dated; change them deliberately, never silently.

## Main goal

**Build a small, solid, trustworthy knowledge base — not a big one fast.**

Earthmania explains sustainability and how everyday materials and systems work,
for ordinary readers. Accuracy and trust come before coverage and speed. Five
excellent, fully verified pages are worth more than a hundred plausible drafts.
We are not trying to map everything with AI as quickly as possible.

Earthmania is part of a wider ecosystem of open knowledge, not a competitor to it.
Where others do something well (e.g. Our World in Data for data and charts),
we link to them and build on them.

## Principles

1. **Verified or not published.** Only pages that a human has verified claim by
   claim appear on earthmania.org.
2. **Every claim is traceable.** Every factual claim maps to a source someone has
   actually opened.
3. **Every number carries context:** region, year, definition, source.
4. **Honest about uncertainty.** Contested figures are shown as ranges with an
   explanation of why sources differ. Unknowns are stated.
5. **Plain and simple.** Stock mdBook, plain Markdown, no custom theme, plugins
   or scripts on the site.

## Decisions (2026-11-26)

| Topic | Decision |
|---|---|
| Role of AI | **Research assistant only.** AI may find, retrieve and summarise sources for the author. A human writes all page text. AI never supplies facts, numbers or citations from memory. |
| Verification | **A human checks every claim** against its source before a page is marked `reviewed`. |
| Visibility | **Only reviewed pages are published.** Drafts stay in the repo but are not listed in `src/SUMMARY.md`. |
| Provenance | **Sources registry + claims files.** `sources/registry.yaml` lists each source once; `claims/<slug>.yaml` lists each claim of a page with its source, location and supporting quote. Neither appears on the site. |
| Interested parties | **Allowed, always labelled.** Industry associations and advocacy NGOs may be cited, with their interest named in the text; never the sole support for a contested claim. |
| Geography | **Global by default, with regional breakouts** (EU, US, others) where figures differ meaningfully. |
| Our World in Data | **Link and cite the original.** Pages link to the matching OWID chart for readers who want the data. When using data OWID compiled, cite the original source and credit OWID as compiler. OWID charts (CC BY) may be embedded with attribution. |
| Page types | **Materials** and **Systems & concepts** for now. Comparisons and myths may come later. |
| Tooling | **Plain mdBook + repo-side checks.** The site is stock mdBook. Quality checks run only in GitHub Actions and never change the site. |
| Automatic checks | Build check on pull requests; validator script; weekly link check; review-by reminders. |
| Contributions | **Solo author for now, open for issues.** Anyone can report errors or suggest sources via GitHub issues. |

## Open questions

- **Advice to readers ("What you can do").** Undecided. Until decided, pages are
  informational only and contain no advice section.

## Sources

### Source tiers

| Tier | Kind | Use |
|---|---|---|
| A | Official statistics, primary datasets, peer-reviewed research and reviews, critically reviewed LCAs | Preferred |
| B | Government agencies and intergovernmental bodies (EEA, EPA, UNEP, OECD, IEA …) | Preferred |
| C | Industry associations, advocacy NGOs, companies | Allowed, interest always named in text |
| D | News, Wikipedia, blogs | Leads only — never cited as support for a number |

### Rules

- Never cite a source you have not opened. Never cite from memory (human or AI).
- Record the access date and, where possible, an archive link
  (e.g. web.archive.org) for every source.
- For data compiled by an aggregator (e.g. OWID), cite the original producer and
  credit the aggregator.
- Restate facts in your own words. Do not copy sentences from sources.

## Licensing

- Earthmania content (`src/`) is CC BY-SA 4.0; repository tooling is MIT. See `LICENSE`.
- Facts and numbers may be restated in our own words with a citation.
- Copied or adapted text, images, charts or data only from **CC0, public domain,
  CC BY or CC BY-SA** sources, credited in TASL format (Title, Author, Source,
  Licence — the *original's* licence). Never from NC, ND or all-rights-reserved
  material beyond a short attributed quote.
- Prefer redrawing charts from underlying data over copying images.

## Workflow

1. **Pick a topic** and create a draft page from the template (not yet in `SUMMARY.md`).
2. **Research.** Collect sources (AI may help find and summarise them). Add each
   to `sources/registry.yaml` with tier, licence, access date and archive link.
3. **Write** the page by hand. Every claim gets a footnote whose key is a registry id.
4. **Record claims** in `claims/<slug>.yaml`: claim, source id, location
   (page/table), short supporting quote.
5. **Verify.** Open each source and tick each claim (`verified_on`).
6. **Check.** Open a pull request; CI must pass (build + validator).
7. **Publish.** Set `status: reviewed`, add the page to `SUMMARY.md`, merge.
8. **Maintain.** Each page has a `review_by` date; reminders and link checks open
   issues. Corrections are logged, never silent.
