import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import geoutil
from sumo import SUMO

def predict(input):
    state = input.split(" ")[0]
    sumo = SUMO()
    sumo.parseElements("../data/sumo/osm_bbox.osm.xml")
    sumo.parseRoutes("../data/sumo/osm.passenger.rou.xml")
    sumo.generateMarkov()

    trajectory = sumo.getLatLon(state)
    while(True):
        max = 0
        nextState = ''
        for transition, probability in sumo.markov.items():
            if state == transition[0]:
                if (probability > max):
                    nextState = transition[1]
                if (probability == 1):
                    continue
        if nextState == '':
            break
        else:
            state = nextState
        trajectory += sumo.getLatLon(state)

    return formatting(trajectory)

def formatting(path):
    return {
        "predicted": geoutil.geojson_path_converter(path),
    }

def main():
    print(predict("4610600"))

if __name__ == '__main__':
    main()