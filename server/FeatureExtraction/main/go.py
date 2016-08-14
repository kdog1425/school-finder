# -*- coding: UTF-8 -*-
from FeatureExtractor import FeatureExtractor
from FeatureLoader import FeatureLoader
from FeatureComparator import FeatureComparator
import os
import pickle
import sys
import json

def processFile(x, dir_name, files):
    print dir_name
    print files
    for f in files:
    	path = os.path.join(dir_name, f)
    	if f.startswith('.') or not os.path.isfile(path):
    		continue
    	print 'Processing ' + path
    	fe = FeatureExtractor();
    	fe.setup(path);
    	extractedFeatures = fe.getAllFeatures();
        sys.stdout.write('Finished extracting features!' + "\n")
    	data = {f: extractedFeatures}
    	pickle.dump(data, open( "extracted_features.pickle", "a" ))
		
if __name__ == '__main__':
    # process existing audio files
    # os.path.walk('../data', processFile, 0)

    fe = FeatureExtractor();
    path = sys.argv[1]
    fe.setup(path)
    extractedFeatures = fe.getAllFeatures();
    currFile = {path: extractedFeatures}

    # load features that were extracted from existing files 
    fl = FeatureLoader()
    dirname, filename = os.path.split(os.path.abspath(__file__))
    ground_truth = os.path.join(dirname, 'extracted_features.pickle')
    data = fl.load(ground_truth)

    # compare features between uploaded file and existing files
    fc = FeatureComparator()
    diffList = [] 
    currFileName = currFile.iterkeys().next()
    for d in data:
        dName = d.iterkeys().next()
        sys.stdout.write("Comparing -> " + "\n" +
            currFileName + "\n" +
            dName + "\n")
    	diff = fc.compare(currFile, d)
    	sys.stdout.write("Diff is " + str(diff) + "\n")
        diffList.append((dName, diff))
    sys.stdout.write("Finished Comparing!" + "\n")
    
    # output results
    sys.stdout.write("Final Results:" + "\n")
    diffList.sort(key=lambda x:x[1])
    sortedFileNamesList = []
    for d in diffList:
        sortedFileNamesList.append(d[0])
    sys.stdout.write('finalList&&&' + json.dumps(sortedFileNamesList) + "\n")

    # delete uploaded file
    os.remove(path)
    sys.stdout.write("Deleted " + path + "\n") 
	