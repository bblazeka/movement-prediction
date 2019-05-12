import sys, os
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
        self.sumo.generateMarkov()


    def predict(self,input):
        state = self.sumo.getClosest(taxi.parseCoordinatesArray(input)[-1])
        prevStates = [state]

        trajectory = self.sumo.getLatLonFromNode(state)
        while(True):
            max = 0
            nextState = ''
            for transition, probability in self.sumo.markov.items():
                if state == transition[0]:
                    if (probability > max):
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