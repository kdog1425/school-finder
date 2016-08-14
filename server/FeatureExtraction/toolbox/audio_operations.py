"""
Basic signal operations, including autocorrelation, fft and dct
"""

import numpy as np
import scipy.fftpack as fftpack

def fft(timeframe):
	"""
	Computes the FFT of the input
	Works for real-valued timeframe
	ifft is the inverse of fft only if timeframe has an even length
	"""
	
	fftspectrum = np.fft.rfft(timeframe)
	
	return fftspectrum

def ifft(fftspectrum):
	"""
	Computes the inverse FFT of the input
	Uses just the n/2+1 first samples of the FFT spectrum, assuming that timeframe is real-valued
	Note that this is exact only if the timeframe has an even length.
	"""
	
	timeframe = np.fft.irfft(fftspectrum)
	
	return timeframe

def dct(timeframe):
	"""
	Compute the DCT of the input
	"""
	
	dctspectrum = fftpack.dct(timeframe, type = 2, norm = 'ortho')
	
	return dctspectrum

def idct(dctspectrum):
	"""
	Compute the inverse IDCT of the input
 	"""

	timeframe = fftpack.idct(dctspectrum, type = 2, norm = 'ortho')

	return timeframe

def autocorr(timeframe):
	"""
	Compute the unnormalized autocorrelation of the input
	"""

	result = np.correlate(timeframe, timeframe, mode='full')
	autocorrelation = result[result.size/2:]

	return autocorrelation

