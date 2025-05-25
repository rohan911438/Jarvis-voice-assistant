# Jarvis Voice Assistant

![License](https://img.shields.io/badge/license-MIT-green) ![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

---

## Overview

**Jarvis Voice Assistant** is a Python-based voice-controlled AI assistant designed to execute commands, open websites, play music, and interact via AI-powered responses using OpenAI's GPT-3.5 Turbo model. It leverages speech recognition and text-to-speech to provide a natural conversational experience.

---

## Features

- **Voice Activation**: Wake Jarvis by saying its name.
- **Web Browsing Automation**: Open Google, Facebook, LinkedIn, YouTube, etc.
- **Music Playback**: Play predefined songs using links from a music library.
- **AI-powered Conversational Abilities**: Integrates OpenAI GPT-3.5 Turbo for answering general queries.
- **Noise Handling**: Dynamic energy threshold adjustment for better speech recognition in noisy environments.
- **Multithreading**: Processes commands asynchronously for smoother performance.

---

## Technologies & Libraries Used

- Python 3.8+
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://pypi.org/project/PyAudio/)
- [pyttsx3](https://pypi.org/project/pyttsx3/) (Text-to-Speech)
- [OpenAI API](https://openai.com/api/)
- Webbrowser (Python built-in module)
- Multithreading for asynchronous command execution

---

## Getting Started

### Prerequisites

- Python 3.8 or higher installed on your system.
- [Pip](https://pip.pypa.io/en/stable/) package manager.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/rohan911438/Jarvis-voice-assistant.git
   cd Jarvis-voice-assistant



2.Create and activate a virtual environment (optional but recommended):

python -m venv .venv
source .venv/bin/activate       # On Linux/macOS
.venv\Scripts\activate          # On Windows


3.Install dependencies:

pip install -r requirements.txt


4.Set your OpenAI API key:

export OPENAI_API_KEY="your_openai_api_key_here"     # Linux/macOS
setx OPENAI_API_KEY "your_openai_api_key_here"       # Windows (restart terminal after)


Usage
Run the main script to start Jarvis:
python main.py



Project Structure



├── main.py                # Main entry point, handles voice recognition and command processing
├── musiclibrary.py        # Contains music links and playback management
├── client.py              # Client-specific operations and integrations
├── requirements.txt       # Project dependencies
├── README.md              # This file
└── jarvis-voice-assistant/ # (Optional submodule or folder containing additional assets or scripts)
