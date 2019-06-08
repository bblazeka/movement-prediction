import sys, os
import numpy
import traceback
from base import BaseMethod
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import taxi
import geoutil
import sumo

class Instance(BaseMethod):
    
    def __init__(self):
        self.sumo = sumo.SUMO()
        self.sumo.parse_elements("../data/zg/osm_bbox.osm.xml")
        self.sumo.parse_routes("../data/zg/osm.passenger.rou.xml")
        self.sumo.generate_markov()

    def get_similar(self,trajectory):
        """
            returns a route that is most similar
        """
        node_array = self.sumo.convert_trajectory_to_nodearray(taxi.ndarrayConverter(taxi.pointsListConverter(trajectory)))
        self.predicted = self.sumo.convert_nodearray_to_trajectory(self.sumo.longest_common_subsequence(node_array))
        return self.predicted

    def formatting(self,path):
        return {
            "blue": geoutil.geojson_path_converter(path,"instance_based_learning")
        }

def main():
    # test method
    instance = Instance()
    print(instance.get_similar("[[-8.618643,41.141412],[-8.618499,41.141376],[-8.620326,41.14251],[-8.622153,41.143815],[-8.623953,41.144373],[-8.62668,41.144778],[-8.627373,41.144697],[-8.630226,41.14521],[-8.632746,41.14692],[-8.631738,41.148225],[-8.629938,41.150385],[-8.62911,41.151213],[-8.629128,41.15124],[-8.628786,41.152203],[-8.628687,41.152374],[-8.628759,41.152518],[-8.630838,41.15268],[-8.632323,41.153022],[-8.631144,41.154489],[-8.630829,41.154507],[-8.630829,41.154516],[-8.630829,41.154498],[-8.630838,41.154489]]"))

if __name__ == '__main__':
    main()