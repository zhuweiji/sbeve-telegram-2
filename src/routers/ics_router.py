from src.models.events import CalendarEvent, EventCreationError, POST_Body_Event
from src.routers.responses import *

from ics import Calendar, Event
from fastapi import APIRouter
import logging

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

ROUTE_PREFIX = '/ics'

router = APIRouter(
    prefix=ROUTE_PREFIX
)


@router.post('/')
def create(new_event: POST_Body_Event):
    try:
        event = CalendarEvent.from_post_body(new_event)
    except EventCreationError as E:
        return RESPONSE_BAD_REQUEST(errors=E.errors)
    object = event.to_ics()
    
    
    if object:
        return RESPONSE_OK(ics_file=object)

    