from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = '7761281791:AAE1GpFLw7nRHhfpqC9qaB96l0fD2A8JGeQ'


async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for nuevo in update.message.new_chat_members:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Bueeena, {nuevo.first_name}! 🦭🦭🦭")
        try:
            await context.bot.send_audio(chat_id=update.effective_chat.id,
                                         audio=open('oñooo.mp3', 'rb'))
        except Exception as e:
            print(f"Error al enviar audio: {e}")


application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))

application.run_polling()
