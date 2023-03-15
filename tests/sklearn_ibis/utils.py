from sklearn import datasets
from sklearn.base import ClassifierMixin, RegressorMixin
from sklearn.pipeline import Pipeline
import ibis
import numpy as np


def ibis_and_back(ibis_wrapper, sklearn_impl, args, frame=None):
    for arg in args:
        sklearn_instance = sklearn_impl(**arg)

        last_estimator = sklearn_impl if not issubclass(sklearn_impl, Pipeline) else type(sklearn_instance.steps[-1][1])

        if issubclass(last_estimator, ClassifierMixin):
            fn_dataset = datasets.load_wine
        else:
            fn_dataset = datasets.load_diabetes

        X, y = fn_dataset(as_frame=True, return_X_y=True) if frame is None else frame

        if issubclass(last_estimator, RegressorMixin) or issubclass(last_estimator, ClassifierMixin):
            sklearn_instance.fit(X, y)
        else:
            sklearn_instance.fit(X)

        ibis_instance = ibis_wrapper(sklearn_instance)
        con = ibis.pandas.connect({"X": X})

        df_ibis = ibis_instance.to_ibis()(con.table('X')).execute()

        if issubclass(last_estimator, RegressorMixin) or issubclass(last_estimator, ClassifierMixin):
            df_sklearn = sklearn_instance.predict(X)
            df_sklearn = df_sklearn.reshape((df_sklearn.shape[0], 1))
        else:
            df_sklearn = sklearn_instance.transform(X)

        np.set_printoptions(precision=10)
        if not np.allclose(df_ibis.values, df_sklearn):
            print(df_sklearn[0])
            print("!!!-----------------------!!!")
            print(df_ibis.values[0])
            print(df_sklearn[0] - df_ibis.values[0])

        assert np.allclose(df_ibis.values, df_sklearn)