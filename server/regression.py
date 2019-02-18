import numpy
import math
import sys, os
import json
import pandas as pd
from collections import defaultdict
from datetime import datetime
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from mapbox import MapMatcher
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import taxi

def prepare_data(query,user=0,daytype="A"):
    """
        Prepares the data for regression
    """
    
    # check if input is a string, parse to an array
    if type(query) is str:
        query = taxi.parseCoordinatesArray(query)
    
    # load data
    if user == 0:
        data = taxi.loadCsv()
    else:
        data = taxi.loadRelated(user)
    
    # 0th row has only column names
    paths = list()

    # A for normal day, B for holiday, C for day before holiday
    # depending on the length of a query, set minimum length
    min_length = len(query)/2

    for x in range(1,len(data)):
        points = taxi.pointsListConverter(data[x][8])
        if data[x][6]==daytype and len(points)>min_length:
            # convert data to array of tuples of float values
            geopoints = taxi.convertPoints(points)
            if taxi.containing(geopoints,query):
                paths.append(geopoints)

    # pass all paths and generate big array of float points
    try:
        allPoints = numpy.concatenate(paths)
    except:
        print("no paths found")

    output_points = []
    for point in allPoints[:-1]:
        output_points.append({
            "lat":point[1],
            "long":point[0]
        })

    return allPoints[:-1],query[-10:]

def poly_regression(points,precision=8):
    """
        Implementation of polynomal regression
    """
    latitudes = []
    longitudes = []
    for point in points[:-1]:
        latitudes.append(point[0])
        longitudes.append(point[1])    
    # store everything in a dataframe
    latDf = pd.DataFrame(numpy.array(latitudes), columns=['latitudes'])
    longDf = pd.DataFrame(numpy.array(longitudes), columns=['longitudes'])

    # learn how to do regression
    reg = linear_model.LinearRegression()

    # pass the order of your polynomial here  
    poly = PolynomialFeatures(precision)
    transform = poly.fit_transform(latDf)

    reg.fit(transform,longDf)
    predictions = reg.predict(transform)
    ending_path = []

    
    predicted_path = []
    for i in range(len(predictions)):
        predicted_path.append([latDf["latitudes"][i],predictions[i][0]])
    sorted_path = sorted(predicted_path, key=lambda k: [k[1], k[0]])

    return sorted_path

def formatting(path,start):
    """
        Method used to format output data, remove part of the prediction that was already passed
    """
    # path manipulation (filtering, road matching and so on)
    filtered_path = []
    for coordinate in path:
        if start[0][0] > coordinate[0]:
            if(len(filtered_path)==5):
                a=filtered_path[0]
                b=filtered_path[4]
            filtered_path.append(coordinate)

    # calculate direction vector
    deltaX = b[0]-a[0]
    deltaY = b[1]-a[1]
    dirX = start[1][0] - start[0][0]
    dirY = start[1][1] - start[0][1]
    base_point = start[-1]
    predicted_path = []
    for i in range(10):
        new_point = [base_point[0]+deltaX+dirX,base_point[1]+deltaY+dirY]
        predicted_path.append(new_point)
        base_point = new_point


    # formatting to be compatible with the map   
    formatted_path = []
    for coordinate in predicted_path:
        formatted_path.append({
            "lat":coordinate[1],
            "long":coordinate[0]
        })

    return formatted_path

def roads_matching(sorted_path):
    """
        ALPHA VERSION: not sure it works
    """
    return_path = []
    # api can only take in 100 points at the time
    for _ in range(1):

        values = []
        prev = datetime(2018,10,10,11,34,59)
        for _ in range(len(sorted_path)):
            min = str('%02d' % prev.minute)
            sec = str('%02d' % prev.second)
            values.append(str(prev.year)+"-"+str(prev.month)+"-"+str(prev.day)+"T"+str(prev.hour)+":"+min+":"+sec+"Z")
            prev = prev + timedelta(0,5)

        line = {
        "type": "Feature",
        "properties": {
            "coordTimes": {}
        },
        "geometry": {
            "type": "LineString",
            "coordinates": sorted_path[:100]}}

        service = MapMatcher(access_token="pk.eyJ1IjoiYnJhbmNhIiwiYSI6ImNqbnliMmVoeTA1MTMzcG54Y3h2bnFtYmwifQ.o6CzepqOg00rpv7wKNeOuQ")
        response = service.match(line, profile='mapbox.driving')
        max = 0
        best = 0
        try:
            features = response.geojson()['features']
            for i in range(len(features)):
                if len(features[i]['geometry']['coordinates'])>max and features[i]['properties']['confidence'] > 0.1:
                    max = len(features[i]['geometry']['coordinates'])
                    best = i

            corrected = response.geojson()['features'][best]['geometry']['coordinates']

            for corr in corrected:
                return_path.append(corr)
        except Exception as e:
            print(e)

    return return_path

def main():
    # not used in this application
    print(regress("41.148,-8.585,41.148,-8.585,41.148,-8.585,41.148,-8.585","A"))

if __name__ == '__main__':
    main()