import os
from collections import defaultdict
import xml.etree.ElementTree as ET
from geoutil import distance, calculate_hausdorff
from util import contains_any_element

class SUMO:

    def __init__(self):
        self.elements = defaultdict(list)
        self.ways = defaultdict(list)
        self.routes = defaultdict(list)

    def parse_elements(self,path):
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

    def parse_routes(self,path):
        """
            Parses the routes in XML and converts them from "way segment" format to a node_id format
        """
        tree = ET.parse(path)
        root = tree.getroot()
        routes = defaultdict(list)
        i = 0
        for child in root:
            if(child.tag == "vehicle"):
                for route in child.iter('route'):
                    routes[i]=self.convert_segments_to_nodes(route.attrib['edges'].split(" "))
                    i+=1
        self.routes = routes

    def get_all_relevant_points(self,query):
        """
            Converts all routes to trajectories and returns all points in dataset
        """
        points = []
        query_nodes = self.convert_trajectory_to_nodearray(query)
        for _,route in self.routes.items():
            if contains_any_element(query_nodes,route):
                trajectory = self.convert_nodearray_to_trajectory(route)
                for point in trajectory:
                    points.append(point)
        return points

    def convert_trajectory_to_nodearray(self,trajectory):
        """
            Convert a trajectory (array of [lat,lon]) to an array of nodes
        """
        node_array = []
        # convert all coordinates to nodes
        for point in trajectory:
            node_array.append(self.get_closest_node(point))
        return node_array

    def convert_nodearray_to_trajectory(self,node_array):
        """
            Converts an array of node ids to an array of lat,lon pairs
        """
        converted = []
        for node in node_array:
            converted.append(self.convert_node_to_coordinate(node))
        return converted

    def convert_segments_to_nodes(self,way_segments):
        """
            Converts an array of [way_id]#[way_position] to array of node_ids
        """
        nodes = []
        for segment in way_segments:
            element = self.node_from_way(segment)
            if(isinstance(element,str)):
                nodes.append(element)
            else:
                nodes.extend(element)
        return nodes

    def convert_node_to_coordinate(self,code):
        """
            Converts an id of a node to a lat,lon pair
        """
        return self.elements[code]

    def convert_waysegment_to_coordinate(self,code):
        """
            Converts an way segment to a lat,lon pair
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

    def coords_from_node(self,code):
        return [self.elements[code]]

    def node_from_way(self,code):
        """
            converts a node identified as [way_id]#[way_position] to node_id format
        """
        scrapped = code.replace("-","").split("#")
        if len(scrapped) > 1:
            return self.ways[scrapped[0]][int(''.join(filter(lambda x: x.isdigit(), scrapped[1])))]
        else:
            return self.ways[scrapped[0]]

    def get_closest_node(self,point):
        """
            Returns the closest node_id to a specific [lon,lat] pair
        """
        min_distance = 1000
        closest_key = ""
        for key,coors in self.elements.items():
            temp_distance = distance(coors,point)
            if temp_distance < min_distance:
                try:
                    condition = self.visits[key] > 2
                except AttributeError:
                    condition = False
                if condition:
                    closest_key = key
                    min_distance = temp_distance
        return closest_key

    def generate_markov(self):
        """
            generates a Markov model for a current SUMO context (existing routes)
        """
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
        self.visits = visits

    def longest_common_subsequence(self,trajectory):
        """
            for a given trajectory, finds a route that has longest common subsequence and returns the best route
        """
        max_length = 0
        best_route = []
        for _,route in self.routes.items():
            m = len(trajectory) 
            n = len(route) 
        
            # declaring the array for storing the dp values 
            L = [[None]*(n + 1) for _ in range(m + 1)] 
        
            """Following steps build L[m + 1][n + 1] in bottom up fashion 
            Note: L[i][j] contains length of LCS of X[0..i-1] 
            and Y[0..j-1]"""
            for i in range(m + 1): 
                for j in range(n + 1): 
                    if i == 0 or j == 0 : 
                        L[i][j] = 0
                    elif trajectory[i-1] == route[j-1]: 
                        L[i][j] = L[i-1][j-1]+1
                    else: 
                        L[i][j] = max(L[i-1][j], L[i][j-1]) 
        
            # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1] 
            if L[m][n] > max_length:
                max_length = L[m][n]
                best_route = route

        return best_route

def main():
    # test method
    sumo = SUMO()
    sumo.parse_elements("../../data/sumo/osm_bbox.osm.xml")
    sumo.parse_routes("../../data/sumo/osm.passenger.rou.xml")
    sumo.generate_markov()

if __name__ == '__main__':
    main()