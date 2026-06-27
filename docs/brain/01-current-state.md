# Current State

Last updated: 2026-06-27

## Repo Identity

- Workspace: `/Users/christopherklein/Desktop/Math_Tutor_App-audit-cleanup`
- Git remote: `https://github.com/BluePalmHub-official/Math_Tutor_App.git`
- Current branch: `audit-cleanup`
- Known upstream: `main` tracks `origin/main`; both `main` and `audit-cleanup` point at commit `4240846 added advanced math module` at audit time.

## App Summary

Math Foundation Builder is now a local Flask browser app for guided math practice. It covers algebra, geometry, and advanced topics. Students move through a three-phase loop:

1. Learn: view lesson cards and worked examples.
2. Practice: answer scaffolded problems with hints until the pass condition is met.
3. Evaluate: complete a scored problem set and unlock mastery.

Subject unlocks are sequential:

- Geometry unlocks after all Algebra topics are mastered.
- Advanced unlocks after all Geometry topics are mastered.

The old Tkinter UI was removed after the browser path was verified. The supported runtime is the local Flask app under `web/`.

## Current Cleanup State

The working tree was already dirty before the brain docs were added. The staged cleanup removes generated/runtime artifacts and adds project hygiene:

- New `.gitignore` ignores bytecode, virtualenvs, tool caches, PyInstaller output, local runtime data, and OS/editor files.
- New `README.md` documents setup, Flask browser running, tests, and build commands.
- New `web/` package provides the local Flask browser UI.
- New `web_launcher.py` starts the local server and opens the default browser.
- `build/`, `dist/`, `__pycache__/`, `.DS_Store`, and `data/` artifacts are staged for deletion.
- Tests were added for problem contracts, progress gating, packaging hidden imports, and Flask route behavior.
- Existing source changes touch problem validation, progress unlock behavior, session-manager accessors, and the Flask browser app.
- Legacy Tkinter files were removed: `main.py`, `gui/`, `tests/test_gui_support.py`, and the Tkinter-only `utils/math_renderer.py`.

Do not revert those staged changes unless the user explicitly asks. Treat them as the current audit-cleanup baseline.

## Runtime Data

Development runs write progress and logs under `data/`. Packaged runs write under platform app data paths through `utils/file_io.py`. Runtime files include:

- `progress.json`
- `session_log.json`
- `app.log`

These are local state and should not be committed.

## Verification Snapshot

Command run during audit:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v
```

Result after the legacy Tkinter removal pass: 22 tests passed.

Focused Flask route coverage:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_web_app -v
```

Result: 9 tests passed.

Additional audit command:

```bash
git diff --cached --check
```

Result after the legacy Tkinter removal pass: passed.

Generator smoke evidence:

- Initial audit: a full configured generator smoke check was stopped after more than 60 seconds. Interrupt landed in `problems/advanced/systems_of_equations.py`, inside `_type_elimination_scale`.
- Root cause: `c1 - c2 == (a - d) * x`; when `a == d`, changing `x` and `y` could not guarantee progress.
- Fix pass: `_type_elimination_scale` now regenerates `d` until `d != a`.
- Verification after fix: 51 configured subject/topic/difficulty combinations completed with zero failures, timeouts, or stubs.

## Local Tooling Notes

- Runtime dependencies now include Flask in `requirements.txt`.
- `requirements-dev.txt` includes runtime requirements and `pyinstaller>=6.0`.
- There is no `pyproject.toml`, `setup.py`, or lockfile.
- `.claude/` is local agent-tool configuration and should stay out of the public source snapshot.

## Status Summary

The app has a working local Flask browser UI that reuses the existing Python core. The highest-risk correctness issues found in the audit have regression coverage now: generator hangs, inequality/quadratic answer semantics, direct phase-gate bypasses, corrupt progress reset, packaging spec alignment, and browser route flow. The Tkinter runtime path has been removed instead of kept as a fallback. The PyInstaller spec now targets `web_launcher.py`, but an actual bundled build has not been run in this pass. The remaining work is release hardening, especially macOS packaging identity/signing.
