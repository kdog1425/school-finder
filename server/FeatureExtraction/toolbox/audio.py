"""""""""""""""""""""""""""""""""""""""""""""""""""
Audio class
Operations with audio files (wav)
"""""""""""""""""""""""""""""""""""""""""""""""""""

import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile
import windowed_features as wf
import spectral_features as sf
import temporal_features as tf
import moments as mo
import logs
 

class Audio():

    def __init__(self,filename,widthSecs=float(2048)/float(44100),hopSecs=float(1024)/float(44100)):

        self.filename = filename
        self.open()

        # Frequency transform
        self.__spectrum = None

        # Windowed transforms
        self.__stft = None                   # The short time Fourier transform
        self.__scqt = None                   # The sampled constant-Q transform
        self.__mfcc = None                   # MFCC features

        # Time domain features
        self.__zcr = None                    # Zero-crossing rate
        self.__rms = None                    # Root-mean-squared (proportional to the spectral energy after squaring)
        self.__time_mean = None              # Mean of the time domain signal
        self.__time_variance = None          # Variance of the time domain signal
        self.__time_skewness = None          # Skewness of the time domain signal
        self.__time_kurtosis = None          # Kurtosis of the time domain signal

        # Spectral features
        self.__spectral_centroid = None      # Spectral centroid
        self.__spectral_mean = None          # Spectral mean
        self.__spectral_variance = None      # Spectral variance
        self.__spectral_skewness = None      # Spectral skewness
        self.__spectral_kurtosis = None      # Spectral kurtosis
        self.__spectral_flatness = None      # Spectral flatness
        self.__spectral_crestFactor = None   # Spectral crest factor
        self.__spectral_rolloff = None       # Spectral roll-off
        self.__spectral_spread = None        # Spectral spread
        self.__spectral_energy = None        # Spectral energy

        # MFCC features
        self.__average_mfcc = None           # The MFCC features averaged over the song

        # Loudness
        self.__loudness = None               # Loudness

        # Default parameters for the windowed features
        self.width = 2*int(widthSecs*self.sampleRate/2) # Ensuring it is an even number, which ensures that audio_operations.fft and audio_operations.ifft are each other's inverses
        self.hop = int(hopSecs*self.sampleRate)

        # Logger
        self.logger = logs.logger
        self.logger.info('creating an instance of Audio from source ' + filename)


    def open(self):
        """
        Open an audio file (wav)
        """
        
        sampleRate, samples = scipy.io.wavfile.read(self.filename)

        samples = samples.astype('float32') / 32767.0

        # Get left channel
        if len(samples.shape) > 1:
            samples = np.mean(samples, axis=1)

        self.samples = samples
        self.sampleRate = sampleRate
        self.channels = 1
        self.duration = samples.shape[0]/float(sampleRate)

    @property
    def all_features(self):
        out = {}
        out.update(self.time_domain_features)
        out.update(self.frequency_domain_features)
        out.update(self.average_mfcc)
        out.update(self.loudness)
        return out

    #================= Frequency representation =================
    @property
    def spectrum(self):
        if self.__spectrum is None:
            self.__spectrum = sf.spectrum(self.samples)
            self.logger.info('Computed spectrum from ' + self.filename)

        return self.__spectrum

    #================= Windowed features and transforms =========
    @property
    def stft(self):
        if self.__stft is None:
            self.__stft = wf.stft(self.samples, self.sampleRate, self.hop, self.width)
            self.logger.info('Computed stft from ' + self.filename)
        return self.__stft

    @property
    def scqt(self):
        if self.__scqt is None:
            self.__scqt = wf.scqt(self.samples, self.sampleRate, self.hop)
            self.logger.info('Computed scqt from ' + self.filename)
        return self.__scqt

    @property
    def mfcc(self):
        if self.__mfcc is None:
            self.__mfcc = wf.mfcc(np.square(np.abs(self.stft['stft'])), self.stft['frequencies'])
            self.__mfcc.update({'times' : self.stft['times']})
            self.logger.info('Computed mfcc from ' + self.filename)
        return self.__mfcc

    #================= Time domain features =====================
    @property
    def time_domain_features(self):
        out = {}
        out.update(self.zcr)
        out.update(self.rms)
        out.update(self.time_mean)
        out.update(self.time_variance)
        out.update(self.time_skewness)
        out.update(self.time_kurtosis)
        return out

    @property
    def zcr(self):
        if self.__zcr is None:
            self.__zcr = tf.zcr(self.samples)
            self.logger.info('Computed zcr from ' + self.filename)
        return self.__zcr 

    @property
    def rms(self):
        if self.__rms is None:
            self.__rms = tf.rms(self.samples) 
            self.logger.info('Computed rms from ' + self.filename)
        return self.__rms          

    @property
    def time_mean(self):
        if self.__time_mean is None:
            self.__time_mean = {'time_mean' : mo.mean(self.samples)}
            self.logger.info('Computed time_mean from ' + self.filename)
        return self.__time_mean

    @property
    def time_variance(self):
        if self.__time_variance is None:
            self.__time_variance = {'time_variance' : mo.variance(self.samples) }
            self.logger.info('Computed time_variance from ' + self.filename)
        return self.__time_variance

    @property
    def time_skewness(self):
        if self.__time_skewness is None:
            self.__time_skewness = {'time_skewness' : mo.skewness(self.samples) }
            self.logger.info('Computed time_skewness from ' + self.filename)
        return self.__time_skewness

    @property
    def time_kurtosis(self):
        if self.__time_kurtosis is None:
            self.__time_kurtosis = {'time_kurtosis' : mo.kurtosis(self.samples) }
            self.logger.info('Computed time_kurosis from ' + self.filename)
        return self.__time_kurtosis


    #================= Frequency domain features ================

    @property
    def frequency_domain_features(self):
        out = {}
        out.update(self.spectral_centroid)
        out.update(self.spectral_mean)
        out.update(self.spectral_variance)
        out.update(self.spectral_skewness)
        out.update(self.spectral_kurtosis)
        out.update(self.spectral_flatness)
        out.update(self.spectral_crestFactor)
        out.update(self.spectral_rolloff)
        out.update(self.spectral_spread)
        out.update(self.spectral_energy)
        return out

    @property
    def spectral_centroid(self):
        if self.__spectral_centroid is None:
            self.__spectral_centroid = sf.centroid(self.spectrum['spectrum'], self.sampleRate)
            self.logger.info('Computed spectral_centroid from ' + self.filename)
        return self.__spectral_centroid

    @property
    def spectral_mean(self):
        if self.__spectral_mean is None:
            self.__spectral_mean = {'spectral_mean' : mo.mean(abs(self.spectrum['spectrum'])) }
            self.logger.info('Computed spectral_mean from ' + self.filename)
        return self.__spectral_mean

    @property
    def spectral_variance(self):
        if self.__spectral_variance is None:
            self.__spectral_variance = {'spectral_variance' : mo.variance(abs(self.spectrum['spectrum'])) }
            self.logger.info('Computed spectral_variance from ' + self.filename)
        return self.__spectral_variance

    @property
    def spectral_skewness(self):
        if self.__spectral_skewness is None:
            self.__spectral_skewness = {'spectral_skewness' : mo.skewness(abs(self.spectrum['spectrum'])) }
            self.logger.info('Computed spectral_skewness from ' + self.filename)
        return self.__spectral_skewness

    @property
    def spectral_kurtosis(self):
        if self.__spectral_kurtosis is None:
            self.__spectral_kurtosis = {'spectral_kurtosis' : mo.kurtosis(abs(self.spectrum['spectrum'])) }
            self.logger.info('Computed spectral_kurtosis from ' + self.filename)
        return self.__spectral_kurtosis

    @property
    def spectral_flatness(self):
        if self.__spectral_flatness is None:
            self.__spectral_flatness = sf.flatness(self.spectrum['spectrum'])
            self.logger.info('Computed spectral_flatness from ' + self.filename)
        return self.__spectral_flatness

    @property
    def spectral_crestFactor(self):
        if self.__spectral_crestFactor is None:
            self.__spectral_crestFactor = sf.crestFactor(self.spectrum['spectrum'])
            self.logger.info('Computed spectral_crestFactor from ' + self.filename)
        return self.__spectral_crestFactor

    @property
    def spectral_rolloff(self):
        if self.__spectral_rolloff is None:
            self.__spectral_rolloff = sf.rolloff(self.spectrum['spectrum'], self.sampleRate)
            self.logger.info('Computed spectral_rolloff from ' + self.filename)
        return self.__spectral_rolloff

    @property
    def spectral_spread(self):
        if self.__spectral_spread is None:
            self.__spectral_spread = sf.spread(self.spectrum['spectrum'], self.sampleRate)
            self.logger.info('Computed spectral_spread from ' + self.filename)
        return self.__spectral_spread

    @property
    def spectral_energy(self):
        if self.__spectral_energy is None:
            self.__spectral_energy = sf.energy(self.spectrum['spectrum'])
            self.logger.info('Computed spectral_energy from ' + self.filename)
        return self.__spectral_energy


    #================= MFCC features ============================
    @property
    def average_mfcc(self):
        if self.__average_mfcc is None:
            self.__average_mfcc = {'average_mfccs' : np.mean(self.mfcc['mfccs'], axis=0).tolist()}
            self.logger.info('Computed average_mfccs from ' + self.filename)
        return self.__average_mfcc


    #================= Loudness =================================
    @property
    def loudness(self):
        if self.__loudness is None:
            self.__loudness = wf.loudness(self.samples, self.sampleRate)
            self.logger.info('Computed loudness from ' + self.filename)
        return self.__loudness


    #================= Plotting functions =======================
    def plotInTime(self, signal, yRange=1):
        """
        Plot the signal in the time domain. Standard audio signals are supposed to be in the interval [-1,1]  
        """

        plt.plot(signal)
        plt.xlim(0, len(signal))
        plt.ylim(-yRange, yRange)
        plt.show()


    def plotInFreq(self, signal):
        """
        Plot the absolute value of the given signal in the frequency domain 
        """

        plt.plot(abs(signal))
        plt.xlim(0, len(signal))
        plt.show()


if __name__ == "__main__":

    a = Audio('../test/test.wav')
    print a.duration
    print a.channels
    print a.sampleRate

