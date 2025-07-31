from flask import Flask, render_template, jsonify, request
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import threading
import time

app = Flask(__name__)

# Initialize recognizer and other components
recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "YOUR API"

# Shared state for communication between threads
assistant_state = {
    'is_listening': False,
    'status': 'Ready',
    'response': '',
    'command': ''
}

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key="Your Key")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        return "Opening Google"
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        return "Opening Facebook"
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        return "Opening LinkedIn"
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, "")
        if link:
            webbrowser.open(link)
            return f"Playing {song}"
        else:
            return f"Sorry, I couldn't find {song} in the library"
    elif "news" in c.lower():
        r = requests.get(f"YOUR API")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            headlines = [article['title'] for article in articles[:3]]  # Get first 3 headlines
            return "Here are the latest headlines: " + ". ".join(headlines)
        else:
            return "Sorry, I couldn't fetch the news right now"
    else:
        return aiProcess(c)

def listen_thread():
    while True:
        if assistant_state['is_listening']:
            try:
                assistant_state['status'] = "Listening..."
                
                with sr.Microphone() as source:
                    print("Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    
                assistant_state['status'] = "Processing..."
                command = recognizer.recognize_google(audio)
                assistant_state['command'] = command
                
                response = processCommand(command)
                assistant_state['response'] = response
                speak(response)
                
            except sr.WaitTimeoutError:
                assistant_state['status'] = "Timeout: No speech detected"
                assistant_state['response'] = "I didn't hear anything. Please try again."
            except sr.UnknownValueError:
                assistant_state['status'] = "Could not understand audio"
                assistant_state['response'] = "Sorry, I didn't understand that."
            except Exception as e:
                assistant_state['status'] = f"Error: {str(e)}"
                assistant_state['response'] = "Something went wrong. Please try again."
            
            assistant_state['is_listening'] = False
            assistant_state['status'] = "Ready"
        
        time.sleep(0.1)

# Start the listening thread
listener_thread = threading.Thread(target=listen_thread, daemon=True)
listener_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'is_listening': assistant_state['is_listening'],
        'status': assistant_state['status'],
        'response': assistant_state['response'],
        'command': assistant_state['command']
    })

@app.route('/api/control', methods=['POST'])
def control_assistant():
    data = request.json
    action = data.get('action')
    
    if action == 'start':
        assistant_state['is_listening'] = True
        assistant_state['response'] = ''
        assistant_state['command'] = ''
        return jsonify({'success': True})
    elif action == 'stop':
        assistant_state['is_listening'] = False
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid action'})

if __name__ == '__main__':
    app.run(debug=True, threaded=True)