from mapbox import Directions, MapMatcher
from haversine import haversine
from datetime import datetime, timedelta
from MDAnalysis.analysis.psa import hausdorff

def convertPoints(points):
    """
        Converts an array from string to float coordinates
    """
    geo_points = []
    for point in points:
        coors = point.split(",")
        lat = float(coors[0])
        long = float(coors[1])
        geo_points.append([lat,long])
    return geo_points

def parseCoordinatesArray(array):
    """
        Convert array in string representation to an actual array of coordinates
    """
    coordinates = []
    for coor in array[2:-2].split("],["):
        coordinates.append(coor)
    return convertPoints(coordinates)

def calculate_hausdorff(A,B):
    """
        Returns hausdorff distance or 1000 if input is empty
    """
    if len(A) == 0 or len(B) == 0:
        return 1000.0
    else:
        return hausdorff(A,B)

def geojson_path_converter(path,title):
    """
        converts list of [latitude,longitude] to geojson point features list
    """
    geojson_path = []
    for coordinate in path:
        if (len(coordinate) > 0):
            geojson_path.append({
                    "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [coordinate[0], coordinate[1]]
                        }
                    })
    return {
        "type": "FeatureCollection",
        "properties": {
            "title": title,
        },
        "features": geojson_path
    }

def path_length(path):
    """
        calculates the length of a path
    """
    return distance((path[0][0],path[0][1]),(path[-1][0],path[-1][1]))

def distance(a,b):
    """
        calculates the haversine distance between two points
    """
    return haversine((a[0],a[1]),(b[0],b[1]))

def roads_matching(sorted_path):
    """
        ALPHA VERSION: not sure it works
    """
    return_path = []
    # api can only take in 100 points at the time
    for _ in range(1):

        values = []
        prev = datetime(2018,10,10,11,34,59)
        for _ in range(len(sorted_path)):
            min = str('%02d' % prev.minute)
            sec = str('%02d' % prev.second)
            values.append(str(prev.year)+"-"+str(prev.month)+"-"+str(prev.day)+"T"+str(prev.hour)+":"+min+":"+sec+"Z")
            prev = prev + timedelta(0,5)

        line = {
        "type": "Feature",
        "properties": {
            "coordTimes": {}
        },
        "geometry": {
            "type": "LineString",
            "coordinates": sorted_path[:100]}}

        service = MapMatcher(access_token="pk.eyJ1IjoiYnJhbmNhIiwiYSI6ImNqbnliMmVoeTA1MTMzcG54Y3h2bnFtYmwifQ.o6CzepqOg00rpv7wKNeOuQ")
        response = service.match(line, profile='mapbox.driving')
        max = 0
        best = 0
        try:
            features = response.geojson()['features']
            for i in range(len(features)):
                if len(features[i]['geometry']['coordinates'])>max and features[i]['properties']['confidence'] > 0.1:
                    max = len(features[i]['geometry']['coordinates'])
                    best = i

            corrected = response.geojson()['features'][best]['geometry']['coordinates']

            for corr in corrected:
                return_path.append(corr)
        except Exception as e:
            print("Road matching failed: "+str(e))

    return return_path

def concatenate_points(start,end):
    """
        Joins two points. Used to convert road segment representation to trajectory
    """
    service = Directions(access_token="pk.eyJ1IjoiYnJhbmNhIiwiYSI6ImNqbnliMmVoeTA1MTMzcG54Y3h2bnFtYmwifQ.o6CzepqOg00rpv7wKNeOuQ")
    origin = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': start,
        }
    }
    destination = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': end,
        }
    }
    response = service.directions([origin, destination],'mapbox/driving')
    return response.geojson()

if __name__ == '__main__':
    print(concatenate_points([13.4010032, 52.5183224],[13.4006712, 52.5182224]))
