import dataCollect as dc
import datetime

schoolsToInclude = [3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
schoolsList = dc.getSchools(2018)
print "Getschools working"
i = 0
schools = {}
for school in schoolsList:
    if i in schoolsToInclude:
        schools[school] = schoolsList[school]
    i += 1
games = dc.getGameList(schools)
print "getGameList working"
newGames = dc.removeGames(games, datetime.datetime(2018, 3, 13))
print "removeGames working"
print "there are %i things in newGames" %(len(newGames))
allGames = dc.gameDataList(newGames)
print "There are %i games with stats" %(len(allGames))
