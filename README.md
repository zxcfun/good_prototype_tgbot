🇬🇧 English       

Telegram Bot — Subscription & Payment Platform

A production-ready Telegram bot for selling subscriptions and managing access to private channels. Built with a focus on reliability, deep security, and real-world use.

Features:

    💳 Payments via YooKassa (cards, SBP) and Bitsby — a highly advantageous, low-fee cryptocurrency provider.

    🔐 Automatic access management — instantly generates a personal invite link upon successful payment. (Note: kicking users upon subscription expiry is handled by a separate script).

    🗄️ PostgreSQL database with async ORM (SQLAlchemy).

    🔔 Webhook-based payment processing (fully asynchronous, no polling).

    🛡️ Bulletproof security — protection against duplicate payments, webhook spoofing, replay attacks, and essentially all other edge cases.

    ⚙️ Fully configurable — subscription plans, prices, and texts are easily managed via a config file without changing the core code.

    (Admin commands are currently in development and not included in this version).

Stack: Python 3.13, aiogram 3, PostgreSQL, SQLAlchemy, Docker, Nginx

Live demo: @somezxc_bot — feel free to try it out.
🇷🇺 Русский 

Telegram-бот для продажи подписок с оплатой

Бот для продажи доступа к закрытым каналам и группам. Принимает оплату картой через ЮKassa и криптовалютой через Bitsby — максимально выгодный провайдер с низкой комиссией. После оплаты автоматически выдаёт доступ к каналу. (Важно: бот занимается только выдачей доступа, а кик по истечении подписки реализуется отдельным скриптом).

Что умеет:

    Приём оплаты через ЮKassa (карты, СБП) и выгодный криптопровайдер Bitsby.

    Автоматическая генерация персональных ссылок и выдача доступа при оплате.

    База данных PostgreSQL с асинхронным ORM (SQLAlchemy).

    Обработка платежей через вебхуки — без постоянного опроса серверов.

    Максимальная защита: от дублирующих платежей, поддельных вебхуков, повторного использования чеков и вообще любых проблем с безопасностью.

    Гибкий конфиг: настройка тарифов, цен и текстов через конфигурационные файлы без правки кода.

    (Команды для администратора в текущей версии отсутствуют).

Стек: Python 3.13, aiogram 3, PostgreSQL, SQLAlchemy, Docker, Nginx

Живое демо: @somezxc_bot — можно потыкать прямо сейчас.
