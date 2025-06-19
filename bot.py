import random
import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiohttp import web  # Needed to bind to port 8080

# Load .env
load_dotenv()

# Get bot token and stickerpacks
BOT_TOKEN = os.getenv("BOT_TOKEN")
stickerpacksnames = os.getenv("STICKERPACKS_NAMES")
if not BOT_TOKEN or not stickerpacksnames:
    raise RuntimeError("BOT_TOKEN or STICKERPACKS_NAMES is not set.")

# Logging
logging.basicConfig(level=logging.INFO)

# Produce sticker dictionary
stickerspacks_ids = stickerpacksnames.split(",")
stickerpacks_objs = {x: {} for x in stickerspacks_ids}

# Init bot and dispatcher
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# /start command
@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer("Hi! Send me anything, and I'll reply with a random sticker!")

# Handle all text messages
@dp.message(F.text)
async def handle_user_text(message: types.Message):
    pack_name = random.choice(list(stickerpacks_objs.keys()))
    logging.info(f"Selected stickerpack: {pack_name}")
    logging.info(f"User Question: {message.text}")

    # Load stickers if not already loaded
    if not stickerpacks_objs[pack_name]:
        logging.info(f"Loading empty stickerpack: {pack_name}")
        sticker_set = await bot.get_sticker_set(pack_name)
        stickerpacks_objs[pack_name] = {
            sticker.file_unique_id: {
                "sticker_obj": sticker,
                "custom_description": "",
            } for sticker in sticker_set.stickers
        }

    random_sticker = random.choice(list(stickerpacks_objs[pack_name].values()))["sticker_obj"]
    logging.info(f"file_unique_id: {random_sticker.file_unique_id}")
    logging.info(f"file_id: {random_sticker.file_id}")
    logging.info(f"emoji: {random_sticker.emoji}")

    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker=random_sticker.file_id,
        reply_to_message_id=message.message_id,
    )

# Dummy web server to bind /healthz for Render
async def dummy_web_server():
    async def handle(request):
        return web.Response(text="Bot is alive!")
    app = web.Application()
    app.add_routes([web.get("/healthz", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0")
    await site.start()

# Main entry
async def main():
    await asyncio.gather(
        dummy_web_server(),  # Binds port 8080 for Render
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
