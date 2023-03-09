from .min_max_scaler_ibis import MinMaxScalerIbis
from .standard_scaler_ibis import StandardScalerIbis
from .binarizer_ibis import BinarizerIbis
from .one_hot_encoder_ibis import OneHotEncoderIbis
__all__ = [
    BinarizerIbis,
    MinMaxScalerIbis,
    OneHotEncoderIbis,
    StandardScalerIbis
]

"""
    preprocessing.Binarizer(*[, threshold, copy])
preprocessing.FunctionTransformer([func, ...])
preprocessing.KBinsDiscretizer([n_bins, ...])
preprocessing.KernelCenterer()
preprocessing.LabelBinarizer(*[, neg_label, ...])
preprocessing.LabelEncoder()
preprocessing.MultiLabelBinarizer(*[, ...])
preprocessing.MaxAbsScaler(*[, copy])
    preprocessing.MinMaxScaler([feature_range, ...])
preprocessing.Normalizer([norm, copy])
    preprocessing.OneHotEncoder(*[, categories, ...])
preprocessing.OrdinalEncoder(*[, ...])
preprocessing.PolynomialFeatures([degree, ...])
preprocessing.PowerTransformer([method, ...])
preprocessing.QuantileTransformer(*[, ...])
preprocessing.RobustScaler(*[, ...])
preprocessing.SplineTransformer([n_knots, ...])
    preprocessing.StandardScaler

"""