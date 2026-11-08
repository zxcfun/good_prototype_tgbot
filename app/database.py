from datetime import datetime
from typing import Optional, AsyncGenerator

from sqlalchemy import Integer
from sqlalchemy import select
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import settings as config_settings


class Settings(BaseSettings):
    DB_HOST: str = config_settings.DB_HOST
    DB_PORT: int = config_settings.DB_PORT
    DB_USER: str = config_settings.DB_USER
    DB_PASS: str = config_settings.DB_PASS
    DB_NAME: str = config_settings.DB_NAME

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# 3. Модели
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    payment_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    amount: Mapped[float]
    provider: Mapped[str] = mapped_column(String(50))
    duration_months: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def check_and_save_payment(
        session: AsyncSession,
        payment_id: str,
        user_id: int,
        amount: float,
        provider: str,
        duration_months: int = 1
) -> bool:
    """
    Проверяет, есть ли платеж в базе.
    Если нет — сохраняет его и возвращает True (доступ можно выдавать).
    Если есть — возвращает False (это дубль или мошенник).
    """
    stmt = select(Payment).where(Payment.payment_id == payment_id)
    result = await session.execute(stmt)
    existing_payment = result.scalar_one_or_none()


    if existing_payment:
        return False

    user_stmt = select(User).where(User.id == user_id)
    user_result = await session.execute(user_stmt)
    existing_user = user_result.scalar_one_or_none()

    if not existing_user:
        new_user = User(id=user_id)
        session.add(new_user)

    new_payment = Payment(
        payment_id=payment_id,
        user_id=user_id,
        amount=amount,
        provider=provider,
        duration_months=duration_months
    )
    session.add(new_payment)


    await session.commit()

    return True