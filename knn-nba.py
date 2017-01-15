
# ------------------------ Load Library ------------------------ #
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
import numpy as np

# ---------------------- Helper functions ---------------------- #
# convert string into float
def convertNum(num):
    try:
        return float(num)
    except ValueError:
        return 0

def return_label(num):
    label_dist = ["Top 10 picks", "Mid 1st round", "Late 1st round",
                   "Early 2nd round", "Mid 2nd round", "Late 2nd round/undrafted"]
    return label_dist[(num-1)/10]

# ---------------------- Load dataset ---------------------- #
nba_stat = []
nba_labels = []

# reading in data
for i in range(1999, 2017):
    name = str(i) + ".txt"
    file = open(name, "r")

    # skip the first two line
    for line in file.readlines()[2:]:
        if line.split(",")[11] == "":
            continue

        # pick out attributes
        stat_list = line.split(",")
        stat = []

        stat += [convertNum(stat_list[18])] # WS, win share
        stat += [convertNum(stat_list[20]) * 20]  # BPM, Box plus, Minus
        stat += [convertNum(stat_list[21])] # VORP, value over replacement player


        nba_stat.append(np.array(stat))
        nba_labels.append(return_label(int(stat_list[1])))


# ---------------------- Train model ---------------------- #
# classfication
test_year = str(2003)
file = open(test_year+".txt","r")
for line in file.readlines()[2:60]:
        # stat is in the order of Rank,FG%,3P%,FT%,MP,PTS,TRB,AST,Year
        print [line.split(",")[3]]
        stat_list = line.split(",")

        stat = []

        stat += [convertNum(stat_list[18])] # WS, win share
        stat += [convertNum(stat_list[20]) * 20] # BPM
        stat += [convertNum(stat_list[21])] # BPM

# ---------------------- Predict result ---------------------- #
        neigh = KNeighborsClassifier(n_neighbors=50)
        # nba_stat = np.array(nba_stat)
        # nsamples, nx, ny = nba_stat.shape
        # d2_train_dataset = nba_stat.reshape((nsamples,nx*ny))
        neigh.fit(nba_stat, np.array(nba_labels).reshape(-1, 1))
        #print np.array(stat).reshape(-1, 1)

# ---------------------- Result visualization ---------------------- #
        print neigh.predict([np.array(stat)])
# ---------------------- Evaluate Result ---------------------- #
# Emprical evaluation:
# The result is more for entertaining purpose, it gives an approximation of how good a player actually is
# The result has shown that:
# Superstars like LeBron, Wade, Melo, and Bosh are definetely Top 10 picks
# Good starting players like David West, Boris Diaw are top 10 picks as well.
# Role players like Chris Kaman, Kirk Hinrich, Hayes, are likely to be pick mid 1st round.
# Players like Xue Yuyang, Andreas Glyniadakis, Paccelis Morlende
# that never play in the league, will stay 2nd round mid, late pick
# Kyle Korver, an All star NBA player, and an exceptional shooter, was picked 2nd round mid before, but according to
# our prediction, he will be picked top 10, which is totally logical,
# Darko Milicic, was picked 2nd, despite 9 years in the league, does not belong to the top 10 picks
# The result shifts slightly when the k changes.