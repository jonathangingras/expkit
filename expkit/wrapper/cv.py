from sklearn.model_selection import GridSearchCV
from .learner import LearnerWrapper, unwrapped


class CVWrapper(LearnerWrapper):
    def __init__(self, estimator_class, *args, cv_strategy_class=GridSearchCV, **kwargs):
        super().__init__(estimator_class, *args, cv_strategy_class=cv_strategy_class, **kwargs)

    @property
    def best_estimator_(self):
        return unwrapped(self).best_estimator_

    @property
    def cv_results_(self):
        return unwrapped(self).cv_results_

    @property
    def best_score_(self):
        return unwrapped(self).best_score_

    @property
    def best_params_(self):
        return unwrapped(self).best_params_
