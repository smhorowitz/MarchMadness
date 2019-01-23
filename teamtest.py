import random
import numpy as np
import pandas as pd

WIN_VALUE = 750
LOSS_VALUE = 250

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
    def __init__(self, name): # Initiates a team, if no record is given default to empty
        self.name = name
        self.gamesWon = []
        self.gamesLost = []

    def addGame(self, game): # Todo: Use new game type to be created
        newgame =  [game]
        if newgame.getWinner() == self:
            self.gamesWon += [newgame]
        else:
            self.gamesLost += [newgame]
        self.wins = len(gamesWon)
        self.losses = len(gamesLost)

    def initialScore(self):
        self.score = (wins * WIN_VALUE + losses * LOSS_VALUE) / (wins + losses)

    def printteam(self):
        print "%s: %d - %d, %d" % (self.name, self.wins, self.losses, self.score)

    def setScore(self, score):
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
    team1: a reference to the team object of the first team
    team2: a reference to the team object of the second team
    box1: a pandas dataframe containing the box score stats of the first team
    box2: a pandas dataframe containing the box score stats of the second team
    home: the name of the home team
"""

class Game(object):
    def __init__(self, team1, team2, box1, box2, home):
        self.team1 = team1
        self.team2 = team2
        self.box1 = box1
        self.box2 = box2
        self.team1.addGame(self) #Adds reference to game in both team objects
        self.team2.addGame(self)
        self.totals1 = {stat:box1[stat].sum() for stat in box1}
        self.totals2 = {stat:box2[stat].sum() for stat in box2} #Keeps total game stats as library for easy access

    def getWinner(self):
        return self.team1.getName() if self.totals1['PTS'] > self.totals2['PTS'] else self.team2.getName()

    def getTotals(self):
        return {team1.getName(): self.totals1, team2.getName(): self.totals2}

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

def printteams(teams):
    for team in teams:
        team.printteam()
