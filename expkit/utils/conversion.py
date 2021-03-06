import numpy as np


def collect_classes(y):
    if isinstance(y, np.ndarray) and len(y.shape) > 1:
        cy = np.ascontiguousarray(y).view(np.dtype((np.void, y.dtype.itemsize * y.shape[1])))
        _, idx = np.unique(cy, return_index=True)
        return y[idx]

    return np.array(list(set(y)))


def per_sample_shape(X):
    return np.array(X, copy=False).shape[1:]


def one_hots_to_indices(one_hots):
    return np.array(list(map(np.argmax, one_hots)))


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
