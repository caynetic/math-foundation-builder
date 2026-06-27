# Beginner Guide

This guide is for someone who has an app idea, can follow step-by-step commands, but may not know Flask, Git, packaging, or the project internals yet.

The original cloned project was a Python desktop app with separate folders for math content, problem generators, and app logic. It did not explain enough about how the pieces fit together or which files were safe to ignore. These guide pages add that missing orientation without making one giant document.

## Reading Order

Read these in order the first time:

1. `01-what-this-app-is.md`
2. `02-run-and-test.md`
3. `03-project-map.md`
4. `04-what-changed.md`
5. `05-next-changes.md`

Stop after the page that answers your question. The deeper docs in `docs/brain/` are for audits, architecture decisions, and future development work.

## Quick Facts

- The app is local-first. It runs on your computer.
- The browser is the user interface.
- Python does the app logic.
- Flask serves the local pages.
- Progress is saved to local JSON files under `data/`.
- `data/`, `build/`, `dist/`, caches, and `.DS_Store` should not be committed.
- The public GitHub repo is `https://github.com/caynetic/math-foundation-builder`.

