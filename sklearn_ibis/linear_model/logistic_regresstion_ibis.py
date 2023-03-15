import ibis.expr.operations
from sklearn.linear_model import LogisticRegression
from ibis.expr.types import Table
from sklearn_ibis.functions import dot, argmax, add


# TODO refactor
# TODO implement predict_proba
class LogisticRegressionIbis:
    def __init__(self, wrapped: LogisticRegression):
        self.coefficients = wrapped.coef_
        self.intercept = wrapped.intercept_

    def to_ibis(self):
        def fn(table: Table):
            return argmax(add(dot(table, self.coefficients.T), self.intercept))

        return fn