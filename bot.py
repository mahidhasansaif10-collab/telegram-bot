import os
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("8756282218:AAE8995rhf9wSZonnJ2udXlZp-ITH_3gle0")
ADMIN_ID = 7852170201  # তোমার Telegram ID বসাও
GROUP_LINK = "https://t.me/AC_Trader_YT"

conn = sqlite3.connect("codes.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS codes (
    code TEXT PRIMARY KEY,
    used INTEGER DEFAULT 0
)
""")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 কোড পাঠাও")

async def addcode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ Admin না")

    code = context.args[0]
    try:
        cursor.execute("INSERT INTO codes VALUES (?,0)", (code,))
        conn.commit()
        await update.message.reply_text("✅ কোড যোগ হয়েছে")
    except:
        await update.message.reply_text("❌ আগে থেকেই আছে")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()

    cursor.execute("SELECT used FROM codes WHERE code=?", (code,))
    data = cursor.fetchone()

    if data:
        if data[0] == 0:
            cursor.execute("UPDATE codes SET used=1 WHERE code=?", (code,))
            conn.commit()
            await update.message.reply_text(f"✅ ঠিক কোড\n{GROUP_LINK}")
        else:
            await update.message.reply_text("❌ আগেই ব্যবহার হয়েছে")
    else:
        await update.message.reply_text("❌ ভুল কোড")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addcode", addcode))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check))

app.run_polling()
