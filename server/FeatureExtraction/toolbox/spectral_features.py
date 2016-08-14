"""
Computation of spectral features 
"""

import numpy as np
import scipy as sp
import audio_operations as ao
from scipy import stats


def spectrum(x):
    """
    Compute the spectrum of the input
    """

    return {'spectrum' : ao.fft(x)}


def energy(spectrum):
    """
    Compute the energy of the spectrum 
    """

    return {'spectral_energy' : (2.0 * np.dot(abs(spectrum),abs(spectrum)) - abs(spectrum[0])**2 - abs(spectrum[-1])**2 ) / (2.0 * (len(spectrum)-1)) }


def flatness(spectrum):
    """
    Compute the flatness of the spectrum, calculated by dividing the 
    geometric mean of the power spectrum by the arithmetic mean of the power spectrum 
    """
   
    f = sp.stats.gmean(abs(spectrum)) / np.mean(abs(spectrum))

    return {'spectral_flatness' : f}


def crestFactor(spectrum):
    """
    Compute the Crest factor, which is a measure of the ratio of peak values to the effective value of the spectrum.
    cf = spectrum_peak/mean(spectrum)
    """

    cf = abs(spectrum)[np.argmax(abs(spectrum))] / np.mean(abs(spectrum))

    return {'spectral_crestFactor' : cf }


def centroid(spectrum, sampleRate):
    """
    Compute the spectral centroid, center of mass (weighted sum) of the spectrum
    """
    
    n = 0
    weightedSumAmp = 0
    sumAmp = 0

    for i in spectrum:    	
        f = n * (sampleRate / 2.0) / len(spectrum) 
        weightedSumAmp = weightedSumAmp + (f * abs(i))
        sumAmp = sumAmp + abs(i)
        n = n + 1
    
    scentroid = (weightedSumAmp * 1.0) / sumAmp        

    return {'spectral_centroid' : scentroid}


def rolloff(spectrum, sampleRate, kappa=0.85):
    """
    Compute the rolloff of the spectrum (usually freq corresponding to 85 per cent of the spectrum)
    """

    absSum   = np.sum(abs(spectrum));
    index  = np.where(np.cumsum(abs(spectrum)) >= kappa*absSum); 

    ro = index[0][0] * (sampleRate / 2.0) / len(spectrum)
    
    return {'spectral_rolloff' : ro}


def spread(spectrum, sampleRate):
    """
    Compute the spread of the spectrum with respect to the centroid, following [JP Bello] 
    """

    scentroid = centroid(spectrum, sampleRate);    
    n = 0
    weightedSumAmp = 0
    sumAmp = 0

    for i in spectrum:    	
        f = n * (sampleRate / 2.0) / len(spectrum) 
        weightedSumAmp = weightedSumAmp + ((f - scentroid['spectral_centroid'])**2 * abs(i))
        sumAmp = sumAmp + abs(i)
        n = n + 1
    
    sspread = np.sqrt((weightedSumAmp * 1.0) / sumAmp)        

    return {'spectral_spread' : sspread}

