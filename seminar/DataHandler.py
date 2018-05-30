import pandas as pd
import csv
import math

def parse(data):
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
	lines = csv.reader(open(filename, "rb"))
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [parse(x) for x in dataset[i]]
	return dataset

def pointsListConverter(raw):
	raw = raw[2:]
	raw = raw[:-2]
	points = raw.split("], [")
	return points

def generateKey(start,end,precision):
	if(start == "" or end == ""):
		return ""
	start = start.split(", ")
	end = end.split(", ")
	latstart = round(float(start[0]),precision)
	longstart = round(float(start[1]),precision)
	latend = round(float(end[0]),precision)
	longend = round(float(end[1]),precision)
	return str(latstart)+","+str(longstart)+","+str(latend)+","+str(longend)