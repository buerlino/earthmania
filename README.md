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

Pushes to `main` are built and deployed to GitHub Pages automatically
(see `.github/workflows/mdbook.yml`).

## License

- **Content** (everything in `src/`): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Configuration, scripts and workflows**: [MIT](https://opensource.org/licenses/MIT)

See [LICENSE](./LICENSE) for full details.
