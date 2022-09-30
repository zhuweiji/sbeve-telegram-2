import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleAuthRequest
from google_auth_oauthlib.flow import Flow
from src.routers import google_auth_router

from src.services.utilities import *

import logging

logging.basicConfig(format='%(process)d-%(levelname)s:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


SCOPES = ['https://www.googleapis.com/auth/calendar']


def save_credentials(key, credentials: Credentials):
    try:
        all_creds = {}
        if (SECRETS_DIR / 'tokens.json').is_file():
            with open(SECRETS_DIR / 'tokens.json', 'r') as f:
                all_creds = json.load(f)
                log.info(f'successfully loaded credentials for user {key}')

        all_creds[key] = credentials.to_json()
        with open(SECRETS_DIR / 'tokens.json', 'w+') as f:
            json.dump(all_creds, f)
            log.info(f'successfully stored credentials for user {key}')

        return True
    except Exception as E:
        log.error(f'Exception encountered while saving credentials:\n{E}')
        return False


def read_credentials(user_id):
    creds = None
    user_id = str(user_id)
    tokens_path = SECRETS_DIR / 'tokens.json'

    if not tokens_path.is_file():
        log.info("no tokens file")
        return False

    with open(tokens_path, 'r') as f:
        all_creds = json.load(f)
        log.info(f'all creds: {all_creds}')

    if user_id not in all_creds:
        log.info(f'tried to load {user_id} but could not find in tokens file')
        return False

    user_cred_info = all_creds[user_id]
    if isinstance(user_cred_info, str):
        user_cred_info = json.loads(user_cred_info)

    try:
        creds = Credentials.from_authorized_user_info(user_cred_info, SCOPES)
        log.info(f'credentials: {creds}')
    except Exception as E:
        log.info('could not create credentials')
        log.error(E)
        return False

    if not creds:
        log.info('credentials are falsy')
        return False

    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(GoogleAuthRequest())
            log.info('creds refreshed')
            log.info(f'credentials: {creds}')
            save_credentials(credentials=creds, key=user_id)
        else:
            log.info('creds not valid')
            return False

    return creds

def generate_auth_url(user_id: str):
    ROUTE_PREFIX = ''.join(google_auth_router.ROUTE_PREFIX.split('/')[1:])
    
    
    flow = Flow.from_client_secrets_file(SECRETS_DIR / 'credentials.json',
                                         SCOPES,
                                         redirect_uri= f"{WEBHOOK_URL}{ROUTE_PREFIX}/oauth2callback")

    flow.redirect_uri = f"{WEBHOOK_URL}{ROUTE_PREFIX}/oauth2callback"
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        state=user_id,
        prompt='consent',  # creates refresh_token on every auth, remove in prod
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    log.info(f'authorization_url :{authorization_url}')
    log.info(f'state :{state}')
    return {'redirect_url': authorization_url}

