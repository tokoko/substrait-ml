from sklearn.preprocessing import MinMaxScaler
from ibis.expr.types import Table


class MinMaxScalerIbis:
    def __init__(self, wrapped: MinMaxScaler):
        self.scale = wrapped.scale_
        self.min = wrapped.min_
        self.clip = wrapped.clip

    def to_ibis(self):
        def fn(table: Table):
            exprs = [table[col] * col_scale for col, col_scale in zip(table.columns, list(self.scale))]
            table = table.select(*exprs)

            exprs = [table[col] + col_min for col, col_min in zip(table.columns, list(self.min))]
            table = table.select(*exprs)

            if self.clip: # TODO implement and test clip
                pass

            return table

        return fn