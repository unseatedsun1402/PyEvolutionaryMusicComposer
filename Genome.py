import random
import mido
from mido import *
import numpy

tonicChord = {'one': [0,5,7],
              'two':[2,5,9],
              'three':[4,7,11],
              'four':[5,8,0],
              'five':[7,11,2],
              'six':[8,0,4],
              'dim':[11,2,5]
            }


###################################################
#           Genome Class
###################################################
class Genome:
    '''largest structure containing pairs of phrases'''
    def __init__(self,**kwargs):
        self.length = kwargs["length"]
        self.dimensions = (4,8)
        self.Phrase = [Phrase(self.dimensions) for  phr in range(self.length)]
        self.Motif = [Measure]
        self.Repitition = None
        self.Fitness = int

    def _shape(self):
        pass

        
            

    def repitition(self):
        for phrase in self.Phrase:
            for measure in phrase.Measure:
                Bar = []
                for note in measure.Bar:
                    if note.type == "note":
                        Bar.append((note.type,note.length,note.note))
                    else:
                        Bar.append((note.type,note.length))
                if not Bar in self.Motif:
                    self.Motif.append(Bar)
                else:
                    self.Repitition += 1/(len(self.Phrase)*self.dimensions[0])

    def genome2midi(self) -> mido.MidiTrack:
        Track = mido.MidiTrack
        for phrase in self.phrase:
            for measure in phrase:
                for div in measure:
                    if not None:
                        Track.append(mido.Message("note_on",note = div + 48, velocity = 55))
    
    def motion(self):
        conjunct = 0
        disjunct = 0
        for phrase in self.Phrase:
            for measure in phrase.Measure:
                try:
                    c,d = measure.Motion
                except AttributeError:
                    measure._motion()
                    c,d = measure.Motion
                conjunct += c
                disjunct += d
            phrase.motionRatio = conjunct/disjunct
        
        self.motionRatio = conjunct/disjunct

###################################################
#               Phrase Class
##################################################
class Phrase:
    '''second structure containing four measures'''
    def __init__(self,args):
        self.measures,self.subdivisions = args
        self.Measure = [Measure(key='C',subdiv=self.subdivisions) for i in range(self.measures)]
        self.motionRatio = float

    def _shape(self):
        values = []
        for measure in self.Measure:
            avg = 0
            for each in measure.gradient:
                avg += each
            values.append(avg)
        f = numpy.array(values, dtype = float)
        try:
            shape = numpy.gradient(f)
            self.gradient = shape
        except:
            self.shape = "stationary"
            self.gradient = [0]
            return
        
        self.shape = str
        gradient = []
        for each in shape:
            if each > 0:
                if not "ascending" in gradient:
                    gradient.append("ascending")
            elif each < 0:
                if not "descending" in gradient:
                    gradient.append("descending")
            elif each == 0:
                if not "stationary" in gradient:
                    gradient.append("stationary")
        if len(gradient) == 1:
            self.shape = gradient[0]
        elif set(["stationary","ascending"]).issubset(gradient):
            self.shape = "stationary-ascending"
        elif set(["ascending","descending"]).issubset(gradient):
            self.shape = "ascending-descending"
        elif set(["descending","ascending"]).issubset(gradient):
            self.shape = "descending-ascending"
        elif set(["descending","stationary"]).issubset(gradient):
            self.shape = "descending-stationary"
        elif set(["stationary","descending"]).issubset(gradient):
            self.shape = "stationary-descending"
        elif set(["ascending","stationary"]).issubset(gradient):
            self.shape = "ascending-stationary"

        else:
            return Exception(str('No Gradient Found'))
                
        self._motion()
    
    def _motion(self):
        pass


###################################################
#                  Measure Class
###################################################
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
                measure.append(Note(length=random.randint(1,8),note=random.randint(0,15),type="note"))
                if subdivisions ==6:
                    measure[len(measure)-1].velocity = 100
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
                if subdivisions ==6:
                    measure[len(measure)-1].velocity = 100
                subdivisions -= measure[count].length
                if subdivisions < 0:
                    measure[count].length = measure[count].length + subdivisions
                count +=1

        self.Bar = measure

    def Closing(self):
        subdivisions = 0                #starting bar must contain a note from tonic chord
        for each in self.Bar:
            subdivisions += each.length
        
        count = 0
        measure = []
        cadence = {0:[0,5,8],
                   1:[4,5,12],
                   2:[5,11,13]}
        c = cadence[random.randint(0,2)]
        while subdivisions > 0:
            note = c[random.randint(0,2)]
            measure.append(Note(length=random.randint(1,4),note=note,type="note"))
            subdivisions -= measure[count].length
            if subdivisions < 0:
                measure[count].length = measure[count].length + subdivisions
            count +=1

        condition = False
        note = self.Bar[len(self.Bar)-1]
        if not note in c:
            self.Bar[len(self.Bar)-1] = 0

            
        self.Bar = measure
        self._motion()

    
    def _shape(self):
        values = []
        for each in self.Bar:
            if each.type == "note":
                values.append(each.note)
        f = numpy.array(values, dtype = float)
        try:
            shape = numpy.gradient(f)
            self.gradient = [each for each in shape]
        except:
            self.shape = "stationary"
            self.gradient = [0]
            return
        
        self.shape = str
        gradient = []
        for each in shape:
            if each > 0:
                if not "ascending" in gradient:
                    gradient.append("ascending")
            elif each < 0:
                if not "descending" in gradient:
                    gradient.append("descending")
            elif each == 0:
                if not "stationary" in gradient:
                    gradient.append("stationary")
        if len(gradient) == 1:
            self.shape = gradient[0]
        elif set(["stationary","ascending"]).issubset(gradient):
            self.shape = "stationary-ascending"
        elif set(["ascending","descending"]).issubset(gradient):
            self.shape = "ascending-descending"
        elif set(["descending","ascending"]).issubset(gradient):
            self.shape = "descending-ascending"
        elif set(["descending","stationary"]).issubset(gradient):
            self.shape = "descending-stationary"
        elif set(["stationary","descending"]).issubset(gradient):
            self.shape = "stationary-descending"
        elif set(["ascending","stationary"]).issubset(gradient):
            self.shape = "ascending-stationary"

        else:
            return Exception(str('No Gradient Found'))
                
        self._motion()
    
    def _motion(self):
        notes = []
        conjunct = 0
        disjunct = 0
        for each in self.Bar:
            notes.append(each.note)
        
        for i in range(len(notes)-1):
            if notes[i] - notes[i+1] < 2 and notes[i] - notes[i+1] > -2:
                conjunct += 1/len(notes)
            else:
                disjunct += 1/len(notes)
        self.Motion = (conjunct,disjunct)

###################################################
#               Subdivision Class
###################################################
class Subdivision:
    '''smallest structure for designating subdivisions'''
    def __init__(self,**kwargs):
        self.length = kwargs["length"]
    


###################################################
#        Note Class (child of subdivision)
###################################################
class Note(Subdivision):
    def __init__(self,**kwargs):
        Subdivision.__init__(self,**kwargs)
        self.type = kwargs['type']
        if self.type == "note":
            self.note = kwargs["note"]
            self.velocity = 80
