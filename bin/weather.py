"""Connection wrapper to the Darksky: weather API. To obtain a free developer API key, 
register at: https://darksky.net/dev 
Due to initial minimal scalability of the project, most of the information is kept as a static
messages in the constructor.
Notes about format options: https://darksky.net/dev/docs#forecast-request
"""

import requests
from requests.exceptions import HTTPError
import json


class Weather:

  def __init__(self):
  	"""Constructor initalizes hardcoded data."""
  	self.cityCoordinates = '-33.868448,151.198763' # Sydney Pyrmont
  	self.weatherRequestOptions = {
  	  'exclude': 'currently;hourly;minutely;alerts',
  	  'units': 'si'
  	} # This version requires just a daily forecast
  	self.weatherRequest = 'https://api.darksky.net/forecast/{weatherAPISecret}/{cityCoordinates}'
  	self.apiErrorMessage = {
      "message": "Weather API wasn't available."
    } # Currently this is a generic error message.

  
  def getForecast(self, apiKey):
    """Get a daily weather forecast.
    Args:
      apiKey: string, Darksky API developer key.
    """
    # Construct a request url based on a template.
    url = self.weatherRequest.replace('{weatherAPISecret}', apiKey).replace('{cityCoordinates}', self.cityCoordinates)
    
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


  def getForecastField(fieldName):
    # This function will return a certain data from JSON
    # i.e. return y["daily"]["data"][0]["summary"]
    return null