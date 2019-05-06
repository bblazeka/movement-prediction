import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import geoutil

class BaseMethod:
    def __init__(self):
        self.predicted = []

    def get_predict(self):
        return self.predicted
    
def comparison(regression,instance,markov):
    return {
        "blue": geoutil.geojson_path_converter(regression),
        "red": geoutil.geojson_path_converter(instance),
        "black": geoutil.geojson_path_converter(markov),
    }
