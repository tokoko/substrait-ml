import ibis.expr.operations
from sklearn.linear_model import LogisticRegression
from ibis.expr.types import Table


# TODO refactor
# TODO implement predict_proba
class LogisticRegressionIbis:
    def __init__(self, wrapped: LogisticRegression):
        self.coefficients = wrapped.coef_.T
        self.intercept = wrapped.intercept_

    def to_ibis(self):
        def fn(table: Table):
            exprs = []
            for i, intercept in enumerate(list(self.intercept)):
                coefficients = self.coefficients[:,i]
                coef_exprs = [table[col] * col_coef for col, col_coef in zip(table.columns, list(coefficients))]
                expr = intercept

                for e in coef_exprs:
                    expr += e

                exprs.append(expr)

            search_max_expr = ibis.case()

            for i, expr in enumerate(exprs):
                cond = True
                for j, other in enumerate(exprs):
                    if i != j:
                        cond = cond & (expr > other)

                search_max_expr = search_max_expr.when(cond, i)

            table = table.select(search_max_expr.end())
            return table

        return fn