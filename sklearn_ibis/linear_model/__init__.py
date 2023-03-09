from .linear_regression_ibis import LinearRegressionIbis
from .logistic_regresstion_ibis import LogisticRegressionIbis

__all__ = [
    LinearRegressionIbis,
    LogisticRegressionIbis
]

"""
linear_model.LogisticRegression([penalty, ...])
linear_model.LogisticRegressionCV(*[, Cs, ...])
linear_model.PassiveAggressiveClassifier(*)
linear_model.Perceptron(*[, penalty, alpha, ...])
linear_model.RidgeClassifier([alpha, ...])
linear_model.RidgeClassifierCV([alphas, ...])
linear_model.SGDClassifier([loss, penalty, ...])
linear_model.SGDOneClassSVM([nu, ...])

    linear_model.LinearRegression(*[, ...])
linear_model.Ridge([alpha, fit_intercept, ...])
linear_model.RidgeCV([alphas, ...])
linear_model.SGDRegressor([loss, penalty, ...])

linear_model.ElasticNet([alpha, l1_ratio, ...])
linear_model.ElasticNetCV(*[, l1_ratio, ...])
linear_model.Lars(*[, fit_intercept, ...])
linear_model.LarsCV(*[, fit_intercept, ...])
linear_model.Lasso([alpha, fit_intercept, ...])
linear_model.LassoCV(*[, eps, n_alphas, ...])
linear_model.LassoLars([alpha, ...])
linear_model.LassoLarsCV(*[, fit_intercept, ...])
linear_model.LassoLarsIC([criterion, ...])
linear_model.OrthogonalMatchingPursuit(*[, ...])
linear_model.OrthogonalMatchingPursuitCV(*)

"""