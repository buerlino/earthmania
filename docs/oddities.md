<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Oddities log

Anything that went wrong or surprised us in the research, fact-check or build
workflow. One row per oddity, newest last, added on the day it happens. Each row
gets a one-word cause, so repeated causes show up when the table is read back.
Fixes to rules, prompts and scripts come out of this file.

Causes used so far: `untested-path`, `silent-fallback`, `scope`, `status`,
`memory`, `unverified`, `docs-drift`, `layout`. Add a new word only when none fits.

| Date | What happened | How it was caught | Cause | Fix |
|---|---|---|---|---|
| 2026-11-27 | `scripts/source-text` printed compressed bytes as if they were text and exited 0. Its 8 tests all passed: none touched the network path. | Review session ran it against a live Wayback snapshot. | `untested-path` | Decompress the response; test the fetch path with the network call replaced; one live check by hand before relying on a script that fetches. |
| 2026-11-27 | A Latin-1 page came out with every umlaut replaced by `�`, exit 0. | Review session fed it a test page. | `silent-fallback` | Decode strictly, read the page's `<meta>` charset, fail loudly, `--encoding` flag. |
| 2026-11-27 | A shortened or wrong Wayback timestamp was accepted and silently redirected to a different capture. | Live check in review. | `silent-fallback` | Require the 14-digit timestamp; fail and name the real capture on redirect. |
| 2026-11-27 | An agent asked for proposed diffs applied them instead, and edited a file outside its list (`docs/backlog.md`), dropping the detail of backlog step 4. Committed locally in `502baf7`, corrected afterwards, never pushed. | Fresh review of the diff. | `scope` | Brief names the files that may be touched; a fresh session reviews every diff before commit. |
| 2026-11-27 | A backlog step was marked done and "in place" before the owner had seen it. | Fresh review of the diff. | `status` | Only the owner marks a step done. |
| 2026-11-27 | A test fixture contained statistics that read like real figures (a collection rate, a year, a tonnage). | Fresh review of the test file. | `memory` | Fixture text is obviously fake ("widgets"). |
| 2026-11-27 | An analysis recommended limiting an agent's shell commands through `.claude/settings.json`. Per the tool's documentation, allow rules there cannot do that. | Checked the documentation before acting. | `unverified` | Check a tool's documented behaviour before writing a rule that depends on it. |
| 2026-11-27 | The fact-checker's reply format gained an `INCONCLUSIVE` line in its agent file but not in `CLAUDE.md`. | A second read of prompts and rules side by side. | `docs-drift` | Change a format in every file that states it, in the same edit. |
| 2026-11-27 | `scripts/source-text` flattened a PDF table (BAFU 2024 overview), so the 63'300 t of the Textilien row appeared right after "PET-Getränkeflaschen". | Research agent rendered the archived page and checked the row by eye. | `layout` | When a number comes from a PDF table, check its row on the rendered page before proposing the claim. |
