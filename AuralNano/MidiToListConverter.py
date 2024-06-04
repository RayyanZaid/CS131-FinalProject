import mido
from mido import MidiFile

def midi_note_to_name(note_number):
    # Maps a MIDI note number to a note name
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return note_names[note_number % 12] + str(note_number // 12 - 1)

def note_frequency(note_number):
    # Converts MIDI note number to frequency
    return 440 * (2 ** ((note_number - 69) / 12))

def read_midi(file_path, user_bpm):
    mid = MidiFile(file_path)
    note_events = []
    ticks_per_beat = mid.ticks_per_beat
    tempo = 60000000 / user_bpm  # Converts BPM to microseconds per beat

    for track in mid.tracks:
        time = 0
        for msg in track:
            # Convert delta times in MIDI ticks to microseconds based on user-defined tempo
            time += mido.tick2second(msg.time, ticks_per_beat, tempo) * 1e6
            if msg.type == 'note_on':
                note = {
                    'note_name': midi_note_to_name(msg.note),
                    'frequency': note_frequency(msg.note),
                    'start': time,
                    'velocity': msg.velocity
                }
                note_events.append(note)
            elif msg.type == 'note_off':
                for note in note_events:
                    if note['note_name'] == midi_note_to_name(msg.note) and 'duration' not in note:
                        note['duration'] = time - note['start']
                        break

    # Converting durations from microseconds to beats and approximating to nearest note value
    output = []
    for note in note_events:
        if 'duration' in note:
            beats_duration = note['duration'] / tempo
            output.append([note['note_name'], note['frequency'], beats_duration])
    return output



if __name__ == '__main__':
    midi_path = r"C:\Users\rayya\Desktop\CS131-FinalProject-Music-Coach\AuralNano\EsAndGsWeb.mid"
    user_bpm = 100  # Define the BPM here
    notes = read_midi(midi_path, user_bpm)
    for note in notes:
        print(note)

