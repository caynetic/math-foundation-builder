import copy
import unittest
from unittest.mock import patch

import config
from core.progress_tracker import ProgressTracker
from utils.file_io import DEFAULT_PROGRESS


def mastered_topic():
    return {
        config.PHASE_LEARN: {"status": config.STATUS_COMPLETE},
        config.PHASE_PRACTICE: {
            "status": config.STATUS_COMPLETE,
            "best_streak": config.PRACTICE_PASS_STREAK,
            "attempts": config.PRACTICE_PASS_STREAK,
        },
        config.PHASE_EVALUATE: {
            "status": config.STATUS_MASTERED,
            "attempts": 1,
            "best_score": 100,
            "mastered": True,
            "difficulty": config.DIFFICULTY_MEDIUM,
        },
    }


class ProgressGatingTests(unittest.TestCase):
    def make_tracker(self):
        tracker = ProgressTracker()
        tracker._data = copy.deepcopy(DEFAULT_PROGRESS)
        return tracker

    def patch_save(self):
        return patch.object(ProgressTracker, "save", return_value=True)

    def test_unlocking_geometry_keeps_phase_sequence_locked(self):
        tracker = self.make_tracker()
        for topic in config.ALGEBRA_TOPICS:
            tracker._data[config.SUBJECT_ALGEBRA][topic] = mastered_topic()

        with self.patch_save():
            result = tracker._check_unlock_geometry()

        self.assertTrue(result)
        self.assertEqual(
            tracker._data[config.SUBJECT_GEOMETRY]["status"],
            config.STATUS_NOT_STARTED,
        )
        for topic in config.GEOMETRY_TOPICS:
            topic_data = tracker._data[config.SUBJECT_GEOMETRY][topic]
            self.assertEqual(
                topic_data[config.PHASE_LEARN]["status"],
                config.STATUS_NOT_STARTED,
            )
            self.assertEqual(
                topic_data[config.PHASE_PRACTICE]["status"],
                config.STATUS_LOCKED,
            )
            self.assertEqual(
                topic_data[config.PHASE_EVALUATE]["status"],
                config.STATUS_LOCKED,
            )

    def test_unlocking_advanced_keeps_phase_sequence_locked(self):
        tracker = self.make_tracker()
        tracker._data[config.SUBJECT_ADVANCED]["status"] = config.STATUS_LOCKED
        for topic in config.GEOMETRY_TOPICS:
            tracker._data[config.SUBJECT_GEOMETRY][topic] = mastered_topic()

        with self.patch_save():
            result = tracker._check_unlock_advanced()

        self.assertTrue(result)
        self.assertEqual(
            tracker._data[config.SUBJECT_ADVANCED]["status"],
            config.STATUS_NOT_STARTED,
        )
        for topic in config.ADVANCED_TOPICS:
            topic_data = tracker._data[config.SUBJECT_ADVANCED][topic]
            self.assertEqual(
                topic_data[config.PHASE_LEARN]["status"],
                config.STATUS_NOT_STARTED,
            )
            self.assertEqual(
                topic_data[config.PHASE_PRACTICE]["status"],
                config.STATUS_LOCKED,
            )
            self.assertEqual(
                topic_data[config.PHASE_EVALUATE]["status"],
                config.STATUS_LOCKED,
            )


if __name__ == "__main__":
    unittest.main()
