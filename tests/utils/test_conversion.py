from unittest import TestCase
import numpy as np
import expkit.utils.conversion as conv


class collect_classes_Test(TestCase):
    def test_returns_all_existing_classes_in_an_iterable(self):
        random_labels = np.random.choice(list(range(0, 100)), 1000)

        self.assertEqual(set(range(0, 100)), set(conv.collect_classes(random_labels)))


class label_to_one_hot_Test(TestCase):
    def test_returns_one_hot_vector_corresponding_to_class_index_given_a_label_and_a_label_array(self):
        class_labels = np.array(tuple(range(0, 100)))
        label = np.random.choice(class_labels, 1)[0]

        expected_one_hot = np.zeros((len(class_labels),))
        expected_one_hot[label] = 1

        self.assertTrue(np.array_equal(expected_one_hot, conv.label_to_one_hot(label, class_labels)))


class labels_to_one_hots_Test(TestCase):
    def test_returns_one_hot_vectors_corresponding_to_class_indices_given_labels_and_a_label_array(self):
        class_labels = np.array(tuple(range(0, 100)))
        y = np.random.choice(class_labels, 1000)

        expected_one_hots = np.zeros((len(y), len(class_labels)))
        def put1(one_hot, label):
            one_hot[label] = 1
        tuple(map(lambda ol: put1(ol[0], ol[1]), zip(expected_one_hots, y)))

        self.assertTrue(np.array_equal(expected_one_hots, conv.labels_to_one_hots(y, class_labels)))
