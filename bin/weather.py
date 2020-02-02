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
  	self.apiErrorMessage = {
      "message": "Weather API wasn't available."
    } # Currently this is a generic error message.

  
  def getForecast(self, config):
    """Get a daily weather forecast. 
    Args:
      config: config object with all required API data.
    """
    # Construct a request url based on a template.
    weatherApi = config['WEATHER_API'];
    url = weatherApi['weatherRequestTemplate'].format(
    	host=weatherApi['weatherApiHost'], 
    	weatherAPISecret=weatherApi['weatherAPISecret'],
    	cityCoordinates=weatherApi['cityCoordinates']
    	)
    
    try:
        response = requests.get(
          url,
          params=config['WEATHER_API_REQUEST_OPTIONS'],
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