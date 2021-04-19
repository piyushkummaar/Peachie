from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./token.pickle'):
        with open('./token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds,cache_discovery=False)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('[INFO] Getting the upcoming 10 events that contains "POSTReminder", "PREReminder" and "Send".')
    events_result = service.events().list(calendarId='c_6c6ue20cugfisv7rh79sge75gg@group.calendar.google.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()

    events = events_result.get('items', [])
    # print(events)
    if events:
        return events
    else:
        return 'No upcoming events found.'
    # page_token = None
    # while True:
    #     events = service.events().list(calendarId='c_6c6ue20cugfisv7rh79sge75gg@group.calendar.google.com', pageToken=page_token).execute()
    #     # for event in events['items']:
    #         # print(event['summary'])
    #     page_token = events.get('nextPageToken')
    #     if not page_token:
    #         break
    # if events:
    #     return events
    #     # return events
    # else:
    #     return 'No upcoming events found.'        
    

def get_by_id(id):
    """Shows basic usage of the Google Calendar API.
        Event by Id.
    """
    creds = None
    if os.path.exists('./token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    events_result = service.events().get(calendarId='c_6c6ue20cugfisv7rh79sge75gg@group.calendar.google.com',eventId=id).execute()
    # events = events_result.getByid(id)
    # print(events_result)
    return events_result

if __name__ == '__main__':
    main()