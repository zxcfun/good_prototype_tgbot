import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH, override=True)

class Settings(BaseSettings):
    BOT_TOKEN: str
    API_KEY_YOOKASSA: str
    SHOP_ID: str
    BITSBY_zxc_PROJECT_API_KEY: str
    BITSBY_zxc_PROJECT_ID: str
    BITSBY_WEBHOOK_SECRET: str
    TELEGRAM_WEBHOOK_SECRET: str
    TELEGRAM_WEBHOOK_URL: str
    BITSBY_WEBHOOK_URL: str
    CHANNEL_ID: int
    USER_ID: int
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    BOT_URL: str
    CURRENCY: str
    BITSBY_BASE_URL : str
    DEFAULT_BACK_BUTTON_CONTENT : str
    BACK_KEYBOARD_ADJUST : int
    SUBSCRIPTION_TEXT : str
    TEXT_CARD_METOD_CHOOSE : str
    TEXT_CRYPTO_METOD_CHOOSE : str
    TEXT_CARD_METOD_CHOSEN : str
    TEXT_CRYPTO_METOD_CHOSEN : str
    INTRODUCTION : str
    MORE_DETAILS : str
    TEXT_1MONTH : str
    TEXT_6MONTH : str
    TEXT_12MONTH : str
    TEXT_BEFORE_CHOOSE_PAYMENT_METHOD_1MONTH : str
    TEXT_BEFORE_CHOOSE_PAYMENT_METHOD_6MONTH : str
    TEXT_BEFORE_CHOOSE_PAYMENT_METHOD_12MONTH : str
    COST_1MONTH : float
    COST_6MONTH : float
    COST_12MONTH : float
    DURATION_1MONTH : int
    DURATION_6MONTH : int
    DURATION_12MONTH : int
    DESCRIPTION_1MONTH : str
    DESCRIPTION_6MONTH : str
    DESCRIPTION_12MONTH : str
    TEXT_PAY_WITH_CARD : str
    TEXT_PAY_WITH_CRYPTO : str
    SEND_PERSONAL_INVITE_TEXT : str
    JOIN_BUTTON_TEXT : str
    MORE_ABOUT_CHANNEL_BUTTON_TEXT : str
    TEXT_AFTER_PAYMENT_RECEIVED : str

    model_config = SettingsConfigDict(extra="ignore")

settings = Settings()