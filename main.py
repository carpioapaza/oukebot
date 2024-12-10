import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Diccionarios de recursos estáticos
AUDIOS = {
    "porlas": "audios/porlas.mp3",
    "oño": "audios/oño.mp3",
    "glogloglo": "audios/glogloglo.mp3",
    "sisoy": "audios/sisoy.mp3",
    "relaxo": "audios/relaxo.mp3"
}

# STICKERS = {
#     "chevere": "CAACAgEAAxkBAAICZGABnOdFvUC9YYbvnGQUL6JPHy0AAjQAA8lYRxDoJqs_mQabcSME",
#     "jaja": "CAACAgIAAxkBAAICZ2ABnOesTxpO7wWR9XGHIUJm1_IAArwAA4tLBAQ"
# }

# GIFS = {
#     "roro": "https://tenor.com/bngj7.gif",
#     "fallo": "https://media.giphy.com/media/3o6ZsWGMzscC8yqnIY/giphy.gif"
# }

def obtener_saludo():
    hora_actual = datetime.now().hour
    if 6 <= hora_actual < 18:
        return "🌞 Bueeeena, mi queriidx"
    else:
        return "🌚 Bueeeena, mi queriidx"

async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for nuevo in update.message.new_chat_members:
        username = f"@{nuevo.username}" if nuevo.username else nuevo.first_name
        saludo = obtener_saludo()
        # Mensaje de bienvenida
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{saludo} {username}! 🦭🏳️‍🌈🦭"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "⚠️ *IMPORTANTE: ¡Uno para todos y todos para uno!.* ⚠️\n\n"
                "❌ NO Contenido pornográfico, ricou 🍆\n"
                "❌ NO spamees pa tu grupo pes 😠\n\n"
            ),
            parse_mode="Markdown"
        )
        try:
            with open('Si, eres.mp3', 'rb') as audio_file:
                await context.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=audio_file
                )
        except Exception as e:
            print(f"Error al enviar audio: {e}")


async def responder_contenido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.lower()

    for palabra, archivo in AUDIOS.items():
        if palabra in mensaje:
            try:
                with open(archivo, 'rb') as audio:
                    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio)
                return
            except FileNotFoundError:
                await update.message.reply_text(f"🔊 El archivo '{archivo}' no se encontró.")
            except Exception as e:
                await update.message.reply_text(f"❌ Error al enviar el audio: {e}")
    
    # for palabra, sticker_id in STICKERS.items():
    #     if palabra in mensaje:
    #         await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=sticker_id)
    #         return

    # for palabra, gif_url in GIFS.items():
    #     if palabra in mensaje:
    #         await context.bot.send_animation(chat_id=update.effective_chat.id, animation=gif_url)
    #         return


async def broma_muerte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Mensaje de "broma" antes de desactivar el bot
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "De tanto ingreso de dibujitos, el bot no pudo más... y ha muerto. 🦭🦭💀 MEEEEEEE\n\n"
        ),
        parse_mode="Markdown"
    )

    # Esperar 24 horas antes de reactivar
    await asyncio.sleep(24 * 60 * 60)

    # Mensaje de reactivación (opcional)
    await context.bot.send_message(
        chat_id=chat_id,
        text="🛠️ *El oño-bot ha revivió.* Iso fálalo! 🎉",
        parse_mode="Markdown"
    )



application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida)
)
application.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, responder_contenido)
)
application.add_handler(CommandHandler("pausar_bot", broma_muerte))



application.run_polling()
