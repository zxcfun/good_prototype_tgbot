import os
import hmac
import hashlib
import time
import json
import ipaddress

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session, check_and_save_payment
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot,Dispatcher
from aiogram.types import Update
from yookassa import Payment
from contextlib import asynccontextmanager
from app.database import create_tables
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("✅ База данных готова!")
    yield

from app.handlers import router,send_personal_invite

YOOKASSA_IP_RANGES = [
    ipaddress.ip_network("185.71.76.0/27"),
    ipaddress.ip_network("185.71.77.0/27"),
    ipaddress.ip_network("77.75.153.0/25"),
    ipaddress.ip_network("77.75.156.11/32"),
    ipaddress.ip_network("77.75.156.35/32"),
    ipaddress.ip_network("77.75.154.128/25"),
    ipaddress.ip_network("2a02:5180::/32"),
]

app = FastAPI(lifespan=lifespan)
bot = Bot(token=os.getenv("BOT_TOKEN",''))
dp = Dispatcher()
dp.include_router(router)


@app.post("/yookassa-webhook")
async def yookassa_webhook(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    client_ip_str = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For")
    if not client_ip_str:
        client_ip_str = request.client.host

    client_ip_str = client_ip_str.split(",")[0].strip()

    try:
        client_ip = ipaddress.ip_address(client_ip_str)

        if not any(client_ip in net for net in YOOKASSA_IP_RANGES):
            print(f"❌ Блокировка: запрос от неизвестного IP {client_ip_str}")
            raise HTTPException(status_code=403, detail="Forbidden IP")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP format")

    data = await request.json()
    event = data.get("event")
    payment_object = data.get("object", {})

    if event == "payment.succeeded":
        payment_id = payment_object.get("id")
        try:
            payment_info = Payment.find_one(payment_id)
            if payment_info.status != "succeeded":
                return {"status": "ok"}
        except Exception as e:
            print(f"Ошибка проверки платежа: {e}")
            return {"status": "ok"}
        metadata = payment_info.metadata or {}
        user_id = metadata.get("user_id")
        duration = metadata.get("duration")
        amount = float(payment_info.amount.value)

        if user_id:
            is_new = await check_and_save_payment(
                session=session,
                payment_id=payment_id,
                user_id=int(user_id),
                amount=amount,
                provider="yookassa",
                duration_months=duration
            )

            if is_new:
                print(f"✅ ЮKassa: успешная оплата! Пользователь: {user_id}|{amount} RUB")
                await send_personal_invite(int(user_id), bot , amount)
                await bot.send_message(int(user_id), settings.TEXT_AFTER_PAYMENT_RECEIVED)
            else:
                print(f"⚠️ ЮKassa: Платеж {payment_id} уже был обработан.")

    return {"status": "ok"}

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):

    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret_token != settings.TELEGRAM_WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid Telegram secret")

    update_data = await request.json()
    update = Update.model_validate(update_data, context={"bot": bot})

    await dp.feed_update(bot, update)

    return {"status": "ok"}

@app.post("/bitsby-webhook")
async def bitsby_webhook(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    timestamp = request.headers.get("X-Timestamp", "")
    signature = request.headers.get("X-Signature", "")
    raw_body = await request.body()

    if abs(time.time() - int(timestamp)) > 300:
        raise HTTPException(status_code=400, detail="Timestamp too old")

    expected_sig = "sha256=" + hmac.new(
        settings.BITSBY_WEBHOOK_SECRET.encode(),
        f"{timestamp}.{raw_body.decode()}".encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    data = json.loads(raw_body)

    invoice = data.get("invoice", data)
    if invoice.get("status") in ["paid", "success"]:
        try:
            service_data = invoice.get("serviceData", "{}")
            if isinstance(service_data, str):
                service_data = json.loads(service_data)

            user_id = service_data.get("user_id")
            duration_months = service_data.get("duration")

            payment_id = invoice.get("uid") or invoice.get("id")
            amount = float(invoice.get("amountFiat", invoice.get("amountFiatUSD", 0.0)))
            print(f"ДАННЫЕ ОТ BITSBY: {invoice}")

            if user_id and payment_id:
                is_new = await check_and_save_payment(
                    session=session,
                    payment_id=str(payment_id),
                    user_id=int(user_id),
                    amount=amount,
                    provider="bitsby",
                    duration_months=duration_months
                )

                if is_new:
                    print(f"✅ Успешная оплата Bitsby! Пользователь: {user_id}|{amount}")
                    await send_personal_invite(user_id, bot , amount)
                    await bot.send_message(user_id, settings.TEXT_AFTER_PAYMENT_RECEIVED)
                else:
                    print(f"⚠️ Платеж {payment_id} уже был обработан ранее (защита от дублей).")

        except Exception as e:
            print(f"Ошибка обработки данных Bitsby: {e}")

    return {"status": "ok"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)