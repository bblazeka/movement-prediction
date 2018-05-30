import DataHandler
import numpy
import pandas as pd
from collections import defaultdict
from sklearn import linear_model

data = DataHandler.loadCsv("../data/Porto_taxi_data_training.csv")
# 0th row has only column names
paths = defaultdict(list)

for x in range(1,len(data)):
    points = DataHandler.pointsListConverter(data[x][8])
    key = DataHandler.generateKey(points[0],points[-1],2)
    paths[key].append(points)

query = "-8.61,41.15,-8.63,41.15"

# pass all paths and generate big array of float points
allPoints = numpy.concatenate(paths[query])
latitudes = []
longitudes = []
for point in allPoints:
    point = point.split(", ")
    latitudes.append(float(point[0]))
    longitudes.append(float(point[1]))
# store everything in a dataframe
latDf = pd.DataFrame(numpy.array(latitudes), columns=['latitudes'])
longDf = pd.DataFrame(numpy.array(longitudes), columns=['longitudes'])

# learn how to do regression
reg = linear_model.LinearRegression()
reg.fit(latDf,longDf)
predictions = reg.predict(latDf)
print(predictions)