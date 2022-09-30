from dataclasses import dataclass, field
from typing import Callable
from src.models.events import CalendarEvent, EventCreationError
from src.routers.responses import *
from src.services.google_auth import generate_auth_url, read_credentials
from src.services.google_events import GoogleCalendarEvent
from src.services.ics_utils import create_ics_data

from src.services.telegram.incoming_message_parsers import parse_create_event
from src.services.telegram.send_functions import send_file, send_message
from googleapiclient.errors import HttpError


handler_map = {}

@dataclass
class UserMessageHandler:
    userid:str
    handler_func: Callable
    data: dict = field(default_factory=dict)
    
    def handle(self, message):
        self.handler_func(message, userid=self.userid, data=self.data)
        return True
        


def add_handler_to_handlermap(handler:Callable, userid: str):
    global handler_map
    handler_map[userid] = handler
    return True

def check_for_handler(userid:str, message:str):
    if userid in handler_map:
        handler_obj = handler_map[userid]
        log.info(f'found handler {handler_obj}')
        return handler_obj
    return False



def add_google_calendar_handler(message:str, userid:str, data):
    response_obj = generate_auth_url(userid)
    send_message(chat_id=userid, text="I'm sending you a link now:")
    redirect_url = response_obj['redirect_url']
    send_message(rf"{redirect_url}",  chat_id=userid)
    send_message(chat_id=userid, text="Click on the link to grant access your calendar so that I can add and display events from it")
    return True

        
def initiate_event_creation_handler(message:str, userid:str, data):
    send_message("Enter the details of your event in the following order e.g.\nAnniversary\n15 Aug 10AM\n15 Aug 10PM", chat_id=userid)
    
    help_text = '\n'.join(
        [":\t\t".join((k,v))
            for k,v in CalendarEvent.attribute_to_description_map.items()])
    
    
    send_message(text=help_text, chat_id=userid)
    next_handler = UserMessageHandler(userid=userid, handler_func=on_event_created_handler)
    add_handler_to_handlermap(next_handler, userid)
    
    return True
    
def on_event_created_handler(message:str, userid:str, data):
    event = parse_create_event(message)
    if isinstance(event, CalendarEvent):
        send_message(chat_id=userid, text='Event created! Would you like to create an ICS file or add this to your Google Calendar?\nEnter either Google or ICS')
        
        next_handler = UserMessageHandler(userid, what_to_do_with_event_handler)
        next_handler.data['CalendarEvent'] = event
        add_handler_to_handlermap(next_handler, userid)
        return True
    
    elif isinstance(event, EventCreationError):
        send_message(chat_id=userid, text=f'Unable to create that event: {event}')
    
    return False

def what_to_do_with_event_handler(message:str, userid:str, data):
    event = data['CalendarEvent']
    message = message.lower()
    
    if 'both' in message:
        pass
    
    elif 'google' in message:
        google_event = GoogleCalendarEvent.from_calendar_event(event)
        creds = read_credentials(user_id=userid)
        
        if creds:
            event_create_result = google_event.create(credentials=creds)
            if isinstance(event_create_result, HttpError):
                send_message('Something went wrong. Please try again later.', chat_id=userid)
                return False
                
            send_message(event_create_result.get('htmlLink', 'Event created.'), chat_id=userid)
            return True

        return False
        
    elif 'ics' in message:
        log.info(event)
        ics_file = create_ics_data(calendar_event=event)
        
        if not ics_file:
            send_message('Something went wrong. Please try again later.', chat_id=userid)
            return False
        
        send_file(file=ics_file, new_filename=f"{event.name}.ics", chat_id=userid)
        send_message(text='Here you go!', chat_id=userid)
        return True
    
    return False