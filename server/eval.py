import sys, os
import numpy

from .regression import Regression
from . import instance, markov, base
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import geoutil

class Evaluation:
    def __init__(self,path):
        # regression
        regression = Regression()
        regression.prepare_data(path)
        regression.poly_regression()
        regression.formatting()
        # instance based learning
        ibl = instance.Instance()
        ibl.get_similar(path)
        # markov
        hmm = markov.Markov()
        hmm.predict(path)
        self.input_path = geoutil.parseCoordinatesArray(path)
        self.regression = regression
        self.ibl = ibl
        self.hmm = hmm
    
    def get_evaluations(self,radius=0.5):
        """
            Returns evaluations in certain area
        """
        center = self.input_path[-1]
        input_path = numpy.array(self.input_path)
        reg_filtered = numpy.array(self.regression.get_filtered_predict(center,radius))
        ibl_filtered = numpy.array(self.ibl.get_filtered_predict(center,radius))
        hmm_filtered = numpy.array(self.hmm.get_filtered_predict(center,radius))
        reg_dist = geoutil.calculate_hausdorff(input_path,reg_filtered)
        ibl_dist = geoutil.calculate_hausdorff(input_path,ibl_filtered)
        hmm_dist = geoutil.calculate_hausdorff(input_path,hmm_filtered)
        return {
            "regression": reg_dist,
            "instance": ibl_dist,
            "markov": hmm_dist,
        }
