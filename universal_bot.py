import telebot
from groq import Groq
import time

TELEGRAM_TOKEN = ""
GROQ_API_KEY = ""

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)
history = {}

@bot.message_handler(func=lambda m: True)
def handle(message):
    user_id = message.chat.id
    try:
        if user_id not in history:
            history[user_id] = [
                {"role": "system", "content": "Сен қазақша сөйлейтін AI көмекшісісің."}
            ]
        history[user_id].append({"role": "user", "content": message.text})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=history[user_id],
            temperature=0.4,
            top_p=1,
            max_tokens=1024,
            stream=False
        )

        reply = response.choices[0].message.content
        history[user_id].append({"role": "assistant", "content": reply})
        bot.send_message(user_id, reply)
    except Exception:
        pass
print("Бот қосылды...")
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception:
        time.sleep(5)
