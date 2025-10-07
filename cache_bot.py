import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN, CACHE_GROUP_ID

app = Client("cache_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 📌 जब कोई bot cache में add करे
@app.on_message(filters.command("cache_add") & filters.private)
async def cache_add_handler(client, message: Message):
    try:
        data = message.text.split(" ", 1)[1]
        title, duration, link, audio_id, video_id = [x.strip() for x in data.split("||")]

        caption = (
            f"<b>🎵 title:</b> {title.lower()}\n"
            f"<b>⏱ duration:</b> {duration}\n"
            f"<b>🔗 link:</b> {link}\n"
            f"<b>🔊 audio_id:</b> {audio_id}\n"
            f"<b>🎬 video_id:</b> {video_id}"
        )

        await client.send_message(
            chat_id=CACHE_GROUP_ID,
            text=caption,
            disable_web_page_preview=True
        )

        await message.reply("✅ Cached successfully.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# 📌 Cache search command
@app.on_message(filters.command("cache_find") & filters.private)
async def cache_find_handler(client, message: Message):
    try:
        query = message.text.split(" ", 1)[1].lower()
        async for msg in client.search_messages(CACHE_GROUP_ID, query):
            if query in msg.text.lower():
                await message.reply(f"✅ Found in cache:\n\n{msg.text}")
                return
        await message.reply("❌ Not found in cache.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

app.run()
