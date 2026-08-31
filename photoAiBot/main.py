import asyncio, logging, os
from contextlib import contextmanager
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from bot.handlers import chat_router, photo_router
from aiohttp import web

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@contextmanager
def polling_lock():
    """Allow only one long-polling process inside a Render container."""
    if os.name == "nt":
        # Local development does not need the Linux file lock used by Render.
        yield True
        return

    import fcntl

    lock_file = open("/tmp/photo-ai-bot.polling.lock", "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock_file.close()
        logger.error("Polling is already running in this container; second process stopped.")
        yield False
        return

    try:
        yield True
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()

async def health_check(request):
    return web.Response(text="Bot is running")

async def main():
    try:
        settings.validate()
        logger.info("Все ключи успешно загружены!")
    except ValueError as e:
        logger.error(f"Ошибка конфигурации: {e}")
        return

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(chat_router)
    dp.include_router(photo_router)

    # запуск веб сервера для Render
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    logger.info(f"Веб-сервер запущен на порту {port}")
    logger.info("Бот запущен!")

    with polling_lock() as has_lock:
        if not has_lock:
            await bot.session.close()
            await runner.cleanup()
            return

        try:
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        finally:
            await bot.session.close()
            await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен!")
