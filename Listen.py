from mido import *
import Genome
import mido
import time

_bpm = 90
_tempo = int(((60/_bpm))*1000000)
TK = 480
SUBDIV = TK/8
global ticks
_ticks = int(mido.second2tick(15/(2*_bpm),TK,_tempo))
KEY = 0

internalMidi = mido.open_output('IAC Driver Bus 1')

def playSequence(genome: Genome.Genome):    
    """Plays back the midi sequence to the internal midi bus or synth"""
    with mido.open_output('IAC Driver Bus 1') as internalMidi:
        for phrase in genome.Phrase:
            for measure in phrase.Measure:
                for noteObj in measure.Bar:
                    if noteObj.type == "pause":
                        time.sleep(mido.tick2second(noteObj.length*SUBDIV,TK,_tempo))
                    else:
                        internalMidi.send(mido.Message("note_on",note=noteObj.note+48,velocity=90,time=0))
                        time.sleep(mido.tick2second(noteObj.length*SUBDIV,TK,_tempo))
                        internalMidi.send(mido.Message("note_off", note = noteObj.note+48, velocity = 55, time = noteObj.length*SUBDIV))
        internalMidi.panic()

