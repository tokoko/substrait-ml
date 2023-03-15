from .utils import ibis_and_back
from sklearn_ibis.ibis import IbisTransformer
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn_ibis.pipeline import PipelineIbis
from ibis.expr.types import Table


def test_pipeline():
    def custom_ibis_transformation(table: Table):
        return table.select(*table.columns[:3])  # Leave first 3 columns

    preprocessor = IbisTransformer(custom_ibis_transformation)
    scaler = StandardScaler()
    pca = PCA()
    logistic = LogisticRegression(max_iter=10000, tol=0.1)

    ibis_and_back(PipelineIbis, Pipeline, [{
        'steps': [
            ("preprocessor", preprocessor),
            ("scaler", scaler),
            ("pca", pca),
            ("logistic", logistic)
        ]
    }])
