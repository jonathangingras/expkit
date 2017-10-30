import numpy as np
from unittest import TestCase
from expkit.utils.arguments import star_wrap


class star_wrap_Test(TestCase):
    VALID_LIST = [ [1, 2] for _ in range(100) ]

    def test_given_a_2_args_function_it_can_splat_arguments_at_call_time(self):
        def somefn(arg1, arg2):
            self.assertEqual(1, arg1)
            self.assertEqual(2, arg2)

        tuple(map(star_wrap(somefn), self.VALID_LIST))


    def test_given_a_n_args_function_it_can_splat_arguments_at_call_time(self):
        n = np.random.choice(list(range(0, 10)), 1)[0]

        def somefn(*args):
            self.assertEqual(n, len(args))

        tuple(map(star_wrap(somefn), [ n * [0] for _ in range(100) ]))


    def test_given_a_n_args_function_it_can_splat_additional_args_at_call_time(self):
        n = np.random.choice(list(range(0, 10)), 1)[0]
        additional_args = ("one", "two", "three")

        def somefn(*args):
            self.assertEqual("one", args[-3])
            self.assertEqual("two", args[-2])
            self.assertEqual("three", args[-1])

        tuple(map(star_wrap(somefn, *additional_args), self.VALID_LIST))
