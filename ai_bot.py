import os
import time
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = 8387096789:AAGoA_dlN0tNS-ax3eZ4L6fXrAo2NMe00oA
AI_API_KEY = os.getenv("AI_API_KEY")  # اختياري

if not BOT_TOKEN:
    raise RuntimeError("رجاءً عيّن متغيّر البيئة BOT_TOKEN بتوكن البوت من BotFather.")

# ---------- طبقة الذكاء ----------
def ask_ai(prompt: str) -> str:
    """
    لو AI_API_KEY موجود، نستخدم API لموديل محادثة.
    غيّر الرابط/الموديل حسب الخدمة اللي عندك.
    """
    if not AI_API_KEY:
        return fallback_reply(prompt)

    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {AI_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "انت مساعد عربي مختصر ومباشر. جاوب بوضوح وبأمثلة عند الحاجة."
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 300,
            "temperature": 0.7
        }
        resp = requests.post(url, headers=headers, json=data, timeout=20)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return "صار خلل مؤقت بالرد الذكي. بحاول أرد بشكل مبسّط."

def fallback_reply(text: str) -> str:
    """رد منطقي بسيط إذا ما في API."""
    t = text.strip().lower()
    if any(x in t for x in ["مرحبا", "السلام", "مرحب", "hello", "hi"]):
        return "أهلاً! كيف فيني أساعدك اليوم؟ 🙂"
    if "/help" in t or "مساعدة" in t:
        return "اكتب سؤالك مباشرة، وبجاوبك. جرّب مثلاً: 'كيف أنشئ بوت تلغرام؟'"
    if "تلغرام" in t and "بوت" in t:
        return "لبناء بوت تلغرام: أنشئه عبر BotFather، خذ التوكن، وبرمج باستخدام python-telegram-bot."
    if "اسم ملف" in t or "سمي الملف" in t:
        return "سمّيه: ai_bot.py أو smart_reply_bot.py — أسماء واضحة وقصيرة."
    # رد عام
    return f"فهمت قصدك: {text}\nإذا بدك تفصيل أكثر، اسألني بشكل محدّد."

# ---------- أوامر ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً! أنا بوت ذكي. اكتب سؤالك مباشرة، أو جرب /help.\n"
        "إذا وفّرت AI_API_KEY بقدّر أعطيك ردود أذكى 😉"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "الأوامر:\n"
        "- /start: ترحيب\n"
        "- /help: هذه المساعدة\n"
        "- /ping: فحص سريع\n"
        "أرسل أي رسالة نصية لأرد عليك بشكل ذكي."
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ts = int(time.time())
    await update.message.reply_text(f"pong ✅ ({ts})")

# ---------- الرد الذكي على الرسائل ----------
async def smart_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    answer = ask_ai(user_text)
    await update.message.reply_text(answer)

# ---------- التشغيل ----------
async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))

    print("البوت شغّال... اضغط Ctrl+C للإيقاف.")
    await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
