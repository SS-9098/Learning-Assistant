import speech_recognition as sr

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        # Adjust for ambient noise and set energy threshold
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 30  # Set the sensitivity manually
        recognizer.pause_threshold = 3  # Stop after 3 seconds of silence

        print("Listening...")
        try:
            # Capture the audio from the microphone
            audio = recognizer.listen(source, timeout=10)
            print("Processing...")

            # Use Google's speech recognition API
            speech_text = recognizer.recognize_google(audio)
            return speech_text

        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Couldn't connect to the API."
