# Math Foundation Builder

Math Foundation Builder is a local browser-based math tutor for guided algebra, geometry, and advanced math practice. It runs a Flask server on `127.0.0.1`, opens in the browser, and reuses the existing Python lesson, problem, progress, and session logic.

## Project Layout

- `web/app.py`: Flask web app entry point.
- `web/templates/`: browser UI templates.
- `web/static/`: browser UI styles.
- `web_launcher.py`: local desktop-style launcher that starts Flask and opens the browser.
- `config.py`: app constants, subject/topic lists, phase settings, and labels.
- `core/`: progress tracking, session state, problem dispatch, and answer evaluation.
- `content/`: lesson cards, worked examples, mistakes, and vocabulary.
- `problems/`: randomized problem generators.
- `tests/`: stdlib `unittest` coverage for core behavior, Flask routes, and packaging coverage.

Generated files such as `build/`, `dist/`, `__pycache__/`, and local runtime `data/` are intentionally ignored.

## Requirements

- Python 3.9 or newer.
- Flask runtime dependencies from `requirements.txt`.
- Optional: PyInstaller for building the macOS app bundle.

Install runtime and build tooling:

```bash
python3 -m pip install -r requirements-dev.txt
```

## Run The App

Run the local Flask web app:

```bash
python3 -m web.app
```

Then open:

```text
http://127.0.0.1:5000
```

Desktop-style local launch:

```bash
python3 web_launcher.py
```

That starts the local server on an available port and opens the default browser.

In development mode, progress and logs are written to `data/`. That directory is local runtime state and should not be committed.

## Run Tests

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v
```

The tests avoid writing bytecode and do not require a display server.

Focused web tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_web_app -v
```

## Build

```bash
pyinstaller MathFoundationBuilder.spec
```

The generated `build/` and `dist/` directories are ignored. Commit source changes and the `.spec` file, not generated app bundles.

The spec now points at `web_launcher.py` and bundles `web/templates` plus `web/static`. A full PyInstaller build, signing, and notarization still need to be run before release.
