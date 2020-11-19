import datetime
import unittest

from demo import models


class ModelsTestCase(unittest.TestCase):
    def test_next_token_id(self):
        dt = datetime.datetime(1999, 12, 31, 11, 59, 59, 12345)
        value = models.next_token_id(dt)

        self.assertEqual(value, '')


if __name__ == '__main__':
    unittest.main()
