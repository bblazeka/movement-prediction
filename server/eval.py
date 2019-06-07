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
    
    def get_evaluations(self,radius=0.5):
        """
            Returns evaluations in certain area
        """
        test = [
            "",
            "[[15.95420,45.78766],[15.95444,45.78800],[15.95463,45.78833],[15.95496,45.78876],[15.95524,45.78912],[15.95543,45.78942],[15.95567,45.78985],[15.95600,45.79031],[15.95635,45.79075],[15.95654,45.79110],[15.95675,45.79141],[15.95701,45.79189],[15.95744,45.79242],[15.95774,45.79276],[15.95791,45.79321],[15.95829,45.79358],[15.95847,45.79390],[15.95876,45.79418],[15.95904,45.79457],[15.95918,45.79498]]",
        }
        reg_dist = []
        ibl_dist = []
        hmm_dist = []
        # specific case of comparsion for polynomial regression
        reg_full = []
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
            self.regression.prepare_sumo_data(path)
            self.regression.poly_regression()
            self.regression.formatting()
            # instance based learning
            self.ibl.get_similar(path)
            # markov
            self.hmm.predict(path)
            reg_full = reg_full + self.regression.get_predict()

        return {
            "regression": reg_dist,
            "regression_full": geoutil.calculate_hausdorff(reg_full,self.input_path),
            "instance": ibl_dist,
            "instance_full": geoutil.calculate_hausdorff(self.ibl.get_predict(),self.input_path),
            "markov": hmm_dist,
            "markov_full": geoutil.calculate_hausdorff(self.hmm.get_predict(),self.input_path)
        }
