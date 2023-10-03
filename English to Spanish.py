import speech_recognition as sr
from translate import Translator
import pyttsx3

# Initialize the recognizer
recognizer = sr.Recognizer()

# Capture audio from the microphone
with sr.Microphone() as source:
    print("Say something in English:")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)

    # Translate the text to Spanish
    translator = Translator(to_lang="es")
    translated_text = translator.translate(text)
    print("Translated to Spanish:", translated_text)

    # Convert the translated text to speech
    engine = pyttsx3.init()
    engine.say(translated_text)
    engine.runAndWait()
except sr.UnknownValueError:
    print("Google Web Speech API could not understand audio.")
except sr.RequestError as e:
    print(f"Could not request results from Google Web Speech API; {e}")
