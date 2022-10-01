from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field

import logging
from typing import Any
logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


@dataclass
class InlineQuery:
    id:str
    _from: dict 
    query: str
    offset: str
    chat_type: str = None
    location: Any = None
    
    @classmethod
    def from_dict(cls, obj: dict):
        if not obj: return False
        try:
            obj['_from'] = obj['from']
            del obj['from']
            return InlineQuery(**obj)
        except Exception as E:
            log.exception(E)
            return False
        


@dataclass
class InlineQueryAnswer:
    inline_query_id: str
    results:list[InlineQueryResult] = field(default_factory=list)
    

class InlineQueryResult(ABC): 
    # https://core.telegram.org/bots/api#inlinequeryresultarticle
    pass


@dataclass
class InlineQueryResultArticle(InlineQueryResult):
    input_message_content:InputTextMessageContent
    id: str
    title: str
    # reply_markup: InlineKeyboardMarkup = None
    url: str = ''
    # hide_url: bool = False
    description: str = ''
    # thumb_url: str = ''
    # thumb_width: int = None
    # thumb_height: int = None
    type: str = 'article'
    
@dataclass
class InlineQueryResultDocument(InlineQueryResult):
    id: str
    title: str
    caption:str = ''
    type: str = 'document'
    

@dataclass
class TelegramMessage:
    update_obj: dict

    update_id            : str = None
    message_obj          : dict = None
    sender_obj           : dict = None
    message              : str = None
    user_id              : str = None
    sender_first_name    : str = None
    sender_username      : str = None
    inline_query         : InlineQuery = None
    chosen_inline_result : str = None

    def __post_init__(self):
        try:
            self.update_id = self.update_obj.get("update_id", None)
            self.message_obj = self.update_obj.get("message", None)

            self.inline_query = self.update_obj.get('inline_query', None)
            self.chosen_inline_result = self.update_obj.get("chosen_inline_result", None)

            if self.message_obj:
                self.sender_obj = self.message_obj.get("from", None)
                self.message = self.message_obj.get("text", None)
            if self.sender_obj:
                self.user_id = self.sender_obj.get("id", None)
                self.sender_first_name = self.sender_obj.get("first_name", None)
                self.sender_username = self.sender_obj.get('username', None)
        except Exception as E:
            log.exception(E)

    def get_user_identifier(self):
        return self.sender_first_name or self.sender_username or 'user'
    
@dataclass
class InlineKeyboardMarkup:
    inline_keyboard: list
    
    
@dataclass
class InlineKeyboardButton:
    text: str
    url:str = ''
    callback_data:str = ''


@dataclass
class InputTextMessageContent:
    message_text:str
    parse_mode: str = 'HTML'