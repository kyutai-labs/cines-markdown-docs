# cines-markdown-docs

Markdown mirror of the [CINES Adastra user documentation](https://dci.dci-gitlab.cines.fr/webextranet/index.html),
meant to be easily searched by coding agents (and humans) working on the Adastra cluster.

## Layout

- [`docs/INDEX.md`](docs/INDEX.md) — every page with its section outline (h2/h3) and links to anchors. Start here.
- `docs/**` — one Markdown file per page of the original site, same paths (`foo/bar.html` → `docs/foo/bar.md`).
  - Each file begins with `<!-- Source: <original URL> -->`.
  - Internal links point to the local `.md` files; Sphinx section/label ids are kept as `<a id="..."></a>` anchors
    so `page.md#label` links resolve.
  - Images and external links point to the original site.

## Tips for agents

```bash
grep -rn -i "slurm" docs/            # full-text search
grep -n '^#' docs/user_support/index.md   # list headings of a (large) page
```

Some pages are large (100 KB+): grep for the heading or anchor first, then read only the relevant range.

## Running Claude Code on Adastra

The login nodes kill any process after 15 minutes of CPU time. [`claude-code/`](claude-code/README.md) has two
scripts that keep a Claude Code session going across those kills and let Claude restart itself cleanly first.

## Updating

A [GitHub Actions workflow](.github/workflows/update-docs.yml) regenerates `docs/` every day and pushes a commit
if anything changed. To run it locally:

```bash
uv run --locked scripts/generate.py
```

Dependencies are pinned in the script header and hash-locked in `scripts/generate.py.lock`
(`--locked` fails if the two disagree). GitHub Actions are pinned by commit SHA. To upgrade, bump the
versions in the header and run `uv lock --script scripts/generate.py`.
