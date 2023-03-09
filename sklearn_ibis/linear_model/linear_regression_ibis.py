from sklearn.linear_model import LinearRegression
from ibis.expr.types import Table


class LinearRegressionIbis:
    def __init__(self, wrapped: LinearRegression):
        self.coefficients = wrapped.coef_.T
        self.intercept = wrapped.intercept_

    def to_ibis(self):
        def fn(table: Table):
            exprs = [table[col] * col_coef for col, col_coef in zip(table.columns, list(self.coefficients))]
            expr = self.intercept

            for e in exprs:
                expr += e

            table = table.select(expr)
            return table

        return fn