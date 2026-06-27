from pathlib import Path
import unittest

import config


class PackagingSpecTests(unittest.TestCase):
    def test_pyinstaller_spec_includes_configured_topic_hidden_imports(self):
        spec_text = Path("MathFoundationBuilder.spec").read_text(encoding="utf-8")
        subjects = {
            config.SUBJECT_ALGEBRA: config.ALGEBRA_TOPICS,
            config.SUBJECT_GEOMETRY: config.GEOMETRY_TOPICS,
            config.SUBJECT_ADVANCED: config.ADVANCED_TOPICS,
        }

        for subject, topics in subjects.items():
            for topic in topics:
                with self.subTest(subject=subject, topic=topic, package="content"):
                    self.assertIn(f"content.{subject}.{topic}", spec_text)
                with self.subTest(subject=subject, topic=topic, package="problems"):
                    self.assertIn(f"problems.{subject}.{topic}", spec_text)

    def test_pyinstaller_spec_uses_web_launcher_and_bundles_web_assets(self):
        spec_text = Path("MathFoundationBuilder.spec").read_text(encoding="utf-8")

        self.assertIn("web_launcher.py", spec_text)
        self.assertIn("web/templates", spec_text)
        self.assertIn("web/static", spec_text)
        self.assertIn("web.app", spec_text)
        self.assertNotIn("['main.py']", spec_text)


if __name__ == "__main__":
    unittest.main()
