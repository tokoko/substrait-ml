import pandas as pd
from sklearn_ibis.functions import dot
import ibis
import numpy as np


def test_dot():
    df = pd.DataFrame([
        [1, 2],
        [3, 4],
        [5, 6]], columns=['Col1', 'Col2'])

    other = np.array([[2, 3]]).T

    con = ibis.pandas.connect({"X": df})
    ibis_computed = dot(con.table("X"), other).execute()

    assert np.array_equal(df.dot(other), ibis_computed.values)


def test_dot_2d():
    df = pd.DataFrame([
        [1, 2],
        [3, 4],
        [5, 6]], columns=['Col1', 'Col2'])

    other = np.array([[2, 3], [9, 15]]).T

    con = ibis.pandas.connect({"X": df})
    ibis_computed = dot(con.table("X"), other).execute()

    assert np.array_equal(df.dot(other).values, ibis_computed.values)

