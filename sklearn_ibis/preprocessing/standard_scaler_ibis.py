from sklearn.preprocessing import StandardScaler
from ibis.expr.types import Table
from sklearn_ibis.functions import subtract, division

class StandardScalerIbis():
    def __init__(self, scaler: StandardScaler):
        self.with_mean = scaler.with_mean
        self.with_std = scaler.with_std
        self.mean = scaler.mean_
        self.std = scaler.scale_

    def to_ibis(self):
        def fn(table: Table):
            if self.with_mean:
                table = subtract(table, self.mean)

            if self.with_std:
                table = division(table, self.std)

            return table

        return fn

