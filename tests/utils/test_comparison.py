from expkit.utils.comparison import *
import numpy as np
from unittest import TestCase
from sklearn.metrics import make_scorer, f1_score
import sklearn.metrics.scorer


class AlwaysEqual:
    def __eq__(self, other):
        return True

class NeverEqual:
    pass

class CanBeEqual:
    def __init__(self, integer=1):
        self.integer = integer

    def __eq__(self, other):
        return self.integer == other.integer


class DeepComparisonTest(TestCase):
    def test_never_equal_objects_compare_to_false(self):
        obj1 = {
            1: NeverEqual()
        }
        obj1_copy = {
            1: NeverEqual()
        }

        self.assertFalse(DeepComparison(obj1, obj1_copy))
        self.assertFalse(DeepComparison(obj1_copy, obj1))

    def test_equal_objects_compare_to_true(self):
        obj1 = {
            1: CanBeEqual()
        }
        obj1_copy = {
            1: CanBeEqual()
        }

        self.assertTrue(DeepComparison(obj1, obj1_copy))
        self.assertTrue(DeepComparison(obj1_copy, obj1))

    def test_different_class_objects_compare_to_false(self):
        obj1 = {
            1: AlwaysEqual()
        }
        obj2 = {
            1: CanBeEqual()
        }

        self.assertFalse(DeepComparison(obj1, obj2))
        self.assertFalse(DeepComparison(obj2, obj1))

    def test_equal_numpy_arrays_compare_to_true(self):
        obj1 = {
            1: np.array([1, 2, 3, 4])
        }
        obj2 = {
            1: np.array([1, 2, 3, 4])
        }

        self.assertTrue(DeepComparison(obj1, obj2))
        self.assertTrue(DeepComparison(obj2, obj1))

    def test_non_equal_numpy_arrays_compare_to_false(self):
        obj1 = {
            1: np.array([1, 2, 3, 4])
        }
        obj2 = {
            1: np.array([1, 2, 3, 3])
        }

        self.assertFalse(DeepComparison(obj1, obj2))
        self.assertFalse(DeepComparison(obj2, obj1))

    def test_equal_complex_dicts_compare_to_true(self):
        dict1 = {'scorer': make_scorer(f1_score), 'param_grid': {'gamma': np.array([ 0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9]), 'kernel': ['linear', 'rbf'], 'C': np.array([ 0.1,  0.3,  0.5,  0.7,  0.9,  1.1,  1.3])}}
        dict2 = {'scorer': make_scorer(f1_score), 'param_grid': {'gamma': np.array([ 0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9]), 'kernel': ['linear', 'rbf'], 'C': np.array([ 0.1,  0.3,  0.5,  0.7,  0.9,  1.1,  1.3])}}

        self.assertTrue(DeepComparison(dict1, dict2))
