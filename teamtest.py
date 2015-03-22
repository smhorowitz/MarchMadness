import random

class Team(object):
    def __init__(self, record):
        seld.name = 
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.games = []

    def addgame(self, game):
        self.games.append(game)
        if game[1] > 0:
            self.wins += 1
        else:
            self.losses += 1

    def updateScore(self):
        totalScore = 0
        gamecount = 0
        for game in games:
            ptdiff = game[1]
            if ptdiff > 0:
                score = 750
            else:
                score = 250

        self.score = totalScore

    def printteam(self):
        print "%s: %d - %d, %d" % (self.name, self.wins, self.losses, self.score)

    def assignScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def getWins(self):
        return self.wins

    def getLosses(self):
        return self.losses

    def getName(self):
        return self.name


def generateteams(n):
    teams = []
    for i in range(n):
        teamname = "Team " + str(i + 1)
        wins = random.randint(11, 20)
        record = (wins, 20 - wins)
        teams.append(Team(teamname, record))
    return teams

def giveScores(teams):
    wins = 0
    losses = 0
    for team in teams:
        wins += team.getWins()
        losses += team.getLosses()
    average = float(wins) / (float(wins) + float(losses))
    for team in teams:
        winpct = float(team.getWins()) / (float(team.getWins()) + float(team.getLosses()))
        team.assignScore(((winpct / average) ** 2) * 500)

def printteams(teams):
    for team in teams:
        team.printteam()
