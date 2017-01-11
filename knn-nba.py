import math

# convert string into float
def convertNum(num):
    try:
        return float(num)
    except ValueError:
        return 0

# calculate the distance between two players
def euclideanDistance(a, b):
    distance = 0
    for x in range(len(a)):
        #print sums[year][x]
        distance += pow(convertNum(a[x]) - convertNum(b[x]), 2)
        #print float(b[x])/sums[year][x]
    return math.sqrt(distance)

def count_labels(list):
    label_dist = ["Top 10 picks", "Mid 1st round", "Late 1st round",
                   "Early 2nd round", "Mid 2nd round", "Late 2nd round/undrafted"]
    label_counting = [0,0,0,0,0,0]
    for num in sorted(list)[1:-1]:
        label_counting [(num-1)/10] +=1
    index = label_counting.index(max(label_counting))
    return label_dist[index]


nba = {}

# reading in data
for i in range(2007, 2017):
    name = str(i) + ".txt"
    file = open(name, "r")

    # skip the first two line
    for line in file.readlines()[2:]:
        if line.split(",")[11] == "":
            continue

        # pick out attributes
        stat_list = line.split(",")
        stat = [stat_list[1]]

        stat += [stat_list[18]] # WS, win share
        stat += [stat_list[20]] * 50 # BPM, Box plus, Minus
        stat += [stat_list[21]] # VORP, value over replacement player
        stat += [i]

        nba[line.split(",")[3]] = stat


# classfication
file = open("2003.txt","r")
for line in file.readlines()[2:]:
        # stat is in the order of Rank,FG%,3P%,FT%,MP,PTS,TRB,AST,Year
        print [line.split(",")[3]]
        stat_list = line.split(",")
        stat = [line.split(",")[1]]

        stat += [stat_list[18]] # WS, win share
        stat += [stat_list[20]] * 50 # BPM
        stat += [stat_list[21]] # BPM
        stat += [2003]

        result = {}
        for key in nba.keys():
            result[key] = euclideanDistance(nba[key][1:-1],stat[1:-1])
        result = sorted(result.items(), key = lambda x: x[1])
        labels = []
        # set the k here
        k = 20
        for people in result[:k]:
            labels.append(int(nba[people[0]][0]))
        print count_labels(labels)