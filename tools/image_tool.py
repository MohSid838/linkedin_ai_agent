import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


async def send_post_for_approval(data):

    bot = Bot(token=TOKEN)

    message = f"""
🚀 LinkedIn Post Draft

🎯 Role: {data['role']}
📌 Topic: {data['topic']}
⭐ Score: {data['score']}

📝 Post:
{data['post']}

🏷️ Hashtags:
{' '.join(data['hashtags'])}

---
Reply: APPROVE or REJECT (manual for now)
"""

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message[:4000]  # Telegram limit safety
    )