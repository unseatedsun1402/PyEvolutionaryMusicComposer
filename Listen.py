from mido import *
import Genome
import Harmonize
import mido
import time

_bpm = 120
'''beats per minute'''

_tempo = int(((60/_bpm))*1000000)
'''milliseconds per quater note'''

TK = 480
'''No. of ticks per quater note divission'''
SUBDIV = TK/4
'''No. of ticks per 16th note subdivision'''
global ticks
_ticks = int(mido.second2tick(15/(2*_bpm),TK,_tempo))


KEY = 0

internalMidi = mido.open_output('IAC Driver Bus 1')
'''Midi Bus to output midi stream to'''

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

def playSequence(genome: Genome):    
    """Plays back the midi sequence to the internal midi bus or synth"""
    with mido.open_output('IAC Driver Bus 1') as internalMidi:
        for phrase in genome.Phrase:
            #print(phrase.shape)
            for measure in phrase.Measure:
                #print(measure.shape)
                harmony = Harmonize.harmonize(measure)
                for i in harmony:
                    internalMidi.send(mido.Message("note_on",note=noteDict[i]-12,velocity = 40,time = 0))
                for noteObj in measure.Bar:
                    if noteObj.type == "pause":
                        time.sleep(mido.tick2second(noteObj.length*SUBDIV,TK,_tempo))
                    else:
                        try:
                            internalMidi.send(mido.Message("note_on",note=noteDict[noteObj.note],velocity=noteObj.velocity,time=0))
                            time.sleep(mido.tick2second(noteObj.length*SUBDIV,TK,_tempo))
                            internalMidi.send(mido.Message("note_off", note = noteDict[noteObj.note], velocity = noteObj.velocity, time = noteObj.length*SUBDIV))
                        except KeyError as k:
                            print(k)
                            print(noteObj)
                for i in harmony:
                    internalMidi.send(mido.Message("note_off",note = noteDict[i]-12,velocity = 40, time = 0))
        internalMidi.panic()

def setTempo(tempo: int):
    '''sets the global bpm and tempo variables'''
    global _bpm
    global _tempo
    _bpm = tempo
    _tempo = int(((60/_bpm))*1000000)

