# Audit Findings And Roadmap

Last updated: 2026-06-27

This doc records the audit findings, the 2026-06-25 fix pass, and the remaining roadmap.

## Web Conversion

### P0: Replace unreliable Tkinter runtime with local browser UI

Status: implemented on 2026-06-27 for local development.

Evidence:

- The target macOS environment rendered the Tkinter welcome screen incorrectly and required interpreter-specific workarounds for `_tkinter`.
- Flask was added as the runtime web dependency.
- `web/app.py` now provides the local browser UI.
- `web_launcher.py` starts a local server and opens the default browser.
- `MathFoundationBuilder.spec` now points at `web_launcher.py` and bundles web templates/static assets.
- `tests/test_web_app.py` covers health, name setup, subject/topic listing, learn completion, locked practice, practice answer feedback, evaluate results, progress, and protected-route redirects.
- The legacy Tkinter entry point and GUI package were removed after the Flask path was verified.

Remaining work:

- Run an actual PyInstaller build and verify packaged browser launch on macOS.
- Run an actual PyInstaller build and verify packaged browser launch on macOS.

## Highest Priority Changes

### P0: Fix generator paths that can hang

Status: fixed on 2026-06-25.

Evidence:

- A configured generator smoke check ran for more than 60 seconds and had to be interrupted.
- The interrupt landed in `problems/advanced/systems_of_equations.py` in `_type_elimination_scale`.
- The loop waits for `c1 != c2`, but `c1 - c2 == (a - d) * x`; if `a == d`, changing `x` and `y` cannot guarantee progress.

Recommended change:

- Ensure `a != d` when generating the hard elimination-scale problem, or generate coefficients from constrained choices that make the system valid by construction.
- Add a deterministic unit test for `_type_elimination_scale` or a timeout-protected public generator test for `systems_of_equations` hard difficulty.

Fix:

- `_type_elimination_scale` now regenerates `d` until it differs from `a`.
- Added `tests/test_generator_regressions.py`.
- Verified with a timeout-protected smoke check across 51 configured subject/topic/difficulty combinations.

### P0: Reconcile answer contracts for inequalities and quadratics

Status: fixed on 2026-06-25 for the audited cases.

Evidence:

- Inequality generators ask students to solve inequalities but store only a numeric boundary answer. A student who types a full valid solution like `x < 5` can fail because the evaluator treats the expected answer as numeric.
- Compound inequalities store only the lower boundary even though the explanation gives a range.
- Quadratic generators ask for solutions and explain both roots, but store only the smaller root as the accepted answer.

Recommended change:

- Decide whether questions should ask for a single requested value or accept full mathematical solution sets.
- For inequalities, either rewrite questions to ask for "the boundary value" or set `type` to `inequality` and store the normalized full inequality.
- For quadratics, either ask for "the smaller root" consistently or extend the evaluator to accept equivalent two-root answer formats.
- Add tests with realistic student inputs, not only generated dict shape checks.

Fix:

- Inequality generators now return full inequality answers with `type: "inequality"`.
- Quadratic generators now return both roots with `type: "solutions"`.
- `Evaluator` now normalizes ASCII/Unicode inequality operators and accepts unordered numeric solution sets.
- Added `tests/test_evaluator_answer_semantics.py`.

### P1: Enforce phase gates outside the UI

Status: fixed on 2026-06-25.

Evidence:

- `AppRoot.go_practice()` and `AppRoot.go_problem()` navigate directly.
- `PracticeScreen` and `ProblemScreen` start sessions unconditionally.
- Current gates are mostly created by which buttons the UI displays.

Recommended change:

- Add a core guard in `SessionManager.start_session()` or in `AppRoot` navigation helpers.
- Block Practice unless Learn is complete.
- Block Evaluate unless Practice is complete.
- Keep GUI button state as a convenience, not the only enforcement.
- Add tests for direct navigation/session attempts.

Fix:

- `SessionManager.start_session()` now raises `PermissionError` if Practice starts before Learn is complete or Evaluate starts before Practice is complete.
- Added `tests/test_session_phase_gates.py`.

