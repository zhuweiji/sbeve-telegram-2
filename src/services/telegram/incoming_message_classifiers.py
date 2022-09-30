import logging
logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)
import re

def is_create_event(message:str):
    message = message.lower()
    return \
        (is_command(message) and 'create' in message) or \
        (all(i in message for i in ('create', 'event')))

def is_add_google_calendar(message:str):
    message = message.lower()
    return is_command(message) and 'addcalendar' in message

def is_command(message:str):
    return message[0] == '/'

