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
    "tomeseñora": "audios/tomeseño.mp3",
    "puno": "audios/estao.mp3",
    "atrapada": "audios/atrapada.mp3"
}

# Funciones auxiliares
def obtener_saludo() -> str:
    """Obtiene un saludo dependiendo de la hora actual."""
    hora_actual = datetime.now().hour
    if 6 <= hora_actual < 18:
        return "🌞 Bueeeena, mi queriiiidx"
    else:
        return "🌚 Bueeeena, mi queriiiidx"

# Handlers
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía un mensaje de bienvenida a los nuevos miembros del grupo."""
    if update.message and update.message.new_chat_members:
        for nuevo in update.message.new_chat_members:
            username = f"@{nuevo.username}" if nuevo.username else nuevo.first_name
            saludo = obtener_saludo()

            # Mensajes de bienvenida
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{saludo} {username}! 🦭🏳️‍🌈🦜"
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

async def notificar_salida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Notifica a los administradores y al dueño cuando un usuario abandona el grupo."""
    if update.message and update.message.left_chat_member:
        usuario_salido = update.message.left_chat_member
        usuario_nombre = f"@{usuario_salido.username}" if usuario_salido.username else usuario_salido.first_name

        try:
            # Obtener los administradores del grupo
            administradores = await context.bot.get_chat_administrators(chat_id=update.effective_chat.id)

            # Notificar a cada administrador
            for admin in administradores:
                try:
                    await context.bot.send_message(
                        chat_id=admin.user.id,
                        text=f"⚠️ El usuario {usuario_nombre} ha abandonado el grupo {update.effective_chat.title}.",
                    )
                except Exception as e:
                    print(f"No se pudo notificar al admin {admin.user.username}: {e}")
        except Exception as e:
            print(f"Error al obtener la lista de administradores: {e}")

async def responder_contenido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde a mensajes con audios si contienen palabras clave."""
    if update.message and update.message.text:  # Verificar que el mensaje no sea None
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
    else:
        print("El mensaje no contiene texto o es None.")

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
        text="De tanto ingreso de dibujitos, el oño-bot no pudo más... y ha muerto. 🧮🧮💀 MEEEEEEE\n\n",
        parse_mode="Markdown"
    )

    # Simular espera de 24 horas
    await asyncio.sleep(1 * 60 * 60)

    # Mensaje de reactivación
    await context.bot.send_message(
        chat_id=chat_id,
        text="🛠️ *El oño-bot ha revivió.* Iso fálalo! 🎉",
        parse_mode="Markdown"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejo de errores global."""
    print(f"Error encontrado: {context.error}")
    if update:
        print(f"Tipo de actualización: {type(update)}")
        if update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ Ocurrió un error inesperado. Por favor, inténtalo de nuevo."
            )

# Configuración de la aplicación
application = ApplicationBuilder().token(TOKEN).build()

# Registro de handlers
application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))
application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, notificar_salida))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_contenido))
application.add_handler(CommandHandler("matar", broma_muerte))

# Registro de manejador de errores
application.add_error_handler(error_handler)

# Ejecutar el bot
if __name__ == "__main__":
    application.run_polling()
