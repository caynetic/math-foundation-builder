# Future Changes

Use this page when you have a new idea and want to know how risky it is.

## Low-Risk Ideas

These are usually safe if tested:

- adjust colors, spacing, or typography in `web/static/app.css`.
- edit copy in `web/templates/`.
- improve lesson text in `content/`.
- add small docs updates.

Run:

```bash
git diff --check
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v
```

## Medium-Risk Ideas

These need more care:

- add a new topic.
- change problem generation.
- change answer checking.
- change unlock or mastery rules.

Update code and tests together. If adding a topic, also update `config.py`, `content/`, `problems/`, `core/problem_engine.py`, and `MathFoundationBuilder.spec`.

## Higher-Risk Ideas

These should be planned before coding:

- switching JSON storage to SQLite.
- adding multiple students.
- adding accounts or cloud sync.
- packaging for real distribution.
- adding payments, auth, or online hosting.

## Current Follow-Ups

- Decide whether Practice should stay streak-based or use the older rolling-window idea.
- Improve session-log durability if the app gets heavy use.
- Run a real PyInstaller build.
- Add release packaging identity: icon, bundle identifier, signing, entitlements, and notarization plan.

