# ------------------------ Load Library ------------------------ #
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
import numpy as np

position_labels = []
player_features = []

sum = [float(0)] * 11

# ---------------------- Helper functions ---------------------- #
# convert string into float
def convertNum(num):
    try:
        return float(num)
    except ValueError:
        return 0

# ---------------------- Load dataset ---------------------- #
def load_data(data):
    for line in data.readlines()[1:]:
        stat_list = line.split(",")
        stat = []

        position_labels.append(stat_list[6])
        # the feature that we are using are ['p/g', '3/g', 'r/g', 'a/g', 's/g', 'b/g', 'fg%', 'fga/g', 'ft%', 'fta/g', 'to/g']
        player_features.append(np.array(stat_list[9:20]))

        for i, num in enumerate(stat_list[9:20]):
            sum[i] += convertNum(num)

# Open files
data = open("2016ranking", "r")
load_data(data)
data = open("2015ranking", "r")
load_data(data)

# ---------------------- Normalization ---------------------- #
for stat in player_features:
    for i, num in enumerate(stat):
        stat[i] = convertNum(stat[i]) / sum[i]

testing_data = open("2014ranking", "r")

wrong = 0
total = 0

# ---------------------- Train model ---------------------- #
for line in testing_data.readlines()[1:]:

    stat_list = line.split(",")
    stat = stat_list[9:20]

    for i,num in enumerate(stat):
        stat[i] = convertNum(stat[i]) / sum[i]

    neigh = KNeighborsClassifier(n_neighbors=9)
    neigh.fit(player_features, np.array(position_labels))

    result = neigh.predict([np.array(stat)])
    if stat_list[6] != result[0]:
        wrong += 1
    total += 1

# ---------------------- Evaluate Result ---------------------- #
correct_rate = (total - wrong) / float(total)
print "When the k is 9, the error rate is " + str(correct_rate)