import numpy
import math
import sys, os
import json
import pandas as pd
from collections import defaultdict
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import taxi
import geoutil

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
        output_points = []
        for point in allPoints[:-1]:
            output_points.append({
                "lat":point[1],
                "long":point[0]
            })
        return allPoints[:-1],query
    except Exception as e:
        print("No paths found: "+str(e))
        return [],query

def linear_regression(points):
    """
        calculates linear regression over a set of points [latitude,longitude]
    """
    latitudes = [[i[0]] for i in points]
    longitudes = [[i[1]] for i in points]

    # regression logic
    regr = linear_model.LinearRegression()
    regr.fit(latitudes,longitudes)
    return [[x[0],y[0]] for x,y in zip(latitudes,regr.predict(latitudes))]

def poly_regression(points,precision=8):
    """
        Implementation of polynomal regression
    """
    # return empty lists if input is empty
    if points == []:
        return [],[]

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

    
    # north-south regression
    vertical_predicted_path = []
    transform = poly.fit_transform(longDf)

    reg.fit(transform,latDf)
    predictions = reg.predict(transform)

    for i in range(len(predictions)):
        vertical_predicted_path.append([predictions[i][0],longDf["longitudes"][i]])

    
    # west-east regression
    horizontal_predicted_path = []
    transform = poly.fit_transform(latDf)

    reg.fit(transform,longDf)
    predictions = reg.predict(transform)

    for i in range(len(predictions)):
        horizontal_predicted_path.append([latDf["latitudes"][i], predictions[i][0]])

    # return sorted horizontal and vertical prediction
    return sorted(horizontal_predicted_path, key=lambda k: [k[1], k[0]]), \
            sorted(vertical_predicted_path, key=lambda k: [k[0], k[1]])

def formatting(hpath,vpath,training_set,trajectory):
    """
        Method used to format output data

        hpath - "horizontal" regression prediction
        vpath - "vertical" regression prediction
        training_set - set of all routes used in prediction
        trajectory - distance that was already passed
    """
    # determine direction of trajectory
    regres = linear_regression(trajectory[-10:])

    # path manipulation (filtering, road matching and so on)
    h_subpath = []
    v_subpath = []
    for hcoor in hpath:
        # filter to show only the points within 2 km
        if geoutil.distance(trajectory[-1],hcoor)<2:
            if(len(h_subpath)==11):
                ha=h_subpath[0]
                hb=h_subpath[10]
            h_subpath.append(hcoor)
    for vcoor in vpath:
        if geoutil.distance(trajectory[-1],vcoor)<2:
            if(len(v_subpath)==11):
                va=v_subpath[0]
                vb=v_subpath[10]
            v_subpath.append(vcoor)

    # calculate direction vector prediction
    predicted_path = []
    try:
        deltaX = (hb[0]-ha[0])/4 + (vb[0]-va[0])/4
        deltaY = (hb[1]-ha[1])/4 + (vb[1]-va[1])/4
        dirX = (trajectory[2][0] - trajectory[0][0])/4
        dirY = (trajectory[2][1] - trajectory[0][1])/4
        base_point = trajectory[-1]
        for i in range(20):
            new_point = [base_point[0]+deltaX+dirX,base_point[1]+deltaY+dirY]
            predicted_path.append(new_point)
            base_point = new_point
    except Exception as e:
        print("Predicted trajectory error: "+str(e))

    return {
        "advanced": geoutil.geojson_path_converter(geoutil.roads_matching(predicted_path)),
        "training": geoutil.geojson_path_converter(training_set),
        "optional": geoutil.geojson_path_converter(regres),
        "predicted": geoutil.geojson_path_converter(h_subpath+v_subpath),
        "direction": geoutil.geojson_path_converter(predicted_path)
    }

def main():
    # not used in this application
    print(regress("41.148,-8.585,41.148,-8.585,41.148,-8.585,41.148,-8.585","A"))

if __name__ == '__main__':
    main()