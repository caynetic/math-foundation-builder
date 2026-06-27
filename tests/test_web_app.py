import copy
import unittest
from unittest.mock import patch

import config
from utils.file_io import DEFAULT_PROGRESS


class WebAppTests(unittest.TestCase):
    def make_client(self):
        from web.app import create_app

        app = create_app(testing=True, progress_data=copy.deepcopy(DEFAULT_PROGRESS))
        return app.test_client()

    def test_health_route_reports_ok(self):
        client = self.make_client()

        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_welcome_to_home_flow_sets_student_name(self):
        client = self.make_client()

        response = client.post("/student", data={"name": "Ada"}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ada", response.data)
        self.assertIn(b"Choose a Module", response.data)

    def test_protected_routes_redirect_to_welcome_before_name(self):
        client = self.make_client()

        response = client.get("/home")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/welcome", response.headers["Location"])

    def test_subject_route_lists_configured_topics(self):
        client = self.make_client()

        client.post("/student", data={"name": "Ada"})
        response = client.get(f"/subjects/{config.SUBJECT_ALGEBRA}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Linear Equations", response.data)
        self.assertIn(b"Start Learning", response.data)

    def test_learn_complete_unlocks_practice(self):
        client = self.make_client()

        client.post("/student", data={"name": "Ada"})
        client.get(f"/learn/{config.SUBJECT_ALGEBRA}/linear_equations")
        response = client.post(
            f"/learn/{config.SUBJECT_ALGEBRA}/linear_equations/complete",
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Go to Practice", response.data)

    def test_practice_route_enforces_phase_gate(self):
        client = self.make_client()

        client.post("/student", data={"name": "Ada"})
        response = client.get(f"/practice/{config.SUBJECT_ALGEBRA}/linear_equations")

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Practice is locked until Learn is complete", response.data)

    def test_practice_answer_renders_feedback_and_next_problem(self):
        client = self.make_client()

        client.post("/student", data={"name": "Ada"})
        client.get(f"/learn/{config.SUBJECT_ALGEBRA}/linear_equations")
        client.post(f"/learn/{config.SUBJECT_ALGEBRA}/linear_equations/complete")

        problem = {
            "question": "Solve: x + 1 = 3",
            "answer": "2",
            "hint": "Subtract 1.",
            "hint2": "x = 3 - 1.",
            "hint3": "x = 2.",
            "explanation": "Subtract 1 from both sides.",
            "type": "numeric",
        }

        with patch("core.session_manager.get_problem_set", return_value=[problem] * 6):
            with patch("core.session_manager.get_problem", return_value=problem):
                with patch("core.evaluator.Evaluator._append_to_session_log", return_value=None):
                    client.get(f"/practice/{config.SUBJECT_ALGEBRA}/linear_equations")
                    response = client.post(
                        f"/practice/{config.SUBJECT_ALGEBRA}/linear_equations",
                        data={"answer": "2"},
                    )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Correct", response.data)
        self.assertIn(b"Solve: x + 1 = 3", response.data)

    def test_evaluate_completion_renders_result_page(self):
        client = self.make_client()

        client.post("/student", data={"name": "Ada"})
        topic_data = client.application.extensions["progress_tracker"]._data[
            config.SUBJECT_ALGEBRA
        ]["linear_equations"]
        topic_data[config.PHASE_LEARN]["status"] = config.STATUS_COMPLETE
        topic_data[config.PHASE_PRACTICE]["status"] = config.STATUS_COMPLETE

        problem = {
            "question": "Solve: x + 1 = 3",
            "answer": "2",
            "hint": "Subtract 1.",
            "hint2": "x = 3 - 1.",
            "hint3": "x = 2.",
            "explanation": "Subtract 1 from both sides.",
            "type": "numeric",
        }

        with patch(
            "core.session_manager.get_problem_set",
            return_value=[problem] * config.PROBLEMS_PER_ROUND,
        ):
            with patch("core.evaluator.Evaluator._append_to_session_log", return_value=None):
                client.get(f"/evaluate/{config.SUBJECT_ALGEBRA}/linear_equations")
                response = None
                for _ in range(config.PROBLEMS_PER_ROUND):
                    response = client.post(
                        f"/evaluate/{config.SUBJECT_ALGEBRA}/linear_equations",
                        data={"answer": "2"},
                        follow_redirects=True,
                    )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Results", response.data)
        self.assertIn(b"100%", response.data)
        self.assertIn(b"Topic Mastered", response.data)

    def test_progress_route_renders_subject_statuses(self):
        client = self.make_client()

        client.post("/student", data={"name": "Ada"})
        response = client.get("/progress")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Progress", response.data)
        self.assertIn(b"Algebra", response.data)
        self.assertIn(b"Geometry", response.data)


if __name__ == "__main__":
    unittest.main()
