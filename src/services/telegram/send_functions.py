import io
import logging
from typing import Union
from fastapi import Path

from src.models.telegram import InlineQueryResultArticle
logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

import httpx
from src.services.telegram.telegram_utils import *



def send_message(text: str, chat_id) -> bool:
    """Send a message to the bot."""
    log.info(text)

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    
    response = httpx.post(
        f"{TELEGRAM_URL}{TOKEN}/sendMessage", data=data
    )

    if response.status_code == 200:
        return True
    else:
        log.exception(response.content)
        return False


def send_file(file: Union[bytes, Path], new_filename, chat_id) -> bool:
    """ Send a file to the bot -- this method is currently not working"""
    
    if isinstance(file, Path):
        file = file.read_bytes()
        
    file = io.BytesIO(file)
    if new_filename: file.name = new_filename
            
    files = {'document': file}

    data = {
        "chat_id": chat_id,
        "parse_mode": None
    }
    
    docresponse = httpx.post(
        f"{TELEGRAM_URL}{TOKEN}/sendDocument", data=data, files=files
    )
    
    if docresponse.status_code == 200: 
        return True
    
    else:
        log.exception(docresponse.content)
        return False
    

def answer_inline_query(inline_query_id: str, results: list[InlineQueryResultArticle], cache_time=10):
    data = {
        "inline_query_id": inline_query_id,
        "results": results,
        'cache_time': cache_time,
    }
    
    response = httpx.post(
        f"{TELEGRAM_URL}{TOKEN}/answerInlineQuery", data=data
    )
    
    if response.status_code == 200:
        return True

    else:
        log.exception(response.content)
        return False
