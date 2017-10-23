from sklearn.model_selection import GridSearchCV
from .learner import LearnerWrapper


class CVWrapper(LearnerWrapper):
    def __init__(self, estimator_class, cv_strategy_class=GridSearchCV, **kwargs):
        self.wrapped = cv_strategy_class(estimator=estimator_class(), **kwargs)

    @property
    def best_estimator_(self):
        return self.wrapped.best_estimator_

    @property
    def cv_results_(self):
        return self.wrapped.cv_results_

    @property
    def best_score_(self):
        return self.wrapped.best_score_

    @property
    def best_params_(self):
        return self.wrapped.best_params_
