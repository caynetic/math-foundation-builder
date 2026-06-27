# Audit Cleanup Change Log

This note documents the working-tree cleanup pass for Math Foundation Builder and why each change was made. It covers both the earlier staged audit cleanup and the later correctness fixes added during this pass.

## Repo Context

- Repo: `/Users/christopherklein/Desktop/Math_Tutor_App-audit-cleanup`
- Origin: `https://github.com/BluePalmHub-official/Math_Tutor_App.git`
- Local branch during audit: `audit-cleanup`
- App type: local Flask browser tutor app

## Documentation Added

- Added `PROJECT_BRAIN.md`.
- Added `docs/brain/01-current-state.md`.
- Added `docs/brain/02-architecture.md`.
- Added `docs/brain/03-audit-findings-and-roadmap.md`.
- Added this change log: `docs/brain/04-audit-cleanup-change-log.md`.
- Added `README.md`.

Why:

- The repo did not have a clear source-of-truth map for status, architecture, verification, and next work.
- Future changes need a route into the correct docs before touching code.
- The audit surfaced correctness, packaging, and repo-hygiene issues that should not live only in chat.

## Repo Hygiene

- Added `.gitignore`.
- Removed generated local artifacts from the tracked working tree, including `build/`, `dist/`, `data/`, `__pycache__/`, `.DS_Store`, and generated app-bundle output.

Why:

- Generated artifacts make diffs noisy and make it hard to review real source changes.
- Local progress/session data should not be committed because it is runtime state, not source.
- PyInstaller output should be reproducible from source and build commands, not stored in git.

## Packaging Coverage

- Updated `MathFoundationBuilder.spec` with hidden imports for advanced problem modules.
- Updated packaging tests so configured content and problem modules are checked instead of only a narrow subset.

Why:

- The app imports topic modules dynamically, which PyInstaller cannot always infer.
- Advanced topics had been added, but packaging visibility needed to keep pace.
- A test-backed packaging contract reduces the chance that a bundled app works for Algebra/Geometry but fails for Advanced.

## Problem Engine Contract

- Tightened `core/problem_engine.py` validation so required fields are `question` and `answer`.
- Made invalid generator output raise into the existing stub fallback path.
- Kept optional defaults for `hint`, `hint2`, `hint3`, `explanation`, and `type`.

Why:

- A problem without a question or answer cannot be safely displayed or graded.
- Optional UI fields can be defaulted without crashing the app.
- The fallback behavior should catch broken generators early while keeping the app from hard-crashing.

## Progress And Phase Gating

- Added default unlocked-topic progress construction in `core/progress_tracker.py`.
- Kept Practice and Evaluate locked when Geometry or Advanced subjects are unlocked.
- Added session-layer enforcement in `core/session_manager.py` so direct navigation cannot start locked phases.
- Added tests for progress gating and session phase gates.

Why:

- UI buttons alone were not a sufficient gate; core/session code also needs to protect phase order.
- Unlocking a new subject should unlock the subject and topics, not skip Learn/Practice/Evaluate sequencing.
- Direct calls to `start_session()` should obey the same rules users see in the UI.

## Learn And Progress UI Support

- Adjusted Learn completion helpers to avoid marking missing/empty content as complete.
- Updated progress rendering to include all configured subjects and locked-subject messaging.
- Added a safe `total_correct` property on `SessionManager` and used it from the problem UI instead of reaching into the evaluator directly.

Why:

- Empty or missing content should not create false completion.
- Advanced exists in config and content, so progress reporting should reflect it.
- UI code should avoid depending on private evaluator internals where a session-manager accessor is enough.

## Answer Semantics

- Added inequality normalization in `core/evaluator.py`.
- Added unordered multi-root solution-set matching in `core/evaluator.py`.
- Updated Algebra inequality generators to return full inequality solutions instead of only boundary numbers.
- Updated Quadratics generators to return both roots instead of only the smaller root.
- Added evaluator tests for inequality and solution-set behavior.

Why:

- Asking a learner to solve an inequality but accepting only `3` loses the direction of the answer.
- A quadratic solution normally requires both roots; accepting only one root is mathematically incomplete.
- Students may enter equivalent forms such as `<=` or `≤`, or roots in either order, and the evaluator should handle that.

## Generator Reliability

