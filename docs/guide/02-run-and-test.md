# Run And Test

Use this page when you want to start the app, stop it, or check that changes did not break it.

## Install Dependencies

From the project folder:

```bash
python3 -m pip install -r requirements-dev.txt
```

If you are using a virtual environment, activate it first.

## Run The App

```bash
python3 -m web.app
```

Then open:

```text
http://127.0.0.1:5000
```

If you want the launcher to open the browser for you:

```bash
python3 web_launcher.py
```

## Stop The App

In the terminal where the app is running, press:

```text
Control-C
```

## Where Progress Is Saved

Development runs save local state in:

```text
data/
```

Important files:

- `data/progress.json`: student name, topic status, mastery, and unlocks.
- `data/session_log.json`: answer attempts and session history.
- `data/app.log`: app log messages.

The `data/` folder is intentionally ignored by Git because it is local runtime state, not source code.

## Run Tests

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v
```

The current expected result after the cleanup is 22 passing tests.

## Quick Server Check

If the app is running, this should return `{"status":"ok"}`:

```bash
curl -s http://127.0.0.1:5000/health
```

