import logging

from src.models.events import CalendarEvent, EventCreationError
logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

import re

def parse_create_event(message:str):
    lines = message.splitlines()
    event = None
    try:
        event = CalendarEvent(*lines)
        return event
    except EventCreationError as ECE:
        return ECE
    except Exception as E:
        log.error(E)
        return EventCreationError(errors=str(E))
    
    
        
    
    