
from django.test import TestCase
class BasicTests(TestCase):

    def test_math(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)