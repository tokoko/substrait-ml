import ibis
from sklearn.preprocessing import OneHotEncoder
from ibis.expr.types import Table


# TODO infrequent / unknown
class OneHotEncoderIbis:
    def __init__(self, wrapped: OneHotEncoder):
        self.categories = wrapped.categories_

    def to_ibis(self):
        def fn(table: Table):
            exprs = []
            for i, col in enumerate(table.columns):
                for category_value in list(self.categories[i]):
                    exprs.append(
                        ibis.case().when(table[col] == category_value, 1).else_(0).end().name(f"{col}_{category_value}")
                    )
            return table.select(*exprs)

        return fn
