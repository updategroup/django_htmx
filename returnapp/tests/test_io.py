import random

from django.test import TestCase
from returns.io import IO, IOResultE

class TestIO(TestCase):
    @staticmethod
    def get_random_number() -> IO[int]:
        return IO(random.randint(1, 10))
    def test_io(self):
        assert isinstance(self.get_random_number(), IO)