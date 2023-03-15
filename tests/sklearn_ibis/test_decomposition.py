from .utils import ibis_and_back

from sklearn_ibis.decomposition import PCAIbis
from sklearn.decomposition import PCA


def test_pca():
    ibis_and_back(PCAIbis, PCA, [{}])