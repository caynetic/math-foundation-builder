import unittest

from core.evaluator import Evaluator


class EvaluatorAnswerSemanticsTests(unittest.TestCase):
    def make_evaluator(self):
        return Evaluator(
            session_id="test",
            subject="algebra",
            topic="test_topic",
            phase="practice",
        )

    def test_inequality_accepts_ascii_input_for_unicode_expected_answer(self):
        evaluator = self.make_evaluator()

        self.assertTrue(evaluator._is_correct("x >= 5", "x ≥ 5", "inequality"))
        self.assertTrue(evaluator._is_correct("x <= -2", "x ≤ -2", "inequality"))

    def test_compound_inequality_accepts_full_solution_range(self):
        evaluator = self.make_evaluator()

        self.assertTrue(evaluator._is_correct("-1 < x < 4", "-1 < x < 4", "inequality"))
        self.assertFalse(evaluator._is_correct("-1", "-1 < x < 4", "inequality"))

    def test_solution_set_accepts_two_roots_in_any_order(self):
        evaluator = self.make_evaluator()

        self.assertTrue(evaluator._is_correct("x = 5 or x = -2", [-2, 5], "solutions"))
        self.assertTrue(evaluator._is_correct("-2, 5", [-2, 5], "solutions"))
        self.assertFalse(evaluator._is_correct("5", [-2, 5], "solutions"))


if __name__ == "__main__":
    unittest.main()
