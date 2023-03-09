from sklearn.pipeline import Pipeline
from ibis.expr.types import Table
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn_ibis.linear_model import LogisticRegressionIbis
from sklearn_ibis.decomposition import PCAIbis
from sklearn_ibis.preprocessing import StandardScalerIbis
from sklearn_ibis.ibis.ibis_transformer import IbisTransformer


class PipelineIbis:
    def __init__(self, wrapped: Pipeline):
        self.steps = wrapped.steps

    def to_ibis(self):
        def fn(table: Table):

            for step in self.steps:
                step = step[1]

                if isinstance(step, StandardScaler):
                    wrapper = StandardScalerIbis(step)
                elif isinstance(step, LogisticRegression):
                    wrapper = LogisticRegressionIbis(step)
                elif isinstance(step, PCA):
                    wrapper = PCAIbis(step)
                elif isinstance(step, IbisTransformer):
                    wrapper = step
                else:
                    raise Exception(f"No Ibis implemntation found for {type(step)}")

                table = wrapper.to_ibis()(table)

            return table

        return fn