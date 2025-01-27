import pyttsx3
import sys
import tkinter as tk
from tkinter import ttk

# Global engine variable
engine = None


def text_to_speech(text, language):
    global engine
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set the language
    voices = engine.getProperty('voices')
    language_map = {
        'tr': ['turkish', 'türkçe', 'türk', 'microsoft zira', 'zira'],
        'en': ['english', 'eng', 'microsoft david', 'david'],
        'de': ['german', 'deutsch', 'ger', 'microsoft hedda', 'hedda'],
        'es': ['spanish', 'español', 'spa', 'microsoft helena', 'helena'],
        'fr': ['french', 'français', 'fra', 'microsoft julie', 'julie']
    }

    target_langs = language_map.get(language, [])
    voice_found = False

    # Print available voices for debugging
    print("Available voices:")
    for voice in voices:
        print(f"ID: {voice.id}, Name: {voice.name}, Languages: {voice.languages}")

    # Try to find an exact match first
    for voice in voices:
        voice_id_lower = voice.id.lower()
        voice_name_lower = voice.name.lower()

        for lang_term in target_langs:
            if (lang_term in voice_id_lower or
                    lang_term in voice_name_lower or
                    (hasattr(voice, 'languages') and any(lang_term in lang.lower() for lang in voice.languages))):
                engine.setProperty('voice', voice.id)
                voice_found = True
                print(f"Selected voice: {voice.id}")
                break
        if voice_found:
            break

    # If no voice found, try to find any voice that contains the language code
    if not voice_found:
        for voice in voices:
            if language.lower() in voice.id.lower() or language.lower() in voice.name.lower():
                engine.setProperty('voice', voice.id)
                voice_found = True
                print(f"Selected fallback voice: {voice.id}")
                break

    if not voice_found:
        print(f"Warning: Voice for {language} not found. Using default voice.")
        # Try to set English as fallback if available
        for voice in voices:
            if 'en' in voice.id.lower() or 'english' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                print(f"Using English fallback voice: {voice.id}")
                break

    try:
        # Set rate and volume properties
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1.0)  # Volume level

        # Convert text to speech
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)
    finally:
        if engine:
            engine.stop()


def convert_text():
    text = text_input.get("1.0", "end-1c")
    language = language_var.get()
    text_to_speech(text, language)


def stop_speech():
    global engine
    if engine:
        engine.stop()


def change_volume(value):
    global engine
    if engine:
        engine.setProperty('volume', float(value) / 100)


if __name__ == "__main__":
    # Create main window
    window = tk.Tk()
    window.title("Metin Okuyucu")
    window.geometry("400x400")  # Increased height for volume control

    # Create text input area
    text_input = tk.Text(window, height=10, width=40)
    text_input.pack(pady=20)

    # Create language selection
    language_frame = ttk.Frame(window)
    language_frame.pack(pady=5)

    ttk.Label(language_frame, text="Dil Seçin:").pack(side=tk.LEFT, padx=5)
    language_var = tk.StringVar(value="tr")  # Default to Turkish
    languages = [
        ("Türkçe", "tr"),
        ("English", "en"),
        ("Deutsch", "de"),
        ("Español", "es"),
        ("Français", "fr")
    ]

    for lang_name, lang_code in languages:
        ttk.Radiobutton(language_frame, text=lang_name, value=lang_code,
                        variable=language_var).pack(side=tk.LEFT, padx=5)

    # Create volume control
    volume_frame = ttk.Frame(window)
    volume_frame.pack(pady=10)
    ttk.Label(volume_frame, text="Ses Seviyesi:").pack(side=tk.LEFT, padx=5)
    volume_scale = ttk.Scale(volume_frame, from_=0, to=100, orient='horizontal',
                             command=change_volume)
    volume_scale.set(100)  # Default volume
    volume_scale.pack(side=tk.LEFT, padx=5)

    # Create button frame
    button_frame = ttk.Frame(window)
    button_frame.pack(pady=10)

    # Create convert button
    convert_button = ttk.Button(button_frame, text="Metni Oku", command=convert_text)
    convert_button.pack(side=tk.LEFT, padx=5)

    # Create stop button
    stop_button = ttk.Button(button_frame, text="Durdur", command=stop_speech)
    stop_button.pack(side=tk.LEFT, padx=5)

    # Start the application
    window.mainloop()
