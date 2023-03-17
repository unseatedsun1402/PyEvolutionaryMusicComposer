import random
import mido
from mido import *

tonicChord = {'one': [0,5,7],
              'two':[2,5,9],
              'three':[4,7,11],
              'four':[5,8,0],
              'five':[7,11,2],
              'six':[8,0,4],
              'dim':[11,2,5]}

class Genome:
    '''largest structure containing pairs of phrases'''
    def __init__(self,**kwargs):
        self.length = kwargs["length"]
        self.Phrase = [Phrase(4,8) for  phr in range(self.length)]

    def _shape(self):
        pass

    def _reptition(self):
        pass

    def genome2midi(self) -> mido.MidiTrack:
        Track = mido.MidiTrack
        for phrase in self.phrase:
            for measure in phrase:
                for div in measure:
                    if not None:
                        Track.append(mido.Message("note_on",note = div + 48, velocity = 55))

class Phrase:
    '''second structure containing four measures'''
    def __init__(self,*args):
        self.measures,subdivisions = args
        self.Measure = [Measure(key='C',subdiv=subdivisions) for i in range(self.measures)]

    def _shape(self):
        score = 0
        #normalise notes
        score = 0
        for each in range(int(len(self.Measure)/2)-1):
            score += self.Measure[each].score
        score = score/self.measures
        
        if score < 0:
            self.shape = "descending"
        if score == 0:
            self.shape = "stationary"
        if score > 0:
            self.shape = "ascending"
        
        score = 0
        for each in range(int(len(self.Measure)/2),len(self.Measure)-1):
            score += self.Measure[each].score
        score = score/self.measures

        match self.shape:
            case "descending":
                if score == 0:
                    self.shape = "descending-stationary"
                if score > 0:
                    self.shape = "descending-ascending"
            case "stationary":
                if score < 0:
                    self.shape = "stationary-descending"
                if score > 0:
                    self.shape = "stationary-ascending"
            case "ascending":
                if score < 0:
                    self.shape = "ascending-descending"
                if score == 0:
                    self.shape = "ascending-stationary"



class Measure:
    '''third structure containing 8 subdivisions'''
    def __init__(self,**kwargs):
        self.subdiv = kwargs["subdiv"]
        self.div = int(kwargs["subdiv"]/2)
        self.key = kwargs['key']
        self.score = float
        self.Bar = [Subdivision(length=1) for i in range(self.subdiv)]
        

    def generateMeasure(self, **kwargs):
        subdivisions = 0
        if kwargs["start"]:                     #starting bar must contain a note from tonic chord
            for each in self.Bar:
                subdivisions += each.length
            
            count = 0
            measure = []
            while subdivisions > 0:
                measure.append(Note(length=random.randint(1,4),note=random.randint(0,15),type="note"))
                subdivisions -= measure[count].length
                if subdivisions < 0:
                    measure[count].length = measure[count].length + subdivisions
                count +=1

            condition = False
            for each in measure:
                if not each.note in tonicChord['one']:
                    continue
                else:
                    condition = True
            if not condition:
                self.Bar[0].note=0
            
        
        else:                                   #requirement waved for specific note appearences
            for each in self.Bar:
                subdivisions += each.length
            
            count = 0
            measure = []
            while subdivisions > 0:
                measure.append(Note(length=random.randint(1,8),note=random.randint(0,15),type="note"))
                subdivisions -= measure[count].length
                if subdivisions < 0:
                    measure[count].length = measure[count].length + subdivisions
                count +=1

        self.Bar = measure      
    
    def _shape(self):
        score = 0
        #normalise notes
        values = []
        min = 99
        max = 0
        stationary = False
        for each in self.Bar:
            if each.type == "note":
                if each.note < min:
                    min = each.note
                if each.note > max:
                    max = each.note
                values.append(each.note)
        for z in range(len(values)):
            if not (max - min) == 0:
                values[z] = (values[z]-min) / (max-min)
            else:
                score = 0
        
        for note in range(1,len(values)):
            score = values[note] - values[note-1]
        self.score = score / self.subdiv
        if score < 0:
            self.shape = "descending"
        elif score == 0:
            self.shape = "stationary"
        elif score > 0:
            self.shape = "ascending"

class Subdivision:
    '''smallest structure for designating subdivisions'''
    def __init__(self,**kwargs):
        self.length = kwargs["length"]
    

class Note(Subdivision):
    def __init__(self,**kwargs):
        Subdivision.__init__(self,**kwargs)
        self.type = kwargs['type']
        if self.type == "note":
            self.note = kwargs["note"]
