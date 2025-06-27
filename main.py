import speech_recognition as sr
import webbrowser
import pyttsx3
import threading
import musiclibrary
import requests
import sys
import queue
import datetime
from listener import VoiceListener
from chat_gui import ChatPanel
from jarvis_ui import JarvisUI
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Initialize speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Improve noise handling
recognizer.energy_threshold = 300  # Lower value makes it more sensitive
recognizer.dynamic_energy_threshold = True  # Adjusts to changing noise levels

# Gemini API Key
GEMINI_API_KEY = "AIzaSyC3Z-jXjIWcH9tSPRHNnD8mSEYC3ZiN0NE"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY

# Global chat panel reference
chat_panel = None

def speak(text):
    engine.say(text)
    engine.runAndWait()

def safe_display(display_callback, sender, message):
    if display_callback:
        QTimer.singleShot(0, lambda: display_callback(sender, message))

def gemini_process(command, display_callback=None):
    # Prepend current date to the command for up-to-date context
    today = datetime.datetime.now().strftime('%B %d, %Y')
    prompt = f"Today is {today}. {command}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
        print(f"Gemini Response: {reply}")
        safe_display(display_callback, "Jarvis", reply)
        speak(reply)
    except Exception as e:
        print(f"Gemini API error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                print(f"Gemini API error response: {e.response.text}")
            except Exception:
                pass
        safe_display(display_callback, "Jarvis", "Sorry, I couldn't get a response from Gemini.")
        speak("Sorry, I couldn't get a response from Gemini.")

# Command queue and worker thread
command_queue = queue.Queue()
worker_thread = None
worker_running = threading.Event()


def command_worker():
    worker_running.set()
    while worker_running.is_set():
        try:
            item = command_queue.get(timeout=0.5)
        except queue.Empty:
            continue
        command, display_callback = item
        safe_display(display_callback, "You", command)
        speak(f"Executing command: {command}")
        print(f"Executing command: {command}")
        if "open google" in command:
            webbrowser.open("https://google.com")
        elif "open facebook" in command:
            webbrowser.open("https://facebook.com")
        elif "open linkedin" in command:
            webbrowser.open("https://linkedin.com")
        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
        elif "play" in command:
            song = command.lower().replace("play", "").strip()
            print(f"Looking for song: '{song}'")
            if song in musiclibrary.music:
                link = musiclibrary.music[song]
                print(f"Playing song: {song} - {link}")
                webbrowser.open(link)
                speak(f"Playing {song}")
                safe_display(display_callback, "Jarvis", f"Playing {song}")
            else:
                speak(f"Sorry, I couldn't find the song '{song}'.")
                safe_display(display_callback, "Jarvis", f"Sorry, I couldn't find the song '{song}'.")
        else:
            gemini_process(command, display_callback)
        command_queue.task_done()


def process_command(command, display_callback=None):
    if display_callback:
        safe_display(display_callback, "Jarvis", "I'm thinking...")
    command_queue.put((command, display_callback))

def on_command(command):
    # Called by voice listener
    if chat_panel:
        chat_panel.display_message("You", command)
    process_command(command, display_callback=chat_panel.display_message if chat_panel else None)

def on_chat_send(user_message):
    process_command(user_message, display_callback=chat_panel.display_message)

def list_gemini_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        models = response.json().get("models", [])
        print("Available Gemini models for your API key:")
        for model in models:
            print(f"- {model.get('name')}")
    except Exception as e:
        print(f"Error listing Gemini models: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                print(f"Gemini ListModels error response: {e.response.text}")
            except Exception:
                pass

if __name__ == "__main__":
    # list_gemini_models()  # Uncomment only if you want to debug available models
    speak("Initializing myself, Jarvis. I'm ready for your command.")
    app = QApplication(sys.argv)
    chat_panel = JarvisUI()
    chat_panel.send_message.connect(on_chat_send)
    # Start command worker thread
    worker_thread = threading.Thread(target=command_worker, daemon=True)
    worker_thread.start()
    # Start voice listener in a background thread
    listener = VoiceListener(on_command_callback=on_command, recognizer=recognizer)
    listener_thread = threading.Thread(target=listener.start_listening, daemon=True)
    listener_thread.start()
    try:
        chat_panel.run()  # This shows the PyQt5 UI
        sys.exit(app.exec_())
    finally:
        listener.stop_listening()
        listener_thread.join(timeout=2)
        worker_running.clear()
        if worker_thread.is_alive():
            worker_thread.join(timeout=2)
        speak("Goodbye!")
