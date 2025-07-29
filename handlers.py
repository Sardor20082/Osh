from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from languages import LANGS, USER_LANG
from utils import save_user
from downloader import handle_download
import os

CHANNEL_ID = os.environ.get("CHANNEL_ID")

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_handler, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(network_handler, pattern="^(youtube|tiktok|instagram)$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_download))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await check_subscription(update, context)
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇿 Uzbek", callback_data="lang_uz")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
    ])
    await update.message.reply_text("Tilni tanlang / Выберите язык / Choose language:", reply_markup=markup)

async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = query.data.split("_")[1]
    USER_LANG[query.from_user.id] = lang
    save_user(query.from_user.id, lang)
    await query.answer()
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("YouTube", callback_data="youtube")],
        [InlineKeyboardButton("TikTok", callback_data="tiktok")],
        [InlineKeyboardButton("Instagram", callback_data="instagram")]
    ])
    await query.edit_message_text(LANGS[lang]["welcome"], reply_markup=markup)

async def network_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    net = query.data
    lang = USER_LANG.get(query.from_user.id, 'uz')
    context.user_data["network"] = net
    await query.answer()
    await query.edit_message_text(LANGS[lang]["send_link"].format(net.title()))

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user.id)
        if member.status not in ["member", "administrator", "creator"]:
            await update.message.reply_text(f"{LANGS['uz']['not_subscribed']} {CHANNEL_ID}")
            return False
        return True
    except:
        await update.message.reply_text("Majburiy kanal sozlanmagan.")
        return False
