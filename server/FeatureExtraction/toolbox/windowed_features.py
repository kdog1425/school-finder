"""
Computation of windowed features such as STFT, CQ, MFCCs over the entire song, etc.
"""

import math
import numpy as np
import scipy as sp
from scipy import signal
import audio_operations as ao
import temporal_features as tf


def mfcc(spectrogram, freqs, n=26, p=13, lowF = 0, highF = 4000):
	"""
	Computes the MFCC for a given spectrogram
	spectrogram is the spectral energy over time
	freqs must be sorted increasingly, and correspond to the rows of spectrogram
	n is the number of mel frequency bands
	p is the number of MFCC coefficients to be returned
	"""

	def mel2freq(mel):
		return 700*(np.exp(mel/float(1125))-1)
	def freq2mel(freq):
		return 1125*np.log(1+freq/float(700))
	def melfilters(freqs, lowF, highF):
		F = np.zeros((freqs.size, n), dtype=float)
		lowM = freq2mel(lowF)
		highM = freq2mel(highF)
		interval = (highM-lowM)/float(n+1)
		freqpoints = [mel2freq(lowM+j*interval) for j in range(0, n+2)]
		for j in range(0, n):
			for i in range(0, freqs.size):
				if freqs[i] < freqpoints[j] or freqs[i] > freqpoints[j+2]:
					F[i,j] = 0
				else:
					if freqs[i] <= freqpoints[j+1]:
						F[i,j] = (freqs[i]-freqpoints[j])/(freqpoints[j+1]-freqpoints[j])
					else:
						F[i,j] = (freqpoints[j+2]-freqs[i])/(freqpoints[j+2]-freqpoints[j+1])
		return F
	filters = melfilters(freqs, lowF, highF)
	logmelspectrum = np.log(np.dot(spectrogram, filters)+0.0000001)
	out = np.array([ao.dct(logmelspectrum[i,::]) for i in range(0,logmelspectrum.shape[0])])
	return {'mfccs' : out[::, 0:p]}


def stft(x, fs, hop, width):
	"""
	Compute the Short Time Fourier Transform of 'x', with sample rate 'fs' (Hz), window width 'width' (samples), and hop length 'hop' (samples)
	Ideally, width is even (this works better with the FFT)
	"""
	window = sp.hanning(width)
	out = sp.array([ao.fft(window*x[i:i+width]) for i in range(0, len(x)-width, hop)])
	times = np.arange(width/float(2*fs), len(x)/float(fs)-width/float(2*fs), hop/float(fs))
	freqs = fs*sp.array([i/float(width) for i in range(0, width/2+1)])
	return {'stft' : out, 'times' : times, 'frequencies' : freqs}


def scqt(x, fs, hop, width=None, minFreq=440/float(16), maxFreq=float(440*32), bins=12, resolution=1):
	"""
	Compute the Sampled Constant Q Transform of the input
	'width' is only important only to determine the time of the first sample, in order for the times to be the same as in stft
	"""
	if width is None:
		width = 2*hop
	samples = np.arange(width/float(2), len(x)-hop, width/float(2))
	times = samples/float(fs)
	n = samples.size

	minFreq = float(minFreq)
	maxFreq = float(maxFreq)

	Q = 1/(math.pow(2, 1/float(bins))-1) * resolution

	nfreqs = int(bins*np.log2(maxFreq/minFreq))
	freqs = np.array([minFreq*math.pow(2, (k/float(bins))) for k in range(0, nfreqs)])
	cq = np.zeros((n, nfreqs), dtype=complex)
	Nx = x.size

	for k in range(0, nfreqs):
		f = freqs[k]
		Ni = Q*fs/f
		N = float(np.round(Ni))
		w = np.hamming(N)*np.exp(-2*np.pi*1j*Q*np.arange(0, N)/Ni)/N
		half = np.floor(N/2)
		if Nx>=N:
			convol = np.zeros(n, dtype=complex)
			for i in range(0,n):
				if samples[i]-half>=0:
					if samples[i]-half+N<=Nx:
						convol[i] = np.sum(w*x[samples[i]-half:samples[i]-half+N:1])
					else:
						endw = Nx-(samples[i]-half)
						convol[i] = np.sum(w[0:endw:1]*x[samples[i]-half:Nx:1])
				else:
					startw = -(samples[i]-half)
					convol[i] = np.sum(w[startw:N:1]*x[0:samples[i]-half+N:1])
		else: # x is too short to estimate the strength of this low a frequency
			convol=np.zeros(n,dtype=complex)
		cq[:,k]= convol

	return {'scqt' : cq, 'times' : times, 'frequencies' : freqs}


