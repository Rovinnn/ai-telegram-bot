import telebot
from gemma_api import call_local_gemma
from whisper_stt import transcribe_ogg
from my_tts_util import text_to_wav
import os

# === Replace with your Telegram Bot Token only ===
<<<<<<< HEAD
TELEGRAM_BOT_TOKEN = "your bot token here"
=======
TELEGRAM_BOT_TOKEN = "YOUR BOT TOKEN"
>>>>>>> 99b8705185692a7410583817ddda3ebad663ef4f

# Initialize Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# === Handle /start command ===
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Hi! I'm a locally-powered AI bot (Gemma + Whisper STT). Send me a voice message or text!")

# === Handle /tts command ===
@bot.message_handler(commands=['tts'])
def handle_tts(message):
    text = message.text[len('/tts'):].strip()
    if not text:
        bot.reply_to(message, "Please provide text to synthesize. Usage: /tts <your text>")
        return
    wav_path = "tts_output.wav"
    try:
        text_to_wav(text, wav_path)
        with open(wav_path, "rb") as audio:
            bot.send_audio(message.chat.id, audio, caption="Here is your TTS audio.")
    except Exception as e:
        bot.reply_to(message, "Sorry, TTS failed.")
        print("TTS error:", e)
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

# === Handle all text messages ===
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    try:
        response = call_local_gemma(user_input)
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, "⚠️ Sorry, something went wrong. Try again.")
        print("Error:", e)

# === Handle voice messages ===
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    if not file_info.file_path:
        bot.reply_to(message, "Sorry, could not retrieve the audio file.")
        return
    downloaded_file = bot.download_file(file_info.file_path)
    with open("voice.ogg", "wb") as f:
        f.write(downloaded_file)
    try:
        text = transcribe_ogg("voice.ogg")
        response = call_local_gemma(text)
        bot.reply_to(message, f"🗣️ You said: {text}\n🤖 {response}")
    except Exception as e:
        bot.reply_to(message, "Sorry, I couldn't understand the audio.")
        print("Whisper error:", e)

# Start polling
print("🤖 Bot is running with Gemma, Whisper STT, and F5-TTS...")
bot.infinity_polling() 
