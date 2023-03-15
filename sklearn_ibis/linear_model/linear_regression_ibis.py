from sklearn.linear_model import LinearRegression
from ibis.expr.types import Table
from sklearn_ibis.functions import dot, add


class LinearRegressionIbis:
    def __init__(self, wrapped: LinearRegression):
        self.coefficients = wrapped.coef_
        self.intercept = wrapped.intercept_

    def to_ibis(self):
        def fn(table: Table):
            return add(dot(table, self.coefficients.reshape(-1, 1)), [self.intercept])

        return fn