import numpy, sys

class FeatureComparator():
	def compare(self, featureDict1, featureDict2):
		sys.stdout.write('FeatureComparator.compare() ' + "\n")
		featureDict1 = featureDict1.itervalues().next()
		featureDict2 = featureDict2.itervalues().next()
		vec1 = []
		vec2 = []
		# retrieve features, flatten into one vector;
		for k, v in featureDict1.items():
			if k not in featureDict2:
				raise
			val1 = v
			val2 = featureDict2[k]
			if (isinstance(v, list)):
				if not (isinstance(val2, list)):
					raise
				
				# current items is a list, in both collections
				val1 = []
				for item in v:
					val1.append(item)
				val2 = []
				for item in featureDict2[k]:
					val2.append(item)
				vec1.extend(val1)
				vec2.extend(val2)
			else:
				vec1.append(val1)
				vec2.append(val2)

		# return distance
		a = numpy.array(vec1)
		b = numpy.array(vec2)
		return numpy.linalg.norm(a-b)

