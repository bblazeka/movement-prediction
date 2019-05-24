import sys, os
import numpy
from base import BaseMethod
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import geoutil
import taxi
from sumo import SUMO

class Markov(BaseMethod):

    def __init__(self):
        self.sumo = SUMO()
        self.sumo.parseElements("../data/sumo/osm_bbox.osm.xml")
        self.sumo.parseRoutes("../data/sumo/osm.passenger.rou.xml")
        self.sumo.generate_markov()


    def predict(self,input):
        # set the last point of trajectory to be the initial point of prediction
        if (isinstance(input,numpy.ndarray)):
            state = self.sumo.get_closest_node(input[-1])
        else:
            state = self.sumo.get_closest_node(geoutil.parseCoordinatesArray(input)[-1])
        prevStates = [state]

        trajectory = self.sumo.getLatLonFromNode(state)
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
            trajectory += self.sumo.getLatLonFromNode(state)

        self.predicted = trajectory
        return formatting(trajectory)

def formatting(path):
    return {
        "blue": geoutil.geojson_path_converter(path,"markov_layer"),
    }

def main():
    # test method
    markov = Markov()
    print(markov.predict("4610600"))

if __name__ == '__main__':
    main()