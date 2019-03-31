import sys, os
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), "./util"))
import taxi
import geoutil

def get_similar(trajectory):
    """
        returns a route that is most similar
    """
    data = taxi.loadCsv()
    trajectoryA = taxi.ndarrayConverter(taxi.pointsListConverter(trajectory))
    minDistance = 0.5
    similarTrajectory = []
    for x in range(1,len(data)):
        try:
            trajectoryB = taxi.ndarrayConverter(taxi.pointsListConverter(data[x][8]))
            distance = taxi.calculate_hausdorff(trajectoryA,trajectoryB)
            lengthB = geoutil.path_length(trajectoryB)
            if distance < minDistance and distance > 0.005 and lengthB > 1 and taxi.containing(trajectoryB,trajectoryA[-8:]):
                minDistance = distance
                similarTrajectory = trajectoryB.tolist()
        except Exception as e:
            pass
    return similarTrajectory

def formatting(path):
    return {
        "predicted": geoutil.geojson_path_converter(path)
    }

def main():
    # not used in this application
    print(get_similar("[[-8.618643,41.141412],[-8.618499,41.141376],[-8.620326,41.14251],[-8.622153,41.143815],[-8.623953,41.144373],[-8.62668,41.144778],[-8.627373,41.144697],[-8.630226,41.14521],[-8.632746,41.14692],[-8.631738,41.148225],[-8.629938,41.150385],[-8.62911,41.151213],[-8.629128,41.15124],[-8.628786,41.152203],[-8.628687,41.152374],[-8.628759,41.152518],[-8.630838,41.15268],[-8.632323,41.153022],[-8.631144,41.154489],[-8.630829,41.154507],[-8.630829,41.154516],[-8.630829,41.154498],[-8.630838,41.154489]]"))

if __name__ == '__main__':
    main()