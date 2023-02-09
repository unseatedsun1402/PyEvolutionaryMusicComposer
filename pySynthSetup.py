import pyaudio
from synthesizer import Player,Synthesizer,Waveform
import mido
from mido import *
import time
import random
import math
from tkinter import *
from tkinter import filedialog as fd
from functools import partial

"""Definitions
###
# 
# Defines the globally accessed varibles/constants
# 
###
"""
array = ['']
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

chordDict = {"major":[0,4],
"sus2":[0,2],
"sus4":[0,5],
"perfect":[0,7],
"add6":[0,9],
"7th":[0,11]}

major =    [0,2,4,5,7,9,11]
minor =    [0,2,3,5,7,8,10]
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

BPM = 120
TEMPO = int(((60/BPM))*1000000)
SIZE = 3           #no. of sequences
LENGTH = 12        #no. of notes
TK = 480
TICKS = int(mido.second2tick(60/BPM,TK,TEMPO))
KEY = 0



def midi2note(msg):
    """Turns mido midi messages into string note value (e.g. xA3)"""
    val = msg.note

    note = noteDict[val%12]+str(val//12)
    return note

def mNote2note(val):
    """Turns midi note value (int) into a string note value (e.g. A3)"""
    note = noteDict[val%12]+str(val//12)
    return note


def quantize2key_(sequence: list,scale: list):
    """Transposes note to fit into the passed scale list"""
    quantized = False
    key_center_found = True
    key_center = KEY
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

def quantize2key(sequence: list,scale: list,key_center: str):
    """Transposes note to fit into the passed scale list"""
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


def msg2dict(msg: Message):
    """turns a mido midi message into a dictionary of accessible variables"""
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

"""Turns a sequence of notes in to a midi sequence"""
def sequence2midi(sequence):
    midiSequence = mido.MidiFile()
    track = mido.MidiTrack()
    metaTsg = mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8,time=0)
    metaTmp = mido.MetaMessage('set_tempo',tempo = TEMPO, time = 0)
    track.append(metaTsg)
    track.append(metaTmp)
    for note in sequence:
        notetime = note.time
        note.time = 0
        track.append(note)
        noteOff = mido.Message('note_off',note=note.note, velocity = note.velocity,time = notetime)
        track.append(noteOff.copy())
    midiSequence.tracks.append(track)
    return (midiSequence)



def __generate_random_notes():
    """Generates a random series of notes and returns them as a mido message sequence"""
    sequence = []
    msg = mido.Message
    rNoteOn = bool
    rVelocity = int
    rNote = int
    for i in range(LENGTH):
        if random.random() > 0.1:
            rVelocity = int(random.uniform(50.0,100.0))
            rNote = int(random.uniform(45.0,71.0) // 1)
        else:
            rVelocity = (0)
            rNote = (0)
        msg = mido.Message('note_on',note = rNote,velocity = rVelocity, time = TICKS)
        sequence.append(msg)
    return sequence

def harmonize(note,interval):
    """harmonizes a note based on the previous interval"""
    player = Player()
    player.open_stream()
    synth = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=True, osc2_waveform=Waveform.sine, osc2_volume=0.8, osc2_freq_transpose=2)
    if (interval%12-note%12) < 0:
        interval = 12-(note%12)
    else:
        interval = int(interval%12)

    #print(mNote2note(note))
    if (intervalDict[interval] == "major" or intervalDict[interval] == "perfect"):
        root = mNote2note(note)
        part1 = (mNote2note(note))[:1]
        try:
            part2 = int(mNote2note(note)[1:]) -1
        except:
            part2 = int(mNote2note(note)[2:]) -1

        tonic = part1+str(part2)
        chord = [root,tonic]
        player.play_wave(synth.generate_chord(chord,length=(60/TEMPO)))
        

def score(sequence):
    """Gives an arbritrary fitness score"""
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
    """Returns a list of midi note sequences"""
    for i in range(SIZE):
        array[i] = __generate_random_notes()
        quantize2key_(array[i],major)
        mutate(array[i])
    return array


def evolve(sequenceA):
    """Generates an list of new midi sequences based on the passed sequence"""
    swap = sequenceA
    newGeneration = create_selection_of_sequences()
    if len(array) < 4:
        array.append(sequenceA)
    else:
        array[len(array)-1] = sequenceA

    spawned = []
    for sequenceB in newGeneration:
        quantize2key(sequenceB,scaleDict[int(random.randrange(0,7))],sequenceA[0].note%12)
        split = int(random.uniform(len(sequenceA)//8,len(sequenceA)-(len(sequenceA)//8)))
        childAB = []
        if(random.random() < 0.5):
            
            sequenceA = sequenceB
            sequenceB = swap            
        for i in range(split):
            childAB.append(sequenceA[i])
        for i in range(split,len(sequenceB)):
            childAB.append(sequenceB[i])
        spawned.append(childAB)
    
    i=0
    for each in spawned:
        array[i] = each
        i += 1


def main():
    """Main Code loop containing the GUI"""
    window = Tk()
    window.title("Evolutionary Composer")
    window.geometry("450x250")
    
    player = Player()
    player.open_stream()
    synth  = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=True, osc2_waveform=Waveform.sine, osc2_volume=0.8, osc2_freq_transpose=2)

    buttonItems = tuple(i for i in range(SIZE))
    buttons = {}
    for i in range(SIZE-1):
        array.append('')
    chord = ["C3", "E3", "G3"]

    #output = mido.open_output('Nord Stage 3 MIDI Input')
    #player.play_wave(synth.generate_chord(chord,1))
    
    lbl = Label(window, text = "Select function: ")
    lbl.grid()

    def clicked():
        internalMidi = mido.open_output('IAC Driver Bus 1')
        
        
        array = create_selection_of_sequences()
        
        buttons = {each: Button(text="Sequence: "+str(each),command=partial(playSequence,each)) for each in buttonItems}

        #counter = 0
        for each in buttons:
            buttons[each].grid(row = 1, column = each)
            #counter =+ 1

        '''
        for sequence in array:,command = playSequence(array[each])
            playSequence(sequence)
            time.sleep(1)
            synth.generate_chord(chord,1)
        selectSequence(array)'''

        lbl.configure(text = "Generate new sample of melodies")

        value_inside = StringVar()
        value_inside.set("-1")

        select_sequence = OptionMenu(window, value_inside, *buttonItems)
        select_sequence.grid(row=2,column = 0,columnspan=1)

        submit_button = Button(window, text='Submit', command=lambda: selectSequence(int(value_inside.get())))
        submit_button.grid(row = 2,column =2)
       
        def saveFile(choice: int):
            filename = fd.asksaveasfilename()
            midFile =  sequence2midi(array[choice])
            try:
                midFile.save(filename)
            except Exception:
                print("Error")
            

        save_button = Button(window, text='Save Midi', command=lambda: saveFile(int(value_inside.get())))
        save_button.grid(row=3,column = 2)

    
    

    btn = Button(window, text = "Click me" ,
                fg = "red", command=clicked)
    # set Button grid
    btn.grid(column=1, row=0)

    window.mainloop()



def selectSequence(choice):
   """Selects the new sequence to evolve"""
   sequenceA = False
   while True:
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
                break

        
def playSequence(choice: Button):    
    """Plays back the midi sequence to the internal midi bus or synth"""
    score(array[choice])
    sequence = array[choice]
    chord = ["C3", "E3", "G3"]
    with mido.open_output('IAC Driver Bus 1'):
        interval = 0
        for msg in sequence:    
            #output.send(msg)
            if msg.velocity == 0:
                time.sleep(mido.tick2second(msg.time,TK,TEMPO))
            else:
                internalMidi.send(msg)
                #harmonize(msg.note,interval)
                interval = msg.note
                time.sleep(mido.tick2second(msg.time,TK,TEMPO))
                noteOff = mido.Message('note_off',channel = 0, note = msg.note, velocity = 0)
                internalMidi.send(noteOff)

            #time.sleep(msg.time/2400)
        time.sleep(1)

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

"""Detects if the script is being ran as a program or called as a library"""
if __name__ == '__main__':
    internalMidi = mido.open_output('IAC Driver Bus 1')
    main()
    #test()