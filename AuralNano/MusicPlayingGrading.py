import time
from sys import platform
from MusicInputRecorder import record_music
from MidiToListConverter import read_midi

path = r'test.txt'
bpm = 100
vol = 500

bps = bpm / 60  # beats per second
count = 4


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
    feedback = []  # Initialize feedback list
    sheet_index = 0
    audio_index = 0
    tone_grade = 0
    rhythm_grade = 0
    mismatches = 0  # Track mismatches

    # Define acceptable tolerance for frequency match in Hz and rhythm match in time units
    frequency_tolerance = 15  # +/- 15 Hz is considered as an acceptable pitch difference
    rhythm_tolerance = 0.1   # 10% of note duration deviation is acceptable

    while sheet_index < len(sheet_music) and audio_index < len(recorded_audio):
        sheet_note, sheet_freq, sheet_duration = sheet_music[sheet_index]
        audio_note, audio_freq, audio_duration = recorded_audio[audio_index]

        # Initialize note feedback
        note_feedback = {
            'note': sheet_note,
            'rhythm_correctness': False,
            'tone': 'In tune'
        }

        # Check for rhythm match
        rhythm_error = abs(sheet_duration - audio_duration) / sheet_duration
        if rhythm_error <= rhythm_tolerance:
            note_feedback['rhythm_correctness'] = True
            rhythm_grade += 1

        # Check for tone match and categorize sharpness or flatness
        freq_diff = sheet_freq - audio_freq
        if abs(freq_diff) <= frequency_tolerance:
            note_feedback['tone'] = 'In tune'
            tone_grade += 1
        elif freq_diff > 0:
            note_feedback['tone'] = 'Flat'
        else:
            note_feedback['tone'] = 'Sharp'

        # Decide which index to increment based on note matches
        if sheet_note == audio_note:
            sheet_index += 1
            audio_index += 1
        elif sheet_index + 1 < len(sheet_music) and sheet_music[sheet_index + 1][0] == audio_note:
            sheet_index += 1  # Audio is behind, skip a sheet note
        elif audio_index + 1 < len(recorded_audio) and recorded_audio[audio_index + 1][0] == sheet_note:
            audio_index += 1  # Audio is ahead, skip an audio note
        else:
            # No clear way to match, increment both and mark feedback as unmatched
            note_feedback['note'] = f"Unmatched Sheet: {sheet_note}, Audio: {audio_note}"
            note_feedback['tone'] = 'Mismatch'
            sheet_index += 1
            audio_index += 1
            mismatches += 1

        # Append current note's feedback to the list
        feedback.append(note_feedback)

    # Calculate final grades considering the length of the music and the number of mismatches
    final_grade = ((tone_grade + rhythm_grade) / (len(sheet_music) + len(recorded_audio))) * 100 - (mismatches * 5)  # Penalize for mismatches

    return final_grade, feedback

# The rest of your testMusic function would follow here



def transpose_by_tone(sheet_music):
    # Create a dictionary to map notes to their next whole tone equivalents
    note_mapping = {
        'C': 'D', 'C#': 'D#', 'D': 'E', 'D#': 'F', 'E': 'F#',
        'F': 'G', 'F#': 'G#', 'G': 'A', 'G#': 'A#', 'A': 'B', 'A#': 'C', 'B': 'C#',
        'C3': 'D3', 'C#3': 'D#3', 'D3': 'E3', 'D#3': 'F3', 'E3': 'F#3',
        'F3': 'G3', 'F#3': 'G#3', 'G3': 'A3', 'G#3': 'A#3', 'A3': 'B3', 'A#3': 'C4', 'B3': 'C#4',
        'C4': 'D4', 'C#4': 'D#4', 'D4': 'E4', 'D#4': 'F4', 'E4': 'F#4',
        'F4': 'G4', 'F#4': 'G#4', 'G4': 'A4', 'G#4': 'A#4', 'A4': 'B4', 'A#4': 'C5', 'B4': 'C#5',
        # You can continue for other octaves as necessary
    }
    
    # Update each note in the sheet music array to its whole tone higher equivalent
    transposed_sheet_music = [[note_mapping.get(note[0], note[0]), note[1], note[2]] for note in sheet_music]
    return transposed_sheet_music


def raise_octave(sheet_music):
    # Create a dictionary to map notes to their higher octave equivalents
    note_mapping = {
        'C3': 'C4', 'D3': 'D4', 'E3': 'E4', 'F3': 'F4', 'G3': 'G4', 'A3': 'A5', 'B3': 'B4',
        # Add more mappings if other notes are used
    }
    
    # Update each note in the sheet music array to its higher octave equivalent
    raised_sheet_music = [[note_mapping.get(note[0], note[0]), note[1], note[2]] for note in sheet_music]
    return raised_sheet_music

# # Example usage
# sheet_music_array = [['C3', 130.8127826502993, 1.0], ['C3', 130.8127826502993, 1.0], ['C3', 130.8127826502993, 1.0], ...]
# raised_sheet_music_array = raise_octave(sheet_music_array)
# print(raised_sheet_music_array)


def testMusic():

    # 1) Convert MIDI file to list format (like result on line 25)
    sheetmusicResult = read_midi("received_midi_file.mid", bpm)

    sheetmusicResult = raise_octave(sheetmusicResult)

    sheetmusicResult = transpose_by_tone(sheetmusicResult)
    print(sheetmusicResult)

    measures = count_measures(sheetmusicResult)
    print(f"Measures: {measures}")

    # bpm of song, total number measures, path is absolute path of output file, volume is sound gate

    measures += 1
    audio_result = record_music(bpm, measures, path, vol)
    audio_result = transpose_by_tone(audio_result)
    print(f"Sheet Music Array: {sheetmusicResult}")
    print(f"Audio Array: {audio_result}")

    # Now grade the music by comparing it to a MIDI file

    


    grade, feedback = grade_recording(sheetmusicResult, audio_result)

    grade = round(grade,0)
    print(grade)
    
    return grade, feedback


if __name__ == "__main__":
    testMusic()
