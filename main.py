from dotenv import dotenv_values
import os
os.environ.update(dotenv_values())

import logging
logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

from fastapi import FastAPI

from src.routers import google_auth_router, ics_router, telegram_router
from src.routers import responses

app = FastAPI()

app.include_router(ics_router.router)
app.include_router(telegram_router.router)
app.include_router(google_auth_router.router)



@app.get('/')
def root():
    return responses.RESPONSE_OK("we're up!")

@app.get('/privacypolicy')
def privacy_policy():
    return responses.RESPONSE_OK("We do not collect any data, and do not store any data on our servers.")