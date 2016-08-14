# -*- coding: UTF-8 -*-
import pickle, sys

class FeatureLoader():
	def load(self, filepath):
		msg = "Loading data from " + filepath
		print msg
		sys.stdout.write(msg + '\n')
		objs = []
		f = open(filepath, "rb")
		while 1:
			try:
				objs.append(pickle.load(f))
			except EOFError:
				break
		msg = "Finished loading feature data"
		sys.stdout.write(msg + '\n')
		f.close()
		return objs