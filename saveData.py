import dataCollect as dc
import pickle
import sys
import datetime
startDates = {'2000': datetime.datetime(2000, 3, 16),
              '2001': datetime.datetime(2001, 3, 13),
              '2002': datetime.datetime(2002, 3, 12),
              '2003': datetime.datetime(2003, 3, 18),
              '2004': datetime.datetime(2004, 3, 16),
              '2005': datetime.datetime(2005, 3, 15),
              '2006': datetime.datetime(2006, 3, 14),
              '2007': datetime.datetime(2007, 3, 13),
              '2008': datetime.datetime(2008, 3, 18),
              '2009': datetime.datetime(2009, 3, 17),
              '2010': datetime.datetime(2010, 3, 16),
              '2011': datetime.datetime(2011, 3, 15),
              '2012': datetime.datetime(2012, 3, 13),
              '2013': datetime.datetime(2013, 3, 19),
              '2014': datetime.datetime(2014, 3, 18),
              '2015': datetime.datetime(2015, 3, 17),
              '2016': datetime.datetime(2016, 3, 15),
              '2017': datetime.datetime(2017, 3, 14),
              '2018': datetime.datetime(2018, 3, 13)}

args = sys.argv
year = args[1]
schools = dc.getSchools(year)
gamesList = dc.getGameList(schools)
seasonGamesList = dc.removeGames(gamesList, startDates[year])
gameStats = dc.gameDataList(seasonGamesList)
outFile = open(args[2], 'w+')
pickle.dump(gameStats, outFile)
outFile.close()
