from ..utils.arguments import star_wrap
from .experiment_setup import ExperimentSetup


def create_experiment_setup(data, learners, learner_label, dataset_label, setup_class):
    configs = learners[learner_label]

    return setup_class(learner_label + '__' + dataset_label,
                       data[dataset_label],
                       configs=configs)


def experiment_combinations(data, learners, rejected_combinations=()):
    for dataset in data.keys():
        for learner in learners.keys():
            combination = (data, learners, learner, dataset)
            if combination not in rejected_combinations:
                yield combination


def create_experiment_setups(data, learners, rejected_combinations=(), setup_class=ExperimentSetup):
    return map(star_wrap(create_experiment_setup, setup_class),
               experiment_combinations(data, learners, rejected_combinations))


def map_experiments(function, data, learners, rejected_combinations=()):
    return map(function,
               create_experiment_setups(data, learners, rejected_combinations))


def run_experiments(data, learners, result_dir='__results__', rejected_combinations=()):
    tuple(map_experiments(lambda e: e(result_dir), data, learners, rejected_combinations))


def save_experiments(data, learners, output_dir='__experiments__', rejected_combinations=()):
    tuple(map_experiments(lambda e: e.save(output_dir), data, learners, rejected_combinations))
