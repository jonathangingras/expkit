import os
import pickle as pkl
import matplotlib.pyplot as plt
from ...graphics.confusion_matrix import plot_binary_confusion_matrix
from ...graphics.pdf import save_to_pdf
import numpy as np


def save_inpdf(pkl_filepath, file_prefix, graphic_code):
    res = pkl.load(open(pkl_filepath, "rb"))
    save_to_pdf(os.path.join(os.path.dirname(pkl_filepath),
                             os.path.basename(pkl_filepath)[:-4] +
                             file_prefix +
                             ".in" + ".pdf"),
                graphic_code,
                res)


def print_feature_importances(pkl_filepath):
    def graphic(res):
        fi = res["learner"].feature_importances_
        plt.plot(range(len(fi)), fi)
        plt.title(res["experiment_label"])

    save_inpdf(pkl_filepath, ".f_imp", graphic)


def print_confusion_matrix(pkl_filepath):
    def graphic(res):
        cnf_matrix = res["confusion_matrix"]
        title = res["experiment_label"]
        plot_binary_confusion_matrix(cnf_matrix, ["False", "True"], title=title)

    save_inpdf(pkl_filepath, ".cnf_mat", graphic)


def print_cv_heatmaps(pkl_filepath, param_name1, param_name2, **fix_params):
    def graphic(res):
        param_grid = res["configs"]["params"]["param_grid"]
        if len(param_grid) < 2:
            raise RuntimeError("not enough hyper parameter ranges")

        params1 = param_grid[param_name1][::-1]
        param1_mask = res["cv_results"]["param_" + param_name1]
        params2 = param_grid[param_name2]
        param2_mask = res["cv_results"]["param_" + param_name2]
        mean_test_scores = res["cv_results"]["mean_test_score"]

        fix_params_mask = np.ones(len(mean_test_scores)) == 1
        for key, val in fix_params.items():
            fix_params_mask = fix_params_mask & \
                              (res["cv_results"]["param_" + key] == val)

        scores = np.zeros((len(params1), len(params2)))

        for i, ival in enumerate(params1):
            for j, jval in enumerate(params2):
                mask = (param1_mask == ival) & (param2_mask == jval) & fix_params_mask
                scores[i, j] = mean_test_scores[mask]

        plt.imshow(scores, interpolation='nearest')
        plt.ylabel(param_name1)
        plt.xlabel(param_name2)
        plt.colorbar()
        plt.title("{}: {} vs {}, scorer={}".format(res["experiment_label"], param_name1, param_name2, res["configs"]["params"]["scoring"]))
        plt.yticks(np.arange(scores.shape[0]), params1)
        plt.xticks(np.arange(scores.shape[1]), params2, rotation=45)

    save_inpdf(pkl_filepath, ".cv_hmap", graphic)
