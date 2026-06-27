# Local Flask Web Conversion Design

## Context

The Tkinter app is unreliable on the target macOS setup because the available Tk runtime renders parts of the UI incorrectly. The app should move to a local browser UI while preserving the existing Python math, lesson, progress, and session logic.

## Decision

Build a local Flask web app as the primary UI path. The app runs on `127.0.0.1`, renders HTML with Jinja templates, stores progress in the existing local JSON files, and reuses the current `core/`, `content/`, `problems/`, and `utils/` packages.

The old Tkinter UI was removed after the web path was verified, so Flask is the only supported runtime path.

## User Experience

Development:

```bash
.venv/bin/python -m web.app
```

Desktop-style launch:

```bash
.venv/bin/python web_launcher.py
```

The launcher starts the local Flask server, waits for `/health`, and opens the default browser to the local URL.

## Scope

The first web version includes:

- Welcome/name setup.
- Home dashboard.
- Subject/topic list.
- Learn content page.
- Practice problem flow.
- Evaluate problem flow.
- Result page.
- Progress page.
- Health route for launcher/server checks.

The first web version does not include:

- Online deployment.
- Multi-user accounts.
- Database migration.
- React or other frontend build tooling.
- Signed/notarized desktop packaging.

## Architecture

- `web/app.py`: Flask app factory, routes, and local server entry point.
- `web/content_loader.py`: imports lesson content modules and normalizes them for templates.
- `web/templates/`: Jinja templates for browser screens.
- `web/static/`: CSS and small browser behavior.
- `web_launcher.py`: local desktop-style launcher that starts Flask and opens the browser.

The Flask app owns one `ProgressTracker` and one `SessionManager` per app process. This matches the current local single-student model.

## Data Flow

Startup:

1. Flask app factory initializes progress/session log files.
2. `ProgressTracker` loads progress.
3. `SessionManager` is created with the tracker.
4. Browser routes render state from tracker/session manager.

Learning:

1. `/learn/<subject>/<topic>` loads content from `content.<subject>.<topic>`.
2. The student completes the page.
3. The route calls `ProgressTracker.complete_learn()`.
4. Practice unlock status appears on the topic page.

Practice/evaluate:

1. A route calls `SessionManager.start_session()`.
2. The current problem is rendered.
3. POSTed answers call `SessionManager.submit_answer()`.
4. Practice unlocks Evaluate through existing tracker logic.
5. Evaluate calls `finish_session()` and renders result summary.

## Error Handling

- Locked Practice/Evaluate routes return HTTP 403 with a user-facing locked message.
- Unknown subjects/topics return HTTP 404.
- Missing content modules render a readable unavailable-content message.
- The launcher exits with an error if the local server does not answer `/health`.

## Verification

- Add Flask route tests with `unittest` and Flask `test_client`.
- Keep existing core tests passing.
- Verify local server with `curl http://127.0.0.1:<port>/health`.
- Verify a rendered page with `curl` before browser use.
