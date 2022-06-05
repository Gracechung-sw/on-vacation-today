import os.path
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

logger = logging.getLogger(__name__)


class GoogleCalendarClient:
    def __init__(self):  # https://developers.google.com/calendar/api/quickstart/python
        creds = None
        # If modifying these scopes, delete the file token.json.
        scopes = SCOPES
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", scopes)
            print("creds", creds)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        self.calendar_service = build("calendar", "v3", credentials=creds)

    def _get_calendar_list(self):
        try:
            calendar_list = self.calendar_service.calendarList().list().execute()
            return calendar_list["items"]
        except Exception as e:
            logger.error(e)
            raise e

    def _get_calendar_id(self, calendar_name):
        try:
            calendar_list = self._get_calendar_list()
            for calendar in calendar_list:
                if calendar["summary"] == calendar_name:
                    return calendar["id"]
        except Exception as e:
            logger.error(e)
            raise e

    def get_events(self, calendar_name, start_date, end_date):
        try:
            calendar_id = self._get_calendar_id(calendar_name)
            events_result = (
                self.calendar_service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=start_date,
                    timeMax=end_date,
                    singleEvents="true",
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            result = []
            for event in events:
                user_name, event_name = event["summary"].split(" ", maxsplit=1)
                result.append({"user_name": user_name, "event_summary": event_name})
            return result
        except HttpError as error:
            logger.error(error)
            raise error
