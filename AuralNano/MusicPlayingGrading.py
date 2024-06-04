from MusicInputRecorder import record_music
from MidiToListConverter import read_midi
import time

path = r'C:\Users\rayya\Desktop\CS131-FinalProject-Music-Coach\yes.txt'
bpm = 100
measures = 4
vol = 500

start = time.time()
count = 4

bps = bpm / 60

#4 beat countdown
while True:
    if time.time() - start > 1/bps:
        if count > 0:
            print(count)
            count -= 1
            start = time.time()
        else:
            break

#bpm of song, total number measures, path is absolute path of output file, volume is sound gate
result = record_music(bpm, measures, path, vol)

print(result)



# Now grade the music by comparing it to a MIDI file


# 1) Convert MIDI file to list format (like result on line 25)

midiFileResult = read_midi("received_midi_file.mid", bpm)

print(midiFileResult)