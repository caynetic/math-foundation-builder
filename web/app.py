"""Flask web UI for Math Foundation Builder."""

from __future__ import annotations

import copy
import logging
import os
import uuid

from flask import (
    Flask,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import config
from core.progress_tracker import ProgressTracker
from core.session_manager import SessionManager
from utils.file_io import (
    initialise_progress_if_missing,
    initialise_session_log_if_missing,
)
from utils.logger import setup_logger
from web.content_loader import load_topic_content

logger = logging.getLogger(__name__)

SUBJECT_TOPICS = {
    config.SUBJECT_ALGEBRA: config.ALGEBRA_TOPICS,
    config.SUBJECT_GEOMETRY: config.GEOMETRY_TOPICS,
    config.SUBJECT_ADVANCED: config.ADVANCED_TOPICS,
}

SUBJECT_LABELS = {
    config.SUBJECT_ALGEBRA: "Algebra",
    config.SUBJECT_GEOMETRY: "Geometry",
    config.SUBJECT_ADVANCED: "Advanced",
}


def create_app(testing: bool = False, progress_data: dict | None = None) -> Flask:
    """Create the local Flask app."""
    if not testing:
        setup_logger()
        initialise_progress_if_missing()
        initialise_session_log_if_missing()

    app = Flask(__name__)
    app.config["TESTING"] = testing
    app.secret_key = os.environ.get("MFB_SECRET_KEY", "math-foundation-builder-local")

    tracker = ProgressTracker()
    if progress_data is None:
        tracker.load()
    else:
        tracker._data = copy.deepcopy(progress_data)
        tracker.save = lambda: True

    app.extensions["progress_tracker"] = tracker
    app.extensions["session_managers"] = {}
    app.extensions["last_results"] = {}

    register_routes(app)
    register_template_helpers(app)
    register_request_guards(app)
    return app


def register_template_helpers(app: Flask) -> None:
    @app.context_processor
    def inject_globals():
        return {
            "config": config,
            "subject_label": subject_label,
            "topic_label": topic_label,
            "status_label": status_label,
        }


def register_routes(app: Flask) -> None:
    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/")
    def index():
        if tracker().get_student_name():
            return redirect(url_for("home"))
        return redirect(url_for("welcome"))

    @app.get("/welcome")
    def welcome():
        name = tracker().get_student_name()
        if name:
            return render_template("welcome.html", name=name, overall=tracker().get_overall_progress())
        return render_template("welcome.html", name="", overall=None)

    @app.post("/student")
    def student():
        name = request.form.get("name", "").strip()
        error = validate_student_name(name)
        if error:
            return render_template("welcome.html", name=name, overall=None, error=error), 400
        tracker().set_student_name(name)
        return redirect(url_for("home"))

    @app.get("/home")
    def home():
        ensure_student()
        overall = tracker().get_overall_progress()
        subjects = subject_cards(overall)
        return render_template(
            "home.html",
            name=tracker().get_student_name(),
            overall=overall,
            subjects=subjects,
        )

    @app.get("/subjects/<subject>")
    def subject_topics(subject: str):
        ensure_student()
        ensure_subject(subject)
        rows = topic_rows(subject)
        return render_template("subjects.html", subject=subject, rows=rows)

    @app.get("/learn/<subject>/<topic>")
    def learn(subject: str, topic: str):
        ensure_student()
        ensure_topic(subject, topic)
        content = load_topic_content(subject, topic)
        mark_lesson_viewed(subject, topic)
        summary = tracker().get_topic_summary(subject, topic)
        return render_template(
            "learn.html",
            subject=subject,
            topic=topic,
            summary=summary,
            content=content,
        )

    @app.post("/learn/<subject>/<topic>/complete")
    def complete_learn(subject: str, topic: str):
        ensure_student()
        ensure_topic(subject, topic)
        if not lesson_was_viewed(subject, topic):
            return render_message(
                "Lesson must be opened before it can be completed.",
                status_code=400,
                back_url=url_for("learn", subject=subject, topic=topic),
                back_label="Open Lesson",
            )
        tracker().complete_learn(subject, topic)
        return redirect(url_for("subject_topics", subject=subject))

    @app.get("/practice/<subject>/<topic>")
    def practice(subject: str, topic: str):
        ensure_student()
        ensure_topic(subject, topic)
        manager = session_manager()
        try:
            manager.start_session(subject, topic, config.PHASE_PRACTICE)
        except PermissionError as exc:
            return render_message(
                str(exc),
                status_code=403,
                back_url=url_for("subject_topics", subject=subject),
                back_label="Back to Topics",
            )
        return render_session_page(subject, topic, config.PHASE_PRACTICE, manager)

    @app.post("/practice/<subject>/<topic>")
    def submit_practice(subject: str, topic: str):
        ensure_student()
        ensure_topic(subject, topic)
        manager = session_manager()
        if manager.phase != config.PHASE_PRACTICE or manager.subject != subject or manager.topic != topic:
            return redirect(url_for("practice", subject=subject, topic=topic))

        if "show_solution" in request.form:
            manager.mark_show_solution_used()
            raw_answer = "__show_solution__"
        else:
            raw_answer = request.form.get("answer", "").strip()
            if not raw_answer:
                return render_session_page(
                    subject,
                    topic,
                    config.PHASE_PRACTICE,
                    manager,
                    error="Please enter an answer first.",
                )

        result = manager.submit_answer(raw_answer)
        if not result.get("practice_passed"):
            manager.next_practice_problem()

        return render_session_page(
            subject,
            topic,
            config.PHASE_PRACTICE,
            manager,
            result=result,
        )

    @app.get("/evaluate/<subject>/<topic>")
    def evaluate(subject: str, topic: str):
        ensure_student()
        ensure_topic(subject, topic)
        manager = session_manager()
        try:
            manager.start_session(subject, topic, config.PHASE_EVALUATE)
        except PermissionError as exc:
            return render_message(
                str(exc),
                status_code=403,
                back_url=url_for("subject_topics", subject=subject),
                back_label="Back to Topics",
            )
        return render_session_page(subject, topic, config.PHASE_EVALUATE, manager)

    @app.post("/evaluate/<subject>/<topic>")
    def submit_evaluate(subject: str, topic: str):
        ensure_student()
        ensure_topic(subject, topic)
        manager = session_manager()
        if manager.phase != config.PHASE_EVALUATE or manager.subject != subject or manager.topic != topic:
            return redirect(url_for("evaluate", subject=subject, topic=topic))

        raw_answer = request.form.get("answer", "").strip()
        if not raw_answer:
            return render_session_page(
                subject,
                topic,
                config.PHASE_EVALUATE,
                manager,
                error="Please enter an answer.",
            )

        result = manager.submit_answer(raw_answer)
        if manager.is_session_complete():
            finished = manager.finish_session()
            last_results()[client_id()] = finished
            return redirect(url_for("result"))

        return render_session_page(
            subject,
            topic,
            config.PHASE_EVALUATE,
            manager,
            result=result,
        )

    @app.get("/result")
    def result():
        ensure_student()
        data = last_results().get(client_id())
        if not data:
            return render_message(
                "No completed evaluation result is available yet.",
                status_code=404,
                back_url=url_for("home"),
                back_label="Go Home",
            )
        return render_template("result.html", result=data)

    @app.get("/progress")
    def progress():
        ensure_student()
        overall = tracker().get_overall_progress()
        subjects = [
            {
                "key": subject,
                "label": subject_label(subject),
                "locked": tracker().is_subject_locked(subject),
                "topics": topic_rows(subject),
            }
            for subject in config.SUBJECTS_IN_ORDER
        ]
        return render_template("progress.html", overall=overall, subjects=subjects)


def register_request_guards(app: Flask) -> None:
    @app.before_request
    def require_student_name():
        public_endpoints = {"health", "index", "welcome", "student", "static"}
        if request.endpoint in public_endpoints:
            return None
        if not tracker().get_student_name():
            return redirect(url_for("welcome"))
        return None


def tracker() -> ProgressTracker:
    return current_app.extensions["progress_tracker"]


def session_managers() -> dict:
    return current_app.extensions["session_managers"]


def last_results() -> dict:
    return current_app.extensions["last_results"]


def client_id() -> str:
    if "client_id" not in session:
        session["client_id"] = uuid.uuid4().hex
    return session["client_id"]


def session_manager() -> SessionManager:
    cid = client_id()
    managers = session_managers()
    if cid not in managers:
        managers[cid] = SessionManager(tracker())
    return managers[cid]


def validate_student_name(name: str) -> str | None:
    if not name:
        return "Please enter your name to continue."
    if len(name) < 2:
        return "Please enter at least 2 characters."
    return None


def ensure_student() -> None:
    if not tracker().get_student_name():
        abort(401)


def ensure_subject(subject: str) -> None:
    if subject not in SUBJECT_TOPICS:
        abort(404)


def ensure_topic(subject: str, topic: str) -> None:
    ensure_subject(subject)
    if topic not in SUBJECT_TOPICS[subject]:
        abort(404)


def mark_lesson_viewed(subject: str, topic: str) -> None:
    session[lesson_key(subject, topic)] = True


def lesson_was_viewed(subject: str, topic: str) -> bool:
    return bool(session.get(lesson_key(subject, topic)))


def lesson_key(subject: str, topic: str) -> str:
    return f"lesson_viewed:{subject}:{topic}"


def subject_label(subject: str) -> str:
    return SUBJECT_LABELS.get(subject, subject.title())


def topic_label(topic: str) -> str:
    return config.TOPIC_LABELS.get(topic, topic.replace("_", " ").title())


def status_label(status: str) -> str:
    return status.replace("_", " ").title()


def subject_cards(overall: dict) -> list[dict]:
    return [
        {
            "key": config.SUBJECT_ALGEBRA,
            "label": "Algebra",
            "mastered": overall["algebra_mastered"],
            "total": overall["algebra_total"],
            "locked": False,
            "lock_message": "",
        },
        {
            "key": config.SUBJECT_GEOMETRY,
            "label": "Geometry",
            "mastered": overall["geometry_mastered"],
            "total": overall["geometry_total"],
            "locked": overall["geometry_locked"],
            "lock_message": "Complete all Algebra topics to unlock.",
        },
        {
            "key": config.SUBJECT_ADVANCED,
            "label": "Advanced",
            "mastered": overall["advanced_mastered"],
            "total": overall["advanced_total"],
            "locked": overall["advanced_locked"],
            "lock_message": "Complete all Geometry topics to unlock.",
        },
    ]


def topic_rows(subject: str) -> list[dict]:
    rows = []
    for topic in SUBJECT_TOPICS[subject]:
        summary = tracker().get_topic_summary(subject, topic)
        rows.append(
            {
                "key": topic,
                "label": summary["label"],
                "summary": summary,
                "action": topic_action(subject, topic, summary),
            }
        )
    return rows


def topic_action(subject: str, topic: str, summary: dict) -> dict:
    if summary.get("locked"):
        return {"label": "Locked", "url": "", "disabled": True}

    learn = summary.get("learn", config.STATUS_NOT_STARTED)
    practice = summary.get("practice", config.STATUS_LOCKED)

    if learn != config.STATUS_COMPLETE:
        return {
            "label": "Start Learning",
            "url": url_for("learn", subject=subject, topic=topic),
            "disabled": False,
        }
    if practice not in (config.STATUS_COMPLETE, config.STATUS_MASTERED):
        return {
            "label": "Go to Practice",
            "url": url_for("practice", subject=subject, topic=topic),
            "disabled": False,
        }
    if not summary.get("mastered"):
        return {
            "label": "Go to Evaluate",
            "url": url_for("evaluate", subject=subject, topic=topic),
            "disabled": False,
        }
    return {
        "label": "Replay",
        "url": url_for("evaluate", subject=subject, topic=topic),
        "disabled": False,
    }


def render_session_page(
    subject: str,
    topic: str,
    phase: str,
    manager: SessionManager,
    result: dict | None = None,
    error: str | None = None,
):
    problem = manager.current_problem()
    if problem is None and phase == config.PHASE_EVALUATE:
        finished = manager.finish_session()
        last_results()[client_id()] = finished
        return redirect(url_for("result"))

    return render_template(
        "session.html",
        subject=subject,
        topic=topic,
        phase=phase,
        mode_label="Practice" if phase == config.PHASE_PRACTICE else "Evaluate",
        problem=problem,
        result=result,
        error=error,
        manager=manager,
    )


def render_message(message: str, status_code: int, back_url: str, back_label: str):
    return (
        render_template(
            "message.html",
            message=message,
            back_url=back_url,
            back_label=back_label,
        ),
        status_code,
    )


def main() -> None:
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()
