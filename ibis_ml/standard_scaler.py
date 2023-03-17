from ibis.expr.types import Table
from ibis_ml.functions import subtract, divide


class StandardScaler:
    def __init__(self,
                 with_mean: bool,
                 with_std: bool,
                 mean, ## TODO list types
                 scale ## TODO list types
                 ):
        self.with_mean = with_mean
        self.with_std = with_std
        self.mean = mean
        self.std = scale

    def transform(self, table: Table):
        if self.with_mean:
            table = subtract(table, self.mean)

        if self.with_std:
            table = divide(table, self.std)

        return table

