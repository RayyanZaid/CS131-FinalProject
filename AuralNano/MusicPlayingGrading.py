from MusicInputRecorder import record_music
import time

path = r'C:\Users\Work\Desktop\131\Project\CS131-FinalProject-Music-Coach\AuralNano\mic_music.txt'
bpm = 120
measures = 1
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