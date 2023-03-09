from sklearn.decomposition import PCA
from ibis.expr.types import Table


# TODO whiten
class PCAIbis:
    def __init__(self, wrapped: PCA):
        self.mean = wrapped.mean_
        self.components = wrapped.components_

    def to_ibis(self):
        def fn(table: Table):
            exprs = [table[col] - col_mean for col, col_mean in zip(table.columns, list(self.mean))]
            table = table.select(*exprs)

            ac = []

            for component in self.components:
                exprs = [table[col] * col_coef for col, col_coef in zip(table.columns, list(component))]
                expr = 0

                for e in exprs:
                    expr += e

                ac.append(expr)

            table = table.select(*ac)
            return table

        return fn