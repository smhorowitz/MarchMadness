import random
import numpy as np

"""
Team is an object for each team in the tournament.
Todo: Add more relevant stats
Team contains:
    Name: The name of the school
    Wins: The number of wins achieved by the team during the season
    Losses: The number of losses achieved by the team during the season
    Games: A list of games played by the team during the season.
        Each game is a reference to a game object that also links back to each team
"""

class Team(object):
    def __init__(self, name, wins = 0, losses = 0): # Initiates a team, if no record is given default to empty
        self.name = name
        self.wins = wins
        self.losses = losses

    def addGame(self, game): # Todo: Use new game type to be created
        self.games +=  [game]

    def updateScore(self):
        totalScore = 0
        gameCount = 0
        for game in games:
            ptdiff = game[1]
            if ptdiff > 0:
                totalScore += 750
            else:
                totalScore += 250

        self.score = totalScore / gameCount

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


"""
Game is an object that contains information about one game played during the season.
Contains:
    homeTeam: a reference to the team object of the home team
    awayTeam: a reference to the team object of the away team
    homeBox: a numpy table containing the box score stats of the home team
    awayBox: a numpy table containing the box score stats of the away team
"""

class Game(object):
    def __init__(self, homeTeam, awayTeam, homeBox, awayBox):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.homeBox = homeBox
        self.awayBox = awayBox
        self.homeTeam.addGame(self)
        self.awayTeam.addGame(self)


def generateteams(n): # Generates a number of random teams with winning records
    teams = []
    for i in range(1, n + 1):
        teamname = "Team " + str(i)
        wins = random.randint(11, 20)
        teams.append(Team(teamname, wins, 20 - wins))
    return teams

def giveScores(teams): # Sets initial team strengths based on record
    wins = 0
    losses = 0
    for team in teams:
        wins += team.getWins()
        losses += team.getLosses()
    average = float(wins) / (float(wins) + float(losses)) # Calculates average record of teams for comparison
    for team in teams:
        winpct = float(team.getWins()) / (float(team.getWins()) + float(team.getLosses()))
        team.assignScore(((winpct / average) ** 2) * 500)

def weightedScore(team): # Gives team a weighted score based on opponent strength
    return

def printteams(teams):
    for team in teams:
        team.printteam()