- Fixed `problems/advanced/systems_of_equations.py` so the elimination-scale generator regenerates `d` when it equals `a`.
- Added generator regression coverage for that hard path.
- Ran a timeout-protected generator smoke check across configured subject/topic/difficulty combinations.

Why:

- The previous loop could hang when `d == a`.
- Random problem generators need targeted regression tests for known bad branches.
- A broad smoke check helps catch generator exceptions and stalls across the configured curriculum.

## Progress File Resilience

- Updated `utils/file_io.py` so missing, empty, corrupt, or unreadable `progress.json` cases are handled distinctly.
- Corrupt progress JSON is preserved as a `.corrupt` file or numbered fallback before defaults are written.
- Added file I/O resilience tests.

Why:

- Silent progress reset is risky for a learning app because it can erase user state without explanation.
- Preserving corrupt files gives a recovery path and a debugging trail.
- The app should still recover to a valid default file when startup state is damaged.

## Test Coverage Added

- Added `tests/test_problem_engine_contract.py`.
- Added `tests/test_progress_gating.py`.
- Added `tests/test_evaluator_answer_semantics.py`.
- Added `tests/test_generator_regressions.py`.
- Added `tests/test_session_phase_gates.py`.
- Added `tests/test_file_io_resilience.py`.
- Expanded `tests/test_packaging_spec.py`.

Why:

- The audit found issues at module boundaries: dynamic imports, progress gates, generator contracts, evaluator semantics, and file recovery.
- Focused unit tests cover those boundaries without requiring a packaged build.

## Verification Run So Far

Commands run during the cleanup pass:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v
git diff --check
git diff --cached --check
```

Observed result:

- Full unittest discovery passed with 22 tests after the legacy Tkinter removal.
- Timeout-protected generator smoke check passed for 51 configured subject/topic/difficulty combinations.
- `git diff --check` passed.
- `git diff --cached --check` passed after cleaning whitespace in staged docs.

Not yet run:

- Actual `pyinstaller MathFoundationBuilder.spec` build.
- Signed/notarized macOS distribution validation.

## Web Conversion Added

- Added `requirements.txt` with Flask.
- Updated `requirements-dev.txt` to include runtime requirements.
- Added `web/app.py`.
- Added `web/content_loader.py`.
- Added `web/templates/` and `web/static/app.css`.
- Added `web_launcher.py`.
- Updated `MathFoundationBuilder.spec` to target the web launcher and bundle browser assets.
- Added `tests/test_web_app.py`.
- Added web conversion design and implementation plan docs under `docs/superpowers/`.

Why:

- The Tkinter UI rendered unreliably on the target macOS setup.
- A local Flask app keeps the app private and local while using the browser for reliable rendering.
- The conversion preserves the existing math engine, content modules, progress tracker, session manager, and local JSON storage.
- The launcher gives a desktop-style start path without introducing Electron, React, hosting, accounts, or a database.

## Legacy Tkinter Removal

- Removed `main.py`.
- Removed `gui/`.
- Removed `tests/test_gui_support.py`.
- Removed Tkinter-only style constants from `config.py`.
- Removed `utils/math_renderer.py`, which only served the Tkinter screens.
- Updated developer messages, comments, README, project brain, and architecture docs to point at `python3 -m web.app` and `web_launcher.py`.

Why:

- The target macOS setup rendered the Tkinter UI unreliably.
- Keeping two UI runtimes would increase maintenance cost while only one path is being tested and packaged.
- The Flask app now covers the learner flow, and the tests cover core behavior, route flow, and packaging alignment.

## Public Repo Snapshot Policy

- Excluded `.claude/` from the public source snapshot.
- Deleted the local `.claude/` folder.

Why:

- `.claude/settings.json` is local agent permission configuration, not app source.
- It referenced old local commands and should not be part of a public project baseline.

## Remaining Follow-Ups

- Clarify Practice pass semantics. Current behavior is streak-based; older comments imply a rolling-window rule.
- Improve session-log durability if the app will be used heavily over time.
- Add release packaging identity before distribution: icon, bundle identifier, signing identity, entitlements, and notarization stance.
- Run an actual PyInstaller build before treating the app as release-ready.
- Run a PyInstaller build to verify the bundled app launches `web_launcher.py`.
