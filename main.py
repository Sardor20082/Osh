import os
from app import flask_app, setup_webhook
from telegram.ext import Application
from handlers import setup_handlers
from admin import setup_admin_handlers
from utils import init_db

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

application = Application.builder().token(TOKEN).build()

setup_handlers(application)
setup_admin_handlers(application)
setup_webhook(application, flask_app, WEBHOOK_URL)
init_db()

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000)
