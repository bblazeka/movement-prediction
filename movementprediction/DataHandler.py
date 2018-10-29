import pandas as pd
import csv
import math

def parse(data):
	"""
		Used to avoid having integers represented as strings
	"""
	try:
		return int(data)
	except ValueError:
		try:
			return data
		except ValueError:
			return data

def loadCsv(filename):
	"""
		Returns a dataset from a csv file
	"""
	lines = csv.reader(open(filename,"rt", encoding="utf8"))
	i = 0
	dataset = list()
	while(next(lines) and i < 100000):
		dataset.append(next(lines))
		i+=1
	return dataset

def pointsListConverter(raw):
	raw = raw[2:]
	raw = raw[:-2]
	points = raw.split("],[")
	return points

def generateKey(points,precision):
	"""
		Generates a key of a start using a list of points
	"""
	key = ""
	for point in points:
		coors = point.split(",")
		lat = round(float(coors[0]),precision)
		long = round(float(coors[1]),precision)
		key += str(long)+","+str(lat)+","
	# when returning the key, remove the last comma since it is too much
	return key[:-1]