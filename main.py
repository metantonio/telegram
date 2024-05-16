import logging
import smtplib
import time
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes


# Configura el token de acceso del bot y las credenciales del servidor de correo electrónico
TOKEN = '6762803307:AAFeCEFixGefIxKi8y0FccBd150aDyDXxmQ'
EMAIL_ADDRESS = 'antonio.martinez@qlx.com'
EMAIL_PASSWORD = 'gxlcqbfskpegulns'
verification_codes = {}

# Configura el nivel de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Inicializa el bot y el servidor SMTP
print("inicializando bot")
bot = Bot(token=TOKEN)
smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

# Manejador para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('¡Hola! Envía /download para descargar el archivo.')

# Manejador para el comando /download
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Genera un código de verificación aleatorio
    verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    verification_codes[update.effective_user.id] = (verification_code, time.time())
    
    # Envía el correo electrónico con el código de verificación
    send_email(update.effective_user.id, verification_code)
    
    await update.message.reply_text('Se ha enviado un correo electrónico con un código de verificación. Por favor, introdúcelo aquí.')

# Función para enviar el correo electrónico con el código de verificación
def send_email(user_id: int, verification_code: str) -> None:
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'antonio.martinez@qlx.com'
    msg['Subject'] = 'Código de Verificación'

    body = f'Su código de verificación es: {verification_code}'
    msg.attach(MIMEText(body, 'plain'))

    smtp_server.send_message(msg)

# Manejador para mensajes de texto
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    input_code = update.message.text.strip()
    
    if user_id in verification_codes:
        stored_code, timestamp = verification_codes[user_id]
        if time.time() - timestamp <= 300:  # Verifica si el código es válido dentro de los 5 minutos
            if input_code == stored_code:
                await update.message.reply_text('¡Código de verificación correcto! Descarga iniciada.')
                # Aquí podrías proporcionar el archivo
                del verification_codes[user_id]  # Elimina el código verificado
            else:
                await update.message.reply_text('¡Código de verificación incorrecto! Por favor, inténtalo de nuevo.')
        else:
            await update.message.reply_text('El código de verificación ha expirado. Por favor, solicita uno nuevo con /download.')
            del verification_codes[user_id]  # Elimina el código expirado
    else:
        await update.message.reply_text('No hay un código de verificación asociado a tu cuenta. Por favor, solicita uno nuevo con /download.')

# Función para verificar el código de verificación
def verificar_codigo(input_code: str) -> bool:
    # Aquí deberías implementar la lógica de verificación del código de verificación
    # Podrías comparar el código introducido con el código enviado previamente
    return input_code == 'CÓDIGO_ENVIADO'  # Solo para fines de ejemplo, debes implementar esto correctamente

# Configura los manejadores de comandos y mensajes
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("download", download))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    application.run_polling()


if __name__ == '__main__':
    main()
