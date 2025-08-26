import os
import requests
from substrateinterface import SubstrateInterface
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TARGET_ADDRESS = os.getenv("TARGET_ADDRESS")

bot = Bot(token=BOT_TOKEN)

substrate = SubstrateInterface(
    url="wss://rpc.polkadot.io",
    ss58_format=0,
    type_registry_preset='polkadot'
)

def send_alert(sender, amount):
    message = f"🚨 Pembelian terdeteksi!\n👤 Dari: {sender}\n💰 Jumlah: {amount} DOT"
    bot.send_message(chat_id=CHAT_ID, text=message)

def listen_events():
    for event in substrate.subscribe_events():
        for e in event['events']:
            if e['event']['module_id'] == 'Balances' and e['event']['event_id'] == 'Transfer':
                params = e['event']['attributes']
                sender = params[0]
                receiver = params[1]
                amount = int(params[2]) / 10**10

                if receiver == TARGET_ADDRESS:
                    send_alert(sender, amount)

if __name__ == "__main__":
    listen_events()
