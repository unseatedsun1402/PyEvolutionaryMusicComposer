import pyaudio
from synthesizer import Player,Synthesizer,Waveform
import mido
from mido import *
import time
import random
import math

noteDict = {9:"A",
            10:"Bb",
            11:"B",
            0:"C",
            1:"Db",
            2:"D",
            3:"Eb",
            4:"E",
            5:"F",
            6:"Gb",
            7:"A",
            8:"Ab"}

def midi2note(msg):
    val = msg.note
    note = noteDict[val%12]+str(val//12)
    return note

def msg2dict(msg):
    result = dict()
    if 'note_on' in msg:
        on_ = True
    elif 'note_off' in msg:
        on_ = False
    else:
        on_ = None
    result['time'] = int(msg[msg.rfind('time'):].split(' ')[0].split('=')[1].translate(
        str.maketrans({a: None for a in string.punctuation})))

    if on_ is not None:
        for k in ['note', 'velocity']:
            result[k] = int(msg[msg.rfind(k):].split(' ')[0].split('=')[1].translate(
                str.maketrans({a: None for a in string.punctuation})))
    return [result, on_]

def __generate_random_notes():
    sequence = []
    msg = mido.Message
    rNoteOn = bool
    rVelocity = int
    rNote = int
    for i in range(32):
        if random.random() > 0.3:
            rVelocity = int(random.uniform(30.0,100.0))
            rNote = int(random.uniform(12.0,64.0) // 1)
        else:
            rVelocity = (0)
            rNote = (0)
        msg = mido.Message('note_on',note = rNote,velocity = rVelocity, time = 50)
        sequence.append(msg)
    return sequence



def main():
    player = Player()
    player.open_stream()
    synth  = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=True, osc2_waveform=Waveform.sine, osc2_volume=0.8, osc2_freq_transpose=2)
    
    #player.play_wave(synth.generate_constant_wave(440.0, 1.0))
    chord = ["C3", "E3", "G3"]
    #output = mido.open_output('Nord Stage 3 MIDI Input')
    player.play_wave(synth.generate_chord(chord,1))
    sequence = __generate_random_notes()
    for msg in sequence:
        #output.send(msg)
        if msg.velocity == 0:
            time.sleep(msg.time/100)
        else:
            player.play_wave(synth.generate_constant_wave((midi2note(msg)),(msg.time/100)))
        time.sleep(msg.time/1000)

def test():
    print(mido.get_output_names())
    output = mido.open_output('Nord Stage 3 MIDI Input')
    testMidi = mido.MidiFile('/Users/ethanblood/Downloads/test.mid',clip=True)
    midiArray = list
    for i, track in enumerate(testMidi.tracks):
        print('Track {}: {}'.format(i, track.name))
        tempo = 100
        for msg in track:
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo/1000
                continue
            else:
                time.sleep(msg.time/tempo)
                output.send(msg)
                #print(msg)
    print(midiArray)

if __name__ == '__main__':
    main()
    #test()