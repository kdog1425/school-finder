"""
Computation of the moments of a vector of numbers
"""

import numpy as np
import scipy as sp


def mean(x):
    """
    Compute the first moment of the signal
    """

    return np.mean(x)


def variance(x):
    """
    Compute the second moment of the signal
    """

    return np.var(x)


def skewness(x):
    """
    Compute the third moment of the signal
    """

    return sp.stats.skew(x)


def kurtosis(x):
    """
    Compute the fourth moment of the signal
    """

    return sp.stats.kurtosis(x)

