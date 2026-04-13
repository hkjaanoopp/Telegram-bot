import os
import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant
import yt_dlp

# --- कॉन्फ़िगरेशन (यहाँ अपनी डिटेल्स भरें) ---
API_ID = "37291932" # अपना API ID डालें
API_HASH = "716f964578425b7015a92517bc8aaabb" # अपना API HASH डालें
BOT_TOKEN = "8617673760:AAFYi5MO3IeQlj8RZG7npzDChYrHzU0ixwo" # अपना BOT TOKEN डालें
UPDATE_CHANNEL = "https://t.me/+9XVKAwoTG61kZmJl" # अपने चैनल का यूजरनेम बिना @ के

app = Client(
    "HK_GAMER_BOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# फोर्स सब्सक्राइब फंक्शन
async def check_user(client, message):
    if not UPDATE_CHANNEL:
        return True
    try:
        user = await client.get_chat_member(UPDATE_CHANNEL, message.from_user.id)
        if user.status == "kicked":
            await message.reply_text("ब्रो, आप बैन हो चुके हो।")
            return False
        return True
    except UserNotParticipant:
        await message.reply_text(
            text=f"🔥 **WELCOME TO HK GAMER MOD VIP** 🔥\n\nबॉट का इस्तेमाल करने के लिए आपको हमारे चैनल को ज्वाइन करना होगा।",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{UPDATE_CHANNEL}")],
                [InlineKeyboardButton("🔄 Joined", callback_data="checksub")]
            ])
        )
        return False
    except Exception:
        return True

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        f"👋 नमस्ते **{message.from_user.mention}**!\n\n"
        "मैं **HK GAMER MOD VIP** वीडियो डाउनलोडर बॉट हूँ।\n"
        "मुझे किसी भी वीडियो का लिंक (YouTube, Insta, Chrome) भेजें, मैं उसे डाउनलोड कर दूँगा।\n\n"
        "🚀 **Status:** Active\n"
        "⚙️ **Speed:** High Speed",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/HKGAMAR_OFFICIAL")]
        ])
    )

@app.on_message(filters.text & filters.private)
async def dl_handler(client, message):
    # लिंक चेक करना
    if not message.text.startswith(("http://", "https://")):
        return

    # सब्सक्राइब चेक
    if not await check_user(client, message):
        return

    url = message.text
    status_msg = await message.reply_text("🔍 **वीडियो की जानकारी निकाली जा रही है...**", quote=True)

    try:
        # फ़ाइल का नाम सेट करना
        file_name = f"HK_Gamer_{int(time.time())}.mp4"
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': file_name,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await status_msg.edit("⚡ **वीडियो डाउनलोड हो रहा है... थोड़ा इंतज़ार करें।**")
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'No Title')

        await status_msg.edit("📤 **टेलीग्राम पर अपलोड किया जा रहा है...**")
        
        await message.reply_video(
            video=file_name,
            caption=f"✅ **Downloaded Successfully!**\n\n📝 **Title:** `{title}`\n\n🚀 **Power by:** @{UPDATE_CHANNEL}\n🤖 **Mod by:** `HK GAMER MOD VIP`",
            supports_streaming=True
        )
        
        await status_msg.delete()
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        await status_msg.edit(f"❌ **Error:** लिंक काम नहीं कर रहा है या सर्वर बिजी है।\n\n`{str(e)[:100]}`")

print("HK GAMER MOD VIP Bot has started!")
app.run()
