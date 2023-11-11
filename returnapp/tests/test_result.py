from typing import Optional, Dict
import json
from django.test import TestCase
import requests
from returns.result import Result, safe, Failure, Success, attempt
from returns.pipeline import flow, is_successful
from returns.pointfree import bind


class TestResult(TestCase):

    @staticmethod
    def check_number(number: Optional[int]) -> Result[int, str]:
        if isinstance(number, int):
            return Success(number)
        else:
            return Failure('Not a number')

    def test_basesic(self):
        self.assertEqual(self.check_number(1), Success(1))
        self.assertEqual(self.check_number(None), Failure('Not a number'))

    @staticmethod
    @safe
    def div(firt_number: int, second_number: int) -> int:
        return firt_number // second_number

    def ex_div(self, firt_number: int, second_number: int) -> Result[int, str]:
        match self.div(firt_number, second_number):
            case Success(result):
                return Success(result)
            case Failure(ZeroDivisionError()):
                return Failure("Division by zero")
            case _:
                return Failure("Unknown error")

    # @staticmethod
    # @safe(exceptions=Exception)
    # def divide(number: int):
    #     if number > 2:
    #         raise ValueError("Number too large")
    #     return number

    def test_match(self):
        self.assertEqual(self.ex_div(1, 1), Success(1))
        self.assertEqual(self.ex_div(1, 0), Failure("Division by zero"))
        self.assertEqual(self.ex_div('s', 2), Failure("Unknown error"))

    @staticmethod
    @attempt
    def divide_itself(number: int) -> float:
        return number / number

    def test_attempt(self):
        """Giống sale nhưng giá trị trả về là giá trị lỗi """
        # self.assertEqual(self.divide_itself(1), Success(1.0))
        # print(self.div(1, 0))
        self.assertEqual(self.divide_itself('error'), Failure('error'))
        self.assertEqual(self.divide_itself(0), Failure(0))

    @staticmethod
    @safe
    def parse_json(arg: str) -> Dict:
        """can produce Exceptions => safe"""
        return json.loads(arg)

    @staticmethod
    def case_to_bool(arg: int) -> bool:
        """doesn't produce any side-effect"""
        return bool(arg)

    def test_map_and_bin(self):
        self.assertEqual(Success(1).map(self.case_to_bool), Success(1))
        self.assertEqual(Success('{"a":1}').bind(self.parse_json), Success({'a': 1}))
        self.assertEqual(is_successful(Success('').bind(self.parse_json)), False)
        print(Success('').bind(self.parse_json))




