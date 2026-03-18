import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import save_task, get_tasks, mark_done
from brain import get_reply

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey Sakshi 👋 I'm your personal assistant!\n\n"
        "Commands:\n"
        "/tasks — see your task list\n"
        "/done <id> — mark task complete\n"
        "/remind <task> — save a reminder\n"
    )

async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_tasks()
    if not tasks:
        await update.message.reply_text("No pending tasks! 🎉 You're all caught up.")
    else:
        msg = "📋 Your tasks:\n\n"
        for t in tasks:
            msg += f"[{t.id}] {t.text}\n"
        msg += "\nType /done <id> to mark complete ✅"
        await update.message.reply_text(msg)

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        task_id = int(context.args[0])
        mark_done(task_id)
        await update.message.reply_text(f"Task {task_id} done! ✅ Great work 💪")
    except:
        await update.message.reply_text("Usage: /done <task_id>")

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task = " ".join(context.args)
    if task:
        save_task(task)
        await update.message.reply_text(f"Saved: '{task}' ✅")
    else:
        await update.message.reply_text("Usage: /remind <your task>")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    reply = get_reply(text)

    if reply == "FETCH_TASKS":
        await show_tasks(update, context)
    elif any(w in text.lower() for w in ["remind me", "add task", "save task"]):
        save_task(text)
        await update.message.reply_text("Task saved! ✅")
    else:
        await update.message.reply_text(reply)

async def night_checkin():
    await bot.send_message(
        chat_id=CHAT_ID,
        text="🌙 Night check-in!\n\nWhat were your top 3 wins today?\nWhat are your 3 priorities for tomorrow?"
    )

async def morning_nudge():
    tasks = get_tasks()
    task_preview = ""
    if tasks:
        task_preview = "\n\nYour pending tasks:\n" + "\n".join(f"• {t.text}" for t in tasks[:3])
    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"☀️ Good morning Sakshi! Let's crush it today 💪{task_preview}"
    )
async def on_startup(app):
    scheduler.start()

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tasks", show_tasks))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    scheduler.add_job(night_checkin, "cron", hour=22, minute=0)
    scheduler.add_job(morning_nudge, "cron", hour=8, minute=0)

    app.post_init = on_startup

    app.run_polling()

if __name__ == "__main__":
    main()