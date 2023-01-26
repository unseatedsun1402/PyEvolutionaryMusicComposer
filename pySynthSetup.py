import pyaudio
from synthesizer import Player,Synthesizer,Waveform
import mido
from mido import *
import time
import random
import math
from tkinter import *

"""Definitions
###
# 
# Defines the globally accessed varibles/constants
# 
###
"""
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

major = [0,2,4,5,7,9,11]
minor = [0,2,3,5,7,8,10]
dorian   = [0,2,3,5,7,9,10]
phrygian = [0,1,3,5,7,8,10]
lydian   = [0,2,4,6,7,9,11]
mix      = [0,2,4,5,7,9,11]
aeolian  = [0,2,3,5,7,8,10]
locrian  = [0,1,3,5,6,8,10]

scaleDict = {0:major,
            1:dorian,
            2:phrygian,
            3:lydian,
            4:mix,
            5:aeolian,
            6:locrian,
            7:minor}
            
intervalDict = {0:'perfect',1:'minor',2:'major',3:'minor',
    4:'major',5:'perfect',6:'augmented',7:'perfect',8:'minor',
    9:'major',10:'minor',11:'major'}

intervalCost = {0:2,1:1,2:3,3:1,4:3,5:2,6:4,7:2,8:1,9:3,10:1,11:3}

TEMPO = 120


