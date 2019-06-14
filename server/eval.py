import sys, os
import numpy

from .regression import Regression
from . import instance, markov, base
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import geoutil

class Evaluation:
    def __init__(self,mode):
        self.mode = mode
        self.regression = Regression()
        self.ibl = instance.Instance(mode)
        self.hmm = markov.Markov(mode)
        self.hmm.train()
    
    def get_evaluations(self,radius=0.5):
        """
            Returns evaluations in certain area
        """
        evaluations = []
        test = get_tests(self.mode)
        # split input path into patches of 5 points
        for route in [geoutil.parse_coords_array(r) for r in test]:
            reg_dist = []
            ibl_dist = []
            hmm_dist = []
            input_patches = numpy.array_split(numpy.array(route),5)
            # specific case of comparsion for polynomial regression
            reg_full = []
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
                self.regression.train(path,self.mode)
                self.regression.formatting()
                # instance based learning
                self.ibl.train()
                self.ibl.predict(path)
                # markov
                self.hmm.train()
                self.hmm.predict(path)
                reg_full = reg_full + self.regression.get_predict()

            evaluations.append(
                {
                    "regression": reg_dist,
                    "regression_full": geoutil.calculate_hausdorff(reg_full,route),
                    "instance": ibl_dist,
                    "instance_full": geoutil.calculate_hausdorff(self.ibl.get_predict(),route),
                    "markov": hmm_dist,
                    "markov_full": geoutil.calculate_hausdorff(self.hmm.get_predict(),route)
                }
            )

        return evaluations

def get_tests(set):
    if set == "porto":
        return [
            "[[-8.61066,41.14626],[-8.60978,41.14665],[-8.60911,41.14681],[-8.60869,41.14743],[-8.60828,41.14837],[-8.60760,41.14935],[-8.60698,41.15044],[-8.60641,41.15134],[-8.60589,41.15235],[-8.60532,41.15345],[-8.60688,41.15364],[-8.60843,41.15364],[-8.61015,41.15360],[-8.61015,41.15454],[-8.61009,41.15540],[-8.60999,41.15608]]",
            "[[-8.618643,41.141412],[-8.618499,41.141376],[-8.620326,41.14251],[-8.622153,41.143815],[-8.623953,41.144373],[-8.62668,41.144778],[-8.627373,41.144697],[-8.630226,41.14521],[-8.632746,41.14692],[-8.631738,41.148225],[-8.629938,41.150385],[-8.62911,41.151213],[-8.629128,41.15124],[-8.628786,41.152203],[-8.628687,41.152374],[-8.628759,41.152518],[-8.630838,41.15268],[-8.632323,41.153022],[-8.631144,41.154489],[-8.630829,41.154507],[-8.630829,41.154516],[-8.630829,41.154498],[-8.630838,41.154489]]",
        ]
    else:
        return [
                "[[15.95322,45.79300],[15.95324,45.79371],[15.95416,45.79425],[15.95608,45.79421],[15.95743,45.79420],[15.95850,45.79413],[15.95911,45.79455],[15.95939,45.79488],[15.95980,45.79579],[15.96042,45.79665],[15.96099,45.79747],[15.96150,45.79825],[15.96204,45.79905],[15.96301,45.79930],[15.96461,45.79935],[15.96594,45.79943]]",
                "[[15.95420,45.78766],[15.95444,45.78800],[15.95463,45.78833],[15.95496,45.78876],[15.95524,45.78912],[15.95543,45.78942],[15.95567,45.78985],[15.95600,45.79031],[15.95635,45.79075],[15.95654,45.79110],[15.95675,45.79141],[15.95701,45.79189],[15.95744,45.79242],[15.95774,45.79276],[15.95791,45.79321],[15.95829,45.79358],[15.95847,45.79390],[15.95876,45.79418],[15.95904,45.79457],[15.95918,45.79498]]",
                "[[15.99004,45.80147],[15.98920,45.80147],[15.98927,45.80109],[15.98924,45.80082],[15.98990,45.80057],[15.99080,45.80062],[15.99176,45.80069],[15.99239,45.80070],[15.99318,45.80077],[15.99411,45.80078],[15.99519,45.80085],[15.99570,45.80044],[15.99614,45.79991],[15.99659,45.79939],[15.99696,45.79882],[15.99731,45.79836],[15.99703,45.79794],[15.99696,45.79744],[15.99724,45.79700]]",
                "[[15.96248,45.79507],[15.96256,45.79545],[15.96327,45.79549],[15.96403,45.79551],[15.96495,45.79552],[15.96466,45.79596],[15.96563,45.79667],[15.96691,45.79695],[15.96825,45.79693],[15.96924,45.79647],[15.97027,45.79613],[15.97056,45.79675],[15.97050,45.79766],[15.97124,45.79826],[15.97252,45.79832],[15.97359,45.79841],[15.97470,45.79825],[15.97467,45.79770],[15.97477,45.79708],[15.97488,45.79640],[15.97572,45.79600]]"        
            ]

def get_geojson_tests(set):
    tests = get_tests(set)
    geo_tests = [geoutil.geojson_path_converter(geoutil.parse_coords_array(tests[i]),i) for i in range(len(tests))]
    return {
        "black": geo_tests[0],
        "blue": geo_tests[1],
        "red": geo_tests[2],
    }