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

    def __init__(self):
        self.sumo = SUMO()
        self.sumo.parse_elements("../data/zg/osm_bbox.osm.xml")
        self.sumo.parse_routes("../data/zg/osm.passenger.rou.xml")
        self.sumo.generate_markov()

    def training(self):
        destinations = []
        i = 0
        for _,route in self.sumo.routes.items():
            destinations.append(self.sumo.convert_node_to_coordinate(route[-1]))
        destination_data = pd.DataFrame(destinations,columns=['lat','lon'])
        clustering.clustering_by_location(destination_data)

    def predict(self,input):
        # set the last point of trajectory to be the initial point of prediction
        if (isinstance(input,numpy.ndarray)):
            state = self.sumo.get_closest_node(input[-1])
        else:
            state = self.sumo.get_closest_node(geoutil.parse_coords_array(input)[-1])
        prevStates = [state]

        trajectory = self.sumo.coords_from_node(state)
        while(True):
            max = 0
            nextState = ''
            # iterate over all transitions in the markov model
            for transition, probability in self.sumo.markov.items():
                if state == transition[0]:
                    if (probability > max):
                        max = probability
                        nextState = transition[1]
                    if (probability == 1):
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
    markov.training()

if __name__ == '__main__':
    main()