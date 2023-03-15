from sklearn.preprocessing import MinMaxScaler
from ibis.expr.types import Table
from sklearn_ibis.functions import multiply, add


# TODO implement and test clip
class MinMaxScalerIbis:
    def __init__(self, wrapped: MinMaxScaler):
        self.scale = wrapped.scale_
        self.min = wrapped.min_
        self.clip = wrapped.clip

    def to_ibis(self):
        def fn(table: Table):
            return add(multiply(table, self.scale), self.min)

        return fn
