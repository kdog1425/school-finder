import sys, os
dirname, filename = os.path.split(os.path.abspath(__file__))
parentFolder = os.path.dirname(dirname)
sys.path.append(os.path.abspath(os.path.join(parentFolder, 'toolbox')))
import audio

class FeatureExtractor():

    def setup(self, filepath):
        sys.stdout.write('FeatureExtractor.setup(): ' + filepath + "\n")
        self.a = audio.Audio(filepath)

    def tearDown(self):

        del self.a

    def getMFCC(self):
        mfcc = self.a.average_mfcc.popitem()
        return mfcc[1].tolist()

    def getAllFeatures(self):
        return self.a.all_features

    def printAllFeatures(self):
        print self.a.all_features
                
