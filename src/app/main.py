import datetime

from adapters.gcal_client import GoogleCalendarClient
from adapters.slack_client import SlackClient
from calendar_client import CalendarClient
from messaging_client import MessagingClient

STATUS = {
    "연차": {'status_text': '[연차] Paid Time Off', 'status_emoji': ':shushing_face:'},
    "보상휴가": {'status_text': '[보상휴가] Paid Time Off', 'status_emoji': ':shushing_face:'},
    "재택근무": {'status_text': '[재택] Work From Home', 'status_emoji': ':house:'},
}
CALENDAR_NAME = 'hjngy0511@gmail.com'



def main(calendar, messaging):
    try:
        start_date = datetime.date.today().strftime("%Y-%m-%d") + 'T00:00:00Z' # 'Z' indicates UTC time
        end_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d") + 'T00:00:00Z' # 'Z' indicates UTC time

        events = calendar.get_events(CALENDAR_NAME, start_date, end_date)
        print("events", events)

        for event in events:
            user_name, event_name = event["user_name"], event["event_summary"]
            if event_name in STATUS:
                print(user_name, event_name) # ex. 정현정 연차
                messaging.update_status(user_name, STATUS[event_name])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    calendar = CalendarClient(calendar_service = GoogleCalendarClient())
    messaging = MessagingClient(messaging_service = SlackClient())
    main(calendar, messaging)