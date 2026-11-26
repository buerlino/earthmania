# Earthmania

A living, non-academic field guide to sustainability and how everyday materials
and systems work. Built with [mdBook](https://rust-lang.github.io/mdBook/).

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

1. Copy `_template.md` to `src/<section>/<slug>.md`.
2. Add the page to `src/SUMMARY.md`.
3. Fill in each section and list your sources with access dates.

Pushes to `main` are built and deployed to GitHub Pages automatically
(see `.github/workflows/mdbook.yml`).

## License

- **Content** (everything in `src/`): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Configuration, scripts and workflows**: [MIT](https://opensource.org/licenses/MIT)

See [LICENSE](./LICENSE) for full details.
