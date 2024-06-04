import time
import simpleaudio as sa
import numpy as np

from MusicInputRecorder import record_music
from MidiToListConverter import read_midi

path = r'C:\Users\rayya\Desktop\CS131-FinalProject-Music-Coach\yes.txt'
bpm = 100
measures = 4
vol = 500

bps = bpm / 60  # beats per second
count = 4

# Generate a simple beep sound for the metronome
def play_metronome():
    frequency = 440  # Frequency in Hertz
    fs = 44100  # Sampling rate
    duration = 0.2  # Duration in seconds
    t = np.linspace(0, duration, int(fs * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    audio = np.hstack([wave, wave])
    audio = (audio * 32767).astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()

def testMusic():
    global count
    start = time.time()
    # 4 beat countdown with metronome sound
    while count > 0:
        if time.time() - start > 1 / bps:
            print(count)
            play_metronome()
            count -= 1
            start = time.time()

    # bpm of song, total number measures, path is absolute path of output file, volume is sound gate
    result = record_music(bpm, measures, path, vol)

    print(result)

    # Now grade the music by comparing it to a MIDI file

    # 1) Convert MIDI file to list format (like result on line 25)
    midiFileResult = read_midi("received_midi_file.mid", bpm)

    print(midiFileResult)

    print("Compare results for a grade")

    return 100


if __name__ == '__main__':
    testMusic()