def loudness(x, sampleRate, width = 8192):
    """
    Compute loudness according to a direct implementation based on a time-frequency decomposition, a mapping
    from db SPL to Phon followed by a mapping to the Sone scale. 
    From http://www.bic.mni.mcgill.ca/~marcs/res/Loudness_dafx04.pdf (first approach).
    From ENHANCED MODIFIED BARK SPECTRAL DISTORTION (EMBSD): AN OBJECTIVE SPEECH QUALITY MEASURE BASED ON 
    AUDIBLE DISTORTION AND COGNITION MODEL (see annex).
    """
    
    #Calibration
    SPLmeas = 70.0
    Pref = 20.e-6
    y_refscaled = np.divide(x, Pref)
    RMS = tf.rms(y_refscaled)
    SPLmat = 20 * np.log10(RMS['rms'])
    c = 10**((SPLmeas - SPLmat) / 20.0)
    ycal = c * y_refscaled

    #EMBSD quality measure
    NFFT = width
    Bf = np.arange(1,19)
    f, Yxx = sp.signal.welch(ycal, fs=sampleRate, nperseg=NFFT, window=sp.signal.get_window('hanning', NFFT), nfft=NFFT)
    Yxx_scale = 2.0 * Yxx / NFFT

    bark = [0, 100, 200, 300, 400, 510, 630, 770, 920, 1080, 1270, 1480, 1720, 2000, 2320, 2700, 3150, 3700, 4400]
    B_XX = np.zeros(18)

    for i in range(2,19):    
        B_XX[i-2] = sum( Yxx_scale[np.logical_and(bark[i-2] <= f, f<bark[i-1])] )
    spread = np.zeros([Bf.size,Bf.size])

    for i in Bf:
        for j in Bf:
            powVal = ( 15.81 + 7.5 * ( (i-j) + 0.474 ) - 17.5 * pow ( pow ( 1 + ( (i-j) + 0.474 ), 2), 0.5)) / 10
            spread[i-1,j-1] = 10**powVal
    C_XX = np.dot(spread,B_XX[:,np.newaxis])    

    eqlcon = \
    np.matrix('12,7,4,1,0,0,0,-0.5,-2,-3,-7,-8,-8.5,-8.5,-8.5;\
    20,17,14,12,10,9.5,9,8.5,7.5,6.5,4,3,2.5,2,2.5;\
    29,26,23,21,20,19.5,19.5,19,18,17,15,14,13.5,13,13.5;\
    36,34,32,30,29,28.5,28.5,28.5,28,27.5,26,25,24.5,24,24.5;\
    45,43,41,40,40,40,40,40,40,39.5,38,37,36.5,36,36.5;\
    53,51,50,49,48.5,48.5,49,49,49,49,48,47,46.5,45.5,46;\
    62,60,59,58,58,58.5,59,59,59,59,58,57.5,57,56,56;\
    70,69,68,67.5,67.5,68,68,68,68,68,67,66,65.5,64.5,64.5;\
    79,79,79,79,79,79,79,79,78,77.5,76,75,74.5,73,73;\
    89,89,89,89.5,90,90,90,89.5,89,88.5,87,86,85.5,84,83.5;\
    100,100,100,100,100,99.5,99,99,98.5,98,96,95,94.5,93.5,93;\
    112,112,112,112,111,110.5,109.5,109,108.5,108,106,105,104.5,103,102.5;\
    122,122,121,121,120.5,120,119,118,117,116.5,114.5,113.5,113,111,110.5')
    
    phonList = np.matrix('0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0')
    T = 10.0 * np.log10(C_XX[3:18])
    P_XX = np.zeros(15)
    
    for i in range(0,15):
        j = 0
        while T[i] >= eqlcon[j,i] and j<12:

            j+=1
            I = np.where(T[i] <= np.array(eqlcon[:,i]))
            if min(I[0]) == 1:
                P_XX[i] = phonList[0,0]
            else:
                t1 = (T[i] - eqlcon[j-1,i]) / (eqlcon[j,i] - eqlcon[j-1,i]);
                P_XX[i] = phonList[0,j-1] + t1*(phonList[0,j] - phonList[0,j-1])

    S_XX = np.zeros(15)

    for i in range(0,15):
        if P_XX[i] >= 40:
            S_XX[i] = ((P_XX[i] - 40)/10)**2
        else:
            S_XX[i] = (P_XX[i]/40.0)**2.642

    N_mbsd = np.sum(S_XX)

    return {'loudness' : N_mbsd} 
    


