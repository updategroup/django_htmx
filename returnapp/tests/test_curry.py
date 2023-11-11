
from django.test import TestCase
from functools import partial

class TestCurry(TestCase):
    @staticmethod
    def some_function(first: int, second: int) -> float:
        return first / second

    def test_curry(self):
        a  = partial(self.some_function, 1)
        print(a(2))