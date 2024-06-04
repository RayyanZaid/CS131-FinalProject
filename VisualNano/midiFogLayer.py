import mido
from mido import MidiFile, MidiTrack, Message


def transposeToBFlat(input_midi_file):
# Load the MIDI file

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

    output_midi_file = f"{input_midi_file}"
    transposed_midi.save(output_midi_file)

    return output_midi_file

def remove_last_note_events(midi_file_path):
    """
    Removes the last note_on and note_off events from the given MIDI file.
    
    Parameters:
    midi_file_path (str): Path to the input MIDI file.
    
    Returns:
    str: Path to the modified MIDI file.
    """
    mid = MidiFile(midi_file_path)
    for i, track in enumerate(mid.tracks):
        new_track = MidiTrack()
        note_on_found = False
        note_off_found = False

        for msg in reversed(track):
            if not note_off_found and msg.type == 'note_off':
                note_off_found = True
                continue
            if note_off_found and not note_on_found and msg.type == 'note_on':
                note_on_found = True
                continue
            new_track.insert(0, msg)

        mid.tracks[i] = new_track

    new_file_path = midi_file_path
    mid.save(new_file_path)
    return new_file_path


if __name__ == '__main__':
    transposeToBFlat("EsAndGs.mid")
