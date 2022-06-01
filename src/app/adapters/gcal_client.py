import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarClient:
  def __init__(self): # https://developers.google.com/calendar/api/quickstart/python
    creds = None
    # If modifying these scopes, delete the file token.json.
    scopes = SCOPES
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
        print("creds", creds)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    self.calendar_service = build('calendar', 'v3', credentials=creds)

  def _get_calendar_list(self):
    calendar_list = self.calendar_service.calendarList().list().execute()
    return calendar_list['items']

  def _get_calendar_id(self, calendar_name):
    calendar_list = self._get_calendar_list()
    for calendar in calendar_list:
      print("calendar['summary']", calendar['summary']) # ex. 생일, 대한민국의 휴일, 글또 6기, hjngy0511@gmai.com(내 google 계정)
      if calendar['summary'] == calendar_name:
        return calendar['id']

  def get_events(self, calendar_name, start_date, end_date):
    try:
      calendar_id = self._get_calendar_id(calendar_name)
      events_result = self.calendar_service.events().list(
              calendarId=calendar_id
              ,timeMin=start_date
              ,timeMax = end_date
              ,singleEvents = 'true'
              ,orderBy='startTime').execute()
      events = events_result.get('items', [])
      result = []
      for event in events:
        user_name, event_name = event['summary'].split(' ', maxsplit=1)
        result.append({"user_name": user_name, "event_summary": event_name})
      return result
    except HttpError as error:
        print('An error occurred: %s' % error)