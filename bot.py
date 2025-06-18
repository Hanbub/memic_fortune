import random
import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Get bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")
stickerpacksnames = os.getenv("STICKERPACKS_NAMES")
if not BOT_TOKEN or not stickerpacksnames:
    raise RuntimeError("BOT_TOKEN is not set. Add it to .env or your environment.")

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
    logging.info(f"Selected stickerpack {pack_name}")
    logging.info(f"Question: {message.text}")

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

    random_sticker = random.choice(list(stickerpacks_objs[pack_name].values()))
    logging.info(f"file_unique_id: {random_sticker["sticker_obj"].file_unique_id}")
    logging.info(f"file_id: {random_sticker["sticker_obj"].file_id}")
    logging.info(f"emoji: {random_sticker["sticker_obj"].emoji}")
    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker=random_sticker["sticker_obj"].file_id,
        reply_to_message_id=message.message_id,
    )

# Main polling loop
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
