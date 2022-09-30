import tempfile
from src.models.events import CalendarEvent, EventCreationError
import httpx

import logging
logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

def create_ics_data(name: str='', start:str='', end:str='', calendar_event:CalendarEvent=None):
    if not calendar_event and not (name and start and end): raise ValueError
    
    event = None
    try:
        if calendar_event: 
            event = calendar_event
        else:
            event = CalendarEvent(name=name, start=start, end=end)
    except EventCreationError as E:
        log.error(E)
        return False
    
    object = event.to_ics()
    return object.encode()
    