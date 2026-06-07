import os
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TOKEN)


async def send_post_for_approval(data):

    message = f"""
🚀 LinkedIn Post Draft

🎯 Role: {data['role']}
📌 Topic: {data['topic']}
⭐ Score: {data['score']}

📝 Post:
{data['post']}

🏷️ Hashtags:
{' '.join(data['hashtags'])}
"""

    keyboard = [
        [
            InlineKeyboardButton("✅ APPROVE", callback_data="approve"),
            InlineKeyboardButton("❌ REJECT", callback_data="reject"),
            InlineKeyboardButton("🔄 REGENERATE", callback_data="regenerate")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message[:4000],
        reply_markup=reply_markup
    )