from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace with your token
BOT_TOKEN = "7810013958:AAExxBHqH3No9CTMWE9zrTNbp714cHRQAso"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your AI summarizer bot 🤖")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"Hello {user}!")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))

print("Bot is running...")
app.run_polling()
