import types
import unittest
from unittest.mock import patch

import config
from core import problem_engine


class ProblemEngineContractTests(unittest.TestCase):
    def test_generator_missing_required_answer_returns_stub_problem(self):
        broken_module = types.SimpleNamespace(
            generate=lambda difficulty: {
                "question": "What is 2 + 2?",
                "hint": "Add.",
                "explanation": "2 + 2 = 4",
                "type": "numeric",
            }
        )
        registry = {
            config.SUBJECT_ALGEBRA: {
                "broken_topic": broken_module,
            }
        }

        with patch.object(problem_engine, "_REGISTRY", registry):
            problem = problem_engine.get_problem(
                config.SUBJECT_ALGEBRA,
                "broken_topic",
                config.DIFFICULTY_EASY,
            )

        self.assertIn("Problem generator coming soon", problem["question"])
        self.assertIn("answer", problem)

    def test_all_configured_generators_return_required_problem_keys(self):
        subjects = {
            config.SUBJECT_ALGEBRA: config.ALGEBRA_TOPICS,
            config.SUBJECT_GEOMETRY: config.GEOMETRY_TOPICS,
            config.SUBJECT_ADVANCED: config.ADVANCED_TOPICS,
        }
        required = {
            "question",
            "answer",
            "hint",
            "hint2",
            "hint3",
            "explanation",
            "type",
        }

        for subject, topics in subjects.items():
            for topic in topics:
                with self.subTest(subject=subject, topic=topic):
                    problem = problem_engine.get_problem(subject, topic)
                    self.assertLessEqual(required, set(problem))


if __name__ == "__main__":
    unittest.main()
