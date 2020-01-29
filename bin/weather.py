"""Connection wrapper to the Darksky: weather API. To obtain a free developer API key, 
register at: https://darksky.net/dev 
Due to initial minimal scalability of the project, most of the information is kept as a static
messages in the constructor.
Notes about format options: https://darksky.net/dev/docs#forecast-request
"""

import json
import requests
import time
from datetime import date, datetime, timedelta
from requests.exceptions import HTTPError


class Weather:

  def __init__(self):
  	"""Constructor initalizes hardcoded data."""
  	self.cityCoordinates = '-33.868448,151.198763' # Sydney Pyrmont
  	self.host = 'https://api.darksky.net/forecast'
  	self.weatherRequestOptions = {
  	  'exclude': 'currently;minutely;alerts',
  	  'units': 'si',
  	  'timezone': 'Australia/Sydney'
  	} # This version requires just a daily forecast
  	self.weatherRequest = '{host}/{weatherAPISecret}/{cityCoordinates}'
  	self.apiErrorMessage = {
      "message": "Weather API wasn't available."
    } # Currently this is a generic error message.

  
  def getForecast(self, apiKey):
    """Get a daily weather forecast. 
    Args:
      apiKey: string, Darksky API developer key.
    """
    # Construct a request url based on a template.
    url = self.weatherRequest.format(host=self.host, weatherAPISecret=apiKey, cityCoordinates=self.cityCoordinates)
    
    try:
        response = requests.get(
          url,
          params=self.weatherRequestOptions,
        )
        response.raise_for_status()
    except HTTPError as http_err:
        return self.apiErrorMessage
    except Exception as err:
        return self.apiErrorMessage
    else:
        return json.loads(response.text)


  def getForecastForDayAndTime(self, daysAhead=1, forecastTime=12):
    # This function is to remove unnecesary JSON elements end return
    # core data for forecast: precipitation, temperature, icon for the day and 1 hour before and after the
    # requested forecast.
    forecastDateTime = date.today() + timedelta(days=daysAhead)
    forecastTime = datetime(forecastDateTime.year, forecastDateTime.month, forecastDateTime.day, forecastTime)
    return forecastTime.isoformat(' ')