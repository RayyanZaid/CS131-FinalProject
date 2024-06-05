from gtts import gTTS
import pygame
import os


def playText(text):


    # Generate speech
    tts = gTTS(text, lang='en')
    # Save the speech to an MP3 file
    tts.save("speech.mp3")

    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the MP3 file
    pygame.mixer.music.load("speech.mp3")
    # Play the loaded file
    pygame.mixer.music.play()

    # Keep the script running until the audio has finished playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Optionally, remove the file after playing
    os.remove("speech.mp3")