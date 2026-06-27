# What Changed

This page summarizes what changed from the original cloned app in plain English.

## Documentation

Added:

- `README.md`
- `PROJECT_BRAIN.md`
- `docs/guide/`
- `docs/brain/`
- `docs/superpowers/`

Why:

- The original repo did not explain enough for a non-expert owner.
- Important decisions should live in the repo, not only in chat.
- The docs are split so each page has one job.

## Web App Conversion

Added:

- `web/app.py`
- `web/content_loader.py`
- `web/templates/`
- `web/static/app.css`
- `web_launcher.py`
- `requirements.txt`

Why:

- The old Tkinter UI was unreliable on the target macOS setup.
- A local Flask browser app is easier to test and more viable across platforms.
- The app still stays local and private.

## Legacy Code Removal

Removed:

- `main.py`
- `gui/`
- `tests/test_gui_support.py`
- `utils/math_renderer.py`
- unused Tkinter color/font constants in `config.py`

Why:

- Keeping two UI systems would make the app harder to maintain.
- The Flask browser path is now the supported runtime.

## Correctness Fixes

Improved:

- generator reliability for an Advanced systems-of-equations path.
- inequality answer checking.
- quadratic two-root answer checking.
- phase gates so Practice and Evaluate cannot be started too early.
- corrupt progress-file recovery.

Why:

- A learning app needs the math and unlock rules to be dependable.

## Repo Hygiene

Changed `.gitignore` to ignore:

- bytecode and Python caches.
- virtual environments.
- test/tool caches.
- PyInstaller build output.
- local runtime `data/`.
- OS/editor files.

Removed local `.claude/` settings from the machine and did not include them in the public repo.

Why:

- Generated files and local state should not be public source code.
- A clean repo is easier to review, clone, and maintain.

## GitHub

Created a clean public repo:

```text
https://github.com/caynetic/math-foundation-builder
```

It was published as a fresh source snapshot instead of keeping the old generated-artifact history.

