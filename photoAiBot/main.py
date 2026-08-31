import asyncio, logging, os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from config import settings
from bot.handlers import chat_router, photo_router
from aiohttp import web

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

    # Webhook mode is used in Render to ensure that Telegram delivers every
    # update to one endpoint instead of multiple polling processes.
    webhook_base_url = os.getenv("WEBHOOK_URL", "").rstrip("/")

    app = web.Application()
    app.router.add_get('/', health_check)

    if webhook_base_url:
        webhook_path = "/webhook"
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=webhook_path)
        setup_application(app, dp, bot=bot)

        runner = web.AppRunner(app)
        await runner.setup()
        port = int(os.environ.get('PORT', 8080))
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()

        await bot.set_webhook(
            f"{webhook_base_url}{webhook_path}",
            allowed_updates=dp.resolve_used_update_types(),
        )
        logger.info("Webhook configured; bot is running at %s", webhook_base_url)

        try:
            await asyncio.Event().wait()
        finally:
            await runner.cleanup()
        return

    # Fallback for local development without WEBHOOK_URL.
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    logger.info(f"Веб-сервер запущен на порту {port}")
    logger.info("Бот запущен!")

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
