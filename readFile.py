import mido

testMidi = mido.MidiFile("/Users/ethanblood/Documents/newfile.mid",clip=True)
for i, track in enumerate(testMidi.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            if message.is_meta:
                print(message)