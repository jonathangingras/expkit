from unittest import TestCase
import numpy as np
from expkit.experiment.dataset import shuffle_arrays, split_arrays_by_amounts, split_arrays_by_ratio, Dataset


class ShuffleArraysTest(TestCase):
    ARRAY1 = None
    ARRAY2 = None
    ARRAY3 = None


    def setUp(self):
        self.ARRAY1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.ARRAY2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.ARRAY3 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


    def test_shuffling_one_array_is_effective(self):
        a1 = shuffle_arrays(self.ARRAY1)

        self.setUp()
        self.assertNotEqual(self.ARRAY1.tolist(), a1.tolist())
        self.assertEqual(len(self.ARRAY1), len(a1))


    def test_shuffling_two_arrays_results_in_the_same_permutations(self):
        a1, a2 = shuffle_arrays(self.ARRAY1, self.ARRAY2)

        self.assertEqual(a1.tolist(), a2.tolist())


    def test_shuffling_two_arrays_is_effective(self):
        a1, a2 = shuffle_arrays(self.ARRAY1, self.ARRAY2)

        self.setUp()
        self.assertNotEqual(self.ARRAY1.tolist(), a1.tolist())
        self.assertNotEqual(self.ARRAY2.tolist(), a2.tolist())
        self.assertEqual(len(self.ARRAY1), len(a1))
        self.assertEqual(len(self.ARRAY2), len(a2))


    def test_shuffling_three_arrays_results_in_the_same_permutations(self):
        a1, a2, a3 = shuffle_arrays(self.ARRAY1, self.ARRAY2, self.ARRAY3)

        self.assertEqual(a1.tolist(), a2.tolist(), a3.tolist())


    def test_shuffling_three_arrays_is_effective(self):
        a1, a2, a3 = shuffle_arrays(self.ARRAY1, self.ARRAY2, self.ARRAY3)

        self.setUp()
        self.assertNotEqual(self.ARRAY1.tolist(), a1.tolist())
        self.assertNotEqual(self.ARRAY2.tolist(), a2.tolist())
        self.assertNotEqual(self.ARRAY3.tolist(), a3.tolist())
        self.assertEqual(len(self.ARRAY1), len(a1))
        self.assertEqual(len(self.ARRAY2), len(a2))
        self.assertEqual(len(self.ARRAY3), len(a3))


    def test_error_is_raised_when_arrays_not_of_the_same_length(self):
        with self.assertRaises(RuntimeError):
            shuffle_arrays(self.ARRAY1, np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))

        with self.assertRaises(RuntimeError):
            shuffle_arrays(self.ARRAY1, np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))


class SplitArraysByAmountsTest(TestCase):
    def test_splitting_one_array_keeps_right_elements(self):
        a1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        a11, a12 = split_arrays_by_amounts(5, 5, a1)

        self.assertEqual([1, 2, 3, 4, 5], a11.tolist())
        self.assertEqual([6, 7, 8, 9, 10], a12.tolist())


    def test_splitting_two_arrays_keeps_right_elements(self):
        a1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        a2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        (a11, a12), (a21, a22) = split_arrays_by_amounts(5, 5, a1, a2)

        self.assertEqual([1, 2, 3, 4, 5], a11.tolist())
        self.assertEqual([6, 7, 8, 9, 10], a12.tolist())
        self.assertEqual([1, 2, 3, 4, 5], a21.tolist())
        self.assertEqual([6, 7, 8, 9, 10], a22.tolist())


    def test_splitting_two_arrays_which_do_not_have_the_same_length_raises_an_error(self):
        a1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        a2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        a3 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

        with self.assertRaises(RuntimeError):
            split_arrays_by_amounts(5, 5, a1, a2)

        with self.assertRaises(RuntimeError):
            split_arrays_by_amounts(5, 5, a1, a3)


class SplitArraysByRatioTest(TestCase):
    def test_splitting_one_array_keeps_right_elements(self):
        a1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

        a11, a12 = split_arrays_by_ratio(0.66, a1)

        self.assertEqual([1, 2, 3, 4, 5, 6], a11.tolist())
        self.assertEqual([7, 8, 9], a12.tolist())


    def test_splitting_two_arrays_keeps_right_elements(self):
        a1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        a2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        (a11, a12), (a21, a22) = split_arrays_by_ratio(0.5, a1, a2)

        self.assertEqual([1, 2, 3, 4, 5], a11.tolist())
        self.assertEqual([6, 7, 8, 9, 10], a12.tolist())
        self.assertEqual([1, 2, 3, 4, 5], a21.tolist())
        self.assertEqual([6, 7, 8, 9, 10], a22.tolist())


    def test_splitting_two_arrays_which_do_not_have_the_same_length_raises_an_error(self):
        a1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        a2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        a3 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

        with self.assertRaises(RuntimeError):
            split_arrays_by_ratio(0.5, a1, a2)

        with self.assertRaises(RuntimeError):
            split_arrays_by_ratio(0.5, a1, a3)
