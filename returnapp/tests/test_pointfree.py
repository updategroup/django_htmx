from django.test import TestCase
from returns.maybe import Maybe, Some, Nothing
from returns import pointfree
from returns.pipeline import flow, pipe
"""
- composing functions with containers easier. 
"""
class PointfreeTests(TestCase):

    @staticmethod
    def as_int(arg: str) -> int:
        return ord(arg)

    @staticmethod
    def index_of_7(arg: str) -> Maybe[int]:
        if '7' in arg:
            return Some(arg.index('7'))
        return Nothing

    @staticmethod
    def double(arg: int) -> int:
        return arg * 2

    @staticmethod
    def index_of_1(arg: str) -> Maybe[int]:
        if '1' in arg:
            return Some(arg.index('1'))
        return Nothing

    def test_pointfree_map_(self):
        """
        It lifts a function to work from container to container.
        a -> b to: Container[a] -> Container[b]
        """
        container: Maybe[str] = Some('a')
        self.assertEqual(container.map(self.as_int), Some(97))
        self.assertEqual(pointfree.map_(self.as_int)(container), Some(97))

    def test_pointfree_pipeline_map_(self):
        result = pipe(
            self.index_of_7,
            pointfree.map_(self.double)
        )
        self.assertEqual(result("007"), Some(4))
        self.assertEqual(flow(
            '006',
            self.index_of_7,
            pointfree.map_(self.double)
        ), Nothing)

    def test_pointfree_bind(self):
        """
        a -> Container[b] to: Container[a] -> Container[b]
        """
        container: Maybe[str] = Some('A1 Steak Sauce')
        self.assertEqual(container.bind(self.index_of_1), Some(1))
        self.assertEqual(pointfree.bind(self.index_of_1)(container), Some(1))


