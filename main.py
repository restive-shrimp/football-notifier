from flask import Flask, render_template, request, redirect, url_for
from apiclient.discovery import build
import configparser
import json

from bin import utils
from bin.weather import Weather
from bin.mailmanager import MailManager


app = Flask(__name__)

#Load config.ini file.
config = configparser.ConfigParser()
config.read('./config/config.ini')


def callFromCron(*args, **kwargs):
  """Function checking if the call was made by cron.
  
  Returns:
    True if headers are from cron job.
  """
  if request.headers.get('X-AppEngine-Cron') is None:
    return False
  else:
    return True

@app.route('/')
def main():
  """Main page of the football notifier.
  
  Returns:
    A redirection to a homepage of a Google Group.
  """
  return redirect(config['REDIRECTS']['googleGroup'], code=302)

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
  """404 error handler.

  Returns:
    A 404 html template.
  """
  return render_template("404.html") 
    
@app.route('/mail/<weekday>')
def sendMail(weekday):
  """This is a page which cron job requests to send an email.
  If 'today' is defined in config.ini, and call was made from cron, 
  get the current forecast and send an email. Otherwise redirect.

  Args: 
  weekday from url
  
  Returns:
    A message content of the email or redirection to Google
  """
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
