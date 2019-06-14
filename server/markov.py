import sys, os
import numpy
import pandas as pd
from base import BaseMethod
import clustering
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import geoutil
import taxi
from sumo import SUMO

class Markov(BaseMethod):

    def __init__(self,mode):
        self.sumo = SUMO()
        self.sumo.parse_elements("../data/"+mode+"/osm_bbox.osm.xml")
        self.sumo.parse_routes("../data/"+mode+"/osm.passenger.rou.xml")
        self.sumo.generate_markov()

    def prob_l_c(self,l,c):
        """
            Trips traversing l in cluster c / trips in cluster c
        """
        try:
            return self.matrix[c][l] / len(self.clusters[c])
        except:
            return 0

    def prob_c_l(self,c,l):
        """
            trips traversing l in cluster c / trips passing via l
        """
        total = 0
        for i in range(len(self.matrix)):
            try:
                total+=self.matrix[i][l]
            except:
                continue
        try:
            return self.matrix[c][l] / total
        except:
            return 0

    def train(self):
        """
            Training Markov through building link-cluster co-occurence matrix
        """
        destinations = []
        i = 0
        for _,route in self.sumo.routes.items():
            destinations.append(self.sumo.convert_node_to_coordinate(route[-1]))
        destination_data = pd.DataFrame(destinations,columns=['lat','lon'])
        self.clusters = clustering.clustering_by_location(destination_data)
        self.matrix = [{} for i in range(len(self.clusters))]
        for key,route in self.sumo.routes.items():
            cluster = clustering.get_cluster_id(self.clusters,key)
            for point in route:
                try:
                    self.matrix[cluster][point]+=1
                except:
                    self.matrix[cluster][point]=1

    def cluster_probabilities(self,input):
        """
            Calculates the probability of input belonging to a certain cluster
        """
        if (isinstance(input,numpy.ndarray) == False):
            input = geoutil.parse_coords_array(input)
        n = len(self.matrix)
        probabilities = [1] * n
        first_node = self.sumo.get_closest_node(input[0])
        for i in range(n):
            probabilities[i] = self.prob_c_l(i,first_node)
        for point in input[1:]:
            node = self.sumo.get_closest_node(point)
            for i in range(n):
                probabilities[i] *= self.prob_l_c(node,i)
        return probabilities.index(max(probabilities))
        
    def predict(self,input):
        """
            Generates a prediction for given input
        """
        cluster = self.cluster_probabilities(input)
        # set the last point of trajectory to be the initial point of prediction
        if (isinstance(input,numpy.ndarray)):
            input_array = input
        else:
            input_array = geoutil.parse_coords_array(input)
        prevStates = []
        for coor in input_array:
            prevStates.append(self.sumo.get_closest_node(coor))

        state = prevStates[-1]
        trajectory = self.sumo.coords_from_node(state)
        while(True):
            max = 0
            nextState = ''
            # iterate over all transitions in the markov model
            for transition, probability in self.sumo.markov.items():
                try:
                    if state == transition[0] and self.matrix[cluster][transition[1]]>0 and not (transition[1] in prevStates):
                        if (probability > max):
                            max = probability
                            nextState = transition[1]
                        if (probability == 1):
                            continue
                except:
                    continue
            if nextState == '' or nextState == state or (nextState in prevStates):
                break
            else:
                prevStates.append(state)
                state = nextState
            trajectory += self.sumo.coords_from_node(state)

        self.predicted = trajectory
        return formatting(trajectory)

def formatting(path):
    return {
        "blue": geoutil.geojson_path_converter(path,"markov_layer"),
    }

def main():
    # test method
    markov = Markov()
    markov.train()
    input = "[[15.95322,45.79300],[15.95324,45.79371],[15.95416,45.79425],[15.95608,45.79421],[15.95743,45.79420],[15.95850,45.79413],[15.95911,45.79455],[15.95939,45.79488],[15.95980,45.79579],[15.96042,45.79665],[15.96099,45.79747],[15.96150,45.79825],[15.96204,45.79905],[15.96301,45.79930],[15.96461,45.79935],[15.96594,45.79943]]"
    cluster = markov.cluster_probabilities(input)
    print(markov.predict(input,cluster))

if __name__ == '__main__':
    main()