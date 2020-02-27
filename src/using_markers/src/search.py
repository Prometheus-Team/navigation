import numpy as np
import math

class Search:
    def __init__(self):
        self.map = np.zeros((20,20,20))
        self.explored = set()
        self.front = []

    def dimNodes(self, val, size):
        vals = []

        vals.append(val)
        if val + 1 < size:
            vals.append(val+1)

        if val - 1 >= 0:
            vals.append(val-1)

        return vals

    def getNextNodes(self, cur):
        sh = self.map.shape
        xArr = self.dimNodes(cur[2], sh[2])
        yArr = self.dimNodes(cur[1], sh[1])
        zArr = self.dimNodes(cur[0], sh[0])
        alts = []

        for i in range(len(zArr)):
            for j in range(len(yArr)):
                for k in range(len(xArr)):
                    alts.append((zArr[i], yArr[j], xArr[k]))

        alts.remove(cur)

        return alts

    def aStar(self, start, end, nodes):
        minCost = 100000
        next = nodes[0]

        for node in nodes:
            cost = self.hx(node, start, end)
            if cost < minCost:
                minCost = cost
                next = node

        return next
    
    def hx(self, cur, start, end):
        return self.getDistance(cur, start) + self.getDistance(cur, end)

    def getDistance(self, s, e):
        return math.sqrt((e[0]-s[0])**2 + (e[1]-s[1])**2 +(e[2]-s[2])**2)

    def search(self, start, end):
        reached = False
        cur = start

        while not reached:
            self.explored.add(cur)
            nodes = self.getNextNodes(cur)
            cur = self.aStar(start, end, nodes)



srch = Search()
# srch.search()