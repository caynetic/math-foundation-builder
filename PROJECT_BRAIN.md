# Math Foundation Builder Project Brain

Last updated: 2026-06-27

This is the routing document for the Math Foundation Builder app. Read this first before nontrivial work, then follow the links below for the current state, architecture, and audit roadmap.

## Source Of Truth

- Repo root: `/Users/christopherklein/Desktop/Math_Tutor_App-audit-cleanup`
- Remote origin: `https://github.com/BluePalmHub-official/Math_Tutor_App.git`
- Local branch at audit time: `audit-cleanup`
- Upstream context: `main` tracks `origin/main`; `audit-cleanup` is local and currently points at the same commit.
- App type: local Flask browser tutor app.
- Runtime state policy: do not commit `data/`, `build/`, `dist/`, `__pycache__/`, `.DS_Store`, or generated app bundles.

## Docs Routing

- Current app state and verification snapshot: `docs/brain/01-current-state.md`
- Architecture, module contracts, and how to add topics: `docs/brain/02-architecture.md`
- Audit findings and recommended change order: `docs/brain/03-audit-findings-and-roadmap.md`
- Audit cleanup change log and rationale: `docs/brain/04-audit-cleanup-change-log.md`
- Web conversion design: `docs/superpowers/specs/2026-06-27-local-flask-web-conversion-design.md`
- Web conversion implementation plan: `docs/superpowers/plans/2026-06-27-local-flask-web-conversion.md`
- User-facing setup and commands: `README.md`

## Working Rules

- Keep app behavior changes small and test-backed. Core risk is product correctness, not infrastructure.
- Before adding a subject or topic, update `config.py`, `content/`, `problems/`, `MathFoundationBuilder.spec`, and tests together.
- Preserve the static import strategy in `core/problem_engine.py` unless packaging is redesigned; PyInstaller depends on explicit visibility.
- Treat `web/app.py` and `web_launcher.py` as the only supported run paths.
- Do not rely on UI buttons alone for learning gates. Core/session code should protect phase transitions.
- Treat generated build output and local progress/session logs as disposable local state.

## Verification Baseline

Smallest routine check:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v
```

Local web smoke check:

```bash
python3 -m web.app
curl -s http://127.0.0.1:5000/health
```

Additional checks before release or packaging work:

```bash
git diff --cached --check
pyinstaller MathFoundationBuilder.spec
```

The broader generator smoke check should use timeouts per generator. A 2026-06-25 fix pass added a regression test for the hard `systems_of_equations` path and verified 51 configured subject/topic/difficulty combinations without timeout or stubs.
