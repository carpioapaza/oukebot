import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

# Cargar el token desde las variables de entorno
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Diccionarios de recursos estáticos
AUDIOS = {
    "porlas": "audios/porlas.mp3",
    "oño": "audios/oño.mp3",
    "glogloglo": "audios/glogloglo.mp3",
    "sisoy": "audios/sisoy.mp3",
    "relaxo": "audios/relaxo.mp3",
    "melo": "audios/chumbi.mp3",
}

# Funciones auxiliares
def obtener_saludo() -> str:
    """Obtiene un saludo dependiendo de la hora actual."""
    hora_actual = datetime.now().hour
    if 6 <= hora_actual < 18:
        return "🌞 Bueeeena, mi queriidx"
    else:
        return "🌚 Bueeeena, mi queriidx"

# Handlers
async def cargar_miembros_existentes(application):
    """Carga los IDs de los miembros existentes al iniciar el bot."""
    global miembros_existentes
    chat_id = "<ID_DEL_GRUPO>"  # Reemplaza con el ID del grupo donde está el bot
    try:
        chat_members = await application.bot.get_chat_administrators(chat_id)
        miembros_existentes = {member.user.id for member in chat_members}
    except Exception as e:
        print(f"Error al cargar miembros existentes: {e}")

# Handlers
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía un mensaje de bienvenida a los nuevos miembros del grupo."""
    for nuevo in update.message.new_chat_members:
        if nuevo.id in miembros_existentes:
            continue  # Evitar saludar a miembros ya registrados

        # Registrar al nuevo miembro en la lista
        miembros_existentes.add(nuevo.id)

        username = f"@{nuevo.username}" if nuevo.username else nuevo.first_name
        saludo = obtener_saludo()

        # Mensajes de bienvenida
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{saludo} {username}! 🦭🏳️‍🌈🦭"
        )
        # Enviar audio de bienvenida
        try:
            with open('Si, eres.mp3', 'rb') as audio_file:
                await context.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=audio_file
                )
        except FileNotFoundError:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ Audio de bienvenida no encontrado."
            )


async def responder_contenido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde a mensajes con audios si contienen palabras clave."""
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

async def broma_muerte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simula la muerte del bot y lo reanima después de 24 horas."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Verificar permisos del usuario
    chat_member = await context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if chat_member.status not in ["administrator", "creator"]:
        await context.bot.send_message(
            chat_id=chat_id,
            text="🚫 *No seas sapo xD 🐸🐸",
            parse_mode="Markdown"
        )
        return

    # Mensaje de "muerte"
    await context.bot.send_message(
        chat_id=chat_id,
        text="De tanto ingreso de dibujitos, el oño-bot no pudo más... y ha muerto. 🦭🦭💀 MEEEEEEE\n\n",
        parse_mode="Markdown"
    )

    # Simular espera de 24 horas
    await asyncio.sleep(24 * 60 * 60)

    # Mensaje de reactivación
    await context.bot.send_message(
        chat_id=chat_id,
        text="🛠️ *El oño-bot ha revivió.* Iso fálalo! 🎉",
        parse_mode="Markdown"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejo de errores global."""
    print(f"Error encontrado: {context.error}")
    if update and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Ocurrió un error inesperado. Por favor, inténtalo de nuevo."
        )

# Configuración de la aplicación
application = ApplicationBuilder().token(TOKEN).build()

# Registro de handlers
application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_contenido))
application.add_handler(CommandHandler("matar", broma_muerte))

# Registro de manejador de errores
application.add_error_handler(error_handler)

# Ejecutar el bot
# Ejecutar el bot
if __name__ == "__main__":
    application.run_polling(before_start=cargar_miembros_existentes(application))