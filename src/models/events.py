from dataclasses import asdict, dataclass
from datetime import datetime
import re
from typing import Any, Union
from pydantic import BaseModel
from ics import Calendar, Event

import logging
logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

import dateparser

class POST_Body_Event(BaseModel):
    name:  str
    start: str
    end:   str
    created:     str = None
    location:    str = ''
    description: str = ''


@dataclass
class CalendarTime:
    dateTime: Union[str, datetime]
    timezone_offset = '+0800'
    
    def __init__(self, datetime) -> None:
        if isinstance(datetime, str):
            datetime = self.add_colon_to_time(datetime)
            
        self.dateTime = self.parse_datetime_to_iso(datetime)

    def __bool__(self): return bool(self.dateTime)
    
    def __str__(self) -> str:
        return self.dateTime.strftime("%a, %m/%d %I:%M %p")
    
    @classmethod
    def parse_datetime_to_iso(cls, datetime_str):
        return dateparser.parse(
            f'{datetime_str} {cls.timezone_offset}', settings={'DATE_ORDER': 'DMY', 'RELATIVE_BASE': datetime.now()}
        )
    
    @classmethod
    def add_colon_to_time(cls, datetime):
        time_regex = r'(\d\d)\s?(\d\d)\s?(AM|PM|$)'
        return re.sub(time_regex, r'\1:\2\3', datetime)
    
    def asdict(self):
        return {"dateTime": str(self.dateTime.isoformat()), "timeZone": 'Asia/Singapore'}
    

@dataclass
class CalendarEvent:
    name:  str
    start: Union[CalendarTime, str]
    end:   Union[CalendarTime, str]

    location:    str = ''
    description: str = ''

    calendarId: str = 'primary'
    sendUpdates: str = 'false'
    created: Union[CalendarTime, str] = None
    
    attribute_to_description_map = {
        "name": "The name/description of the event",
        "start": "The starting date and time of the event - eg. 10 May 10:00PM",
        "end": "The ending date and time of the event - eg. 15 May 8:00AM\n",
        "location [optional]":  "The location of the event",
        "description [optional]": "A description of the event",
        "sendUpdates [optional]": "this feature is WIP"
    }
    
    def __post_init__(self):
        # probably can skip the asdict calls on the start,end attributes since asdict calling asdict on this datacalss will act recursively on all attrs
        if isinstance(self.start, str): self.start = CalendarTime(self.start)
        if isinstance(self.end, str): self.end = CalendarTime(self.end)
        if not self.created: self.created = CalendarTime.parse_datetime_to_iso(datetime.now())
        
        self.check_errors()

        
    @classmethod
    def from_post_body(cls, other:POST_Body_Event):
        return cls(
            name=other.name,
            start=other.start,
            end=other.end,
            created=other.created,
            )
        
    def check_errors(self):
        errors = {}
        
        if not self.start: errors['start date'] = 'invalid/missing start date'
        if not self.end: errors['end date'] = 'invalid/missing end date'
        if not self.name: errors['name'] = 'invalid/missing name'
        
        if errors: 
            raise EventCreationError(errors=errors)
        else:
            return False
        
    def to_ics(self):
        e = Event()
        c = Calendar()
        e.name  = self.name
        e.begin = self.start.dateTime
        e.end   = self.end.dateTime
        e.created = self.created
        c.events.add(e)
        
        return c.serialize()
    
    def __str__(self) -> str:
        return f"Event: {self.name}\nFrom: {self.start} | Till: {self.end}"
        
    
class EventCreationError(Exception): 
    def __init__(self, message='', errors:dict={}):            
        super().__init__(message)
        self.errors = errors
    
    def __str__(self) -> str:
        return str(self.errors)