from sklearn.preprocessing import Binarizer
from ibis.expr.types import Table
import ibis


class BinarizerIbis:
    def __init__(self, wrapped: Binarizer):
        self.threshold = wrapped.threshold

    def to_ibis(self):
        def fn(table: Table):
            exprs = [ibis.case().when(table[col] > self.threshold, 1).else_(0).end().name(col)
                     for col in table.columns]
            table = table.select(*exprs)

            return table

        return fn
