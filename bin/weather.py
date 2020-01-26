import requests
import json


class Weather:

  def __init__(self):
  	self.cityCoordinates = '-33.868448,151.198763'
  	self.weatherRequestOptions = '?exclude=currently;hourly;minutely;alerts&units=si'
  	self.weatherRequest = 'https://api.darksky.net/forecast/{weatherAPISecret}/{cityCoordinates}{weatherRequestOptions}'

  def getForecast(self, apiKey):
    # Create a request url and parse data.
    url = self.weatherRequest.replace('{weatherAPISecret}', apiKey).replace('{cityCoordinates}', self.cityCoordinates).replace('{weatherRequestOptions}', self.weatherRequestOptions)
    weatherApiResponse = requests.get(url)
    forecastJSON = json.loads(weatherApiResponse.text)
    return forecastJSON

  def getForecastField(fieldName):
    # This function will return a certain data from JSON
    # i.e. return y["daily"]["data"][0]["summary"]
    return null