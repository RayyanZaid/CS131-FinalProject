import time
import simpleaudio as sa
from sys import platform
from MusicInputRecorder import record_music
from MidiToListConverter import read_midi

path = r'test.txt'
bpm = 100
vol = 500

bps = bpm / 60  # beats per second
count = 4

# Load the beep sound
beep_wave = sa.WaveObject.from_wave_file("beep.wav")

def play_metronome():
    play_obj = beep_wave.play()
    play_obj.wait_done()

def count_measures(sheet_music):
    measures = 0
    current_measure_time = 0
    
    # Iterate through each note in the sheet music
    for note in sheet_music:
        # Increment current measure time by the duration of the note
        current_measure_time += note[2]
        
        # Check if the current measure time exceeds the time signature
        if current_measure_time >= 4.0:  # Assuming 4/4 time signature
            measures += 1
            current_measure_time = current_measure_time % 4.0  # Reset current measure time
    
    # Check if there are any remaining notes that don't form a complete measure
    if current_measure_time > 0:
        measures += 1
        
    return measures

def grade_recording(sheet_music, recorded_audio):
    # Parse sheet music
    sheet_notes = [(note[0], note[2], note[1]) for note in sheet_music]
    

    recorded_audio = recorded_audio[1:]
    # Parse recorded audio
    recorded_notes = [(note[0], note[2], note[1]) for note in recorded_audio]
    
    # Initialize variables for grading
    total_notes = len(sheet_notes)
    correct_notes = 0
    timing_error = 0
    
    # Iterate through each note in sheet music
    for i, (sheet_note, sheet_duration, sheet_time) in enumerate(sheet_notes):
        if i < len(recorded_notes):
            recorded_note, recorded_duration, recorded_time = recorded_notes[i]
            
            # Check if note name and duration match
            if sheet_note == recorded_note and sheet_duration == recorded_duration:
                correct_notes += 1
                
                # Calculate timing error (absolute difference in time)
                timing_error += abs(sheet_time - recorded_time)
    
    # Calculate accuracy and timing grades
    accuracy_grade = (correct_notes / total_notes) * 100
    timing_grade = max(0, 100 - timing_error)  # Penalize timing errors
    
    # Final grade is a combination of accuracy and timing
    final_grade = (accuracy_grade + timing_grade) / 2
    
    return final_grade

def testMusic():

    # 1) Convert MIDI file to list format (like result on line 25)
    sheetmusicResult = read_midi("received_midi_file.mid", bpm)

    print(sheetmusicResult)

    measures = count_measures(sheetmusicResult)
    print(f"Measures: {measures}")

    global count
    start = time.time()
    # 4 beat countdown with metronome sound
    while count > 0:
        if time.time() - start > 1 / bps:
            print(count)

            if platform != "win32":
                play_metronome()
            count -= 1
            start = time.time()

    # bpm of song, total number measures, path is absolute path of output file, volume is sound gate
    audio_result = record_music(bpm, measures, path, vol)

    print(f"Sheet Music Array: {sheetmusicResult}")
    print(f"Audio Array: {audio_result}")

    # Now grade the music by comparing it to a MIDI file

    


    grade = grade_recording(sheetmusicResult, audio_result)
    print(grade)
    return grade
if __name__ == "__main__":
    testMusic()
