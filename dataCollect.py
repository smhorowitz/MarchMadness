import numpy as np
import pandas as pd
import requests as req
import time
import datetime
import re
from bs4 import BeautifulSoup

STAT_SITE = "https://www.sports-reference.com"
SCHOOLS_EXT = "/cbb/seasons/YEAR-school-stats.html" #YEAR can be replaced with any year to get school stats for that season
STAT_CATEGORIES = ['MP', 'FG', 'FGA', '2P', '2PA', '3P', '3PA', 'FT', 'FTA',
                   'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']


"""
makeRequests gets a request from a webpage, then waits a second
prevents tons of requests being made per second out of consideration to people running server
takes:
    url: the url requested
returns:
    r: a BeautifulSoup object with info from url
"""

def makeRequest(url):
    r = req.get(url)
    time.sleep(1) #wait a second after making a request
    return BeautifulSoup(r.text, 'lxml')

"""
getSchools collects all the DIV1 schools that participated in a given season, 
taking a season year and returning a dictionary of schools with school names and gamelog extensions
takes:
    year: the year the season wanted ended
returns:
    schools: a dictionary with school names as indices and stat pages extentions as values
"""

def getSchools(year):
    schoolURL = STAT_SITE + SCHOOLS_EXT.replace('YEAR', str(year))
    soup = makeRequest(schoolURL)
    schools = {school.find('a').text:school.find('a')['href'].replace('.html','-gamelogs.html') #Gets URL extensions for every school gamelog
            for school in soup.find_all('td', attrs={'data-stat': 'school_name'})}
    return schools


"""
getGames finds URL extensions and the home team for each game a school has played
takes:
    school: The name of the school to be looked up
    schoolExt: The extension for the list of school gamelogs
returns:
    games: A list of tuples of games the school has played. For each game contains the
    URL extension and who was the home team. For neutal games the home team is 
    listed as 'Neutral'
"""

def getGames(school, schoolExt):
    soup = makeRequest(STAT_SITE + schoolExt)
    games = []
    # gameList is a list of table rows for each game
    gameList = [game.parent for game in
            soup.find('table', {'id': 'sgl-basic'}).find_all('td', {'data-stat':'date_game'})
            if (game.find('a') and game.parent.find('td', {'data-stat': 'opp_id'}).find('a'))] #prevents adding game to list if opponent has no URL
    for game in gameList:
        opponent = game.find('td', {'data-stat' :'opp_id'}).find('a').text # Gets school name of opponent
        homeIndicator = game.find('td', {'data-stat': 'game_location'}).text #determines where game was played
        if homeIndicator == '':
            home = school
        elif homeIndicator == 'N':
            home = 'Neutral'
        else:
            home = opponent
        gameExt = game.find('td', {'data-stat': 'date_game'}).find('a')['href'] #Gets URL extention for game
        games += [(gameExt, home)] # Adds tuple to list, tuple containing URL extension and home team name

    return games


"""
getGameList finds URL extensions for the box score page of each school's game
takes:
    schools: a dictionary of schools' names and gamelog extentions
returns:
    games: a list of tuples with extensions for each box score and home team name
"""

def getGameList(schools):
    games = []
    exts = []
    # Cycles through each school, adding all previously unadded games to list
    for school in schools:
        gameList = getGames(school, schools[school])
        for game in gameList:
            if game[0] not in exts: # Checks for duplicate
                games += [game]
                exts += [game[0]] # Keeps list of exts for duplicate prevention
    print "Done getting game lists"

    return games


"""
removeGames goes through a list of box score urls and removes any after a certain date
used primarily for removing tournament games from old seasons
takes:
    games: A list of game url extensions
    date: a date to remove games before
returns:
    newGames: an updated list
"""

def removeGames(games, date):
    newGames = []
    for game in games:
        if datetime.datetime.strptime(game[0][15:25], '%Y-%m-%d') < date:
            newGames += [game]

    return newGames


"""
collectGameData takes a list of box score url extensions and returns a list of box score dataframes
takes:
    games: A game url extension and home team name
returns:
    gameData: A dictionary, containing the names of both teams, the name of the home team and 
    DataFrame object containing the box score for each team. If game is played on neutral ground,
    home team name will be listed as 'Neutral'
"""

def collectGameData(game):
    ext = game[0]
    home = game[1]
    soup = makeRequest(STAT_SITE + ext)
    # Get names of teams involved
    teamNames = [team.text for team in soup.find_all('a', {'itemprop': 'name'})]
    team1 = teamNames[0]
    team2 = teamNames[1]
    # Gets tables containing box scores
    boxScores = soup.find_all('table',{'id':re.compile('box-score-basic')}) 
    # Gets list of players on each side
    players1 = [row.find('th').find('a').text for row in boxScores[0].find('tbody').find_all('tr',{'class':None})] 
    players2 = [row.find('th').find('a').text for row in boxScores[1].find('tbody').find_all('tr',{'class':None})] 
    # Creates tables of raw stats not including any percentage, as those can be calculated at need
    box1raw = [[int(stat.text) for stat in row.find_all('td', {'data-stat':re.compile('.*(?<!pct)$')})]
            for row in boxScores[0].find('tbody').find_all('tr',{'class':None})] 
    box2raw = [[int(stat.text) for stat in row.find_all('td', {'data-stat':re.compile('.*(?<!pct)$')})]
            for row in boxScores[1].find('tbody').find_all('tr',{'class':None})] 
    # Create pandas DataFrames containing all stats
    boxScore1 = pd.DataFrame(data=box1raw, index=players1, columns=STAT_CATEGORIES)
    boxScore2 = pd.DataFrame(data=box2raw, index=players2, columns=STAT_CATEGORIES)
    return {'team1':team1, 'team2':team2, 'boxScore1':boxScore1, 'boxScore2':boxScore2, 'home':home}


"""
gameDataList creates a list of all gamedata from a list of games
takes:
    games: a list of tuples, containing game extensions and home team names
returns:
    gameList: a list of dictionaries containing team names, box scores, and home team
"""

def gameDataList(games):
    gameList = []
    totalGames = len(games)
    counter = 0
    for game in games:
        gameList += [collectGameData(game)]
        counter += 1
        if counter % 100 == 0:
            print "%d/%d games complete" % (counter, totalGames)
    return gameList
