import numpy
import sys, os
import json
import pandas as pd
from collections import defaultdict
from datetime import datetime
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import taxi

def regress(query,daytype):
    data = taxi.loadCsv()
    # 0th row has only column names
    paths = defaultdict(list)

    # A for normal day, B for holiday, C for day before holiday
    # depending on the length of a query, set minimum length
    min_length = int(len(query.split(","))/2)

    for x in range(1,len(data)):
        points = taxi.pointsListConverter(data[x][8])
        if data[x][6]==daytype and len(points)>min_length:
            key = taxi.generateKey(points[:min_length],3)
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
    poly = PolynomialFeatures(12)
    transform = poly.fit_transform(latDf)

    reg.fit(transform,longDf)
    predictions = reg.predict(transform)
    predicted_path = []
    for i in range(len(predictions)):
        predicted_path.append({
                    "lat":predictions[i][0],
                    "long":latDf["latitudes"][i]
        })

    return predicted_path

def main():
    print(regress("41.148,-8.585,41.148,-8.585,41.148,-8.585,41.148,-8.585","A"))

if __name__ == '__main__':
    main()