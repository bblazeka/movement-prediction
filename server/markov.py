import sys, os
from base import BaseMethod
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import geoutil
from sumo import SUMO

class Markov(BaseMethod):

    def __init__(self):
        self.sumo = SUMO()
        self.sumo.parseElements("../data/sumo/osm_bbox.osm.xml")
        self.sumo.parseRoutes("../data/sumo/osm.passenger.rou.xml")
        self.sumo.generateMarkov()


    def predict(self,input):
        state = input.split(" ")[0]

        trajectory = self.sumo.getLatLon(state)
        while(True):
            max = 0
            nextState = ''
            for transition, probability in self.sumo.markov.items():
                if state == transition[0]:
                    if (probability > max):
                        nextState = transition[1]
                    if (probability == 1):
                        continue
            if nextState == '':
                break
            else:
                state = nextState
            trajectory += self.sumo.getLatLon(state)

        self.predicted = trajectory
        return formatting(trajectory)

def formatting(path):
    return {
        "blue": geoutil.geojson_path_converter(path),
    }

def main():
    # test method
    markov = Markov()
    print(markov.predict("4610600"))

if __name__ == '__main__':
    main()