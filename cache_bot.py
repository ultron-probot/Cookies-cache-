from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, CACHE_GROUP_ID

app = Client("cache_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("cache_add") & filters.private)
async def cache_add_handler(client, message):
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
        await client.send_message(CACHE_GROUP_ID, caption, disable_web_page_preview=True)
        await message.reply("✅ Cached successfully.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@app.on_message(filters.command("cache_find") & filters.private)
async def cache_find_handler(client, message):
    try:
        query = message.text.split(" ", 1)[1].lower()
        async for msg in client.search_messages(CACHE_GROUP_ID, query):
            if query in msg.text.lower():
                await message.reply(f"✅ Found in cache:\n\n{msg.text}")
                return
        await message.reply("❌ Not found in cache.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# 📌 Startup message
@app.on_connect()
async def on_connect(client):
    try:
        await client.send_message(CACHE_GROUP_ID, "Cache bot started successfully ❤️‍🔥🥀")
        print("Startup message sent!")
    except Exception as e:
        print(f"Error sending startup message: {e}")

if __name__ == "__main__":
    app.run()
