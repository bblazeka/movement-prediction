import scipy.cluster.hierarchy as hcluster
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd

def get_cluster_id(clusters,route_id):
    """
        Returns the cluster_id of a given route_id
    """
    for i in range(len(clusters)):
        try:
            clusters[i].loc[route_id]
            return i
        except:
            continue

def calculate_route_similarity(routeA,routeB):
    """
        calculates the similarity between two routes
    """
    return len(list(set(routeA).intersection(routeB))) / len(list(dict.fromkeys(routeA + routeB)))

def clustering_by_similarity(routes):
    """
        NOT IMPLEMENTED YET
        clustering of routes by the factor of similarity between them
    """
    clusters = np.zeros(shape=(len(routes.items()),len(routes.items())))
    for key,route in routes.items():
        for subkey,subroute in routes.items():
            if(key>subkey):
                clusters[key][subkey]=SUMO.calculate_route_similarity(route,subroute)
            elif(key==subkey):
                clusters[key][subkey]=1
    print("implemented only to generate similarity matrix")

def clustering_by_location(coords):
    """
        Clustering points by location
    """
    kms_per_radian = 6371.0088
    # by setting epsilon, we set max distance that points can be from each other in a cluster
    # 0.3 km in this example
    epsilon = 0.2 / kms_per_radian
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
    return clusters
