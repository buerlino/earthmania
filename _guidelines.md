<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Earthmania writing guidelines

An editorial compass, not a form to fill in. Read it before starting or revising
any page in `src/`. Binding policy: `EDITORIAL.md`. Rules for AI sessions: `CLAUDE.md`.

## What a page is

Every page is a **node in a connected map** of how materials, processes and
systems actually work. A reader should leave understanding the mechanics well
enough to reason about them and act on them, in industry, policy or everyday life.

Write about:

- **Physical reality:** what the thing is, chemically and physically, and what
  that implies.
- **Transformations and flows:** what it is made from, what it turns into, which
  processes move it between states, and where it goes.
- **Impacts and bottlenecks:** which systems it affects, and where the *real*
  technical or industrial limits sit. The kind of question to ask: what happens to
  a material's structure when it is reprocessed? What contaminates a recycling
  stream, and why can't it be removed? Where does a "recycled" product go next?

Do not write:

- Preachy "X is bad, use Y" framing, or eco-blog tropes.
- Generic "Alternatives / Advantages / Drawbacks" tables.
- Advice lists ("What you can do"). Explain the system; readers draw conclusions.
- Filler written to fill a heading. If there is nothing solid to say, leave it out.

## Structure

Free-form. Let the topic decide its own sections. As a loose guide, most pages move through:

> physical reality → transformations & flows → impacts & bottlenecks → sources & attribution

Only these parts are fixed:

1. Line 1 is the status line (below). Then an `# H1` title and one or two plain
   sentences saying what the topic is.
2. The page ends with `## Sources`, then `## Attribution` if anything was reused,
   then the licence line.

A page may be published section by section: leave unverified sections out.

## Status line

The first line of every page, never shown on the site:

```markdown
<!-- status: draft -->
<!-- status: stub · verified: YYYY-MM-DD by <github-handle> (PR #n) -->
<!-- status: verified · verified: YYYY-MM-DD by <github-handle> (PR #n) -->
```

A **stub** is a short definition with no numbers, verified like any page. It
starts with: `> **Stub:** this page is a short definition; a full page is planned.`

## Links are the backbone

- Link a related topic **at its first mention**, using a relative Markdown link:
  `[mechanical recycling](../processes/mechanical-recycling.md)`.
- Link outwards in every direction: feedstocks, chemical processes, failure modes,
  downstream industries, pollutants, wider systems.
- **Links only point to published pages** (`stub` or `verified`). A page that does not
  exist yet is written as plain text followed by a planned marker, which the site
  does not show and a script can read:

  ```markdown
  mechanical recycling<!-- planned: processes/mechanical-recycling.md -->
  ```

  When the target is published, turn the marker into a link.
- Folders by kind of node:

  | Folder | Holds | Example |
  |---|---|---|
  | `src/materials/` | substances and materials, including classes of materials | `pet.md`, `polymers.md` |
  | `src/processes/` | things done to materials: chemical, physical, industrial | `mechanical-recycling.md` |
  | `src/impacts/` | consequences: pollutants, effects, failure modes | `microplastics.md` |
  | `src/systems/` | arrangements of many actors and processes | `waste-collection.md` |

  Tie-break: name the page after its main noun. A *thing* goes in `materials/`, a
  *verb* (something done) in `processes/`, a *consequence* in `impacts/`, and an
  *organisation of many parts* in `systems/`.
- File names: lowercase, hyphenated, singular. **Never rename a published file.**
- Link to external resources (e.g. Our World in Data) where they explain something
  better, instead of repeating them.

## Grounding

- **Never write a number, quote, date or citation from memory.** Every figure comes
  from a source someone opened, and is recorded in the claims ledger first.
- **Every sentence containing a digit** (years included) carries a claim footnote in
  that sentence. **Every paragraph** carries at least one footnote. Names that
  contain digits (CO2, PM2.5, nylon 6,6, standard numbers) don't count.
- The home page, `src/intro.md`, is exempt from the paragraph rule: it describes
  the project, not the world. Its sentences with digits and its factual
  references (a book, a model, an organisation's work) are still cited.
- Put the data year next to every number. Never show more precision than the
  source. Keep ranges as ranges. When good sources disagree, show both and say why.
- **Write numbers in one house style** (ISO style), so a script can compare them
  with the ledger without guessing: a decimal point (`1.3`), and numbers of
  five or more digits before the point grouped in threes with a no-break space,
  written `&nbsp;` (`40&nbsp;792`, shown as 40 792). Never use a comma or a
  point to group digits. Years and numbers of four digits or fewer are not
  grouped (`2024`, `4500`).
- Avoid vague quantifiers ("most", "rarely", "common") unless a source supports them;
  the fact-checker looks for them.
- Name an interested party (industry body, advocacy group) in the text when citing it.
- Restate facts in your own words. Never put quotations from NC, ND or
  all-rights-reserved sources in a page.

## Markdown conventions

- Footnote keys are ledger claim ids prefixed `c-`: `…in <year>.[^c-<claim-id>]`
- One claim per sentence where possible, so each footnote has a clear target.
- Define a technical term at its first use, or link to its page.
- Images need alt text that says what the image shows.
- Our World in Data charts may be embedded, with attribution, where the chart's
  own page states a licence that allows it:

  ```html
  <iframe src="https://ourworldindata.org/grapher/<chart>?tab=chart" loading="lazy"
          style="width: 100%; height: 600px; border: 0;" title="<chart title>"></iframe>
  ```

## Sources and attribution block

Copy this to the bottom of each page:

```markdown
## Sources

[^c-<claim-id>]: <Author or Organisation> (<publication date>). *<Title>*. <Publisher>.
    <URL> — archived <archive URL>, accessed <YYYY-MM-DD>. [via <aggregator URL>, if any]

[^c-<claim-id>]: <Authors> (<year>). *<Title>*, <edition>. <Publisher>.
    ISBN <isbn>, p. <page>. <!-- printed book without an open full text -->

## Attribution

<!-- Only if text, images, figures or data were copied or adapted. Otherwise delete.
     Allowed: CC0, public domain, CC BY, CC BY-SA. Never NC, ND or all rights reserved.
     The licence is the ORIGINAL's licence, as stated on its own page. -->

- "<Title>" by <Author>, from <Source> (<URL>), licensed under
  [<Licence>](<licence URL>). <Adapted: what changed | Not modified>.

---

<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
*This page is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).*
```
