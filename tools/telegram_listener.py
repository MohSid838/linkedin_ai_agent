import os
import asyncio
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes
)

from tools.linkedin_post import post_to_linkedin

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# ---------------- HANDLER ----------------
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    action = query.data

    print("🔥 CALLBACK RECEIVED:", action)

    post_text = query.message.text

    if "📝 Post:" in post_text:
        post_text = post_text.split("📝 Post:")[-1].strip()

    # ---------------- APPROVE ----------------
    if action == "approve":

        await query.edit_message_text("🚀 Posting to LinkedIn...")

        print("🚀 BEFORE LINKEDIN CALL")

        # ✅ IMPORTANT: run async properly
        await post_to_linkedin(post_text)

        print("🚀 AFTER LINKEDIN CALL")

        await query.message.reply_text("✅ Posted on LinkedIn!")

    # ---------------- REJECT ----------------
    elif action == "reject":
        await query.edit_message_text("❌ Rejected")

    # ---------------- REGENERATE ----------------
    elif action == "regenerate":
        await query.edit_message_text("🔄 Regenerating post...")
        await query.message.reply_text("Use pipeline again for regeneration")


# ---------------- RUN APP ----------------
def run_listener():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("🤖 Telegram Listener Running...")

    app.run_polling()


if __name__ == "__main__":
    run_listener()