import os
import json

from flask import Flask, render_template, request
from google.cloud import datastore
from apiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
import requests
from requests.auth import HTTPDigestAuth
import configparser
import json
from datetime import date, datetime

from bin import utils
from bin.weather import Weather


app = Flask(__name__)


config = configparser.ConfigParser()
config.read('./config/config.ini')

@app.route('/')
def main():
  #Main page will display current week counter with number of players who accepted an invitation.
  return str(config.sections())

    
@app.route('/mail/<weekday>')
def sendMail(weekday):
  #This is a page which cron job requests to send an email.
  #If 'today' is defined in config.ini, get the current forecast and
  #send an email. Otherwise return.

  #Check if call which is made, is actually matching today's day name.
  #if str(weekday).upper() == str(date.today().strftime('%A')).upper():
  #  todayWeekday = weekday
  #else:
  #	todayWeekday = date.today().strftime('%A')
  todayWeekday = weekday

  #Check config.ini to confirm configuration. 
  for section in config.sections():
    if(str(todayWeekday).upper() == str(section).upper()):
      forecast = readWeather()
      extractedForecast = Weather().extractForecastForDayAndTime(forecast, 
      	config[section]['daysAhead'], 
      	config[section]['forecastTime'])
      return render_template('email_template.html',
        config=config[section],
        forecast=extractedForecast,
        icons=config['ICONS']
        )
      #return extractedForecast
  return 'nothing today'

@app.route('/weather')
def readWeather():
  forecast = Weather().getForecast(config)
  return forecast

@app.route('/weather2')
def readWeather2():
  forecast = Weather().getForecastForDayAndTime()
  return forecast
  

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

def service_account_login():
  SCOPES = ['https://www.googleapis.com/auth/gmail.send']
  SERVICE_ACCOUNT_FILE = '/config/football-pyrmont-0534a031aea2.json'

  credentials = service_account.Credentials.from_service_account_file(
          SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  delegated_credentials = credentials.with_subject(EMAIL_FROM)
  service = build('gmail', 'v1', credentials=delegated_credentials)
  return service
