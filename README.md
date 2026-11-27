<p align="center"><img src="logo/earthmania.svg" alt="Earthmania logo: a globe with the letters EM" width="160"></p>

# Earthmania

A connected, non-academic knowledge base on how materials, industrial processes
and systems actually work. Built with [mdBook](https://rust-lang.github.io/mdBook/).

📖 **Read it at [earthmania.org](https://earthmania.org)**

## Local preview

1. Install mdBook (pick one):
   - Download a binary from the [mdBook releases](https://github.com/rust-lang/mdBook/releases), or
   - `cargo install mdbook`
2. From the repository root, run:

   ```sh
   mdbook serve --open
   ```

   This builds the book, opens it in your browser at `http://localhost:3000`,
   and live-reloads as you edit files in `src/`.

## Adding a page

1. Read `_guidelines.md` (editorial compass, Markdown conventions, attribution block).
2. Create `src/<materials|processes|impacts|systems>/<slug>.md` as a draft.
3. Add it to `src/SUMMARY.md` only once every claim has been verified (see `EDITORIAL.md`).

## Provenance & models (planned)

- **Single ledger (`data/sources.toml`, `data/claims.toml`):** every number and
  checkable fact lives in one TOML ledger (see `docs/sources-and-claims.md`).
- **Declarative mass-flow models (`models/`):** verified by a planned Rust tool
  (`w4`), which exports committed Markdown fragments included in pages via stock
  `mdBook` `{{#include}}` (schema draft in `docs/world4-model-schema.md`).

Pushes to `main` are built and deployed to GitHub Pages automatically
(see `.github/workflows/mdbook.yml`).

## License

- **Content, documentation, ledger and models** (`src/`, `docs/`, `data/`, `models/`): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Code, configuration, scripts and workflows** (`crates/`, `book.toml`, `scripts/`, `.github/`): [MIT](https://opensource.org/licenses/MIT)

See [LICENSE](./LICENSE) for full details.
