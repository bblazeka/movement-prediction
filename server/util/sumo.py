import os
from collections import defaultdict
import xml.etree.ElementTree as ET

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

    def getLatLon(self,code):
        nodes = []
        scrapped = code.replace("-","").split("#")
        if len(scrapped) > 1:
            # we are looking for a specific segment
            nodes.append(self.elements[self.ways[scrapped[0]][int(scrapped[1])]])
        else:
            # we take whole element in
            for node in self.ways[scrapped[0]]:
                nodes.append(self.elements[node])
        return nodes

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
                visits[current]+=1
                transitions[current,next]+=1

        # calculate all probabilities
        for transition,count in transitions.items():
            probabilites[transition]=count/visits[transition[0]]

        self.markov = probabilites