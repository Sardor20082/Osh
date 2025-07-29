from telegram import Update
from telegram.ext import ContextTypes
from languages import LANGS, USER_LANG
import yt_dlp
import tempfile
import os
import shutil

async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    lang = USER_LANG.get(update.effective_user.id, "uz")
    msg = await update.message.reply_text("⏳ Yuklanmoqda...")

    tempdir = tempfile.mkdtemp()
    try:
        ydl_opts = {
            'outtmpl': os.path.join(tempdir, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        with open(video_path, 'rb') as f:
            await update.message.reply_video(video=f, caption=info.get("title", "🎥 Video"))
        await msg.delete()
    except Exception as e:
        await msg.edit_text("❌ Yuklab bo‘lmadi. Link noto‘g‘ri bo‘lishi mumkin.")
    finally:
        shutil.rmtree(tempdir, ignore_errors=True)
