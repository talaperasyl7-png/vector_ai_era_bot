import telebot
import google.generativeai as genai
from datetime import datetime

# 1. ТОКЕНДЕР
TELEGRAM_TOKEN = '8550555561:AAGnOOe46gHQP3Xb9KvsTV8jCLCTVOReNqw'
GEMINI_API_KEY = 'AIzaSyAY7OnrF37r5V_A-_85IEucQ1ToCtHGotw'

# 2. GEMINI-ДІ БАПТАУ
genai.configure(api_key=GEMINI_API_KEY)

# Қолжетімді модельдерді тізімнен автоматты түрде табу (404 қатесін болдырмау үшін)
try:
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Егер тізімде модельдер болса, ең біріншісін немесе 1.5-flash нұсқасын таңдаймыз
    selected_model_name = models[0] if models else 'gemini-1.5-flash'
    print(f"Қолданылатын модель: {selected_model_name}")
except Exception as e:
    selected_model_name = 'gemini-1.5-flash'
    print(f"Модель тізімін алу мүмкін болмады, әдепкі модель таңдалды.")

# Жүйелік нұсқаулық: Ботты 2026 жылға "көшіру"
system_instruction = (
    "Сен Ерасылдың ақылды ассистентісің. Бүгінгі күн: 20 наурыз 2026 жыл. "
    "Өзіңді осы уақытта тұрғандай сезініп жауап бер. "
    "2024 жыл туралы ескі мәліметтерді қазіргі жағдай ретінде айтпа."
)

model = genai.GenerativeModel(
    model_name=selected_model_name,
    system_instruction=system_instruction
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 3. КОМАНДАЛАР
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Сәлем! 2026 жылғы интеллектуалды бот дайын. Сұрағыңды қоя бер!")

# 4. ЧАТ ФУНКЦИЯСЫ
@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Бот жауап бере алмады, қайталап көріңіз.")
    except Exception as e:
        bot.reply_to(message, f"Қате шықты: {str(e)}")

# 5. ІСКЕ ҚОСУ
print("Бот қосылды! Telegram-ды тексер...")
bot.polling(none_stop=True)