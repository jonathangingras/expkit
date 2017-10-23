from expkit.experiment import run_experiments, save_experiments
from expkit.dispatch.slurm import dispatch_experiments
from expkit.experiment.result_producers import apply_classification_metrics
from sklearn.ensemble import AdaBoostClassifier
from data import *


data = {
    "iris": {
        "train": iris_train,
        "test": iris_test
    }
}


learners = {
    "AdaBoostClassifier": {
        "class": AdaBoostClassifier,
        "producers": [
            apply_classification_metrics
        ],
        "dispatch": {
            "email": "hello@me.com"
        }
    }
}


if __name__ == '__main__':
    dispatch_experiments(data, learners, common_job_options={
        "gpus_per_node": 2,
        "modules": [
            "somemodule"
        ],
        "previous_commands": [
            "cd"
        ]
    })
