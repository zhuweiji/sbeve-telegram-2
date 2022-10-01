import logging
from src.routers.responses import RESPONSE_CREATED, RESPONSE_OK, RESPONSE_SERVER_ERROR

from src.services import google_auth
from src.services.utilities import *
from src.services import telegram 


logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

from fastapi import APIRouter, Request
from google_auth_oauthlib.flow import Flow

ROUTE_PREFIX = '/oauth2'

router = APIRouter(
    prefix=ROUTE_PREFIX
)


@router.get("/oauth2callback")
def oauth2callback(code: str, scope: str, state: str, request: Request):
    log.info(f'request :{request}')
    log.info(f'request.query_params :{request.query_params}')
    log.info(f'request url: {request.url}')

    AMMENDED_ROUTE_PREFIX = ''.join(ROUTE_PREFIX.split('/')[1:])
    
    try:
        authorization_response = str(request.url)
        authorization_response = authorization_response.replace(r'http:', 'https:')
        user_id = state

        flow = Flow.from_client_secrets_file(SECRETS_DIR / 'credentials.json',
                                             google_auth.SCOPES,
                                             redirect_uri=f"{WEBHOOK_URL}{AMMENDED_ROUTE_PREFIX}/oauth2callback")
        log.info(authorization_response)
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
    except Exception as E:
        log.exception(E)
        return RESPONSE_SERVER_ERROR('Could not fetch credentials')

    log.info(credentials)
    success = google_auth.save_credentials(user_id, credentials)
    if not success:
        telegram.send_functions.send_message("Sorry, I'm unable to save your credentials at this time. Please try again in a bit.", user_id)
        return RESPONSE_SERVER_ERROR('Could not complete saving of credentials')

    telegram.send_functions.send_message('successfully saved your credentials', user_id)
    return RESPONSE_OK("OAuth Flow complete!")
