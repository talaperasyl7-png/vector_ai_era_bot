import telebot
from groq import Groq

TELEGRAM_TOKEN = "8764490514:AAGZYuTF1LdywG3nMDWIRB14mUnAlhkQMqs"
GROQ_API_KEY = "YOUR_KEY_HERE"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

history = {}

@bot.message_handler(func=lambda m: True)
def handle(message):
    user_id = message.chat.id

    if user_id not in history:
        history[user_id] = [
            {"role": "system", "content": "Сен қазақша сөйлейтін AI көмекшісісің."}
        ]

    history[user_id].append({"role": "user", "content": message.text})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history[user_id],
        max_tokens=1000
    )

    reply = response.choices[0].message.content
    history[user_id].append({"role": "assistant", "content": reply})

    bot.send_message(user_id, reply)

bot.polling()