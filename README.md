from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, jsonify
import random
import os
from datetime import datetime
import threading
import time

# === إعدادات البوت ===
TOKEN = "8446070901:AAEEl7gFxqyA_cExC5yGXzygAcZMdjIipmI"
CHANNEL_USERNAME = "@Flix1211"

# === تخزين البيانات ===
bot_data = {
    "bot_name": "البوت الإسلامي المتقدم",
    "channel": CHANNEL_USERNAME,
    "last_message": "لم يتم إرسال رسائل بعد",
    "last_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_messages": 0,
    "status": "🟢 يعمل - يرسل كل 10 دقائق",
    "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "messages_history": [],
    "message_types": {
        "آيات": 0,
        "أحاديث": 0,
        "أذكار": 0
    }
}

# === قاعدة البيانات الإسلامية ===
islamic_content = {
    "آيات": [
        "📖 {قُلْ هُوَ اللَّهُ أَحَدٌ، اللَّهُ الصَّمَدُ، لَمْ يَلِدْ وَلَمْ يُولَدْ، وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ} - سورة الإخلاص",
        "📖 {رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ} - سورة البقرة",
        "📖 {إِنَّ مَعَ الْعُسْرِ يُسْرًا، إِنَّ مَعَ الْعُسْرِ يُسْرًا} - سورة الشرح",
        "📖 {وَإِذَا سَأَلَكَ عِبَادِي عَنِّي فَإِنِّي قَرِيبٌ أُجِيبُ دَعْوَةَ الدَّاعِ إِذَا دَعَانِ} - سورة البقرة",
        "📖 {يَا أَيُّهَا الَّذِينَ آمَنُوا اصْبِرُوا وَصَابِرُوا وَرَابِطُوا وَاتَّقُوا اللَّهَ لَعَلَّكُمْ تُفْلِحُونَ} - سورة آل عمران",
        "📖 {وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا وَيَرْزُقْهُ مِنْ حَيْثُ لَا يَحْتَسِبُ} - سورة الطلاق",
        "📖 {إِنَّ اللَّهَ مَعَ الصَّابِرِينَ} - سورة البقرة",
        "📖 {وَلَا تَيْأَسُوا مِن رَّوْحِ اللَّهِ إِنَّهُ لَا يَيْأَسُ مِن رَّوْحِ اللَّهِ إِلَّا الْقَوْمُ الْكَافِرُونَ} - سورة يوسف",
        "📖 {وَعَسَى أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ وَعَسَى أَن تُحِبُّوا شَيْئًا وَهُوَ شَرٌّ لَّكُمْ} - سورة البقرة",
        "📖 {وَذَكِّرْ فَإِنَّ الذِّكْرَى تَنفَعُ الْمُؤْمِنِينَ} - سورة الذاريات"
    ],
    
    "أحاديث": [
        "🌙 قال رسول الله ﷺ: 'تبسمك في وجه أخيك صدقة'",
        "🌙 قال رسول الله ﷺ: 'الكلمة الطيبة صدقة'",
        "🌙 قال رسول الله ﷺ: 'اتق الله حيثما كنت، وأتبع السيئة الحسنة تمحها، وخالق الناس بخلق حسن'",
        "🌙 قال رسول الله ﷺ: 'من كان يؤمن بالله واليوم الآخر فليقل خيراً أو ليصمت'",
        "🌙 قال رسول الله ﷺ: 'لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه'",
        "🌙 قال رسول الله ﷺ: 'إن الله لا ينظر إلى صوركم وأموالكم، ولكن ينظر إلى قلوبكم وأعمالكم'",
        "🌙 قال رسول الله ﷺ: 'الراحمون يرحمهم الرحمن، ارحموا من في الأرض يرحمكم من في السماء'",
        "🌙 قال رسول الله ﷺ: 'طلب العلم فريضة على كل مسلم'",
        "🌙 قال رسول الله ﷺ: 'إنما الأعمال بالنيات، وإنما لكل امرئ ما نوى'",
        "🌙 قال رسول الله ﷺ: 'الدين النصيحة'"
    ],
    
    "أذكار": [
        "💫 سبحان الله، والحمد لله، ولا إله إلا الله، والله أكبر",
        "💫 أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه",
        "💫 لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير",
        "💫 حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم",
        "💫 بسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء وهو السميع العليم",
        "💫 أعوذ بكلمات الله التامات من شر ما خلق",
        "💫 اللهم إني أسألك علماً نافعاً، ورزقاً طيباً، وعملاً متقبلاً",
        "💫 اللهم أنت ربي لا إله إلا أنت، خلقتني وأنا عبدك، وأنا على عهدك ووعدك ما استطعت",
        "💫 سبحان الله وبحمده، سبحان الله العظيم",
        "💫 لا حول ولا قوة إلا بالله العلي العظيم"
    ]
}

