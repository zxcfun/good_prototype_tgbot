import uuid
from config import settings
from yookassa import Payment,Configuration

Configuration.account_id = settings.SHOP_ID
Configuration.secret_key = settings.API_KEY_YOOKASSA

async def create_yookassa_payment(amount_rub: str, description: str, user_id: int,duration: int):
    payment = Payment.create(
        {
            "amount": {
                "value": amount_rub,
                "currency": settings.CURRENCY,
            },
            "confirmation": {
                "type": "redirect",
                "return_url": settings.BOT_URL,
            },
            "capture": True,
            "description": description,
            "metadata": {
                "user_id": user_id,
                "duration": duration
            },
        },
        str(uuid.uuid4()),
    )

    return payment.id, payment.confirmation.confirmation_url

async def check_payment_status(payment_id):
    payment=Payment.find_one(payment_id)
    return payment.status