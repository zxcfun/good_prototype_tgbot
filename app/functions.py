from .build_keyboard import *
from aiogram.exceptions import TelegramBadRequest

async def back_button(callback_data:str,extra_buttons: list[list[str]]|None = None):
    return await build_back_keyboard(callback_data,settings.DEFAULT_BACK_BUTTON_CONTENT,extra_buttons)


async def safe_edit_text(message, text, reply_markup=None, parse_mode=None):
    """Безопасно редактирует сообщение, игнорируя ошибку 'message is not modified'."""
    try:
        await message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise