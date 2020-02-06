# Utilities which are used throughout the project.

import time
import json


class Utils:
  DEFAULT_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

  def __init__(self):
  	print("init utils")
  
  def convertTime(self, unixTime):
  	# Converts Unix time which is used by weather API to human readable format.
  	return time.strftime(DEFAULT_TIME_FORMAT, time.localtime(unixTime))

  def convertDayAndHourToUnixTime(dayOfTheWeek='Tuesday', hour="12:00PM"):
  	return '1580273280' #TODO. This will return time 

  def extractNodeByTimestamp(self, weatherObj, value):
  	# Function which extracts forecast node for certain time.
  	# TODO: make it more general, to find a node by value recursively.
    returnArr = []
    for i in range(len(weatherObj)):
      for k in weatherObj[i]:
        if k == "time" and str(weatherObj[i][k]) == str(value):
          returnArr.append(weatherObj[i])
    return returnArr
