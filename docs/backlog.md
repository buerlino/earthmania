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
- No published content pages yet; `src/materials/pet.md` is a draft skeleton of
  open research questions.
- Live at https://earthmania.org (GitHub Pages via Actions, custom domain, HTTPS
  enforced). Only the introduction is published so far.

## Next steps (in order; each step is shown to the owner before the next)

1. **Research and fact-check setup** (in place; untested on a real claim)
   - `docs/sources-and-claims.md`: ledger format for `data/sources.toml` and
     `data/claims.toml`. Keeps from the N62 kit: `basis: quoted | estimate`
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
   each source and accepts or rejects each claim into `data/sources.toml` and
   `data/claims.toml`.
3. **Ledger checks + PR workflow** (each with a test that must fail first): ledger
   schema, quote match (only claims changed in the PR; network failure =
   inconclusive), licence lint.
4. **Model tool v0.1 (`crates/earthmania-core`, `crates/earthmania-cli`)**, built
   on the verified ledger, checking before export: `earthmania check` (goods-level
   interval balance, `share_of`, explicit `residual`, implied `sorry` bounds,
   `ratio` assertion, standalone `models/reactions.toml` integer atom-count
   balance), then `earthmania export` (tables-only fragments under
   `models/generated/` for stock `{{#include}}`), `earthmania export --check`, and
   a `wasm32` check in PR CI.
5. **First page.** The owner writes the text of one section of
   `src/materials/pet.md` by hand around the generated table. Page checks, each
   with a test that must fail first: claims lint (digit-in-sentence and
   footnote-per-paragraph rules, digit-name allowlist, ledger value appears
   verbatim in its sentence), internal-link and planned-marker check, footnote
   text vs. ledger. Then a fresh fact-checker session, the owner's verification,
   and publication.
6. **Later, in order:** monthly freshness and dead-link check; cross-page
   consistency check; attribution check.

## Ideas, not scheduled

- Issue forms for corrections and source suggestions.
