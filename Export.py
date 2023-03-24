import mido
from Genome import *
import Harmonize
from tkinter import filedialog as fd

_bpm = 160
_tempo = int(((60/_bpm))*1000000)
TK = 480
SUBDIV = TK/2
global ticks
_ticks = int(mido.second2tick(15/(2*_bpm),TK,_tempo))
KEY = 0

internalMidi = mido.open_output('IAC Driver Bus 1')

noteDict = {0:60,
            1:62,
            2:64,
            3:65,
            4:67,
            5:69,
            6:71,
            7:72,
            8:74,
            9:76,
            10:77,
            11:79,
            12:81,
            13:83,
            14:84,
            15:86
            }

def as_midi(genome: Genome, **kwargs):
    melodyTrk = mido.MidiTrack()
    metaTsg = mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8,time=0)
    metaTmp = mido.MetaMessage('set_tempo',tempo = _tempo, time = 0)
    melodyTrk.append(metaTsg)
    melodyTrk.append(metaTmp)
    
    if kwargs["harmony"]:
        harmonyTrk = mido.MidiTrack()
        for phrase in genome.Phrase:
            #print(phrase.shape)
            for measure in phrase.Measure:
                print(measure.shape)
                length = 0
                harmony = Harmonize.harmonize(measure)
                for i in harmony:
                    harmonyTrk.append(mido.Message("note_on",note = noteDict[i]-12, velocity = 45, time = 0))
                for noteObj in measure.Bar:
                    length += noteObj.length
                    pause = 0
                    if noteObj.type == "pause":
                        pause += mido.tick2second(noteObj.length*SUBDIV,TK,_tempo)
                    else:
                        melodyTrk.append(mido.Message("note_on",note=noteDict[noteObj.note],velocity=noteObj.velocity,time=int(pause)))
                        melodyTrk.append(mido.Message("note_off", note = noteDict[noteObj.note], velocity = noteObj.velocity, time = int(noteObj.length*SUBDIV)))
                for i in range(len(harmony)-1):
                    if i == 0:
                        harmonyTrk.append(mido.Message("note_off",note = noteDict[harmony[i]]-12,velocity = 45, time = int(length*SUBDIV)))
                    else:
                        harmonyTrk.append(mido.Message("note_off",note = noteDict[harmony[i]]-12,velocity = 45, time = 0))
    else:
        for phrase in genome.Phrase:
            #print(phrase.shape)
            for measure in phrase.Measure:
                for noteObj in measure.Bar:
                    pause = 0
                    if noteObj.type == "pause":
                        pause += noteObj.length
                    else:
                        melodyTrk.append(mido.Message("note_on",note=noteDict[noteObj.note],velocity=noteObj.velocity,time=int(pause)))
                        melodyTrk.append(mido.Message("note_off", note = noteDict[noteObj.note], velocity = noteObj.velocity, time = int(noteObj.length*SUBDIV)))

    file = mido.MidiFile()
    file.tracks.append(melodyTrk)
    try:
        file.tracks.append(harmonyTrk)
    except ReferenceError:
        pass
    try:
        filename = fd.asksaveasfilename()
        if not filename[:3] == ".mid":
            filename += ".mid"
        file.save(filename)
    except Exception as e:
        print(e)