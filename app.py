import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import wikipedia

# Inicializar pygame para la reproducción de audio
pygame.mixer.init()

def speak(text):
    """Convert text to speech and play it."""
    try:
        tts = gTTS(text=text, lang='es')
        filename = "voice.mp3"
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # Esperar hasta que la música termine usando pygame.mixer.music.get_busy()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Esperar un poco antes de verificar de nuevo
    finally:
        # Eliminar el archivo de audio si existe
        if os.path.exists(filename):
            os.remove(filename)

def listen():
    """Listen for a command from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language='es-ES')
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Lo siento, no entendí lo que dijiste.")
    except sr.RequestError:
        speak("Lo siento, no puedo conectar al servicio de reconocimiento de voz.")
    return None

def search_wikipedia(query):
    """Search Wikipedia for a given query and return a summary."""
    wikipedia.set_lang('es')
    wikipedia.set_user_agent('MyAssistantBot/1.0 (your.email@example.com)')
    try:
        summary = wikipedia.summary(query, sentences=5)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Tu consulta es ambigua. Podría referirse a: {', '.join(e.options)}"
    except wikipedia.exceptions.PageError:
        return "No encontré información sobre eso en Wikipedia."

def main():
    speak("Hola, soy tu asistente. ¿En qué puedo ayudarte hoy?")
    while True:
        command = listen()
        if command:
            if any(keyword in command for keyword in ["wikipedia", "busca", "dame información de"]):
                if "wikipedia" in command:
                    query = command.replace("wikipedia", "").strip()
                elif "busca" in command:
                    query = command.replace("busca", "").strip()
                elif "dame información de" in command:
                    query = command.replace("dame información de", "").strip()
                
                if query:
                    # Solo di que estás buscando información antes de realizar la búsqueda
                    speak(f"Buscando información sobre {query}.")
                    result = search_wikipedia(query)
                    # Luego habla el resultado de la búsqueda
                    speak(result)
            elif "salir" in command:
                speak("Hasta luego.")
                break
            else:
                speak("Lo siento, no sé cómo ayudarte con eso.")

if __name__ == "__main__":
    main()
