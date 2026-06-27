# What This App Is

Math Foundation Builder is a local math tutor. It helps a student move through Algebra, Geometry, and Advanced math in a structured order.

Each topic has three phases:

1. Learn: read the lesson and examples.
2. Practice: answer practice problems until the required streak is met.
3. Evaluate: complete a scored round to show mastery.

## What Local Means

The app runs on your computer and opens in a browser at a local address like:

```text
http://127.0.0.1:5000
```

That address is not a public website. It is your own machine talking to itself.

## Current Tech Stack

- Python: main programming language.
- Flask: small local web server.
- Jinja templates: HTML pages rendered by Flask.
- CSS: visual design and layout.
- JSON files: local saved progress and session logs.
- unittest: automated tests.
- PyInstaller: planned desktop packaging path.

There is no React, Electron, cloud backend, user account system, or SQLite database right now.

## Why It Uses The Browser Now

The original cloned app used Tkinter, Python's desktop UI toolkit. On the target macOS setup, that UI rendered unreliably. The app was converted to a local Flask browser app because browsers render forms, text, and layout more predictably across machines.

The math engine, lesson content, progress rules, and problem generators are still Python.