def midi2note(msg):
    val = msg.note
    note = noteDict[val%12]+str(val//12)
    return note

def quantize2key_(sequence,scale):
    quantized = False
    key_center_found = False
    key_center = 0
    while not key_center_found:
        if not sequence[key_center].velocity == 0:
            key_center = sequence[key_center].note%12
            key_center_found = True
        else:
            key_center += 1
    print("Key Centre is",noteDict[key_center])
    for each in sequence:
        if each.velocity == 0:
            continue
        quantized = False
        while not quantized:
            print(midi2note(each))
            if not (key_center + (each.note%12)) in scale:
                each.note += 1
                #print('Quantized ' + str(each.note-1) + 'to' + str(each.note))
                print(midi2note(each))
            else:
                quantized = True

def quantize2key(sequence,scale,key_center):
    quantized = False
    print("Key Centre is",noteDict[key_center])
    for each in sequence:
        if each.velocity == 0:
            continue
        quantized = False
        while not quantized:
            print(midi2note(each))
            if not (key_center + (each.note%12)) in scale:
                each.note += 1
                #print('Quantized ' + str(each.note-1) + 'to' + str(each.note))
                print(midi2note(each))
            else:
                quantized = True


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

def sequence2midi(sequence):
    midiSequence = mido.MidiFile()
    track = mido.MidiTrack()
    meta = mido.MetaMessage('set_tempo',tempo = TEMPO)
    track.append(meta)
    for note in sequence:
        track.append(note)
        noteOff = mido.Message('note_off',note=note.velocity, velocity = note.velocity,time = note.time)
        track.append(noteOff.copy())
    midiSequence.tracks.append(track)
    return (midiSequence)



def __generate_random_notes():
    sequence = []
    msg = mido.Message
    rNoteOn = bool
    rVelocity = int
    rNote = int
    for i in range(8):
        if random.random() > 0.1:
            rVelocity = int(random.uniform(50.0,100.0))
            rNote = int(random.uniform(33.0,71.0) // 1)
        else:
            rVelocity = (0)
            rNote = (0)
        msg = mido.Message('note_on',note = rNote,velocity = rVelocity, time = int(mido.second2tick(second = 0.5,ticks_per_beat = 96, tempo = mido.bpm2tempo(TEMPO))))
        sequence.append(msg)
    return sequence

def harmonize(sequence,key,scale):
    stepsCount = 0
    step = 0
    for msg in sequence:
        if step == 0 and msg.velocity == 0:
            chord = [str(noteDict[key]+3),str(noteDict[(key+5)%12]+3)]
            step += 1
            stepsCount += 1
            continue
        if step == 0:
            chord = [msg.note, msg.note +5] 
        elif step == 4:
            step = 0
            stepsCount += 1


def score(sequence):
    noteA = int
    noteB = int
    cost = 0
    for i in range(len(sequence)-2):
        noteA = sequence[i].note % 12
        noteB = sequence[i+1].note % 12
        interval = (noteA - noteB)
        if interval < 0:
            interval = 12 + interval
        print(intervalDict[interval])
        cost += intervalCost[interval]
    print('cost', cost)

def mutate(sequence):
    for each in sequence:
        if random.random() > 0.75:
            scale = int(random.uniform(0.0,8.0) // 1)
            quantize2key_(sequence,scaleDict[scale])


def create_selection_of_sequences():
    array = ['','','']
    for i in range(3):
        array[i] = __generate_random_notes()
        quantize2key_(array[i],major)
        mutate(array[i])
    return array

def evolve(sequenceA):
    newGeneration = create_selection_of_sequences()
    spawned = []
    for sequenceB in newGeneration:
        quantize2key(sequenceB,major,sequenceA[0].note%12)
        split = int(random.uniform(len(sequenceA)//8,len(sequenceA)-(len(sequenceA)//8)))
        childAB = []
        for i in range(split):
            childAB.append(sequenceA[i])
        for i in range(split,len(sequenceB)):
            childAB.append(sequenceB[i])
        spawned.append(childAB)
    for each in spawned:
        playSequence(each)
    spawned.append(sequenceA)
    selectSequence(spawned)

def main():
    window = Tk()
    window.title("Evolutionary Composer")
    window.geometry("300x250")
    
    player = Player()
    player.open_stream()
    synth  = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=True, osc2_waveform=Waveform.sine, osc2_volume=0.8, osc2_freq_transpose=2)

    buttons = {}
    
    chord = ["C3", "E3", "G3"]

    #output = mido.open_output('Nord Stage 3 MIDI Input')
    #player.play_wave(synth.generate_chord(chord,1))
    
    lbl = Label(window, text = "Select function: ")
    lbl.grid()

    def clicked():
        internalMidi = mido.open_output('IAC Driver Bus 1')
        array = create_selection_of_sequences()
        for i in range(len(array)):
            

        buttons = {name: Button(name=name) for name in instanceIDs}

        for sequence in array:
            playSequence(sequence)
            time.sleep(1)
            synth.generate_chord(chord,1)
        selectSequence(array)
        lbl.configure(text = "I just got clicked")
    

    btn = Button(window, text = "Click me" ,
                fg = "red", command=clicked)
    # set Button grid
    btn.grid(column=1, row=0)

    window.mainloop()


def selectSequence(array):
    sequenceA = False
    while True:
        choice = input("Choose the sequence you want to pass to the next level choosing 1 - " + str(len(array)) + " or enter 0 to stop the evolution: ")
        if choice.isdigit:
            choice = int(choice) - 1
            if len(array) > choice > -1:
                if not sequenceA:
                    sequenceA = array[choice]
                    buffer = sequenceA
                    evolve(sequenceA)
                    break
            if choice == -1:
                print("Quitting...")
                if not len(array)< 4:
                    midFile = sequence2midi(array[3])
                    try:
                        midFile.save('newSequence.mid')
                    except:
                        print(mido.KeySignatureError)
                
                else:
                    midFile =  sequence2midi(array[0])
                    try:
                        midFile.save('newSequence.mid')
                    except ValueError:
                        print(ValueError)
                time.sleep(1)
                break

        else:
            print("invalid choice")
    quit
        
def playSequence(sequence):
    player = Player()
    player.open_stream()
    synth = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=True, osc2_waveform=Waveform.sine, osc2_volume=0.8, osc2_freq_transpose=2)    
    score(sequence)
    chord = ["C3", "E3", "G3"]
    with mido.open_output('IAC Driver Bus 1'):
        for msg in sequence:    
            #output.send(msg)
            if msg.velocity == 0:
                time.sleep(msg.time/96)
            else:
                internalMidi.send(msg)
                time.sleep(msg.time/96)
                noteOff = mido.Message('note_off',channel = 0, note = msg.note, velocity = 0)
                internalMidi.send(noteOff)

            #time.sleep(msg.time/2400)
        time.sleep(1)
        player.play_wave(synth.generate_chord(chord,1))

def test():
    print(mido.get_output_names())
    output = mido.open_output('Nord Stage 3 MIDI Input')
    testMidi = mido.MidiFile('/Users/ethanblood/Downloads/test.mid',clip=True)
    midiArray = list
    for i, track in enumerate(testMidi.tracks):
        print('Track {}: {}'.format(i, track.name))
        tempo = TEMPO
        for msg in track:
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo/1000
                continue
            else:
                time.sleep(msg.time/TEMPO)
                output.send(msg)
                #print(msg)
    print(midiArray)

if __name__ == '__main__':
    internalMidi = mido.open_output('IAC Driver Bus 1')
    main()
    #test()