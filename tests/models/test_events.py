import pytest
from src.models.events import CalendarEvent, CalendarTime, EventCreationError, POST_Body_Event

import logging

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

def test_calendartime_add_colon_to_time():
    mytime = '10 June 2004 1000'
    assert CalendarTime.add_colon_to_time(mytime) == "10 June 2004 10:00"
    
def test_create_post_body_event():
    details = {
        "name": "my event",
        "start": "10 Aug 2022 10PM",
        "end": "11 Aug 2022 12AM",
    }
    
    assert isinstance(POST_Body_Event(**details), POST_Body_Event)
    
def test_create_calendarevent_from_postbodyevent():
    details = {
        "name": "my event",
        "start": "10 Aug 2022 10PM",
        "end": "11 Aug 2022 12AM",
    }
    
    object = POST_Body_Event(**details)
    assert isinstance(CalendarEvent.from_post_body(object), CalendarEvent)
    
def test_create_calendarevent_from_postbodyevent__start_not_date():
    details = {
        "name": "my event",
        "start": "112039",
        "end": "11 Aug 2022 12AM",
    }
    
    object = POST_Body_Event(**details)
    
    with pytest.raises(EventCreationError):
        event = CalendarEvent.from_post_body(object)