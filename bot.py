# ===============================
# 🤖 Telegram AI Summarizer Bot
# ===============================

# 📦 Telegram Bot Imports
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# 📦 System / Environment Imports
import os
from dotenv import load_dotenv

# 📦 AI Summarization
from summarizer import summarize_text


# 🔐 Load environment variables from a .env file
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

# 🧠 Store chat history (last 500 messages)
chat_history = []


# ===============================
# 📌 Command Handlers
# ===============================

# /start command – Greets the user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your AI summarizer bot 🤖")


# /hello command – Says hello with user's first name
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"Hello {user}!")


# /history command – Displays the last 10 stored messages
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not chat_history:
        await update.message.reply_text("❌ No chat history yet.")
        return

    recent = "\n".join(chat_history[-10:])
    await update.message.reply_text(f"🧾 Last 10 messages:\n{recent}")


# /summary command – Summarizes the last few messages
async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not chat_history:
        await update.message.reply_text("❌ No chat history to summarize.")
        return

    # Tell user bot is working
    thinking_message = await update.message.reply_text("🤔 Summarizing, please wait...")

    full_text = "\n".join(chat_history)
    summary = summarize_text(full_text)

    # Edit the "thinking..." message to show summary
    await thinking_message.edit_text(f"📋 *Summary:*\n{summary}", parse_mode='Markdown')


# /help command – Displays available commands
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Available Commands:*\n\n"
        "/start - Start the bot\n"
        "/hello - Say hello\n"
        "/history - Show last 10 messages\n"
        "/summarize - Summarize recent chat\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')


# ===============================
# 📝 Message Handler
# ===============================

# Handles all non-command text messages (group or private)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.text:
        chat_history.append(message.text)

        # Limit chat history to last 500 messages
        if len(chat_history) > 500:
            chat_history.pop(0)


# ===============================
# 🚀 Bot Application Setup
# ===============================

app = ApplicationBuilder().token(bot_token).build()

# Register Command Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("history", history))
app.add_handler(CommandHandler("summarize", summarize))
app.add_handler(CommandHandler("help", help_command))

# Register Message Handler
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# Start polling
print("✅ Bot is running...")
app.run_polling()