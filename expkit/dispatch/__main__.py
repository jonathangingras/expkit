import sys
import pickle as pkl


if __name__ == "__main__":
    experiment_path = sys.argv[1]
    results_dir = sys.argv[2]

    with open(experiment_path, "rb") as f:
        experiment = pkl.load(f)

    experiment(results_dir)
