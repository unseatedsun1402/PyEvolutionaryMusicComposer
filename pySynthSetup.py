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
buttonItems = tuple
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
            1:minor,
            2:dorian,
            3:phrygian,
            4:lydian,
            5:mix,
            6:aeolian,
            7:locrian}
            
intervalDict = {0:'perfect',1:'minor',2:'major',3:'minor',
    4:'major',5:'perfect',6:'augmented',7:'perfect',8:'minor',
    9:'major',10:'minor',11:'major'}

intervalCost = {0:2,1:1,2:3,3:1,4:3,5:2,6:4,7:2,8:1,9:3,10:1,11:3}

_bpm = 160
_tempo = int(((60/_bpm))*1000000)
_size = 7           #no. of sequences
_length = 64       #no. of subdivisions / genome length
TK = 480
_ticks = int(mido.second2tick(15/(2*_bpm),TK,_tempo))
KEY = 0



def midi2note(msg: mido.Message):
    """Turns mido midi messages into string note value (e.g. xA3)"""
    val = msg.note

    note = noteDict[val%12]+str(val//12)
    return note

def mNote2note(val: int):
    """Turns midi note value (int) into a string note value (e.g. A3)"""
    note = noteDict[val%12]+str(val//12)
    return note


def quantize2key_(sequence: list,scale: list):
    """Transposes note to fit into the passed scale list"""
    quantized = False
    key_center_found = True
    key_center = KEY
    scale = scaleDict[random.randint(0,1)]
    match scale:
        case 0:
            key_signature = mNote2note(KEY)[0]
        case 1: 
            key_signature = mNote2note(KEY)[0] + 'm'
        case _:
            key_signature = mNote2note(KEY)[0]
    

    while not key_center_found:
        try:
            if not sequence[key_center].velocity == 0:
                key_center = sequence[key_center].note%12
                key_center_found = True
            else:
                key_center += 1
        except:
            print("Non Message Type")
    print("Key Centre is",noteDict[key_center])
    for each in sequence:
        try:
            if each.velocity == 0:
                continue
            quantized = False
            while not quantized:
                #print(midi2note(each))
                if not (key_center + (each.note%12)) in scale:
                    each.note += 1
                    #print('Quantized ' + str(each.note-1) + 'to' + str(each.note))
                    #print(midi2note(each))
                else:
                    quantized = True
        except:
            print("Non Message Type")
    sequence.append(mido.MetaMessage('key_signature',key = key_signature))

def quantize2key(sequence: list,scale: list,key_center: str):
    """Transposes notes in sequence to fit into the passed scale list"""
    quantized = False
    print("Key Centre is",noteDict[key_center])
    for each in sequence:
        try:
            if each.velocity == 0:
                continue
            quantized = False
            while not quantized:
                print(midi2note(each))
                if not (key_center + (each.note%12)) in scale:
                    if (key_center + (each.note%12)+1) in scale:
                        each.note += 1
                    else:
                        each.note -= 1
                    #print('Quantized ' + str(each.note-1) + 'to' + str(each.note))
                    print(midi2note(each))
                else:
                    quantized = True
        except Exception:
            #print("Non Message Type")
            pass



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
    metaTmp = mido.MetaMessage('set_tempo',tempo = _tempo, time = 0)
    track.append(metaTsg)
    track.append(metaTmp)
    for note in sequence:
        if hasattr(note,"velocity"):
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
    rVelocity = int
    rNote = int
    genome = _length
    oldNote = int
    while len(sequence) < _length:
        if random.random() > 0.1:
            rVelocity = random.randint(50,100)
            rNote = random.randint(45,71)
            octave = rNote // 12
            try:
                if oldNote // 12 < (rNote // 12):
                    rNote -= 12
                elif oldNote // 12 > (rNote // 12):
                    rNote += 12
            except:
                pass
        else:
            rVelocity = (0)
            rNote = (0)
        
        length = random.randint(2,4)
        length *= 2
        
        time = length*_ticks
        if time >= ((genome*_ticks)-time):
            time = int(genome*_ticks)
        
        msg = mido.Message('note_on',note = rNote,velocity = rVelocity, time = 0)
        sequence.append(msg)
        
        msg = mido.Message('note_off',note=rNote,velocity = rVelocity, time = time)
        sequence.append(msg)
        
        genome -= int(time/_ticks)
        for each in range(int(time/_ticks)-2):
            sequence.append('')
        oldNote = rNote
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
        player.play_wave(synth.generate_chord(chord,length=(60/_tempo)))
        

def score(sequence):
    """Gives an arbitrary fitness score"""
    noteA = int
    noteB = int
    cost = 0
    for i in range(len(sequence)-2):
        try:
            noteA = sequence[i].note % 12
            noteB = sequence[i+1].note % 12
            interval = (noteA - noteB)
            if interval < 0:
                interval = 12 + interval
            #print(intervalDict[interval])
            cost += intervalCost[interval]
        except:
            #print("Non Message Type")
            pass
    print('cost', cost)

def mutateSeq(sequence):
    for each in sequence:
        if random.random() > 0.75:
            scale = random.randint(0,1)
            #quantize2key_(sequence,scaleDict[scale])

def mutateNote(note: int):
    note += random.randint(-11,11)
    return note

def create_selection_of_sequences():
    """Returns a list of midi note sequences"""
    for i in range(_size):
        array[i] = __generate_random_notes()
        quantize2key_(array[i],major)
        mutateSeq(array[i])
    return array


def evolve(sequenceA):
    """Generates an list of new midi sequences based on the passed sequence"""
    swap = sequenceA
    newGeneration = create_selection_of_sequences()
    if len(array)-1 == _size:
        array.append(sequenceA)
    else:
        array[len(array)-1] = sequenceA

    spawned = []
    for sequenceB in newGeneration:
        quantize2key(sequenceB,scaleDict[int(random.randrange(0,1))],sequenceA[0].note%12)
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

def difference():
    for each in range(len(array)-2):
        aDiff = 0
        bDiff = 0
        counter = 0
        for msg in array[each]:
            try:
                if msg == array[len(array)-2][counter]:
                    aDiff += 1
            except:
                pass
            try:
                if msg == array[len(array)-1][counter]:
                    bDiff += 1
            except:
                pass
            counter +=1
        print(aDiff / _length)
        print(bDiff / _length)

def difference_(a: list, b: list, c: list):
        aDiff = 0
        bDiff = 0
        counter = 0
        for msg in c:
            try:
                if msg == a[counter]:
                    aDiff += 1
            except:
                pass
            try:
                if b[counter]:
                    bDiff += 1
            except:
                pass
            counter +=1
        print(aDiff / _length)
        print(bDiff / _length)

def repair(sequence: list):
    notesOpen = []
    openFlag = False
    for each in sequence:
        if hasattr(each,"type"):
            if each.type == "note_on":
                notesOpen.append(each.note)
                openFlag = True
            elif each.type == "note_off":
                if each.note in notesOpen:
                    notesOpen.pop(notesOpen.index(each.note))
            if each.type == "note_off" and not openFlag:
                each = ''
            openFlag = False
    count = 0
    for each in notesOpen:
        sequence[_length-1-count]= mido.Message("note_off",note = each, velocity = 0, time = 0)
        count -= 1
    print(notesOpen)


def crossCombine(sequenceA: list,sequenceB: list):
    """Generates an list of new midi sequences based on the parent sequences"""
    array[_size-2] = list(each for each in sequenceA)
    array[_size -1] = list(each for each in sequenceB)
    m = list(each for each in sequenceB)

    for arrayIndex in range(_size-2):                         #crossover
        
        array[arrayIndex] = list(each for each in sequenceA)
        """if random.random() >= 0.5:
            m = array[_size - 2]
            array[arrayIndex] = array[_size -1]"""

        switched = []
        instead = []
        for i in range(_length-1):
            chanceChange = random.random()
            if chanceChange > 0.3:
                array[arrayIndex][i] = m[i]
                if hasattr(m[i],"type"):
                    if m[i].type == "note_on":
                        if hasattr(array[arrayIndex][i+1],"note"):
                            instead.append(array[arrayIndex][i+1].note)
                        array[arrayIndex][i+1] = m[i+1]
                        try:
                            tMinus = int(m[i+1].time)
                            while tMinus > _ticks*2:
                                array[arrayIndex][i +int(tMinus/(_ticks*2))] = ''
                                tMinus -= _ticks*2
                        except:
                            pass
                        switched.append(m[i].note)
                        if random.random() < 0.01:
                            try:
                                array[arrayIndex][i].note = mutateNote(array[arrayIndex][i].note)
                                array[arrayIndex][i+1].note = array[arrayIndex][i].note
                            except:
                                #print("i = "+ str(i))
                                #print(array[arrayIndex][i].note)
                                #print(array[arrayIndex][i+1])
                                pass
            else:
                if hasattr(array[arrayIndex][i],"type"):
                    if array[arrayIndex][i].type == "note_on":
                        i += 1
            repair(array[arrayIndex])
    difference()
    
    return 1

def main():
    """Main Code loop containing the GUI"""
    window = Tk()
    window.title("Evolutionary Composer")
    window.geometry("875x250")
    
    player = Player()
    player.open_stream()
    synth  = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=True, osc2_waveform=Waveform.sine, osc2_volume=0.8, osc2_freq_transpose=2)

    buttonItems = tuple(i for i in range(_size))
    for i in range(_size-1):
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


        lbl.configure(text = "Generate new sample of melodies")
        lbl.grid(columnspan=2)

        instuction = Label(window,text="Use the dropdowns to select the parents to start the new generation")
        instuction.grid(column=1,row=2,columnspan=3)

        value_inside1 = StringVar()
        value_inside1.set("0")

        value_inside2 = StringVar()
        value_inside2.set("1")

        select_sequence = OptionMenu(window, value_inside1, *buttonItems)
        select_sequence.grid(row=3,column = 0,columnspan=1)

        select_sequence = OptionMenu(window, value_inside2, *buttonItems)
        select_sequence.grid(row=3,column = 1,columnspan=1)

        '''submit_button = Button(window, text='Submit', command=lambda: selectSequence(int(value_inside1.get())))
        submit_button.grid(row = 2,column =2)'''

        submit_button = Button(window, text='Submit', command=lambda: crossCombine(array[int(value_inside1.get())],array[int(value_inside2.get())]))
        submit_button.grid(row = 3,column =2)
       
        def saveFile(choice: int):
            filename = fd.asksaveasfilename()
            midFile =  sequence2midi(array[choice])
            try:
                midFile.save(filename)
            except Exception:
                pass
                #print("Error")
            

        save_button = Button(window, text='Save Midi', command=lambda: saveFile(int(value_inside1.get())))
        save_button.grid(row=5,column = 2)
    
    def setTempo(val: int):
        _bpm = val
        _tempo = int(((60/_bpm))*1000000)
    

    btn = Button(window, text = "Click me" ,
                fg = "red", command=clicked)
    # set Button grid
    btn.grid(column=3, row=0)
        
    slowtmp = Button(window, text="Slow", command=lambda: setTempo(60))
    slowtmp.grid(column=3,row = 3)
    
    medtmp = Button(window, text="Andante", command=lambda: setTempo(100))
    medtmp.grid(column=3,row = 4)

    fasttmp = Button(window, text="Fast", command=lambda: setTempo(180))
    fasttmp.grid(column=3,row = 5)

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

        
def playSequence(choice: int):    
    """Plays back the midi sequence to the internal midi bus or synth"""
    score(array[choice])
    sequence = array[choice]
    chord = ["C3", "E3", "G3"]
    with mido.open_output('IAC Driver Bus 1'):
        #interval = 0
        for msg in sequence:
            if hasattr(msg,"velocity"):
                #output.send(msg)
                if msg.velocity == 0:
                    time.sleep(mido.tick2second(msg.time,TK,_tempo))
                else:
                    time.sleep(mido.tick2second(msg.time,TK,_tempo))
                    internalMidi.send(msg)
                    #harmonize(msg.note,interval)
                    #interval = msg.note
                    
                    #noteOff = mido.Message('note_off',channel = 0, note = msg.note, velocity = 0)
                    #internalMidi.send(noteOff)

                #time.sleep(msg.time/2400)
        time.sleep(1)

def test():
    print(mido.get_output_names())
    output = mido.open_output('Nord Stage 3 MIDI Input')
    testMidi = mido.MidiFile('/Users/ethanblood/Downloads/test.mid',clip=True)
    midiArray = list
    for i, track in enumerate(testMidi.tracks):
        print('Track {}: {}'.format(i, track.name))
        tempo = _tempo
        for msg in track:
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo/1000
                continue
            else:
                time.sleep(msg.time/_tempo)
                output.send(msg)
                #print(msg)
    print(midiArray)

"""Detects if the script is being ran as a program or called as a library"""
if __name__ == '__main__':
    internalMidi = mido.open_output('IAC Driver Bus 1')
    main()
    #test()