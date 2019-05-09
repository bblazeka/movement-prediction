import os
from collections import defaultdict
import xml.etree.ElementTree as ET
from geoutil import distance

class SUMO:

    def __init__(self):
        self.elements = []
        self.ways = []
        self.routes = []

    def parseElements(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        elements = defaultdict(list)
        ways = defaultdict(list)
        for child in root:
            if(child.tag == "node"):
                elements[child.attrib["id"]] = [float(child.attrib["lon"]),float(child.attrib["lat"])]
            elif(child.tag == "way"):
                nodes = []
                for nd in child.iter('nd'):
                    nodes.append(nd.attrib['ref'])
                ways[child.attrib["id"]]=nodes
        self.elements = elements
        self.ways = ways

    def parseRoutes(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        routes = defaultdict(list)
        for child in root:
            if(child.tag == "vehicle"):
                for route in child.iter('route'):
                    routes[child.attrib["id"]]=route.attrib['edges'].split(" ")
        self.routes = routes

    def convertToLatLonRoute(self,route):
        """
            Converts an array of node ids to an array of lat,lon pairs
        """
        converted = []
        for node in route:
            converted.push(getLatLon(node))
        return converted

    def getLatLon(self,code):
        """
            Converts an id of a node to a lat,lon pair
        """
        nodes = []
        scrapped = code.replace("-","").split("#")
        if len(scrapped) > 1:
            # we are looking for a specific segment
            nodes.append(self.elements[self.ways[scrapped[0]][int(scrapped[1].replace('AddedOnRampEdge',''))]])
        else:
            # we take whole element in
            for node in self.ways[scrapped[0]]:
                nodes.append(self.elements[node])
        return nodes

    def getLatLonFromNode(self,code):
        return [self.elements[code]]

    def getNodeFromWay(self,code):
        """
            if we have node identified as [way_id]#[way_position], it returns node_id
        """
        scrapped = code.replace("-","").split("#")
        if len(scrapped) > 1:
            return self.ways[scrapped[0]][int(''.join(filter(lambda x: x.isdigit(), scrapped[1])))]
        else:
            return self.ways[scrapped[0]]

    def getClosest(self,point):
        """
            Returns the closest node to a specific [lon,lat] pair
        """
        min_distance = 1000
        closest_key = ""
        for key,coors in self.elements.items():
            temp_distance = distance(coors,point)
            if temp_distance < min_distance and self.visits[key] > 4:
                closest_key = key
                min_distance = temp_distance
        return closest_key

    def generateMarkov(self):
        # count of transitions between states
        transitions = defaultdict(int)
        # count of total visits of each state
        visits = defaultdict(int)
        # probabilities of transitions
        probabilites = defaultdict(int)
        
        # iterate over all routes, count visits and transitions in training
        for _,route in self.routes.items():
            for current, next in zip(route[:-1], route[1:]):
                start = self.getNodeFromWay(current)
                end = self.getNodeFromWay(next)
                if(type(start)!=list and type(end)!=list):
                    visits[self.getNodeFromWay(current)]+=1
                    transitions[self.getNodeFromWay(current),self.getNodeFromWay(next)]+=1

        # calculate all probabilities
        for transition,count in transitions.items():
            probabilites[transition]=count/visits[transition[0]]

        self.markov = probabilites
        self.visits = visits

def main():
    # test method
    sumo = SUMO()
    sumo.parseElements("../../data/sumo/osm_bbox.osm.xml")
    sumo.parseRoutes("../../data/sumo/osm.passenger.rou.xml")
    sumo.generateMarkov()

if __name__ == '__main__':
    main()