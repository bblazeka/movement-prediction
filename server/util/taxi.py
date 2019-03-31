import pandas as pd
import csv
import math
from MDAnalysis.analysis.psa import hausdorff
from pymongo import MongoClient
import numpy

folder = "../data/PortoTaxi/train.csv"
distances = "../data/PortoTaxi/distances.csv"
groups = "../data/PortoTaxi/groups.csv"

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

def loadCsv():
    """
        Returns a dataset from a csv file
    """
    lines = csv.reader(open(folder,"rt", encoding="utf8"))
    i = 0
    dataset = list()
    for line in lines:
        dataset.append(line)
        i+=1
        if(i>10000):
            break
    return dataset

def loadMongo():
    """
        Read data from mongo database into a dataset
    """
    client = MongoClient("127.0.0.1:27017")
    db=client.movementprediction
    collection=db['things']
    cursor=collection.find({})
    for document in cursor:
        print(document)
    # currently, it only prints all documents, it should be converted to returning an array
    # or csv loader should return json

def loadRelated(id):
    """
        Returns a dataset of trajectories that are from the same user
    """
    # reading similar routes ids from csv
    similar_routes = csv.reader(open(groups,"rt", encoding="utf8"))
    # file with exact trajectories of all routes
    lines = csv.reader(open(folder,"rt", encoding="utf8"))

    dataset = list()
    filtered = list()
    # find a list of similar routes to the input route
    for line in similar_routes:
        if int(line[0]) == id:
            filtered = [int(x) for x in line[1][1:-1].split(", ")]
            break
    i=0
    last_element = filtered[-1]
    # add similar routes to the dataset
    for line in lines:
        i+=1
        if i in filtered:
            dataset.append(line)
        if i > last_element:
            break
    return dataset

def pointsListConverter(raw):
    raw = raw[2:]
    raw = raw[:-2]
    points = raw.split("],[")
    return points

def ndarrayConverter(data):
    """
        Converts a list of strings to ndarray
    """
    ndarraylist = []
    for point in data:
        try:
            ndarraylist.append([float(point.split(",")[0]),float(point.split(",")[1])])
        except Exception as e:
            # parsing error, probably is the list empty
            pass
    return numpy.array(ndarraylist)


def containing(points,query,precision=0.001):
    """
        Check if query is contained within given points array
    """
    # remove first third of the query when generating a pattern
    pattern = query[int(len(query)/2):]
    # take subsets of points and check if they are equal to the query
    for i in range(len(points)-(len(query)+1)):
        # iterate over each point in both lists and return True if they are equal
        for j in range(len(pattern)):
            if abs(points[j+i][0]-pattern[j][0])>precision or abs(points[i+j][1]-pattern[j][1])>precision:
                break
            if j+1 == len(pattern):
                return True
    return False

def starting(points,query,precision=0.001):
    """
        Check if query is the start of points array
    """
    for i in range(len(query)):
        if abs(points[i][0]-query[i][0])>precision or abs(points[i][1]-query[i][1])>precision:
            break
        return True
    return False

def parseCoordinatesArray(array):
    """
        Convert array in string representation to an actual array of coordinates
    """
    coordinates = []
    for coor in array[2:-2].split("],["):
        coordinates.append(coor)
    return convertPoints(coordinates)

def convertPoints(points):
    """
        Converts an array from string to float coordinates
    """
    geo_points = []
    for point in points:
        coors = point.split(",")
        lat = float(coors[0])
        long = float(coors[1])
        geo_points.append([lat,long])
    return geo_points

def calculate_hausdorff(A,B):
    """
        Returns hausdorff distance or 1000 if input is empty
    """
    if len(A) == 0 or len(B) == 0:
        return 1000.0
    else:
        return hausdorff(A,B)

def generate():
    """
        Generates groups of similar paths
        https://www.mdanalysis.org/docs/documentation_pages/analysis/psa.html
    """
    data = loadCsv()
    trajectories = dict()
    # 0th row has only column names
    for x in range(1,len(data)):
        trajectories[x] = ndarrayConverter(pointsListConverter(data[x][8]))

    # grouping
    with open(distances, 'w', newline='') as csvfile, open(groups, 'w', newline='') as csvgroups:
        output_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        groups_writer = csv.writer(csvgroups, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        distances_dict = dict()
        for x in range(1,len(data)):
            points = trajectories[x]
            neighbours = []
            for y in range(1,len(data)):
                if x == y:
                    continue
                try:
                    # check if already calculated in opposite order
                    distance = distances_dict[(y,x)]
                except:
                    other_trajectory = trajectories[y]
                    try:
                        distance = hausdorff(points,other_trajectory)
                        distances_dict[(x,y)] = distance
                    except:
                        output_writer.writerow([x,y,'nan'])
                # grouping threshold
                if distance < 0.05:
                        neighbours.append(y)
                output_writer.writerow([x,y,distance])                        
            groups_writer.writerow([x,neighbours])


if __name__ == '__main__':
    mongo = loadMongo()