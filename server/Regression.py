import DataHandler
import numpy
import pandas as pd
from collections import defaultdict
from datetime import datetime
from sklearn import linear_model

data = DataHandler.loadCsv("../data/Porto_taxi_data_training.csv")
# 0th row has only column names
paths = defaultdict(list)

query = "41.15,-8.61,41.15,-8.61,41.15,-8.61"
# depending on the length of a query, set minimum length
min_length = int(len(query.split(","))/2)

for x in range(1,len(data)):
    points = DataHandler.pointsListConverter(data[x][8])
    date_timestamp = datetime.utcfromtimestamp(data[x][5]).strftime('%Y-%m-%d %H:%M:%S')
    if len(points)>min_length:
        key = DataHandler.generateKey(points[:min_length],2)
        paths[key].append(points)

# pass all paths and generate big array of float points
try:
    allPoints = numpy.concatenate(paths[query])
except:
    print("no paths found")
latitudes = []
longitudes = []
for point in allPoints[:-1]:
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
for i in range(len(predictions)):
    if i % 2000 == 0:
        print(str(predictions[i][0])+","+str(latDf["latitudes"][i]))