import numpy as np


def collect_classes(y):
    return np.array(list(set(y)))


def per_sample_shape(X):
    return np.array(X, copy=False).shape[1:]


def label_to_one_hot(label, classes, dtype=np.float64):
    """
    y:       class label, for e.g. "positive"
    classes: list of classes, for e.g. ["negative", "positive"]
    """
    one_hot = np.zeros((len(classes),), dtype=dtype)
    class_index = np.argmax(np.array(tuple(map(lambda lbl: lbl == label, classes))))
    one_hot[class_index] = 1
    return one_hot


def labels_to_one_hots(y, classes, dtype=np.float64):
    one_hots = np.zeros((len(y), len(classes)), dtype=dtype)

    def apply_ones(label):
        class_index = np.argmax(np.array(tuple(map(lambda lbl: lbl == label, classes))))
        one_hots[y == label, class_index] = 1

    tuple(map(apply_ones, classes))
    return one_hots