### P1: Protect progress data from silent reset

Status: fixed on 2026-06-25 for corrupt JSON parse failures.

Evidence:

- `read_json()` returns `{}` for missing, unreadable, and malformed JSON.
- `initialise_progress_if_missing()` treats any falsy read as missing state and writes defaults.
- A corrupt `progress.json` can therefore be replaced with default progress.

Recommended change:

- Distinguish missing file from parse error.
- On parse error, preserve the bad file with a `.corrupt` or timestamped backup before creating defaults.
- Surface a recoverable error path in logs and, if appropriate, the GUI.

Fix:

- `initialise_progress_if_missing()` now distinguishes missing, empty, corrupt, and unreadable progress files.
- Corrupt progress files are moved to `.corrupt`, with numbered fallbacks if needed, before defaults are written.
- Added `tests/test_file_io_resilience.py`.

### P1: Expand packaging verification

Status: fixed on 2026-06-25 for spec/test alignment.

Evidence:

- `MathFoundationBuilder.spec` manually enumerates hidden imports.
- Lesson content is dynamically imported by the web content loader.
- The current packaging test only checks advanced content hidden imports.

Recommended change:

- Test all configured `content.<subject>.<topic>` and `problems.<subject>.<topic>` hidden imports.
- Add a test that config topics, problem-engine registry entries, content modules, and spec hidden imports stay aligned.
- Run an actual PyInstaller build before any release candidate.

Fix:

- `tests/test_packaging_spec.py` now checks all configured `content.<subject>.<topic>` and `problems.<subject>.<topic>` hidden imports.

## Medium Priority Changes

### P2: Clarify Practice pass semantics

Evidence:

- `config.py` comments say Practice requires a streak within a window.
- Implementation checks only consecutive streak.
- `PRACTICE_WINDOW_SIZE` is currently used as a generated-problem buffer, not as a scoring window.

Recommended change:

- Either update comments/docs to say "consecutive streak only" or implement the configured rolling-window rule.

### P2: Improve session log durability

Evidence:

- Each answer reads the full `session_log.json`, appends one entry, and rewrites the whole file.

Recommended change:

- Consider newline-delimited JSON for append-only logs, or rotate/summarize old session logs.
- Keep atomic writes for progress state.

### P2: Remove local tool config from source snapshot

Status: decided on 2026-06-27.

Evidence:

- `.claude/settings.json` was local agent command-permission state.

Decision:

- Delete the local `.claude/` folder.
- Keep local agent-tooling state out of the public source snapshot.

### P2: Prepare packaging for distribution

Evidence:

- PyInstaller spec has no icon, bundle identifier, signing identity, or entitlements.
- `APP_NAME` is `MathLearningApp`, while the app title/bundle name is `MathFoundationBuilder`.
- Actual PyInstaller build verification has not been run for the Flask browser launcher.

Recommended change:

- Choose a canonical app identifier and data directory name.
- Add a bundle identifier before macOS distribution.
- Add icon/signing/notarization decisions to a release checklist.

## Existing Staged Cleanup To Finish

The staged cleanup is directionally right:

- Removes generated artifacts from Git.
- Adds ignore rules.
- Adds tests.
- Documents basic setup in the README.

The staged whitespace check was fixed on 2026-06-25:

```bash
git diff --cached --check
```

Result: passed after staging corrected `.gitignore` and `README.md` EOFs.

## Recommended Work Order

1. Clarify whether Practice is a pure streak rule or a true rolling-window rule.
2. Improve session log durability if long-term use creates large logs.
3. Add release packaging identity: bundle identifier, icon, signing, and notarization stance.
4. Run an actual PyInstaller build before any release candidate.

## Verification Definition For Next Code Pass

Minimum for correctness fixes:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v
```

Minimum for generator fixes:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_problem_engine_contract -v
```

Also run a timeout-protected smoke test that exercises each configured topic and difficulty without allowing a randomized generator to hang the suite.
