import csv
import os

folder = "../../../data/Geolife Trajectories 1.3/Data/"

def loadData():
    """
        Iterate over content
    """
    for user in [os.path.join(folder, o) 
                for o in os.listdir(folder) if os.path.isdir(os.path.join(folder,o))]:
        if (user[-3:] != "010"):
            continue
        for trajectory in [os.path.join(user, o)
                for o in os.listdir(user) if os.path.isdir(os.path.join(user,o))]:
            for title in os.listdir(trajectory):
                with open(os.path.join(trajectory, title)) as f:
                    content = f.readlines()
                # you may also want to remove whitespace characters like `\n` at the end of each line
                content = [x.strip() for x in content if len(x) > 50]
                for line in content:
                    lat = line.split(",")[0]
                    lng = line.split(",")[1]
                    date = line.split(",")[5]
                    time = line.split(",")[6]
                    print(lat+" "+lng+" "+date+" "+time)

loadData()
    