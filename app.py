from flask import Flask, request
from telegram import Update
import asyncio

flask_app = Flask(__name__)

def setup_webhook(application, flask_app, webhook_url):
    async def set_webhook():
        await application.bot.set_webhook(webhook_url + f"/{application.bot.token}")
    
    asyncio.get_event_loop().run_until_complete(set_webhook())

    @flask_app.post(f"/{application.bot.token}")
    async def webhook():
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
        return "ok"
