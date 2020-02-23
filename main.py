import os
import json

from flask import Flask, render_template, request, redirect, url_for
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
from bin.mailmanager import MailManager


app = Flask(__name__)


config = configparser.ConfigParser()
config.read('./config/config.ini')

def callFromCron(*args, **kwargs):
  if request.headers.get('X-AppEngine-Cron') is None:
    return False
  else:
    return True

@app.route('/')
def main():
  #Main page will display current week counter with number of players who accepted an invitation.
  return str(config.sections())

    
@app.route('/mail/<weekday>')
def sendMail(weekday):
  #This is a page which cron job requests to send an email.
  #If 'today' is defined in config.ini, get the current forecast and
  #send an email. Otherwise return.
  if callFromCron():
    m = MailManager(config, weekday)
    return m.createEmailMessageContent()
  else:
  	return redirect(url_for('main'))


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
