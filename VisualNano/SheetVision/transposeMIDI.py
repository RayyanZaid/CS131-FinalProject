import mido
from mido import MidiFile, MidiTrack, Message

# Load the MIDI file
input_midi_file = 'output.mid'
output_midi_file = 'transposed_to_Bb.mid'
midi = MidiFile(input_midi_file)

# Calculate transposition interval (example: to transpose to Bb, -2 semitones from C)
transposition_interval = -2

# Create a new MIDI file to store the transposed notes
transposed_midi = MidiFile()

for track in midi.tracks:
    transposed_track = MidiTrack()
    transposed_midi.tracks.append(transposed_track)
    for msg in track:
        if msg.type in ['note_on', 'note_off']:
            # Transpose the note
            msg.note += transposition_interval
        transposed_track.append(msg)

# Save the transposed MIDI file
transposed_midi.save(output_midi_file)
