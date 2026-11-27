<p align="center"><img src="logo/earthmania.svg" alt="Earthmania logo: a globe with the letters EM" width="160"></p>

# Earthmania

**How materials, industrial processes and systems actually work.**

What happens to a plastic when it is melted a second time? What gets into a
recycling stream that shouldn't, and can it be taken out again? Where does a
"recycled" bottle go next?

Earthmania is a knowledge base for questions like these. Each page is one node
in a connected map: a material, a process, an impact or a system. A page says
what the thing physically is, what it turns into, what it touches, and where
the real technical limits sit. It explains; it does not hand out verdicts.

📖 **Read it at [earthmania.org](https://earthmania.org)**

## Where it stands

Early. The site has an introduction and no content pages yet. The first page,
on PET plastic, is still a list of research questions.

That is on purpose. A page goes live only when every claim in it has been
checked against its source, so the site grows slowly. Five solid pages are
worth more here than a hundred plausible ones.

## How a fact gets onto a page

1. **A source is opened and archived.** It is recorded once, with its licence,
   access date and a Wayback Machine snapshot.
2. **Each number or checkable statement becomes a claim.** A claim holds the
   value, its region, year and definition, and a short exact quote from the
   source.
3. **The page is written by hand.** Every sentence with a number carries a
   footnote that points at its claim.
4. **It is checked twice.** A fresh fact-check pass re-reads the sources, then
   the author verifies each claim before the page is published.

AI is used for research and fact-checking only. It writes no pages and supplies
no fact from memory. The full policy is in [`EDITORIAL.md`](EDITORIAL.md).

## What is in this repository

| Path | What it is |
|---|---|
| [`src/`](src/) | The book: the pages you read on the site |
| [`EDITORIAL.md`](EDITORIAL.md) | The working agreement: principles, decisions, source tiers, workflow |
| [`_guidelines.md`](_guidelines.md) | How to write a page |
| [`docs/sources-and-claims.md`](docs/sources-and-claims.md) | Format of the sources and claims ledger (`data/`, starts with the first page) |
| [`docs/model-schema.md`](docs/model-schema.md) | Draft: mass-flow models whose numbers come only from the ledger (planned) |
| [`scripts/source-text`](scripts/source-text) | Prints the exact text of an archived source, so quotes can be checked |
| [`docs/backlog.md`](docs/backlog.md) | Current state and next steps |

## Run it locally

The site is plain [mdBook](https://rust-lang.github.io/mdBook/): no plugins, no
custom theme.

```sh
mdbook serve --open                                  # preview at http://localhost:3000
python3 -B -m unittest scripts/test_source_text.py   # tests for scripts/source-text
```

Install mdBook from its [releases page](https://github.com/rust-lang/mdBook/releases)
or with `cargo install mdbook`. The PDF tests need `pdftotext` (part of Poppler).

Every push to `main` is built and deployed to GitHub Pages by
[`.github/workflows/mdbook.yml`](.github/workflows/mdbook.yml).

## Found an error?

Please [open an issue](https://github.com/buerlino/earthmania/issues), ideally
with a source. Corrections are made openly, never silently. Earthmania has one
author for now, and issues are the way to contribute.

## Licence

- **Content, documentation, ledger and models:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Code, configuration, scripts and workflows:** [MIT](https://opensource.org/licenses/MIT)
- **The name "Earthmania" and the logo:** all rights reserved

Details are in [`LICENSE`](LICENSE).
