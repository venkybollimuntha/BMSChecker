from flask import Flask,request
from flask_mail import Mail, Message
from flask_cors import CORS
import json
import requests
import os
from lxml import html
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import time
import threading
app =Flask(__name__)
app.config.update(
    DEBUG=False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='doubts2venky@gmail.com',
    MAIL_PASSWORD='******************'
)
mail = Mail(app)
sched = BlockingScheduler()
if __name__ == '__main__':
      @sched.scheduled_job('interval', minutes=int(os.environ.get('INTERVAL',2)))
      def index():
        print('Ticket Check Method Called')
        BMS_URL =os.environ.get('BMS_URL','https://in.bookmyshow.com/buytickets/maharshi-hyderabad/movie-hyd-ET00081372-MT/20190509') 
        SEARCH_VALUE =os.environ.get('SEARCH_VALUE','PVR')
        SEARCH_VALUE_2 =os.environ.get('SEARCH_VALUE_2','INOX')
        r = requests.get(BMS_URL)
        soup = BeautifulSoup(r.content, "html.parser")
        for td in soup.findAll("a", class_="__venue-name"):
            theatre = str(td.text).strip()
            click_url = "https://in.bookmyshow.com"+td['href']
            if theatre.find(SEARCH_VALUE) != -1 or theatre.find(SEARCH_VALUE_2) != -1 :
                print('mail sent',theatre)
                mail_list = ['venkybollimuntha@gmail.com','harishdhanumuri@gmail.com','rakeshreddy.nayini@gmail.com','yashwanth408@gmail.com']
                msg = Message ('Tickets available in Book my show for theater:'+theatre, sender = 'doubts2venky@gmail.com',recipients = mail_list)
                msg.body = "please click here to book tickets: "+str(click_url) 
                with app.app_context():
                    mail.send(msg)
           
        print('BMS Ticket Req Check Completed at ::',datetime.now())
        return 'Request Process done'
sched.start()
app.run(environ.get('PORT',5000))
