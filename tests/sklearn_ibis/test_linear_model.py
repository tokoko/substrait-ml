from .utils import ibis_and_back

from sklearn_ibis.linear_model import LinearRegressionIbis, LogisticRegressionIbis
from sklearn.linear_model import LinearRegression, LogisticRegression


def test_linear_regression():
    ibis_and_back(LinearRegressionIbis, LinearRegression, [{}])


def test_logistic_regression():
    ibis_and_back(LogisticRegressionIbis, LogisticRegression, [{'max_iter': 4000}])