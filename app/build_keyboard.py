from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import settings

async def build_back_keyboard(callback_data: str, text: str = settings.DEFAULT_BACK_BUTTON_CONTENT, extra_buttons: list[list[str]]|None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if extra_buttons:
        for btn_info in extra_buttons:
            builder.add(InlineKeyboardButton(text=btn_info[0], callback_data=btn_info[1]))
    builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    builder.adjust(settings.BACK_KEYBOARD_ADJUST)
    return builder.as_markup()

async def get_button_to_choose_payment_method(data):

    button_to_choose_payment_method = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=settings.TEXT_CARD_METOD_CHOOSE,callback_data=f"pay_with_yookassa_{data}")],
                                                           [InlineKeyboardButton(text=settings.TEXT_CRYPTO_METOD_CHOOSE,callback_data=f"pay_with_bitsby_{data}")],
                                                           #[InlineKeyboardButton(text="Договор оферты",callback_data="choose_channels")],
                                                           #[InlineKeyboardButton(text="Задать вопрос",callback_data="...")],
                                                           [InlineKeyboardButton(text=settings.DEFAULT_BACK_BUTTON_CONTENT,callback_data="to_join")]])
    return button_to_choose_payment_method

async def get_button_to_payment_with_yookassa(yookassa_payment_url,data):
    if data=="pay_with_yookassa_1month":
        button_to_choose_payment_method = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=settings.TEXT_CARD_METOD_CHOSEN,url=yookassa_payment_url)],
                                                                            [InlineKeyboardButton(text=settings.DEFAULT_BACK_BUTTON_CONTENT,callback_data="1month")]])
    elif data=="pay_with_yookassa_6month":
        button_to_choose_payment_method = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=settings.TEXT_CARD_METOD_CHOSEN,url=yookassa_payment_url)],
                                                                                [InlineKeyboardButton(text=settings.DEFAULT_BACK_BUTTON_CONTENT,callback_data="6month")]])
    else:
        button_to_choose_payment_method = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=settings.TEXT_CARD_METOD_CHOSEN,url=yookassa_payment_url)],
                                                                                [InlineKeyboardButton(text=settings.DEFAULT_BACK_BUTTON_CONTENT,callback_data="12month")]])
    return button_to_choose_payment_method

async def get_button_to_payment_with_bitsby(bitsby_payment_url,data):
    if data=="pay_with_bitsby_1month":
        button_to_choose_payment_method = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=settings.TEXT_CRYPTO_METOD_CHOSEN,url=bitsby_payment_url)],
                                                                                [InlineKeyboardButton(text="Назад",callback_data="1month")]])
    elif data=="pay_with_bitsby_6month":
        button_to_choose_payment_method = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=settings.TEXT_CRYPTO_METOD_CHOSEN,url=bitsby_payment_url)],
                                                                                [InlineKeyboardButton(text="Назад",callback_data="6month")]])
    else:
        button_to_choose_payment_method = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=settings.TEXT_CRYPTO_METOD_CHOSEN,url=bitsby_payment_url)],
                                                                                [InlineKeyboardButton(text="Назад",callback_data="12month")]])
    return button_to_choose_payment_method