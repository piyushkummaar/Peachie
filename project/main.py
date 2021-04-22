from flask import Blueprint,render_template, request,flash
from flask_login import login_required, current_user
from . import db
from .gcalendar import getEvents
from datetime import datetime
from twilio.rest import Client
from werkzeug.exceptions import HTTPException
import logging
import time
import os
import configparser

config = configparser.ConfigParser()

try:
    os.makedirs("logs")
except FileExistsError:
    pass

fname = 'logs/log'+datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")+'.log'
logging.basicConfig(filename=fname, level=logging.INFO)

main = Blueprint('main', __name__)

config.read('project/config/creds.ini')

# Twilio Credentials
account_sid = config.get("twilio.com","account_sid")
auth_token = config.get("twilio.com","auth_token")

client = Client(account_sid, auth_token)

SaveID = []

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    try:
        idcontainer = []
        title = 'SMS service reminder'
        status = False
        print('[INFO] Start Getting data from Google API.')
        events = getEvents.main()
        logging.info(events)
        print('[INFO] Execute Successfully.')
        status_list = []
        if events == 'No upcoming events found.':
            return render_template('dashboard.html', name=current_user.name,title=title)
        else: 
            for event in events:
                idcontainer.append(event['id'])
                if event['summary'].split(' ')[0] == 'PreReminder' \
                    or event['summary'].split(' ')[0] == 'PREReminder':
                        # SaveID.append(event['id'])
                        cont_no = event['summary'].split(' ')[::-1][0]
                        flash(f'Messsage send with in 4hr to {cont_no}') 
                        status = 'PreReminder'

                elif event['summary'].split(' ')[0] == 'PostReminder'\
                    or event['summary'].split(' ')[0] == 'POSTReminder':
                        cont_no = event['summary'].split(' ')[::-1][0]
                        # message = client.messages \
                        #             .create(
                        #                 body='description',
                        #                 from_='+18183505192',
                        #                 to='+917807445246'
                        #             )    
                        # print(message.sid," : ",event['id'])
                        flash(f'Messsage sended to the {cont_no}') 
                        status = 'PostReminder' 
                elif event['summary'].split(' ')[0] == 'Send':
                    cont_no = event['summary'].split(' ')[1]
                    print(idcontainer)
                    if event['id'] in idcontainer:
                        flash(f'Messsage already sended to the {cont_no}')
                    else:
                        if not event['description']:
                            pass
                            # message = client.messages \
                            #             .create(
                            #                 body='Message',
                            #                 from_='+18183505192',
                            #                 to='+91'+cont_no
                            #             )
                            # idcontainer.append(event['id'])
                            # print(message.sid)
                            flash(f'Messsage sended to the {cont_no}')
                        # message = client.messages \
                        #             .create(
                        #                 body=event['description'],
                        #                 from_='+18183505192',
                        #                 to='+91'+cont_no
                        #             )    
                        # idcontainer.append(event['id'])
                        # print(message.sid)
                        flash(f'Messsage sended to the {cont_no}')
                        # status = 'Send'
            return render_template('dashboard.html', name=current_user.name,context=events,title=title,status=status_list) 
    except Exception as e:
        print('[ERROR] ',e)
        logging.error(e)
    return render_template('dashboard.html', name=current_user.name,title=title)

@main.route('/edit/<string:cal_id>', methods=['GET','POST'])
def editform(cal_id):
    if request.method == "POST":
        print('================***================')
        print('[INFO] Start Getting data from Google API.')
        event = getEvents.get_by_id(cal_id) 
        srt = datetime.fromisoformat(event['start']['dateTime'])
        ed = datetime.fromisoformat(event['end']['dateTime'])
        start = srt.strftime('%Y-%m-%d %H:%M:%S')
        end = ed.strftime('%Y-%m-%d %H:%M:%S') 
        print('[INFO] Execute Successfully...')
        val = request.form.get('optionsRadios')
        flash(f'Set to {val}.')
        if val == '4hr':
            return render_template('form.html', event=event,end=end,start=start,val4=val)
        elif val == '8hr':
            return render_template('form.html', event=event,end=end,start=start,val8=val)
        elif val == '12hr':
            return render_template('form.html', event=event,end=end,start=start,val12=val) 
        print('================***================')
    
    print('[INFO] Start Getting data from Google API.')
    event = getEvents.get_by_id(cal_id) 
    srt = datetime.fromisoformat(event['start']['dateTime'])
    ed = datetime.fromisoformat(event['end']['dateTime'])
    start = srt.strftime('%Y-%m-%d %H:%M:%S')
    end = ed.strftime('%Y-%m-%d %H:%M:%S') 
    print('[INFO] Execute Successfully...')
    return render_template('form.html', event=event,end=end,start=start)

@main.route('/template/<string:event_id>', methods=['GET','POST'])
def template(event_id):
    if request.method == "POST":
        pass
    print('[INFO] Start Getting data from Google API.')
    event = getEvents.get_by_id(event_id) 
    des = event['description']
    print('[INFO] Execute Successfully...')
    return render_template('template-view.html',event_id=event_id,des=des)

@main.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("errors/500.html", e=e), 500

@main.route('/callback',methods=['GET','POST'])
def callback():
    return "Sucessfully!!"