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
import json
import datetime

from bin import utils
from bin.weather import Weather
from config import config

app = Flask(__name__)


@app.route('/')
def main():
  #Main page will display current week counter with number of players who accepted an invitation.
  return 'Main page'
    
@app.route('/mail/<weekday>')
def sendMail(weekday):
  #This is a page which cron job requests to send an email.
  return weekday

@app.route('/weather')
def readWeather():
  forecast = Weather().getForecast(config.weatherAPISecret)
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