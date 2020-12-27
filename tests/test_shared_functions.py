import unittest

import resampling


class TestCase(unittest.TestCase):
    def setUp(self):
        self._raw_values = [1.0, 2.0, 3.0, 4.0, 5.0]

    def test_resampling(self):
        actual_result = resampling.mean(self._raw_values)
        self.assertEqual(3.0, actual_result)


if __name__ == "__main__":
    unittest.main()
