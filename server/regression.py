import numpy
import math
import sys, os
import json
import pandas as pd
from collections import defaultdict
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from base import BaseMethod

sys.path.append("./util")
import taxi
import geoutil
import sumo

class Regression(BaseMethod):
    def __init__(self):
        self.training = []
        self.horizontal = []
        self.vertical = []
        self.query = ""

        self.sumo = sumo.SUMO()
        self.sumo.parse_elements("../data/zg/osm_bbox.osm.xml")
        self.sumo.parse_routes("../data/zg/osm.passenger.rou.xml")
        self.sumo.generate_markov()

    def prepare_sumo_data(self,query):
        """
            prepares the training data from sumo format
        """
        # check if input is a string, parse to an array
        if type(query) is str:
            query = geoutil.parse_coords_array(query)
        self.query = query
        try:
            self.training = self.sumo.get_all_relevant_points(query)
            return self.training, self.query
        except Exception as e:
            print("No paths found: "+str(e))
            return [],query

    def prepare_data(self,query,user=0,daytype="A"):
        """
            Prepares the data for regression
        """
        # check if input is a string, parse to an array
        if type(query) is str:
            query = geoutil.parse_coords_array(query)
        
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
                geopoints = geoutil.convert_points(points)
                if taxi.containing(geopoints,query):
                    paths.append(geopoints)

        self.query = query
        # pass all paths and generate big array of float points
        try:
            allPoints = numpy.concatenate(paths)
            output_points = []
            for point in allPoints[:-1]:
                output_points.append({
                    "lat":point[1],
                    "long":point[0]
                })
            self.training = allPoints[:-1]
            return self.training,query
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

    def poly_regression(self,precision=8):
        """
            Calculates polynomal regression variant suitable for needs of our prediction algorithm
        """
        # return empty lists if input is empty
        if self.training == []:
            return [],[]

        latitudes = []
        longitudes = []
        for point in self.training[:-1]:
            latitudes.append(point[0])
            longitudes.append(point[1])    
        # store everything in a dataframe
        latDf = pd.DataFrame(numpy.array(latitudes), columns=['latitudes'])
        longDf = pd.DataFrame(numpy.array(longitudes), columns=['longitudes'])

        # learn how to do regression
        reg = linear_model.LinearRegression()

        # pass the order of your polynomial here  
        poly = PolynomialFeatures(precision)

        
        # regression with latitude as domain
        vertical_predicted_path = []
        transform = poly.fit_transform(longDf)

        reg.fit(transform,latDf)
        predictions = reg.predict(transform)

        for i in range(len(predictions)):
            vertical_predicted_path.append([predictions[i][0],longDf["longitudes"][i]])

        
        # regression with longitude domain
        horizontal_predicted_path = []
        transform = poly.fit_transform(latDf)

        reg.fit(transform,longDf)
        predictions = reg.predict(transform)

        for i in range(len(predictions)):
            horizontal_predicted_path.append([latDf["latitudes"][i], predictions[i][0]])

        self.horizontal = sorted(horizontal_predicted_path, key=lambda k: [k[1], k[0]])
        self.vertical = sorted(vertical_predicted_path, key=lambda k: [k[0], k[1]])
        
        # return sorted horizontal and vertical prediction
        return self.horizontal, self.vertical
            

    def formatting(self):
        """
            Method used to format output data

            hpath - "horizontal" regression prediction
            vpath - "vertical" regression prediction
            training_set - set of all routes used in prediction
            trajectory - distance that was already passed
        """
        trajectory = self.query
        # determine direction of trajectory
        regres = Regression.linear_regression(trajectory[-10:])
        first_point = regres[0]
        last_point = regres[-1]

        # path manipulation (filtering, road matching and so on)
        h_subpath = geoutil.filter_by_longitude(self.horizontal,trajectory[-1],0.005)
        v_subpath = geoutil.filter_by_latitude(self.vertical,trajectory[-1],0.0005)

        # calculate direction vector prediction
        predicted_path = []
        try:
            # remove first third of each regression
            h_start = int(len(h_subpath)/2)
            v_start = int(len(v_subpath)/2)
            base_point = trajectory[-1]
            for i in range(10):
                deltaX = (h_subpath[h_start+i+1][0]-h_subpath[h_start+i][0] + v_subpath[v_start+i+1][0] - v_subpath[v_start+i][0])*2
                deltaY = (h_subpath[h_start+i+1][1]-h_subpath[h_start+i][1] + v_subpath[v_start+i+1][1] - v_subpath[v_start+i][1])*2
                dirX = (last_point[0]-first_point[0])/20
                dirY = (last_point[1]-first_point[1])/20
                new_point = [base_point[0]+(deltaX+dirX),base_point[1]+(deltaY+dirY)]
                predicted_path.append(new_point)
                base_point = new_point
        except Exception as e:
            print("Predicted trajectory error: "+str(e))

        self.predicted = predicted_path

        return {
            "maroon": geoutil.geojson_path_converter(geoutil.roads_matching(predicted_path),"road_matching"),
            "orange": geoutil.geojson_path_converter(self.training,"training"),
            "red": geoutil.geojson_path_converter(regres,"lin regression"),
            "blue": geoutil.geojson_path_converter(h_subpath+v_subpath,"h and v regression"),
            "black": geoutil.geojson_path_converter(predicted_path,"prediction")
        }

def main():
    # test only
    path = "[[15.9533,45.7944],[15.9554,45.7944],[15.9582,45.7943],[15.9590,45.7952],[15.9599,45.7960],[15.9602,45.7972],[15.9609,45.7979],[15.9618,45.7984],[15.9621,45.7991],[15.9636,45.7995],[15.9654,45.7995],[15.9667,45.7996],[15.9679,45.7996],[15.9693,45.7995],[15.9689,45.8007]]"
    regression = Regression()
    regression.prepare_sumo_data(path)
    regression.poly_regression()
    regression.formatting()

if __name__ == '__main__':
    main()