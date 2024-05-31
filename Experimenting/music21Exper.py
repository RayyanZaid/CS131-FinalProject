from music21 import *


s = stream.Stream()

s.append(meter.TimeSignature('3/4'))
s.append(note.Note('C4'))

s.append(note.Note('D4'))

s.append(note.Note('E4'))

configure.run()