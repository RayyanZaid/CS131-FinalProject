import mido

# Open the MIDI file
mid = mido.MidiFile('EsAndGsWhole.mid')

# Print the file's metadata
print(f'Number of tracks: {len(mid.tracks)}')
print(f'Ticks per quarter note: {mid.ticks_per_beat}')

# Iterate over the tracks
for i, track in enumerate(mid.tracks):
    print(f'Track {i+1}:')
    # Iterate over the messages in the track
    for msg in track:
        # Print the message type and data
        print(f'  {msg.type}: {msg}')