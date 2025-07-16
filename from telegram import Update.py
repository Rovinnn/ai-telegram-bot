from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import whisper
from TTS.api import TTS
import openai
import os
from pydub import AudioSegment

# Load models
whisper_model = whisper.load_model("base")
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

openai.api_key = "sk-proj-1234567890"

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Step 1: Download voice
    file = await update.message.voice.get_file()
    file_path = await file.download_to_drive("user_voice.ogg")
    
    # Step 2: Convert OGG to WAV
    audio = AudioSegment.from_ogg("user_voice.ogg")
    audio.export("user_voice.wav", format="wav")
    
    # Step 3: Transcribe with Whisper
    result = whisper_model.transcribe("user_voice.wav")
    user_text = result["text"]

    # Step 4: Get GPT response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_text}]
    )
    ai_text = response['choices'][0]['message']['content']

    # Step 5: Convert AI response to speech
    tts_model.tts_to_file(text=ai_text, file_path="response.wav")
    response_audio = AudioSegment.from_wav("response.wav")
    response_audio.export("response.ogg", format="ogg")

    # Step 6: Send audio back
    await update.message.reply_voice(voice=open("response.ogg", "rb"))

# Bot setup
app = Application.builder().token("8103527229:AAG2JtczgdhblXSFMbrgBnanfJ2ysn2NtRA").build()
app.add_handler(MessageHandler(filters.VOICE, handle_voice))
app.run_polling()
