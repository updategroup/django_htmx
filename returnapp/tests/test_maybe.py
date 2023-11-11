from django.test import TestCase
from typing import Optional, TypeVar
from returns.maybe import Maybe, maybe, Some, Nothing
from dataclasses import dataclass

"""
map, apply, bind, bind_optional, lash, do, value_or, or_else_call, unwrap, failure, from_value, from_optional
"""

@dataclass
class User:
    id: int
    name: str

    def get_balance(self):
        return Balance(user=self)


@dataclass
class Balance:
    user: User = None

    def credit_amount(self):
        return 12


def choose_discount(credit: int):
    return 10

@maybe
def number(num: int) -> Optional[int]:
    if num:
        return num
    else:
        return None

def mappable(string: str) -> str:
    return string + 'b'

class ReturnCase(TestCase):

    def test_case_old(self):
        user: User = User(id=1, name="John")

        # user: Optional[User] = Maybe.from_optional(user)
        discount_program: Optional['DiscountProgram'] = None

        if user is not None:
            balance = user.get_balance()
            if balance is not None:
                credit = balance.credit_amount()
                if credit is not None and credit > 0:
                    discount_program = choose_discount(credit)
        # print(discount_program)

        # Type hint here is optional, it only helps the reader here:

    def test_case_new(self):
        user: User = User(id=1, name="John")
        discount_program: Maybe['DiscountProgram'] = Maybe.from_optional(
            user,
        ).bind_optional(  # This won't be called if `user is None`
            lambda real_user: real_user.get_balance(),
        ).bind_optional(  # This won't be called if `real_user.get_balance()` is None
            lambda balance: balance.credit_amount(),
        ).bind_optional(  # And so on!
            lambda credit: choose_discount(credit) if credit > 0 else None,
        )
        # print(discount_program)
        # print(discount_program.unwrap())

    def test_decor_maybe(self):
        _ValueType = TypeVar('_ValueType', covariant=True)
        print("test__numb___", number(1))
        print(Maybe.from_optional(1).value_or(None))

        print(Maybe.do(x for x in [8,2,3]))
        assert Maybe.from_optional(1).value_or(None) == 1
        assert Maybe.from_optional(None).value_or(None) == None

    def test_maybe_map(self):
        """
        Composes successful container with a pure function.
        https://viblo.asia/p/javascript-ham-thuan-khiet-pure-function-la-gi-OeVKBqz05kW
        """
        self.assertEqual(Some('a').map(mappable), Some("ab"), "should be ab")
        self.assertEqual(Nothing.map(mappable), Nothing, "should be nothing")

    def test_apply(self):
        """
        Calls a wrapped function in a container on this container.
        Wrapper function là một function có mục đích chính là gọi hàm thứ hai
        """
        self.assertEqual(Some('a').apply(Some(mappable)), Some("ab"), "should be ab")
        self.assertEqual(Nothing.apply(Nothing), Nothing, "should be nothing")
        self.assertEqual(Nothing.apply(Some(mappable)), Nothing, "should be nothing")
        self.assertEqual(Nothing.apply(Nothing), Nothing, "should be nothing")


    @staticmethod
    def bind_able(string: str) -> Maybe[str]:
        return Some(string + 'b')
    def test_bind(self):
        """Composes successful container with a function that returns a container."""
        self.assertEqual(Some('a').bind(self.bind_able), Some("ab"), "should be ab")
        self.assertEqual(Nothing.bind(self.bind_able), Nothing, "should be nothing")

    @staticmethod
    def bin_optional(string: str) -> Optional[int]:
        return len(string) if string else None

    def test_bind_optional(self):
        """Binds a function returning an optional value over a container."""
        self.assertEqual(Some('a').bind_optional(self.bin_optional), Some(1), "should be 1")
        self.assertEqual(Nothing.bind_optional(self.bin_optional), Nothing, "should be nothing")


