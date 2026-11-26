# Backlog

Status and open work. One line per item; rewrite in place, history lives in git.
Policy and decisions: `EDITORIAL.md`. Rules for AI sessions: `CLAUDE.md`.

## State (2026-11-26)

- Scaffold, editorial direction (free-form connected nodes) and policy are in place.
- No published content pages yet; `src/materials/pet.md` is a draft skeleton of
  open research questions.
- Owner action pending: GitHub Settings → Pages → Source: **GitHub Actions**, then
  re-run the deploy workflow and set the custom domain `earthmania.org`.

## Next steps (in order; each step is shown to the owner before the next)

1. **Research and fact-check setup**
   - `docs/sources-and-claims.md`: ledger format for `data/sources.yaml` and
     `data/claims.yaml`. Keep from the N62 kit: `basis: quoted | estimate`
     (`derived` only once needed), `licence_seen_at`, `use: cite | adapted | copied`,
     `match: manual` + reason, a cap on quote length.
   - `.claude/agents/research.md`: dossier of proposed ledger entries, never prose;
     may answer `BLOCKED`.
   - `.claude/agents/factcheck.md`: read-only, fresh session; `APPROVED` + claim ids,
     or `FIX` with at most five findings.
   - `scripts/source-text <archive-url>`: Wayback raw text, PDFs via pdftotext, to
     stdout; with a test that must fail first. The only way agents get exact text.
2. **Research trial:** one section of `src/materials/pet.md` (proposed: mechanical
   recycling bottlenecks). Show the dossier to the owner.
3. **Owner writes that section** by hand; run a fresh fact-checker session.
4. **Scripts + PR workflow** (each with a test that must fail first): claims lint
   (digit-in-sentence and footnote-per-paragraph rules, digit-name allowlist,
   ledger value appears verbatim in its sentence), ledger schema, quote match
   (only claims changed in the PR; network failure = inconclusive), licence lint,
   internal-link and planned-marker check, footnote text vs. ledger.
5. **Later, in order:** monthly freshness and dead-link check; cross-page
   consistency check; attribution check.

## Ideas, not scheduled

- Issue forms for corrections and source suggestions.
- A one-file log of oddities in the research/fact-check workflow.
