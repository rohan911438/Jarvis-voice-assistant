import speech_recognition as sr
import webbrowser
import pyttsx3
import threading
import musiclibrary
import openai

# Initialize speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Improve noise handling
recognizer.energy_threshold = 300  # Lower value makes it more sensitive
recognizer.dynamic_energy_threshold = True  # Adjusts to changing noise levels

# OpenAI API Key
openai.api_key = "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"

# Function to make Jarvis speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process AI commands
def aiprocess(command):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": command},
    ]
    
    # Make the request to the API for a chat completion using the gpt-3.5-turbo model
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the newer model
        messages=messages,       # Include the conversation history
        max_tokens=150,          # Limit the length of the response
        temperature=0.7          # Control creativity of the response
    )

    # Extract and print the assistant's response from the completion
    assistant_response = completion['choices'][0]['message']['content']
    print(f"AI Response: {assistant_response}")
    speak(assistant_response)

# Function to process voice commands
def process_command(command):
    speak(f"Executing command: {command}")
    print(f"Executing command: {command}")  # Debugging line

    def execute():
        if "open google" in command:
            webbrowser.open("https://google.com")
        elif "open facebook" in command:
            webbrowser.open("https://facebook.com")
        elif "open linkedin" in command:
            webbrowser.open("https://linkedin.com")
        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
        elif "play" in command:  # Check if 'play' is in the command
            song = command.lower().replace("play", "").strip()  # Remove 'play' and trim extra spaces
            print(f"Looking for song: '{song}'")  # Debugging: Check what song name was detected
            if song in musiclibrary.music:
                link = musiclibrary.music[song]
                print(f"Playing song: {song} - {link}")  # Debugging: Check if the song is found
                webbrowser.open(link)
                speak(f"Playing {song}")
            else:
                speak(f"Sorry, I couldn't find the song '{song}'.")
        else:
            # Process command with AI
            aiprocess(command)
            

    # Run in a separate thread to prevent lag
    threading.Thread(target=execute).start()

# Main loop
if __name__ == "__main__":
    speak("Initializing myself, Jarvis...")

    while True:
        try:
            # Listening for the wake word "Jarvis"
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)  # Quick noise adaptation
                print("Listening for 'Jarvis'...\n")
                audio = recognizer.listen(source, timeout=1.5, phrase_time_limit=1.5)  # Short response time

            command = recognizer.recognize_google(audio).lower()
            print("Recognized:", command)

            # Check if 'Jarvis' is mentioned
            if "jarvis" in command:
                speak("Yes?")
                
                # Listen for the actual command
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening for command...\n")
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)  # Faster response
                    command = recognizer.recognize_google(audio).lower()

                    print(f"Command to process: '{command}'")  # Debugging: Check what command was received
                    process_command(command)

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        except Exception as e:
            print(f"Error: {e}")
