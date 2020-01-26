# Utilities which are used throughout the project.

import time

class Utils:
  DEFAULT_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
  
  def convertTime(self, unixTime):
  	# Converts Unix time which is used by weather API to human readable format.
  	return time.strftime(DEFAULT_TIME_FORMAT, time.localtime(unixTime))
