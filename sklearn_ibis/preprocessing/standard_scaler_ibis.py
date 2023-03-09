from sklearn.preprocessing import StandardScaler
from ibis.expr.types import Table


class StandardScalerIbis():
    def __init__(self, scaler: StandardScaler):
        self.with_mean = scaler.with_mean
        self.with_std = scaler.with_std
        self.mean = scaler.mean_
        self.std = scaler.scale_

    def to_ibis(self):
        def fn(table: Table):
            if self.with_mean:
                exprs = [table[col] - col_mean for col, col_mean in zip(table.columns, list(self.mean))]
                table = table.select(*exprs)

            if self.with_std:
                exprs = [table[col] / col_std for col, col_std in zip(table.columns, list(self.std))]
                table = table.select(*exprs)

            return table

        return fn

