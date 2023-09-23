from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from tkinter import *
import threading
from PIL import Image, ImageTk  # Import Pillow modules

# add dictionary of languages
dic = ('afrikaans', 'af', 'albanian', 'sq', 'amharic', 'am',
       'arabic', 'ar', 'armenian', 'hy', 'azerbaijani', 'az',
       'basque', 'eu', 'belarusian', 'be', 'bengali', 'bn', 'bosnian',
       'bs', 'bulgarian', 'bg', 'catalan', 'ca',
       'cebuano', 'ceb', 'chichewa', 'ny', 'chinese (simplified)',
       'zh-cn', 'chinese (traditional)', 'zh-tw',
       'corsican', 'co', 'croatian', 'hr', 'czech', 'cs', 'danish',
       'da', 'dutch', 'nl', 'english', 'en', 'esperanto',
       'eo', 'estonian', 'et', 'filipino', 'tl', 'finnish', 'fi',
       'french', 'fr', 'frisian', 'fy', 'galician', 'gl',
       'georgian', 'ka', 'german', 'de', 'greek', 'el', 'gujarati',
       'gu', 'haitian creole', 'ht', 'hausa', 'ha',
       'hawaiian', 'haw', 'hebrew', 'he', 'hindi', 'hi', 'hmong',
       'hmn', 'hungarian', 'hu', 'icelandic', 'is', 'igbo',
       'ig', 'indonesian', 'id', 'irish', 'ga', 'italian', 'it',
       'japanese', 'ja', 'javanese', 'jw', 'kannada', 'kn',
       'kazakh', 'kk', 'khmer', 'km', 'korean', 'ko', 'kurdish (kurmanji)',
       'ku', 'kyrgyz', 'ky', 'lao', 'lo',
       'latin', 'la', 'latvian', 'lv', 'lithuanian', 'lt', 'luxembourgish',
       'lb', 'macedonian', 'mk', 'malagasy',
       'mg', 'malay', 'ms', 'malayalam', 'ml', 'maltese', 'mt', 'maori',
       'mi', 'marathi', 'mr', 'mongolian', 'mn',
       'myanmar (burmese)', 'my', 'nepali', 'ne', 'norwegian', 'no',
       'odia', 'or', 'pashto', 'ps', 'persian',
       'fa', 'polish', 'pl', 'portuguese', 'pt', 'punjabi', 'pa',
       'romanian', 'ro', 'russian', 'ru', 'samoan',
       'sm', 'scots gaelic', 'gd', 'serbian', 'sr', 'sesotho',
       'st', 'shona', 'sn', 'sindhi', 'sd', 'sinhala',
       'si', 'slovak', 'sk', 'slovenian', 'sl', 'somali', 'so',
       'spanish', 'es', 'sundanese', 'su',
       'swahili', 'sw', 'swedish', 'sv', 'tajik', 'tg', 'tamil',
       'ta', 'telugu', 'te', 'thai', 'th', 'turkish', 'tr',
       'ukrainian', 'uk', 'urdu', 'ur', 'uyghur', 'ug', 'uzbek',
       'uz', 'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh',
       'yiddish', 'yi', 'yoruba', 'yo', 'zulu', 'zu')

# Voice command through mic
def vcCommand():
    speechRec = sr.Recognizer()
    with sr.Microphone() as source:
        update_status("Listening...")  # Update status label
        print("Listening...")
        speechRec.pause_threshold = 1
        audio = speechRec.listen(source)

    try:
        update_status("Recognizing...")  # Update status label
        print("Recognizing...")
        query = speechRec.recognize_google(audio, language="en-in")
        update_status(f"You said: {query}")  # Update status label with recognized text
        print(f"You said {query}\n")
    except Exception as e:
        update_status("I didn't understand that, can you please say that again?...")  # Update status label
        print("I didn't understand that, can you please say that again?...")
        return None
    return query

# Input language from user, Mapping user input with language code
def destination_language():
    print("Enter the language you want to convert: Ex. English, Spanish, etc.")
    print()

    # Input destination language user wants to translate
    to_lang = vcCommand()
    while to_lang is None:
        to_lang = vcCommand()
    to_lang = to_lang.lower()
    return to_lang

# Translate function
def translate_text():
    query = vcCommand()
    while query is None:
        query = vcCommand()

    to_lang = destination_language()
    while to_lang not in dic:
        print("Language not found, please put another language")
        to_lang = destination_language()
    to_lang = dic[dic.index(to_lang) + 1]

    # invoking Translator
    translator = Translator()

    # Translating from src to dest
    text_to_translate = translator.translate(query, dest=to_lang)
    text = text_to_translate.text

    # Update the label with the translated text
    label.config(text=text)

# Quit function to exit the program
def quit_program():
    if not translation_in_progress:
        root.quit()

# Create a Tkinter window
root = Tk()
root.title("Translation App")

# Set the icon for the window (replace 'icon.ico' with the path to your icon file)
# root.iconbitmap('off.png')

# Create a label to display the translated text
label = Label(root, text="", font=("Helvetica", 16))
label.pack(pady=20)

# Create a label to display the status and recognized text
status_label = Label(root, text="", font=("Helvetica", 14))
status_label.pack(pady=10)

# Function to update the status label with the provided text
def update_status(text):
    status_label.config(text=text)

# Variable to check if translation thread is running
translation_in_progress = False

# Function to perform translation in a separate thread
def translate_thread():
    global translation_in_progress
    translation_in_progress = True
    translate_text()
    translation_in_progress = False

# Create a button to trigger translation
def start_translation():
    if not translation_in_progress:
        threading.Thread(target=translate_thread).start()


translate_button = Button(root, text="Translate", command=start_translation)
translate_button.pack()

# Create a button to quit the program
quit_button = Button(root, text="Quit", command=quit_program)
quit_button.pack()

# Periodically check if the translation thread has finished and allow quitting
def check_translation_status():
    if not translation_in_progress:
        quit_button.config(state=NORMAL)
    else:
        root.after(100, check_translation_status)  # Check again after 100 milliseconds

# Start checking translation status
check_translation_status()

# Start the Tkinter main loop
root.mainloop()

