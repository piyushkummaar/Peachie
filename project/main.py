from flask import Blueprint,render_template, request,flash
from flask_login import login_required, current_user
from . import db
from .gcalendar import getEvents
from datetime import datetime
from twilio.rest import Client
from werkzeug.exceptions import HTTPException
import logging
import time
import configparser

config = configparser.ConfigParser()


fname = 'logs/log'+datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")+'.log'
logging.basicConfig(filename=fname, level=logging.INFO)

main = Blueprint('main', __name__)

config.read('project/config/creds.ini')

# Twilio Credentials
account_sid = 'AC079c58693b2f2b23330d76a774f40000'
auth_token = '0690d01528f8844283784625d34214a3'

SaveID = []

def send_sms(cont_no,description,id):
    if id in SaveID:
        return False
    else:
        client = Client(account_sid, auth_token)
        message = client.messages \
                        .create(
                            body=description,
                            from_='+18183505192',
                            to='+91'+cont_no

                        )
        SaveID.append(id)                
        return True  


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard',methods=["GET","POST"])
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
        if request.method == "POST":
            event_type = request.form.get("selecttype")
            events = getEvents.main_envid(event_type)
            if events == 'No upcoming events found.':
                return render_template('dashboard.html', name=current_user.name,title=title)
            else: 
                for event in events:
                    idcontainer.append(event['id'])
                    if event['summary'].split(' ')[0] == 'PreReminder' \
                        or event['summary'].split(' ')[0] == 'PREReminder' or event['summary'].split(' ')[0] == 'Prereminder' \
                            or event['summary'].split(' ')[0] == 'prereminder' :
                            # SaveID.append(event['id'])
                            cont_no = event['summary'].split(' ')[::-1][0]
                            # call function
                            flash(f'Messsage send with in 24hr to {cont_no}') 
                            status = 'PreReminder'

                    elif event['summary'].split(' ')[0] == 'PostReminder'\
                        or event['summary'].split(' ')[0] == 'POSTReminder' or event['summary'].split(' ')[0] == 'Postreminder':
                            cont_no = event['summary'].split(' ')[::-1][0]
                            # call function
                            stat = send_sms(cont_no,event['description'],event['id'])
                            if stat == True:
                                flash(f'Messsage sended to {cont_no}')  
                            else:
                                flash(f'Messsage already sended to {cont_no}')
                            status = 'PostReminder' 
                    elif event['summary'].split(' ')[0] == 'Send' or event['summary'].split(' ')[0] == 'SEND':
                        cont_no = event['summary'].split(' ')[::-1][0]
                        stat = send_sms(cont_no,event['description'],event['id'])
                        print(stat)
                        if stat == True:
                            flash(f'Messsage sended to {cont_no}')  
                        else:
                            flash(f'Messsage already sended to {cont_no}')
                        status = 'Send'
                return render_template('dashboard.html', name=current_user.name,context=events,title=title,status=status_list,selectval=event_type)
        if events == 'No upcoming events found.':
            return render_template('dashboard.html', name=current_user.name,title=title)
        else: 
            return render_template('dashboard.html', name=current_user.name,context=events,title=title,status=status_list) 
    except Exception as e:
        print('[ERROR] ',e)
        logging.error(e)
    
        # print(request.get("selecttype"))    
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