from sklearn.decomposition import PCA
from ibis.expr.types import Table
from sklearn_ibis.functions import dot

# TODO whiten
class PCAIbis:
    def __init__(self, wrapped: PCA):
        self.mean = wrapped.mean_
        self.components = wrapped.components_

    def to_ibis(self):
        def fn(table: Table):
            # TODO when in subtract needed???
            # exprs = [table[col] - col_mean for col, col_mean in zip(table.columns, list(self.mean))]
            # table = table.select(*exprs)

            return dot(table, self.components.T)

        return fn