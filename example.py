from ibis.expr.types import Table
from sklearn_ibis.ibis import IbisTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn_ibis.pipeline import PipelineIbis
from sklearn.datasets import load_wine
import ibis

pipe = Pipeline(steps=[
    ("preprocessor", IbisTransformer(lambda table: table.select(*table.columns[:6]))),
    ("scaler", StandardScaler()),
    ("pca", PCA()),
    ("logistic", LogisticRegression(max_iter=10000, tol=0.1))
])

X, y = load_wine(as_frame=True, return_X_y=True)
pipe.fit(X, y)

con = ibis.pandas.connect({"X": X})
ibis_plan = PipelineIbis(pipe).to_ibis()(con.table('X'))

print(ibis_plan.execute())
print(ibis_plan.compile())
