# Project Map

Use this page when you want to know where to make a change.

## Most Important Folders

- `web/`: browser app routes, templates, and CSS.
- `core/`: progress tracking, sessions, problem dispatch, and answer checking.
- `content/`: lesson text, examples, mistakes, and vocabulary.
- `problems/`: random problem generators.
- `tests/`: automated checks.
- `docs/`: project documentation.

## Common Changes

Change page layout or wording:

- `web/templates/`
- `web/static/app.css`

Change app flow or routes:

- `web/app.py`

Change progress rules:

- `core/progress_tracker.py`
- `core/session_manager.py`
- related tests in `tests/`

Change answer checking:

- `core/evaluator.py`
- `tests/test_evaluator_answer_semantics.py`

Add or edit lesson content:

- `content/<subject>/<topic>.py`

Add or edit generated problems:

- `problems/<subject>/<topic>.py`
- `core/problem_engine.py`
- `MathFoundationBuilder.spec`
- tests in `tests/`

## Files To Avoid Committing

These are generated or local-only:

- `data/`
- `build/`
- `dist/`
- `__pycache__/`
- `.DS_Store`
- `.venv/`

They are ignored in `.gitignore` so the public repo stays clean.

