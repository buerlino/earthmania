# Backlog

Status and open work. One line per item; rewrite in place, history lives in git.
Policy and decisions: `EDITORIAL.md`. Rules for AI sessions: `CLAUDE.md`.

## State (2026-11-27)

- Scaffold, editorial direction (free-form connected nodes) and policy are in place.
- Step 1 is in place: `docs/sources-and-claims.md`, `.claude/agents/research.md`,
  `.claude/agents/factcheck.md` and `scripts/source-text` (offline tests pass;
  checked once by hand against a live Wayback snapshot). `docs/model-schema.md`
  is a draft for step 5. None of it has been used on a real claim yet.
- Oddities are logged in `docs/oddities.md` from 2026-11-27, one row each, on
  the day they happen.
- First research dossier returned (PET beverage bottles, Switzerland, reference
  year 2024: placed on market, separately collected, recycling rate). Not yet
  checked by the owner; nothing in `data/` yet.
- Ledger design revised the same day, before any claim was stored (see
  `EDITORIAL.md`, 2026-11-27): one file per source, permanent IDs with the
  source ID as prefix, printed books by ISBN, `bound` for one-sided values,
  printed rounding in model assertions.
- No published content pages yet; `src/materials/pet.md` is a draft skeleton of
  open research questions.
- Live at https://earthmania.org (GitHub Pages via Actions, custom domain, HTTPS
  enforced). Only the introduction is published so far.

## Next steps (in order; each step is shown to the owner before the next)

1. **Research and fact-check setup** (in place; untested on a real claim)
   - `docs/sources-and-claims.md`: ledger format (one file per source under
     `data/`). Keeps from the N62 kit: `basis: quoted | estimate`
     (`derived` only once needed), `licence_seen_at`, `use: cite | adapted | copied`,
     `match: manual` + reason, and a 300-character quote cap.
   - `.claude/agents/research.md`: dossier of proposed ledger entries, never prose;
     may answer `BLOCKED`.
   - `.claude/agents/factcheck.md`: read-only, fresh session; `APPROVED` + claim ids,
     or `FIX` with at most five findings.
   - `scripts/source-text <archive-url>`: Wayback raw text, PDFs via pdftotext, to
     stdout; with a test that must fail first. The only way agents get exact text.
     Run its tests with `python3 -B -m unittest scripts/test_source_text.py`.
2. **Research trial on the first model flows.** The owner names the flows and the
   boundary (first model: PET bottles, Switzerland; draft in
   `docs/model-schema.md`). The research agent returns a dossier; the owner opens
   each source and accepts or rejects each claim into the ledger.
   - Dossier returned (reference year 2024); next: regroup it into per-source
     files under the new layout and ID rules, then the owner checks each claim.
   - BAFU's 2024 PET rate (table "> 84", note "85", own tonnages 83.81%) goes
     in as two claims linked by `alternatives`. Owner: ask BAFU which is meant;
     archive the BAFU PET Faktenblatt (method of the rate).
3. **Ledger checks + PR workflow** (each with a test that must fail first):
   layout, ID patterns and limits (prefix = file name, year suffix = single-year `data_year`,
   `-r<n>` only after a retired claim), schema (incl. the three kinds of source,
   `bound`, `licence_archive`, `"undated"`), claim IDs unique across files,
   references (incl. two-way `alternatives`, no retired claim cited),
   permanence against `main` (no deleted or renamed claim, no changed frozen
   field), quote match for every live claim in a changed file (network failure
   = inconclusive), printed number (whole number in the quote, declared marks,
   exact conversion to `value`), licence lint.
4. **Model tool v0.1 (`crates/earthmania-core`, `crates/earthmania-cli`)**, built
   on the verified ledger, checking before export: `earthmania check` (goods-level
   interval balance, `share_of`, explicit `residual`, implied `sorry` bounds,
   closing `bound` claims by use, `ratio` assertion within printed rounding,
   standalone `models/reactions.toml` integer atom-count balance), then
   `earthmania export` (tables-only fragments under
   `models/generated/` for stock `{{#include}}`), `earthmania export --check`, and
   a `wasm32` check in PR CI.
5. **First page.** The owner writes the text of one section of
   `src/materials/pet.md` by hand around the generated table. Page checks, each
   with a test that must fail first: claims lint (digit-in-sentence and
   footnote-per-paragraph rules, digit-name allowlist, every number in a
   sentence is written in the house style of `_guidelines.md` and converts
   exactly to the value of a claim footnoted in that sentence), internal-link
   and planned-marker check, footnote
   text vs. ledger, and CI failing on any undefined or unused footnote (mdBook
   renders a mistyped footnote as plain text without a warning). Then a fresh
   fact-checker session, the owner's verification, and publication.
6. **Later, in order:** monthly freshness and dead-link check; cross-page
   consistency check; attribution check.

## Ideas, not scheduled

- Issue forms for corrections and source suggestions.
- A command that prints the canonical footnote line for a claim, so hand-written
  footnotes can be checked exactly against the ledger.
