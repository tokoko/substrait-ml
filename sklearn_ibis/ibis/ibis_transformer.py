from sklearn.base import BaseEstimator, TransformerMixin
import ibis


class IbisTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, plan):
        self.fn_ibis_plan = plan

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        con = ibis.pandas.connect({"X": X})
        return self.fn_ibis_plan(con.table('X')).execute()

    def to_ibis(self):
        return self.fn_ibis_plan