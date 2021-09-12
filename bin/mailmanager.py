from __future__ import print_function

import pickle
import os.path
import datetime
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from bin import utils
from bin.weather import Weather


class MailManager:

  def __init__(self, config, weekday, mail):
  	self.config = config
  	self.weekday = weekday
  	self.mail = mail
  	self.todayWeekday = weekday #temp
  	#self.todayWeekday = self.getTodayWeekday()
  	self.emailMessageContent = self.createEmailMessageContent()

  def getTodayWeekday(self):
  	 #Check if call which is made, is actually matching today's day name.
    if str(self.weekday).upper() == str(date.today().strftime('%A')).upper():
      return self.weekday
    else:
      return date.today().strftime('%A')

  def getTitle(self):
      date = datetime.date.today() + datetime.timedelta(days=1)
      emailTitle = self.config[self.todayWeekday.upper()]['emailTitle']
      return  f'{emailTitle} {date}'

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

  def sendEmail(self):
    """Sending email using data from config.ini. """
      msg = Message(self.getTitle(),
        sender = self.config['EMAIL']['MAIL_USERNAME'],
        recipients = [self.config['EMAIL']['EMAIL_TO']])
      msg.html = self.createEmailMessageContent()
      self.mail.send(msg)
