from collections import defaultdict

import csv
import getopt
import itertools
import math
import random
import sys


def euclideanDistance(p, q):
    return math.sqrt(sum([(q[i] - p[i]) ** 2 for i in xrange(len(p))]))

def point2str(p, c):
    return p

class Cluster:
    def __init__(self, points):
        self.points = points
        self.centroid = self.calcCentroid()

    def add(self, point):
        self.points.append(point)

    def clear(self):
        self.points = []

    def calcCentroid(self):
        # Perform point-wise averaging to calculate centroid.
        if len(self.points) == 0:
            return self.centroid

        cent = [0] * len(self.points[0]['data'])

        for i in xrange(len(self.points[0]['data'])):
            cent[i] = sum([p['data'][i] for p in self.points]) / float(len(self.points))

        self.centroid = cent
        return cent

def usage():
    print '$> python kmeans.py <required args>\n' + \
        '\t-k <#>\t\tNumber of clusters\n' + \
        '\t-i <file>\tInput filename for the raw data\n'

def handleArgs(args):
    k = 2
    u = 0.0001
    input = None
    output = None

    if len(args) <= 1:
        usage()
        sys.exit(2)

    try:
        optlist, args = getopt.getopt(args[1:], 'k:i:')
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)

    for key, val in optlist:
        if key == '-k':
            k = int(val)
        elif key == '-i':
            input = val

    return (type, k, u, input)

def objFunc(clusters):
    return sum([euclideanDistance(p['data'], c.centroid) ** 2 for c in clusters for p in c.points])


def main(currRound=0):
    (type, k, u, infile) = handleArgs(sys.argv)

    f = open(infile, "r")

    distance = euclideanDistance
    # Read file into lists for each coordinate.
    points = [{'id': i, 'data': [float(x) for x in line.split(",")]} for i, line in enumerate(f)]
    numPoints = len(points)
    # Pick random starting centroids.
    clusters = [Cluster([c]) for c in random.sample(points, k)]

    iter = 0
    while True:
        oldC = []
        # Save old cluster centroids for future comparison.
        for c in clusters:
            oldC.append(c.centroid)
            c.clear()

        # Find nearest centroid to each point and add it to cluster.
        for p in points:
            minDist = float("inf")
            for c in clusters:
                dist = distance(p['data'], c.centroid)
                if dist < minDist:
                    minDist = dist
                    minClus = c
            minClus.add(p)

        # Calculate all the new centroids.
        for c in clusters:
            c.calcCentroid()

        # If the change in centroids is <= u, break.
        distDelta =  max([distance(oldC[i], clusters[i].centroid)
                            for i in range(0, len(clusters))])
        if distDelta <= u:
            break
        iter += 1

    # Load true labels into mem
    trueLabels = []
    with open("true.txt") as ftrue:
        for l in ftrue:
            trueLabels.append(int(l))

        # Save output to CSV file.

        out = []
        for ci in xrange(len(clusters)):
            trueCMap = defaultdict(int)
            c = clusters[ci]
            for p in c.points:
                trueCMap[trueLabels[p['id']]] += 1

            maxCount = float('-inf')
            maxLabel = -1
            for clabel in trueCMap:
                if trueCMap[clabel] > maxCount:
                    maxCount = trueCMap[clabel]
                    maxLabel = clabel
            c.id = maxLabel

            for p in c.points:
                out.append((p['id'], c.id))

        out.sort(key=lambda tup: tup[0])

    with open('true.txt') as ftrue, file("out.txt", 'w') as fout, file("readings.txt", 'a') as accFile:
        for p in out:
            print >> fout, p[1]
        count = 0.0
        for line in itertools.izip(out, ftrue):
            if line[0][1] == int(line[1]):
                count += 1.0

        print "Accuracy: %f, ObjScore: %f" % (count / len(out), objFunc(clusters))
        



if __name__ == "__main__":
    # Use cProfile to profile process.
    # Can be replaced with just a call to main() to disable profiling.
    #import cProfile
    #cProfile.run('main()')
    for i in xrange(10):
        main()
