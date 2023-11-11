from django.test import TestCase
from returns.pipeline import flow, pipe
from returns.result import ResultE, Success, Result, Failure
from returns.pointfree import bind

class PipelineTestCase(TestCase):

    @staticmethod
    def returns_result(arg: int) -> ResultE[int]:
        return Success(arg)
    @staticmethod
    def works_with_result(arg: int) -> ResultE[int]:
        return Success(arg+3)

    @staticmethod
    def regular_function(arg: int) -> float:
        return float(arg)

    @staticmethod
    def return_container(arg: float) -> Result[str, ValueError]:
        if arg !=0:
            return Success(str(arg))
        return Failure(ValueError("Wrong arg"))

    @staticmethod
    def also_return_container(arg: str) -> Result[str, ValueError]:
        return Success(arg+"b")

    def test_negative_number(self):
        max_number = flow(
            [1,2,3],
            lambda x: max(x),
            lambda y: -y
        )
        self.assertEqual(max_number, -3)

    def test_flow_with_point_free(self):
        result = flow(
            1,
            self.regular_function,
            self.return_container,
            bind(self.also_return_container)
        )
        self.assertEqual(result, Success('1.0b'))

    def test_pipe_upper(self):
        upper = pipe(
            int,
            lambda x: str(x) + 'b',
            lambda y : y.upper()
        )
        self.assertEqual(upper(1), '1B')

