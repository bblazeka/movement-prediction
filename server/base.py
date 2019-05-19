import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import geoutil

class BaseMethod:
    def __init__(self):
        self.predicted = []

    def get_predict(self):
        return self.predicted

    def get_filtered_predict(self,center,radius):
        filtered = []
        for point in self.predicted:
            if geoutil.distance(point,center)<radius:
                filtered.append(point)
        return filtered
    
def comparison(regression,instance,markov):
    return {
        "blue": geoutil.geojson_path_converter(regression,"regression"),
        "red": geoutil.geojson_path_converter(instance,"instance_based_learning"),
        "black": geoutil.geojson_path_converter(markov,"markov"),
    }
