import pandas as pd
import csv
import math
from MDAnalysis.analysis.psa import hausdorff
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
    while(next(lines) and i < 1000):
        dataset.append(next(lines))
        i+=1
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
        except:
            # error in parsing
            pass
    return numpy.array(ndarraylist)


def containing(points,query,precision=0.001):
    """
        Check if query is contained within given points array
    """
    trim_factor = len(query)+1
    for i in range(len(points)-trim_factor):
        for j in range(len(query)):
            if abs(points[j+i][0]-query[j][0])>precision or abs(points[i+j][1]-query[j][1])>precision:
                break
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
    generate()