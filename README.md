# Virtual Voice Assistant 🎙️🤖

A Python-based virtual voice assistant with a modern web interface, built with Flask and speech recognition technologies.

## Features ✨

- **Voice Commands**: Interact naturally using your voice
- **Web Integration**: Open websites with voice commands
- **Music Playback**: Play songs from your music library
- **News Updates**: Get the latest headlines
- **AI-Powered**: ChatGPT integration for general queries
- **Modern Web Interface**: Responsive design that works on all devices
- **Command History**: Keeps track of your interactions

## Technologies Used 🛠️

- **Backend**: Python, Flask
- **Speech Recognition**: `speech_recognition`, `pyttsx3`, `gTTS`
- **AI Integration**: OpenAI API
- **Frontend**: HTML5, CSS3, JavaScript
- **Audio Processing**: `pygame`

### Prerequisites

- Python 3.7+
- Microphone
- Internet connection

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/virtual-voice-assistant.git
   cd virtual-voice-assistant

### Setup Keys
- OPENAI_API_KEY=your-api-key-here
- NEWS_API_KEY=your-newsapi-key-here

### Usage
- Run the Flask application:
  bash
  python app.py
  
- Open your web browser to:
  text
  http://localhost:5001

### Available Commands
  "Open Google/Facebook/YouTube/LinkedIn"
  "Play [song name]"
  "What's the news?"
  Any general question or command
  
### Project Structure 
   virtual-voice-assistant/
      ├── app.py                # Main Flask application
      ├── musicLibrary.py       # Music library configuration
      ├── .env.example          # Environment variables template
      ├── Interface/            # HTML templates, CSS, JS
      │   └── index.html        # Main interface
          └── style.css         # css file
      └── README.md             # This file<img width="1883" height="891" alt="VVA" src="https://github.com/user-attachments/assets/60d9f9f8-c1de-45db-b4f1-2bd207252d90" />
