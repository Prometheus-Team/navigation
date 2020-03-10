import numpy as np
import math

from search import Search

class PathSmoother:
    def __init__(self):
        pass

    def smooth(self, path, alpha, beta, tolerance):
        x = path
        y = self.copyPath(path)
        c = 0
        totErr = 100
        print("Initial path: ", x)
        while totErr > tolerance:
            c += 1
            if c > 100:
                print("No smooth path")
                return False
            totErr = 0
            for j in range(1, len(path)-1):
                xi = np.array(x[j])
                yi = np.array(y[j])

                totErr = alpha * (self.euclideanDist(xi, yi)**2) + beta * (self.euclideanDist(yi, y[j+1])**2)

                k = yi + alpha * (xi - yi) + beta * (np.array(y[j-1]) - 2*yi + np.array(y[j+1]))
                y[j] = tuple(k)

                print(k, y[j])

            print("Error:", totErr)
        return y

    def euclideanDist(self, s, e):
        return math.sqrt((e[0]-s[0])**2 + (e[1]-s[1])**2 +(e[2]-s[2])**2)

    def copyPath(self, path):
        nPath = []
        for node in path:
            nPath.append((node[0], node[1], node[2]))

        return nPath

srch = Search()
strt = (2,3,5)
x = srch.ngraphSearch(strt,(6,8,9),srch.A_STAR_STRGY)
path = srch.getPathToFollow(strt, x)
path.reverse()
print(path)


sm = PathSmoother()

# print("Final path:",sm.smooth([(1,2,3),(1,2,4),(2,2,4)], 0.5, 0.1, 0.1))
print("Final path:",sm.smooth(path, 0.5, 0.1, 0.5))