import sys, os
import numpy

from .regression import Regression
from . import instance, markov, base
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import geoutil

class Evaluation:
    def __init__(self,path):
        self.input_path = geoutil.parse_coords_array(path)
        self.regression = Regression()
        self.ibl = instance.Instance()
        self.hmm = markov.Markov()
    
    def get_evaluations(self,radius=1):
        """
            Returns evaluations in certain area
        """
        reg_dist = []
        ibl_dist = []
        hmm_dist = []
        # split input path into patches of 5 points
        input_patches = numpy.array_split(numpy.array(self.input_path),5)
        for i in range(len(input_patches)):
            path = input_patches[i]
            center = path[-1]
            if i>0:
                reg_filtered = numpy.array(self.regression.get_filtered_predict(center,radius))
                ibl_filtered = numpy.array(self.ibl.get_filtered_predict(center,radius))
                hmm_filtered = numpy.array(self.hmm.get_filtered_predict(center,radius))
                reg_dist.append(geoutil.calculate_hausdorff(path,reg_filtered))
                ibl_dist.append(geoutil.calculate_hausdorff(path,ibl_filtered))
                hmm_dist.append(geoutil.calculate_hausdorff(path,hmm_filtered))
            # regression
            self.regression.prepare_data(path)
            self.regression.poly_regression()
            self.regression.formatting()
            # instance based learning
            self.ibl.get_similar(path)
            # markov
            self.hmm.predict(path)
        return {
            "regression": reg_dist,
            "instance": ibl_dist,
            "markov": hmm_dist,
        }
