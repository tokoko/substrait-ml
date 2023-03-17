from sklearn.preprocessing import StandardScaler
from ibis.expr.types import Table
from ibis_ml.standard_scaler import StandardScaler as _StandardScaler


class StandardScalerIbis:
    def __init__(self, scaler: StandardScaler):
        self.impl = _StandardScaler(
            scaler.with_mean,
            scaler.with_std,
            scaler.mean_,
            scaler.scale_
        )

    def to_ibis(self):
        def fn(table: Table):
            return self.impl.transform(table)

        return fn

