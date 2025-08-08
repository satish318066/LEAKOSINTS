
import os
import re
import requests
import telebot
from random import randint
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
API_URL = "https://leakosintapi.com/"

bot = telebot.TeleBot(BOT_TOKEN)
user_db = {}
redeem_codes = {}
referrals = {}

# Helper to calculate coin cost
def get_coin_cost(mode):
    return 5 if mode == "adv" else 2

def user_init(user):
    uid = user.id
    if uid not in user_db:
        user_db[uid] = {
            "username": user.username or "N/A",
            "coins": 200,
            "ref": None
        }

@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.from_user.id
    user_init(message.from_user)

    parts = message.text.split()
    if len(parts) > 1:
        ref = parts[1]
        try:
            ref_uid = int(ref)
            if uid != ref_uid and uid not in referrals:
                referrals[uid] = ref_uid
                user_db[ref_uid]["coins"] += 100
        except:
            pass
    bot.reply_to(message, f"👋 Welcome! You have {user_db[uid]['coins']} coins.
Use /searchnrm or /searchadv to begin.")

@bot.message_handler(commands=['balance'])
def balance_cmd(message):
    uid = message.from_user.id
    user_init(message.from_user)
    coins = user_db[uid]["coins"]
    bot.reply_to(message, f"💰 Your balance: {coins} coins")

@bot.message_handler(commands=['searchnrm', 'searchadv'])
def search_handler(message):
    uid = message.from_user.id
    user_init(message.from_user)

    mode = 'adv' if message.text.startswith('/searchadv') else 'nrm'
    cost = get_coin_cost(mode)
    if user_db[uid]["coins"] < cost:
        bot.reply_to(message, f"❌ Not enough coins! You need {cost} coins.")
        return

    query = message.text.split(' ', 1)[-1].strip()
    if not query:
        bot.reply_to(message, "❗ Please provide a query.")
        return

    limit = 300 if mode == "adv" else 100
    lang = "en"
    data = {"token": API_TOKEN, "request": query, "limit": limit, "lang": lang}
    try:
        res = requests.post(API_URL, json=data)
        j = res.json()
        if "Error code" in j:
            bot.reply_to(message, "⚠️ API Error: " + j["Error code"])
            return

        user_db[uid]["coins"] -= cost
        reply_texts = []
        for db_name, result in j["List"].items():
            header = f"<b>{db_name}</b>\n"
            content = result["InfoLeak"] + "\n"
            for row in result.get("Data", []):
                for k, v in row.items():
                    content += f"<b>{k}</b>: {v}\n"
            reply_texts.append(header + content)
        for part in reply_texts:
            bot.send_message(message.chat.id, part[:4000], parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ Failed to get response. Try again later.")

@bot.message_handler(commands=['give'])
def admin_give(message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split()
    if len(parts) != 3:
        bot.reply_to(message, "Usage: /give <user_id> <amount>")
        return
    uid = int(parts[1])
    amount = int(parts[2])
    user_db.setdefault(uid, {"username": "N/A", "coins": 0, "ref": None})
    user_db[uid]["coins"] += amount
    bot.reply_to(message, f"✅ Added {amount} coins to {uid}")

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.reply_to(message, "❓ Unknown command. Use /searchnrm or /searchadv.")

bot.polling()
    