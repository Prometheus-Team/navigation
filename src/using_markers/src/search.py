import numpy as np
import math

class Search:
    A_STAR_STRGY = 'A*'
    def __init__(self):
        # self.map = np.zeros((20,20,20))
        self.parentPaths = {}
        self.edges = {}
        self.edgesIndex = {}
        self.randomMap()

    def randomMap(self):
        x = np.random.rand(20,20,20)
        x = x > 0.5
        x = x.astype(int)
        self.map = x

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
                    if self.map[zArr[i], yArr[j], xArr[k]] == 0:
                        alts.append((zArr[i], yArr[j], xArr[k]))
        if cur in alts:
            alts.remove(cur)

        return alts

    def getNextEdges(self, startEdge, endNodes):
        startNode = startEdge[1]
        edges = []
        for i in endNodes:
            edge = (startNode, i)
            edges.append(edge)
            l = len(self.edges)
            if edge not in self.edges:
                self.edges[edge] = l
                self.edgesIndex[l] = edge
                if l not in self.parentPaths:
                    self.parentPaths[l] = self.edges[startEdge]
            

        return edges

    def aStar(self, start, end, edges):
        minCost = 100000
        next = edges[0][1]

        for edge in edges:
            node = edge[1]
            cost = self.hx(node, start, end)
            if cost < minCost:
                minCost = cost
                next = edge

        return next
    
    def hx(self, cur, start, end):
        return self.euclideanDist(cur, start) + self.euclideanDist(cur, end)

    def euclideanDist(self, s, e):
        return math.sqrt((e[0]-s[0])**2 + (e[1]-s[1])**2 +(e[2]-s[2])**2)

    def pathToExpand(self, strategy, frontier, start, end):
        if strategy == self.A_STAR_STRGY:
            return self.aStar(start, end, frontier)

        return None

    def ngraphSearch(self, start, end, strategy):
        self.edges[("Start", start)] = 0
        self.edgesIndex[0] = ("Start", start)

        frontier = []
        exploredEdges = set()
        exploredNodes = set()

        paths = self.getNextEdges(("Start", start), self.getNextNodes(start))

        for x in paths:
            if x not in exploredEdges:
                frontier.append(x)

        while True:
            if not frontier:
                return False

            pathToExpand = self.pathToExpand(self.A_STAR_STRGY, frontier, start, end)
            nodeToExpand = pathToExpand[1]
            frontier.remove(pathToExpand)

            if pathToExpand not in exploredEdges and nodeToExpand not in exploredNodes:
                exploredEdges.add(pathToExpand)
            else:
                continue

            if pathToExpand[1] not in exploredNodes:
                exploredNodes.add(nodeToExpand)

            # Goal Test
            if nodeToExpand == end:
                return pathToExpand

            for i in self.getNextEdges(pathToExpand, self.getNextNodes(nodeToExpand)):
                if i not in exploredEdges and i not in frontier and i[1] not in exploredNodes:
                    frontier.append(i)


    def getPathToFollow(self, start, finalEdge):
        path = [(finalEdge[1])]

        while finalEdge != ("Start", start):
            indFinalEdge = self.edges[finalEdge]
            path.append(finalEdge[0])
            finalEdge = self.edgesIndex[self.parentPaths[indFinalEdge]]
        return path

# srch = Search()
# strt = (2,3,5)
# x = srch.ngraphSearch(strt,(6,8,9),srch.A_STAR_STRGY)
# path = srch.getPathToFollow(strt, x)
# path.reverse()
# print(path)

# srch.search()