from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from dotenv import load_dotenv,find_dotenv
import json
import os

import app.keyboards as kb
from .functions import *
from .Yookassa.oplata import create_yookassa_payment
from .bitsby_api import BitsbyAPI
from config import settings

router = Router()

@router.message(CommandStart())
@router.callback_query(F.data == "start")
async def cmd_start(event: Message | CallbackQuery):
    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.edit_text(text=settings.INTRODUCTION, reply_markup=kb.start_info)
    else:
        await event.answer(text=settings.INTRODUCTION, reply_markup=kb.start_info)

@router.callback_query(F.data=="more_about_channel")
async def more_about_channel(callback_query_:CallbackQuery):
    if callback_query_.message:
        await safe_edit_text(callback_query_.message,settings.MORE_DETAILS,reply_markup=await back_button("start"))

@router.callback_query(F.data=="to_join")
async def to_join(callback_query_:CallbackQuery):
    extra_buttons=extra_buttons=[
        [settings.TEXT_1MONTH, "1month"],
        [settings.TEXT_6MONTH, "6month"],
        [settings.TEXT_12MONTH, "12month"],
    ]
    if callback_query_.message:
        await safe_edit_text(callback_query_.message,settings.SUBSCRIPTION_TEXT,reply_markup=await back_button("start",extra_buttons=extra_buttons))

@router.callback_query(F.data.in_(["1month","6month","12month"]))
async def pay(callback_query_:CallbackQuery):
    if callback_query_.data=="1month":
        TEXT_BEFORE_CHOOSE_PAYMENT_METHOD=settings.TEXT_BEFORE_CHOOSE_PAYMENT_METHOD_1MONTH
    elif callback_query_.data=="6month":
        TEXT_BEFORE_CHOOSE_PAYMENT_METHOD=settings.TEXT_BEFORE_CHOOSE_PAYMENT_METHOD_6MONTH
    elif callback_query_.data=="12month":
        TEXT_BEFORE_CHOOSE_PAYMENT_METHOD=settings.TEXT_BEFORE_CHOOSE_PAYMENT_METHOD_12MONTH
    try:
        await callback_query_.answer()
    except TelegramBadRequest:
        pass
    if callback_query_.message:
        await safe_edit_text(callback_query_.message,TEXT_BEFORE_CHOOSE_PAYMENT_METHOD, reply_markup=await get_button_to_choose_payment_method(callback_query_.data))


@router.callback_query(F.data.in_(["pay_with_yookassa_1month","pay_with_yookassa_6month","pay_with_yookassa_12month"]))
async def pay_with_yookassa(callback_query_:CallbackQuery):
    if callback_query_.data == "pay_with_yookassa_1month":
        cost = settings.COST_1MONTH
        duration = settings.DURATION_1MONTH
        description = settings.DURATION_1MONTH
    elif callback_query_.data =="pay_with_yookassa_6month":
        cost = settings.COST_6MONTH
        duration =  settings.DURATION_6MONTH
        description = settings.DURATION_6MONTH
    elif callback_query_.data=="pay_with_yookassa_12month":
        cost = settings.COST_12MONTH
        duration =  settings.DURATION_12MONTH
        description = settings.DURATION_12MONTH
    payment_id, pay_url_yookassa = await create_yookassa_payment(str(cost), description, callback_query_.from_user.id,duration)
    await safe_edit_text(callback_query_.message,settings.TEXT_PAY_WITH_CARD,reply_markup=await get_button_to_payment_with_yookassa(pay_url_yookassa,callback_query_.data))

@router.callback_query(F.data.in_(["pay_with_bitsby_1month","pay_with_bitsby_6month","pay_with_bitsby_12month"]))
async def pay_with_bitsby(callback_query_:CallbackQuery):
    if callback_query_.data=="pay_with_bitsby_1month":
        cost = settings.COST_1MONTH
        duration = settings.DURATION_1MONTH
        description = settings.DURATION_1MONTH
    elif callback_query_.data=="pay_with_bitsby_6month":
        cost = settings.COST_6MONTH
        duration =  settings.DURATION_6MONTH
        description = settings.DURATION_6MONTH
    elif callback_query_.data=="pay_with_bitsby_12month":
        cost = settings.COST_12MONTH
        duration =  settings.DURATION_12MONTH
        description = settings.DURATION_12MONTH
    pay_url_bitsby = await create_bitsby_payment(cost, description, callback_query_.from_user.id,duration)
    await safe_edit_text(callback_query_.message,settings.TEXT_PAY_WITH_CRYPTO,reply_markup=await get_button_to_payment_with_bitsby(pay_url_bitsby,callback_query_.data))

async def create_bitsby_payment(cost,description,user_id,duration):

    api = BitsbyAPI()

    service_data = json.dumps({
        "user_id": user_id,
        "duration": duration
    })

    response = await api.create_invoice(
        amount=cost,
        currency=settings.CURRENCY,
        description=description,
        service_data=service_data
    )

    if response and response.get("result") == "success":
        pay_url = response["data"]["url"]
    return pay_url

async def send_personal_invite(user_id,bot,cost):
    invite_link = await bot.create_chat_invite_link(
        chat_id=settings.CHANNEL_ID,
        member_limit=1,
        name=f"Для {user_id}|{cost}"
    )
    await bot.send_message(
        user_id,
        f"{settings.SEND_PERSONAL_INVITE_TEXT}\n{invite_link.invite_link}"
    )
