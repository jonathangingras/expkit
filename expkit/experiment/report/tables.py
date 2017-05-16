import pickle as pkl
import itertools
import pandas as pd


def main_outputs_table(filepath):
    res = pkl.load(open(filepath, "rb"))
    cols = [
        "experiment_label",
        "accuracy",
        "precision",
        "recall",
        "f1_score"
    ]
    res = {key: res[key] for key in cols}
    return pd.DataFrame(res, index=(1,))[cols]


def feature_importance_table(filepath):
    p = pkl.load(open(filepath, "rb"))

    cols = p["feature_names"]
    res = {name: p["learner"].feature_importances_[idx] for idx, name in enumerate(cols)}

    ret = pd.DataFrame(data=res, index=(0,))
    ret['experiment_label'] = p["experiment_label"]

    cols = list(itertools.chain(['experiment_label'], cols))

    ret = ret[cols]

    return ret
