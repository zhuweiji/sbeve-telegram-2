import logging
import traceback
from typing import Any, Dict, List, Union

from fastapi import APIRouter
from src.routers.responses import (RESPONSE_BAD_REQUEST, RESPONSE_OK,
                                   RESPONSE_SERVER_ERROR)
from src.services.telegram.incoming_message_classifiers import *
from src.services.telegram.incoming_message_handlers import *
from src.services.telegram.telegram_utils import establish_webhook
from src.models.telegram import *

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


ROUTE_PREFIX = '/telegram'

router = APIRouter(
    prefix=ROUTE_PREFIX
)

@router.on_event("startup")
def startup_event():
    log.info(f"webhook established: {establish_webhook(ROUTE_PREFIX.replace('/','')+'/')}")


@router.post("/")
def handle(request: Union[List, Dict, Any] = None):
    try:
        request_object = TelegramMessage(request)
        user_id = request_object.user_id
        message = request_object.message
        inline_query = request_object.inline_query
        
        if inline_query:
            pass
        
        elif handler_obj := check_for_handler(userid=user_id, message=message):
            handler_obj.handle(message)
            
        elif not message:
                pass
            
        elif message.strip().lower() == '/start':
            send_message(chat_id=user_id, text=r"Hello there! To get started, either add your Google Calendar via /addcalendar or create an event with /create")
            
        elif is_create_event(message=message):
            initiate_event_creation_handler(userid=user_id, message=request_object.message, data={})
            
        elif is_add_google_calendar(message=message):
            add_google_calendar_handler(userid=user_id, message=request_object.message, data={})
        
        return RESPONSE_OK()
    
    except Exception as E:
        log.error(E)
        traceback.print_exc()
        return RESPONSE_OK()
