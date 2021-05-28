import numpy as np
from numpy import ma
from scipy.stats import hmean, gmean

def pairwise_ratios(X, Y):
    return ma.masked_array(Y, Y == 0) / ma.masked_array(X, X== 0)


def worst_case_distortion(X, Y, axis=None):
    ratios = pairwise_ratios(X, Y)
    stretched = ratios.max(axis=axis)
    compressed = (1 / ratios).max(axis=axis)
    return stretched * compressed


def average_case_distortion(X, Y, axis=None):
    ratios = pairwise_ratios(X, Y)
    return ratios.mean(axis=axis)


alpha_methods = {
    'min': np.min,
    'hmean': hmean,
    'gmean': gmean,
    'mean': np.mean,
    'max': np.max,
}


def normalized_average_distortion(X, Y, axis=None, alpha_method=None,
                                  alpha_use_axis=False,
                                  ):
    ratios = pairwise_ratios(X, Y)
    calc_alpha = alpha_methods.get(alpha_method, np.min)
    alpha = calc_alpha(ratios, axis=axis if alpha_use_axis else None)
    return ratios.mean(axis=axis) / alpha


def element_wise_normalized_ratios(X, Y):
    ratios = pairwise_ratios(X, Y)
    logratios = np.log2(ratios)
    geom_mean = logratios[np.triu_indices_from(logratios, k=1)].mean()
    logratios -= geom_mean
    np.fill_diagonal(logratios, 0)
    return logratios


def mean_absolute_distortion(X, Y, axis=None):
    logratios = element_wise_normalized_ratios(X, Y)
    if axis is None:
        triu_ratios = logratios[np.triu_indices_from(logratios, k=1)]
        mad = np.abs(triu_ratios).mean()
    else:
        masked_ratios = ma.masked_array(logratios, np.eye(*logratios.shape))
        mad = masked_ratios.mean(axis=axis)
    return mad


distortion_measures = {
    'worst': worst_case_distortion,
    'average': average_case_distortion,
    'normalized_average': normalized_average_distortion,
    'mean_absolute': mean_absolute_distortion,
}


def distortion(X, Y, kind, axis=None, measure_kwargs=None):
    if measure_kwargs is None:
        measure_kwargs = dict()
    measure = distortion_measures[kind]
    result = measure(X, Y, axis=axis, **measure_kwargs)
    if ma.is_masked(result):
        return result.filled()
    return result
