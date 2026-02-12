import os
import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration
TOKEN = os.environ.get("BOT_TOKEN")
QUESTIONS = [
    "Q1: What is your primary marketing goal?",
    "Q2: Which platform do you use most (IG, FB, LinkedIn)?",
    "Q3: Do you currently use paid ads?",
    "Q4: What is your monthly budget?",
    "Q5: Would you like a free consultation?"
]

# Simple in-memory database (Resets on deploy/restart)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    now = datetime.datetime.now()
    
    # Check if user already finished this week
    if user_id in user_data and user_data[user_id].get('finished'):
        last_date = user_data[user_id]['date']
        if (now - last_date).days < 7:
            await update.message.reply_text("Please come back next week for new channeling!")
            return

    user_data[user_id] = {'step': 0, 'date': now, 'finished': False}
    await update.message.reply_text("Welcome to the Digital Marketing Quiz! Let's begin.\n\n" + QUESTIONS[0])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data or user_data[user_id]['finished']:
        return

    current_step = user_data[user_id]['step']
    current_step += 1
    
    if current_step < len(QUESTIONS):
        user_data[user_id]['step'] = current_step
        await update.message.reply_text(QUESTIONS[current_step])
    else:
        user_data[user_id]['finished'] = True
        await update.message.reply_text("Thank you for your answers! Please come back next week for new channeling.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()
