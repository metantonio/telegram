import os
import logging
import smtplib
import time
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import telebot
from dotenv import load_dotenv

from utils import find_user, find_files

# Carga las variables de entorno desde el archivo .env
load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')

# Diccionario para almacenar los códigos de verificación
verification_codes = {}


# Configura el nivel de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
print("initializing bot")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):    
    user = message.from_user
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    bot.reply_to(message, f'Howdy, how are you doing {first_name}?')

""" @bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text) """

@bot.message_handler(commands=['download'])
def handle_download_request(message):
    print("correo de verificación")
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username

    # Genera un código de verificación aleatorio
    verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    timestamp = time.time()
    verification_codes[user_id] = (verification_code, timestamp)
    # Aquí deberías almacenar el código de verificación en una base de datos
    # o en una estructura de datos en memoria para su posterior validación

    # Envía el correo electrónico con el código de verificación
    verification_user = send_email(username, verification_code)
    if verification_user == None:
        response = (f"Hola, {first_name} (@{username}). "
                f"Tu usuario no concuerda con nuestros registros."
                f"Por favor, intenta de nuevo o comunícate con el administrador")
        bot.reply_to(message, response)
        return


    response = (f"Hola, {first_name} (@{username}). "
                f"Si el usuario es correcto, se le ha enviado un correo electrónico con un código de verificación. "
                f"Por favor, introdúcelo aquí para continuar.")
    bot.reply_to(message, response)

# Función para enviar el correo electrónico con el código de verificación
def send_email(user, verification_code):
    email = find_user(user)
    if email == None:
        print("user email not found")
        return None
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = email 
    msg['Subject'] = 'Código de Verificación'

    body = f'Su código de verificación es: {verification_code}'
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
    
    return True

@bot.message_handler(func=lambda message: True)
def verify_code(message):
    user = message.from_user
    user_id = user.id
    input_code = message.text.strip()

    username = user.username

    if user_id in verification_codes:
        stored_code, timestamp = verification_codes[user_id]
        if time.time() - timestamp <= 300:  # Verifica si el código es válido dentro de los 5 minutos
            if input_code == stored_code:
                urls = find_files(username)
                bot.reply_to(message, f'¡Código de verificación correcto! Aquí está tu archivo(s). {urls}')
                # Proporcionar el archivo para descargar
                """ with open('path_to_your_file', 'rb') as file:
                    bot.send_document(user_id, file) """
                del verification_codes[user_id]  # Elimina el código verificado
            else:
                bot.reply_to(message, '¡Código de verificación incorrecto! Por favor, inténtalo de nuevo.')
        else:
            bot.reply_to(message, 'El código de verificación ha expirado. Por favor, solicita uno nuevo con /download.')
            del verification_codes[user_id]  # Elimina el código expirado
    else:
        bot.reply_to(message, 'No hay un código de verificación asociado a tu cuenta. Por favor, solicita uno nuevo con /download.')


bot.infinity_polling()