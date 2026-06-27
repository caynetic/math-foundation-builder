import copy
import unittest
from unittest.mock import patch

import config
from core.session_manager import SessionManager
from utils.file_io import DEFAULT_PROGRESS


class SessionPhaseGateTests(unittest.TestCase):
    def make_manager(self):
        tracker = type("Tracker", (), {})()
        tracker._data = copy.deepcopy(DEFAULT_PROGRESS)
        tracker.get_current_difficulty = (
            lambda subject, topic: tracker._data[subject][topic][config.PHASE_EVALUATE]
            .get("difficulty", config.DIFFICULTY_EASY)
        )
        tracker.get_phase_status = (
            lambda subject, topic, phase: tracker._data[subject][topic][phase]["status"]
        )
        return SessionManager(tracker), tracker

    def test_practice_requires_completed_learn_phase(self):
        manager, tracker = self.make_manager()
        topic = "linear_equations"

        with patch("core.session_manager.get_problem_set", return_value=[]):
            with self.assertRaises(PermissionError):
                manager.start_session(config.SUBJECT_ALGEBRA, topic, config.PHASE_PRACTICE)

            tracker._data[config.SUBJECT_ALGEBRA][topic][config.PHASE_LEARN]["status"] = (
                config.STATUS_COMPLETE
            )
            manager.start_session(config.SUBJECT_ALGEBRA, topic, config.PHASE_PRACTICE)

    def test_evaluate_requires_completed_practice_phase(self):
        manager, tracker = self.make_manager()
        topic = "linear_equations"
        topic_data = tracker._data[config.SUBJECT_ALGEBRA][topic]
        topic_data[config.PHASE_LEARN]["status"] = config.STATUS_COMPLETE

        with patch("core.session_manager.get_problem_set", return_value=[]):
            with self.assertRaises(PermissionError):
                manager.start_session(config.SUBJECT_ALGEBRA, topic, config.PHASE_EVALUATE)

            topic_data[config.PHASE_PRACTICE]["status"] = config.STATUS_COMPLETE
            manager.start_session(config.SUBJECT_ALGEBRA, topic, config.PHASE_EVALUATE)


if __name__ == "__main__":
    unittest.main()
