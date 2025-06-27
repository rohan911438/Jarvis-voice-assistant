import speech_recognition as sr
import threading
from datetime import datetime

class VoiceListener:
    def __init__(self, on_command_callback, recognizer=None, wake_word="jarvis"):
        self.recognizer = recognizer or sr.Recognizer()
        self.on_command_callback = on_command_callback
        self.listening = False
        self.thread = None
        self.wake_word = wake_word.lower()

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()

    def stop_listening(self):
        self.listening = False
        if self.thread:
            self.thread.join()

    def _log_command(self, command):
        with open("jarvis.log", "a", encoding="utf-8") as log_file:
            log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {command}\n")

    def _listen_loop(self):
        while self.listening:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.15)
                    print("Listening for command...")
                    audio = self.recognizer.listen(source, timeout=3.0, phrase_time_limit=2.0)
                try:
                    command = self.recognizer.recognize_google(audio).lower()
                    print("Recognized:", command)
                    self._log_command(command)
                    if self.wake_word in command:
                        # Remove wake word and extra spaces
                        actual_command = command.replace(self.wake_word, "").strip()
                        if actual_command:
                            self.on_command_callback(actual_command)
                except sr.UnknownValueError:
                    print("Could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")
            except Exception as e:
                print(f"Error: {e}")
