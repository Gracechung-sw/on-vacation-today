from typing import Dict, List


class EventsList(Dict):
  user_name: str
  event_summary: str


class CalendarClient:
  def __init__(self, calendar_service):
    self.calendar_service = calendar_service

  def get_events(self, calendar_name, start_date, end_date) -> List[EventsList]:
    events = self.calendar_service.get_events(calendar_name, start_date, end_date)
    return events