# Local Flask Web Conversion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the unreliable Tkinter-first experience with a local Flask web app that opens in the browser and reuses the existing math engine.

**Architecture:** Add a `web/` package with Flask routes, Jinja templates, CSS, and content-loading helpers. Keep `core/`, `content/`, `problems/`, and `utils/` as the source of behavior. Remove the old Tkinter runtime after the Flask path is verified.

**Tech Stack:** Python, Flask, Jinja templates, vanilla CSS/JavaScript, stdlib `unittest`, PyInstaller later for desktop packaging.

---

### Task 1: Add Flask Dependency

**Files:**
- Create: `requirements.txt`
- Modify: `requirements-dev.txt`
- Modify: `README.md`

- [ ] Add `Flask==3.0.3` to runtime dependencies.
- [ ] Keep PyInstaller in development/build dependencies.
- [ ] Document `.venv/bin/python -m web.app` and `.venv/bin/python web_launcher.py`.
- [ ] Verify `import flask` succeeds in `.venv`.

### Task 2: Add Web App Factory And Route Tests

**Files:**
- Create: `web/__init__.py`
- Create: `web/app.py`
- Create: `web/content_loader.py`
- Create: `tests/test_web_app.py`

- [ ] Write route tests for `/health`, `/student`, `/home`, `/subjects/<subject>`, learn completion, locked practice, and practice feedback.
- [ ] Implement `create_app(testing=False, progress_data=None)`.
- [ ] Initialize `ProgressTracker` and `SessionManager` inside the Flask app.
- [ ] Add subject/topic validation helpers.
- [ ] Verify focused web tests pass.

### Task 3: Add Templates And Static Assets

**Files:**
- Create: `web/templates/base.html`
- Create: `web/templates/welcome.html`
- Create: `web/templates/home.html`
- Create: `web/templates/subjects.html`
- Create: `web/templates/learn.html`
- Create: `web/templates/session.html`
- Create: `web/templates/result.html`
- Create: `web/templates/progress.html`
- Create: `web/templates/message.html`
- Create: `web/static/app.css`

- [ ] Build a compact, form-first browser UI.
- [ ] Keep controls visible and responsive on desktop and mobile widths.
- [ ] Avoid browser dependencies beyond standard HTML/CSS.
- [ ] Verify templates render through Flask tests.

### Task 4: Add Browser Launcher

**Files:**
- Create: `web_launcher.py`

- [ ] Start Flask on `127.0.0.1` using an available local port.
- [ ] Wait for `/health`.
- [ ] Open the default browser only from the launcher path.
- [ ] Shut the server down when the launcher exits.

### Task 5: Update Docs And Verification

**Files:**
- Modify: `PROJECT_BRAIN.md`
- Modify: `docs/brain/01-current-state.md`
- Modify: `docs/brain/02-architecture.md`
- Modify: `docs/brain/03-audit-findings-and-roadmap.md`
- Modify: `docs/brain/04-audit-cleanup-change-log.md`
- Modify: `README.md`

- [ ] Mark the local Flask web app as the primary run path.
- [ ] Remove the legacy Tkinter entry point and GUI package.
- [ ] Add server and launcher commands.
- [ ] Run full unit tests.
- [ ] Start the local server and verify `/health` with `curl`.
- [ ] Capture remaining follow-ups: PyInstaller packaging of web launcher, signing/notarization, and release hardening.
