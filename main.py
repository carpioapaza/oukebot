import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

def obtener_saludo():
    hora_actual = datetime.now().hour
    if 6 <= hora_actual < 18:
        return "🌞 Bueeeenaaa"
    else:
        return "🌚 Bueeeenaaa"

async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for nuevo in update.message.new_chat_members:
        username = f"@{nuevo.username}" if nuevo.username else nuevo.first_name
        saludo = obtener_saludo()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{saludo}, {username}! 🦭🦭🦭"
        )
        try:
            with open('porlas.mp3', 'rb') as audio_file:
                await context.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=audio_file
                )
        except Exception as e:
            print(f"Error al enviar audio: {e}")

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida)
)

application.run_polling()
