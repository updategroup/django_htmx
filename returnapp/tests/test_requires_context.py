from django.test import TestCase
from typing import Protocol
from returns.context import RequiresContext
from django.conf import settings

def calculate_points(word: str) -> int:
    guessed_letters_count = len([letter for letter in word if letter != '.'])
    return _award_points_for_letters(guessed_letters_count)

def _award_points_for_letters(guessed: int) -> int:
    return 0 if guessed < 5 else guessed

def _award_points_for_letters_update_second(guessed: int, threshold: int) -> int:
    return 0 if guessed < threshold else guessed


class _Deps(Protocol):
    WORD_THRESHOLD: int

def calculate_points_new(word: str) -> RequiresContext[int, _Deps]:
    guessed_letters_count = len([letter for letter in word if letter != '.'])
    return _award_points_for_letters_new(guessed_letters_count)

def _award_points_for_letters_new(guessed: int) -> RequiresContext[int, _Deps]:
    return RequiresContext(
        lambda deps: 0 if guessed < deps.WORD_THRESHOLD else guessed
    )
class RequiresContextTestCase(TestCase):

    def test_case_old(self):
        first = calculate_points("hello")
        self.assertEqual(first, 5, "should be 5")
        print("case first: ", first)

    def test_case_new(self):
        second = calculate_points_new("hello")(settings)
        print("case second: ", second)


