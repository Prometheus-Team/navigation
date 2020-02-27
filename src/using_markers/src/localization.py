

import mapper

class ParticleFilter:
    def __init__(self):
        pass

    def guessPossibleLocations(self, curLoc, no=100):
        pass

    def check(self, curView):
        loc = mapper.mapperInst.getCurLoc()
        guesses = self.guessPossibleLocations(loc)
        possibleLoc = []

        for i in range(len(guesses)):
            guessMap = mapper.mapperInst.getMap(guesses[i])
            if curView - guessMap < threshold:
                possibleLoc.append(guesses[i])2