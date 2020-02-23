from __future__ import print_function
from flask import Flask, render_template, request

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import base64
from email import encoders

from bin import utils
from bin.weather import Weather

SCOPES = ['https://www.googleapis.com/auth/gmail.send']



# https://developers.google.com/gmail/api/guides/sending
def create_message(sender, to, subject, message_text):
  """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  encoded_message = urlsafe_b64encode(message.as_bytes())
  return {'raw': encoded_message.decode()}


# https://developers.google.com/gmail/api/guides/sending
def send_message(service, user_id, message):
  """Send an email message.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  #except errors.HttpError, error:
  except:
    print('An error occurred: %s' % error)

class MailManager:

  def __init__(self, config, weekday):
  	self.config = config
  	self.weekday = weekday

  	self.todayWeekday = weekday #temp
  	#self.todayWeekday = self.getTodayWeekday()

  	self.emailMessageContent = self.createEmailMessageContent()
  	self.configEmail = config['EMAIL']
  	self.emailMessage = self.createEmailMessage(self.configEmail['EMAIL_FROM'], 
  		self.configEmail['EMAIL_TO'], 
  		self.configEmail['EMAIL_SUBJECT'],
  		self.emailMessageContent)

  	self.gmailService = self.returnService()
  	self.sendMessage(self.gmailService, 'me', self.emailMessage)


  def getTodayWeekday(self):
  	 #Check if call which is made, is actually matching today's day name.
    if str(self.weekday).upper() == str(date.today().strftime('%A')).upper():
      return self.weekday
    else:
      return date.today().strftime('%A')

  def createEmailMessageContent(self):
  	#Check config.ini to confirm configuration. 
    for section in self.config.sections():
      if(str(self.todayWeekday).upper() == str(section).upper()):
        forecast = Weather().getForecast(self.config)
        extractedForecast = Weather().extractForecastForDayAndTime(forecast, 
      	  self.config[section]['daysAhead'], 
      	  self.config[section]['forecastTime'])
        return render_template('email_template_inline_style.html',
          config=self.config[section],
          forecast=extractedForecast,
          icons=self.config['ICONS']
          )
      #else:
      	#return "There was a problem to create email content."

  def createEmailMessage(self, sender, to, subject, messageText):

    message = MIMEText(messageText, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = self.config[self.todayWeekday.upper()]['emailTitle']
    encoders.encode_base64(message)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

  def returnService(self):
    """Creates Gmail API Service authorization.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './config/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

  def sendMessage(self, service, userId, message):
    try:
      message = (service.users().messages().send(userId='me', body=message)
               .execute())
      print('Message Id: %s' % message['id'])
      return message
    except errors.HttpError as error:
      print('An error occurred: %s' % error)

