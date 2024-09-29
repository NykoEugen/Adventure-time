import logging
from contextlib import asynccontextmanager

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot

from config import BOT_TOKEN, NGROK_TUNNEL_URL
from handlers.db import check_connection, close_connection

from handlers import promt_handler, start_message

logger = logging.getLogger("Main")
logging.basicConfig(
    level=logging.INFO,
    format=u'%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)

storage = MemoryStorage()

WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}"


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_connection()

    try:
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != WEBHOOK_URL:
            await bot.set_webhook(url=WEBHOOK_URL)
            webhook_info = await bot.get_webhook_info()
            logger.info(webhook_info.url)
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")

    logger.info("App started")
    dp.include_routers(start_message.router, promt_handler.router, )
    yield  # This will allow the app to run
    await bot.session.close()
    await close_connection()
    logger.info("App stopped")

app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)
