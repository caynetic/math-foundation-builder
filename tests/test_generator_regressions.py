import signal
import unittest
from itertools import chain, repeat
from unittest.mock import patch

from problems.advanced import systems_of_equations


class Timeout(Exception):
    pass


def raise_timeout(signum, frame):
    raise Timeout()


class GeneratorRegressionTests(unittest.TestCase):
    def test_systems_elimination_scale_returns_when_initial_coefficients_match(self):
        previous_handler = signal.signal(signal.SIGALRM, raise_timeout)
        try:
            signal.alarm(1)
            with patch(
                "problems.advanced.systems_of_equations.random.randint",
                side_effect=chain([3, 2, 3, 1, 1], repeat(1)),
            ):
                problem = systems_of_equations._type_elimination_scale("hard")
            signal.alarm(0)
        except Timeout:
            self.fail("_type_elimination_scale did not terminate")
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous_handler)

        self.assertIn("question", problem)
        self.assertIn("answer", problem)


if __name__ == "__main__":
    unittest.main()
