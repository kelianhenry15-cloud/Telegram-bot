from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
import os

# ==============================
# IDENTIFIANTS TELEGRAM VIA VARIABLES D'ENVIRONNEMENT
# ==============================
api_id = int(os.getenv("API_ID"))        # Ajouter API_ID dans Render
api_hash = os.getenv("API_HASH")         # Ajouter API_HASH dans Render

# Session
client = TelegramClient('session_test', api_id, api_hash)

# ==============================
# CANAUX
# ==============================
SOURCE_CHANNEL_1 = "https://t.me/BTCsignala1"
SOURCE_CHANNEL_2 = "https://t.me/learn2tradefxfree"
TARGET_CHANNEL = -1002849978325  # ton canal privé

# ==============================
# FLASK POUR UPTIME ROBOT
# ==============================
app = Flask('')

@app.route('/')
def home():
    return "Bot actif!"

@app.route('/ping')
def ping():
    return "pong"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# ==============================
# FONCTION FORMATAGE GENERIQUE
# ==============================
def format_signal_generic(message: str) -> str:
    lines = message.splitlines()
    if not lines:
        return None

    header = lines[0].strip().upper()
    
    if "BUY" in header:
        direction = "🟢 J’ACHÈTE"
    elif "SELL" in header:
        direction = "🔴 JE VENDS"
    else:
        return None

    # Detect symbol
    symbol = "?"
    parts = header.split()
    for part in parts:
        if any(x in part for x in ["XAU", "BTC", "ETH", "USD"]):
            symbol = part
            break

    # Entry price
    entry_price = "?"
    if "@" in header:
        entry_price = header.split("@")[-1].strip()
    elif "ZONE" in header:
        entry_price = header.split("ZONE")[-1].strip()

    # TP & SL
    tps = []
    sl = ""
    for line in lines[1:]:
        line_clean = line.strip()
        if "TP" in line_clean.upper():
            tps.append("🎯 " + line_clean)
        elif "SL" in line_clean.upper() or "STOPLOSS" in line_clean.upper():
            sl = "🔒 " + line_clean

    final_msg = f"{direction} {symbol} à {entry_price}\n"
    for tp in tps:
        final_msg += tp + "\n"
    if sl:
        final_msg += sl

    return final_msg.strip()

# ==============================
# HANDLERS
# ==============================
@client.on(events.NewMessage(chats=SOURCE_CHANNEL_1))
async def handler1(event):
    raw = event.message.message
    formatted = format_signal_generic(raw)
    if formatted:
        await client.send_message(TARGET_CHANNEL, formatted)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL_2))
async def handler2(event):
    raw = event.message.message
    formatted = format_signal_generic(raw)
    if formatted:
        await client.send_message(TARGET_CHANNEL, formatted)

# ==============================
# LANCEMENT
# ==============================
print("✅ Bot lancé, en attente de signaux...")
with client:
    client.run_until_disconnected()
