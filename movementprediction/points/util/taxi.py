import pandas as pd
import csv
import math
from MDAnalysis.analysis.psa import hausdorff
import numpy

folder = "../data/PortoTaxi/train.csv"
distances = "../../../data/PortoTaxi/distances.csv"
groups = "../../../data/PortoTaxi/groups.csv"

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
    while(next(lines) and i < 500000):
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


def generateKey(points,precision):
    """
        Generates a key of a start using a list of points
    """
    key = ""
    for point in points:
        coors = point.split(",")
        lat = round(float(coors[0]),precision)
        long = round(float(coors[1]),precision)
        key += str(long)+","+str(lat)+","
    # when returning the key, remove the last comma since it is too much
    return key[:-1]

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

    # grouping threshold set to < 0.2
    with open(distances, 'w', newline='') as csvfile, open(groups, 'w', newline='') as csvgroups:
        output_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        groups_writer = csv.writer(csvgroups, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for x in range(1,len(data)):
            points = trajectories[x]
            neighbours = []
            for y in range(1,len(data)):
                if x == y:
                    continue
                other_trajectory = trajectories[y]
                try:
                    distance = hausdorff(points,other_trajectory)
                    output_writer.writerow([x,y,distance])
                    if distance < 0.05:
                        neighbours.append(y)
                except:
                    output_writer.writerow([x,y,'nan'])
            groups_writer.writerow([x,neighbours])


if __name__ == '__main__':
    generate()