# Architecture

Last updated: 2026-06-27

## System Shape

Math Foundation Builder is a local Flask browser app:

- `web/app.py` creates the Flask app, initializes local progress/session files, owns the shared `ProgressTracker`, and creates per-browser-session `SessionManager` objects.
- `web/templates/` contains Jinja templates for welcome, home, topic list, learn, practice/evaluate sessions, results, progress, and messages.
- `web/static/app.css` contains the browser UI styling.
- `web/content_loader.py` imports lesson content modules for browser rendering.
- `web_launcher.py` starts the local Flask server on `127.0.0.1`, waits for `/health`, and opens the default browser.
- `core/` contains the app logic that should stay independent of the browser UI where possible.
- `content/` contains lesson content modules.
- `problems/` contains randomized problem generators.
- `utils/` contains file paths, JSON persistence, logging, and resource helpers.

## Core Data Flow

Flask startup:

1. `web/app.py` calls logger setup when not testing.
2. `web/app.py` initializes `progress.json` and `session_log.json` if missing.
3. The Flask app creates one `ProgressTracker` and loads progress.
4. The Flask app creates a `SessionManager` per browser session and stores it in memory.
5. Routes render Jinja templates from tracker/session state.

Practice/evaluate flow:

1. A Flask route calls `SessionManager.start_session(subject, topic, phase)`.
2. `SessionManager` asks `core/problem_engine.py` for a problem set.
3. `problem_engine` uses a static registry of imported problem modules.
4. A problem generator returns a problem dict.
5. `Evaluator.check()` compares student input to the expected answer and appends a session-log entry.
6. `ProgressTracker` updates phase status, mastery, difficulty, and subject unlocks.
7. Jinja templates render status from `ProgressTracker.get_topic_summary()` and `get_overall_progress()`.

## Problem Contract

Every generator should return a dict with at least:

- `question`
- `answer`

The problem engine applies defaults for:

- `hint`
- `hint2`
- `hint3`
- `explanation`
- `type`

Supported answer types in `Evaluator`:

- `numeric`
- `multiple_choice`
- `expression`
- `inequality`
- `solutions`

## Progress Contract

Topic state is nested by subject, topic, then phase:

- `learn.status`
- `practice.status`, `practice.best_streak`, `practice.attempts`
- `evaluate.status`, `evaluate.attempts`, `evaluate.best_score`, `evaluate.mastered`, `evaluate.difficulty`

Unlock rules:

- Learn completion unlocks Practice.
- Practice streak completion unlocks Evaluate.
- Evaluate score at or above `MASTERY_SCORE_PERCENT` marks a topic mastered.
- All Algebra topics mastered unlock Geometry.
- All Geometry topics mastered unlock Advanced.

The Flask routes still show/hide actions for convenience, but `SessionManager.start_session()` is the enforcement layer for Practice and Evaluate gates.

Learn completion in Flask is tied to opening the lesson page before posting completion. This avoids a blind unlock POST and keeps the first web version simple.

## Packaging Contract

The app currently uses PyInstaller with a manually maintained `MathFoundationBuilder.spec`. The spec now targets `web_launcher.py` as the primary executable and includes `web/templates` plus `web/static` as bundled data.

Packaging-sensitive patterns:

- `core/problem_engine.py` uses explicit static imports for problem modules.
- `web/content_loader.py` dynamically imports lesson content by `content.{subject}.{topic}`.
- `MathFoundationBuilder.spec` must enumerate dynamically loaded content modules and any modules PyInstaller cannot infer.

Distribution gaps:

- No app icon.
- No bundle identifier.
- No signing identity.
- No entitlements file.
- Actual PyInstaller build verification has not been run for the web launcher.
- `APP_NAME` is `MathLearningApp`, while user-facing and bundle names are `MathFoundationBuilder`.

## How To Add A Topic

When adding or renaming a topic, update all of these together:

1. Add the topic key in `config.py`.
2. Add a human-readable label in `config.TOPIC_LABELS`.
3. Add lesson content under `content/<subject>/<topic>.py`.
4. Add a generator under `problems/<subject>/<topic>.py`.
5. Add a static import and registry entry in `core/problem_engine.py`.
6. Add hidden imports in `MathFoundationBuilder.spec`.
7. Extend tests so configured topics, content modules, problem modules, and packaging hidden imports stay in sync.

## Verification Commands

Routine:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v
```

Focused:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_problem_engine_contract tests.test_progress_gating -v
```

Packaging:

```bash
pyinstaller MathFoundationBuilder.spec
```

Use timeout-protected generator smoke tests before trusting randomized content changes.
