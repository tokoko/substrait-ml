from .utils import ibis_and_back
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, Binarizer
from sklearn_ibis.preprocessing import StandardScalerIbis, MinMaxScalerIbis, OneHotEncoderIbis, BinarizerIbis
import pandas as pd


def test_standard_scaler():
    ibis_and_back(StandardScalerIbis, StandardScaler, [
        {'with_mean': True, 'with_std': True},
        {'with_mean': True, 'with_std': False},
        {'with_mean': False, 'with_std': True},
        {'with_mean': False, 'with_std': False}
    ])


def test_min_max_encoder():
    ibis_and_back(MinMaxScalerIbis, MinMaxScaler, [
        {'feature_range': (0, 1), 'clip': False},
        {'feature_range': (0, 1), 'clip': True},
        {'feature_range': (1, 2), 'clip': False}
    ])


def test_binarizer():
    ibis_and_back(BinarizerIbis, Binarizer, [
        {'threshold': 10.0},
        {'threshold': -10.0}
    ])


def test_one_hot_encoder():
    ibis_and_back(OneHotEncoderIbis, OneHotEncoder, [{'sparse_output': False}],
     frame=(pd.DataFrame([['male', 'US'], ['female', 'Europe'], ['female', 'Asia']], columns=['Sex', 'Country']), None))



