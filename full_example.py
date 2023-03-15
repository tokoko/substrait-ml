from sklearn_ibis.ibis import IbisTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn_ibis.pipeline import PipelineIbis
from sklearn.datasets import load_wine
import ibis
from substrait_c.algebra.relations import RootRelation
from ibis_substrait.compiler.core import SubstraitCompiler

pipe = Pipeline(steps=[
    ("preprocessor", IbisTransformer(lambda table: table.select(*table.columns[:6]))),
    ("scaler", StandardScaler()),
    ("pca", PCA()),
    # ("logistic", LogisticRegression(max_iter=10000, tol=0.1))
])

X, y = load_wine(as_frame=True, return_X_y=True)

X = X[['alcohol', 'malic_acid', 'ash']]

pipe.fit(X, y)

con = ibis.pandas.connect({"X": X})
ibis_plan = PipelineIbis(pipe).to_ibis()(con.table('X'))

print(X.iloc[0]['alcohol'])
print(ibis_plan.execute().iloc[0])

plan = SubstraitCompiler().compile(ibis_plan.compile().unbind())

root = RootRelation(plan.relations[0].root, plan.extensions)
root.compile_cffi('substrait_example')

inp = {'alcohol': X.iloc[0]['alcohol'], 'malic_acid': X.iloc[0]['malic_acid'], 'ash': X.iloc[0]['ash']}
print(f'Called with {inp}')
res = root.execute_cffi(inp)
print(f'Returned {res}')