from aiogram.types import (InlineKeyboardMarkup,InlineKeyboardButton)
from config import settings

start_info=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=settings.JOIN_BUTTON_TEXT,callback_data="to_join")],
                                                  [InlineKeyboardButton(text=settings.MORE_ABOUT_CHANNEL_BUTTON_TEXT,callback_data="more_about_channel")],
                                                 #[InlineKeyboardButton(text="задать вопрос",callback_data="ask_question")],
                    ])
