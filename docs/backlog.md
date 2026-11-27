# Backlog

Status and open work. One line per item; rewrite in place, history lives in git.
Policy and decisions: `EDITORIAL.md`. Rules for AI sessions: `CLAUDE.md`.

## State (2026-11-27)

- Scaffold, editorial direction (free-form connected nodes) and policy are in place.
- Single TOML ledger spec (`docs/sources-and-claims.md`) and v0.1 World4 model
  schema draft (`docs/world4-model-schema.md`) are in place; dated policy decision
  recorded in `EDITORIAL.md`.
- No published content pages yet; `src/materials/pet.md` is a draft skeleton of
  open research questions.
- Live at https://earthmania.org (GitHub Pages via Actions, custom domain, HTTPS
  enforced). Only the introduction is published so far.

## Next steps (in order; each step is shown to the owner before the next)

1. **Research and fact-check setup**
   - ~~`docs/sources-and-claims.md`~~ (done: TOML schema for `data/sources.toml`
     and `data/claims.toml`).
   - `.claude/agents/research.md`: dossier of proposed ledger entries, never prose;
     may answer `BLOCKED`.
   - `.claude/agents/factcheck.md`: read-only, fresh session; `APPROVED` + claim ids,
     or `FIX` with at most five findings.
   - `scripts/source-text <archive-url>`: Wayback raw text, PDFs via pdftotext, to
     stdout; with a test that must fail first. The only way agents get exact text.
2. **Research trial:** one section of `src/materials/pet.md` (proposed: mechanical
   recycling bottlenecks, or Swiss PET bottle collection & recycling). Show the
   dossier to the owner.
3. **Owner writes that section** by hand; run a fresh fact-checker session.
4. **World4 v0.1 (`crates/w4-core`, `crates/w4-cli`) + PR checks** (each with a
   test that must fail first): `w4 check`, `w4 export` / `w4 export --check`
   (stock `{{#include}}` fragments), claims & ledger lints, quote match, licence
   lint, internal-link and planned-marker check, footnote text vs. ledger.
5. **Later, in order:** monthly freshness and dead-link check; cross-page
   consistency check; attribution check.

## Ideas, not scheduled

- Issue forms for corrections and source suggestions.
- A one-file log of oddities in the research/fact-check workflow.
