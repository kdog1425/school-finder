"""
Computation of temporal features 
"""

import math


def zcr(x):
    """
    Compute the Zero Crossing Rate of the input
    """
    
    count = 0
    numSamples = len(x)

    for i in range(1, numSamples):
        if (x[i] * x[i-1]) < 0:
            count = count + 1
    
    count = count / (1.0 * (numSamples - 1))

    return {'zcr' : count}


def rms(x):
    """
    Compute the root-mean-squared amplitude, i.e., the square root of 
    the arithmetic mean of the squares of the values
    """

    count = 0
    numSamples = len(x)

    for i in range(0, numSamples):
        count = count + abs(x[i]) ** 2
    
    count = count / (1.0 * numSamples)
        
    return {'rms' : math.sqrt(count)}