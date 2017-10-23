from sklearn.datasets import load_iris


def iris_train():
    i = load_iris()
    return {"X": i.data[:75], "y": i.target[:75], "feature_names": None}


def iris_test():
    i = load_iris()
    return {"X": i.data[75:], "y": i.target[75:], "feature_names": None}
