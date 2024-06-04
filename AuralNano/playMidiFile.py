import pygame

def play_midi(file_path):
    """
    Plays a MIDI file.

    Args:
        file_path (str): Path to the MIDI file.
    """
    # Initialize pygame
    pygame.mixer.init()
    
    # Load the MIDI file
    pygame.mixer.music.load(file_path)
    
    # Play the MIDI file
    pygame.mixer.music.play()
    
    # Keep the script running while the music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)



if __name__ == '__main__':
    play_midi('received_midi_file.mid')
