import DataHandler
import numpy
import json
import pandas as pd
from collections import defaultdict
from datetime import datetime
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

data = DataHandler.loadCsv("../data/train.csv")
# 0th row has only column names
paths = defaultdict(list)

query = "41.15,-8.61,41.15,-8.61,41.15,-8.61"
daytype = "A"
# A for normal day, B for holiday, C for day before holiday
# depending on the length of a query, set minimum length
min_length = int(len(query.split(","))/2)

for x in range(1,len(data)):
    points = DataHandler.pointsListConverter(data[x][8])
    if data[x][6]==daytype and len(points)>min_length:
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
    point = point.split(",")
    latitudes.append(float(point[0]))
    longitudes.append(float(point[1]))
# store everything in a dataframe
latDf = pd.DataFrame(numpy.array(latitudes), columns=['latitudes'])
longDf = pd.DataFrame(numpy.array(longitudes), columns=['longitudes'])

# learn how to do regression
reg = linear_model.LinearRegression()

# pass the order of your polynomial here  
poly = PolynomialFeatures(6)
transform = poly.fit_transform(latDf)

reg.fit(transform,longDf)
predictions = reg.predict(transform)
predicted_path = []
for i in range(len(predictions)):
    if i % 2000 == 0:
        predicted_path.append({  
            "model":"points.point",
            "pk":i,
            "fields":{  
                "lat":predictions[i][0],
                "long":latDf["latitudes"][i]
            }
        })

with open('points.json', 'w') as outfile:
    json.dump(predicted_path,outfile)