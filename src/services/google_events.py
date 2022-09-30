from dataclasses import dataclass, asdict

from src.models.events import CalendarEvent, CalendarTime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import logging
logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

@dataclass
class GoogleCalendarEvent:
    summary: str
    start: dict
    end: dict

    location: str = ''
    description: str = ''

    calendarId: str = 'primary'
    sendUpdates: str = 'false'
    
    @classmethod
    def from_calendar_event(cls, calendar_event: CalendarEvent):
        start = calendar_event.start.asdict()
        end   = calendar_event.end.asdict()
        
        return GoogleCalendarEvent(
            summary=calendar_event.name,
            start=start,
            end=end,
            location=calendar_event.location,
            description=calendar_event.description,
            calendarId=calendar_event.calendarId,
            sendUpdates=calendar_event.sendUpdates
        )

    def create(self, credentials):
        event = self.asdict()
        log.warning(event)
        log.info(f'parsed event: {event}')
        try:
            service = build('calendar', 'v3', credentials=credentials)
            event_result = service.events().insert(calendarId=event['calendarId'], body=event).execute()
            log.info(f"Event created: {event_result}")
        except HttpError as e:
            logging.error(e)
            return e

        return event_result


    def asdict(self): return asdict(self)