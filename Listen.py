from mido import *
import Genome
import mido
import time

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

def playSequence(genome: Genome.Genome):    
    """Plays back the midi sequence to the internal midi bus or synth"""
    with mido.open_output('IAC Driver Bus 1') as internalMidi:
        for phrase in genome.Phrase:
            #print(phrase.shape)
            for measure in phrase.Measure:
                print(measure.shape)
                for noteObj in measure.Bar:
                    if noteObj.type == "pause":
                        time.sleep(mido.tick2second(noteObj.length*SUBDIV,TK,_tempo))
                    else:
                        internalMidi.send(mido.Message("note_on",note=noteDict[noteObj.note],velocity=90,time=0))
                        time.sleep(mido.tick2second(noteObj.length*SUBDIV,TK,_tempo))
                        internalMidi.send(mido.Message("note_off", note = noteDict[noteObj.note], velocity = 55, time = noteObj.length*SUBDIV))
        internalMidi.panic()