# === تطبيق ويب للعرض ===
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>البوت الإسلامي المتقدم</title>
        <style>
            body { font-family: Arial; background: #f0f8ff; padding: 40px; text-align: center; }
            .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
            h1 { color: #2c5aa0; }
            .stats { background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .message { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-right: 4px solid #2c5aa0; }
            .types { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0; }
            .type-card { background: #e8f5e8; padding: 15px; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🕌 البوت الإسلامي المتقدم</h1>
            <p>يعمل على السحابة - يرسل كل 10 دقائق ⏰</p>
            
            <div class="stats">
                <h3>📊 الإحصائيات</h3>
                <p><strong>القناة:</strong> """ + bot_data["channel"] + """</p>
                <p><strong>عدد الرسائل:</strong> """ + str(bot_data["total_messages"]) + """</p>
                <p><strong>آخر رسالة:</strong> """ + bot_data["last_message"] + """</p>
                <p><strong>الوقت:</strong> """ + bot_data["last_time"] + """</p>
                <p><strong>الحالة:</strong> """ + bot_data["status"] + """</p>
            </div>

            <div class="types">
                <div class="type-card">
                    <h4>📖 الآيات</h4>
                    <p>""" + str(bot_data["message_types"]["آيات"]) + """ رسالة</p>
                </div>
                <div class="type-card">
                    <h4>🌙 الأحاديث</h4>
                    <p>""" + str(bot_data["message_types"]["أحاديث"]) + """ رسالة</p>
                </div>
                <div class="type-card">
                    <h4>💫 الأذكار</h4>
                    <p>""" + str(bot_data["message_types"]["أذكار"]) + """ رسالة</p>
                </div>
            </div>
            
            <div class="message">
                <h3>📨 آخر الرسائل</h3>
                <p>""" + bot_data["last_message"] + """</p>
                <small>""" + bot_data["last_time"] + """</small>
            </div>
            
            <p>⏰ البوت يرسل رسائل تلقائية كل 10 دقائق إلى القناة</p>
            <p>🎯 يتناوب بين الآيات القرآنية، الأحاديث النبوية، والأذكار اليومية</p>
        </div>
    </body>
    </html>
    """

@app.route('/api/data')
def api_data():
    return jsonify(bot_data)

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

def update_bot_data(message, message_type):
    """تحديث بيانات البوت"""
    bot_data["last_message"] = message
    bot_data["last_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot_data["total_messages"] += 1
    bot_data["message_types"][message_type] += 1
    
    bot_data["messages_history"].append({
        "message": message,
        "time": bot_data["last_time"],
        "type": message_type
    })
    
    if len(bot_data["messages_history"]) > 20:
        bot_data["messages_history"].pop(0)

# === دوال بوت التلجرام ===
async def send_islamic_content(context: ContextTypes.DEFAULT_TYPE):
    try:
        # تناوب بين أنواع المحتوى
        message_types = list(islamic_content.keys())
        current_type = message_types[bot_data["total_messages"] % len(message_types)]
        
        # اختيار رسالة عشوائية من النوع المحدد
        message = random.choice(islamic_content[current_type])
        
        await context.bot.send_message(
            chat_id=CHANNEL_USERNAME,
            text=message,
            parse_mode='Markdown'
        )
        
        update_bot_data(message, current_type)
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] تم إرسال {current_type}: {message[:50]}...")
        
    except Exception as e:
        print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] خطأ: {e}")
        bot_data["status"] = f"🔴 خطأ: {str(e)}"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🕌 البوت الإسلامي المتقدم\n\n"
        f"📊 الإحصائيات:\n"
        f"• القناة: {CHANNEL_USERNAME}\n"
        f"• الرسائل المرسلة: {bot_data['total_messages']}\n"
        f"• آخر رسالة: {bot_data['last_time']}\n"
        f"• يعمل منذ: {bot_data['start_time']}\n\n"
        f"🎯 يرسل كل 10 دقائق:\n"
        f"• 📖 آيات قرآنية\n"
        f"• 🌙 أحاديث نبوية\n"
        f"• 💫 أذكار يومية\n\n"
        f"⚡ يعمل تلقائياً 24/7"
    )

def run_flask_app():
    """تشغيل تطبيق Flask"""
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 بدء خادم Flask على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_bot():
    """تشغيل بوت التلجرام"""
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start_command))
        
        job_queue = application.job_queue
        if job_queue:
            # إرسال رسالة كل 10 دقائق (600 ثانية)
            job_queue.run_repeating(send_islamic_content, interval=600, first=10)
            print("✅ تم تفعيل الجدولة التلقائية - رسائل كل 10 دقائق")
        
        print("🤖 بوت التلجرام يعمل...")
        print("⏰ يرسل كل 10 دقائق: آيات، أحاديث، أذكار")
        application.run_polling()
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")
        bot_data["status"] = f"🔴 خطأ: {str(e)}"

if __name__ == "__main__":
    print("🚀 بدء التشغيل الكامل للبوت الإسلامي المتقدم...")
    print("🎯 الميزات الجديدة:")
    print("   • ⏰ إرسال كل 10 دقائق")
    print("   • 📖 تناوب بين الآيات والأحاديث والأذكار")
    print("   • 📊 إحصائيات مفصلة")
    
    # تحديث حالة البوت
    bot_data["status"] = "🟢 يعمل - يرسل كل 10 دقائق"
    
    # تشغيل Flask في thread منفصل
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    # تشغيل البوت بعد تأخير بسيط
    time.sleep(5)
    
    # تشغيل البوت
    run_bot()
