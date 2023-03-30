import random
import mido
from mido import *
import numpy
import copy


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
        '''defines no. of phrases in an indiviual genome'''
        self.dimensions = (4,8)
        '''defines the no. of measures and no. of subdivisions to a meaure'''
        self.Phrase = [Phrase(self.dimensions) for  phr in range(self.length)]
        '''container for Phrase objects'''
        self.Motif = []
        '''container for desireable motifs'''
        self.Repitition = 0
        '''repitition score'''
        self.Fitness = int
        '''Fitness score'''
        self.Motion = 0
        '''motion score'''
        self.AvgMotion = 0
        ''' average motion score'''

    def _shape(self):
        pass
        
    def get_features(self):
        '''returns genome features'''
        gFeatures = [self.length,self.dimensions,self.repitition,self.Fitness]
        pFeatures = [[phrase.shape,phrase.motionRatio]for phrase in self.Phrase]
        return [gFeatures,pFeatures]

    def repitition(self):
        sequence = []
        for phrase in self.Phrase:
            notes = 0
            for measure in phrase.Measure:
                subsequence = []
                for note in measure.Bar:
                    notes += 1
                    subsequence.append(note.note)
                    if len(subsequence) > 1:
                        if set(subsequence).issubset(sequence):
                            self.Repitition += 1
                    sequence.append(note.note)
            self.Repitition = self.Repitition / notes
            self.motion()
                

    def genome2midi(self) -> mido.MidiTrack:
        '''converts a genome into a midiTrack object'''
        Track = mido.MidiTrack
        for phrase in self.phrase:
            for measure in phrase:
                for div in measure:
                    if not None:
                        Track.append(mido.Message("note_on",note = div + 48, velocity = 55))
    
    def motion(self):
        '''gets the conjunct motion percentage of the genome'''
        motion = []
        avgmmotion = 0
        for phrase in self.Phrase:
            avgmmotion += phrase.MotionAvg
            motion.append(phrase.Motion)
        
        
        avgmmotion = avgmmotion/self.length
        self.Motion = motion
        self.AvgMotion = avgmmotion

###################################################
#               Phrase Class
##################################################
class Phrase:
    '''second structure containing four measures'''
    def __init__(self,args):
        self.measures,self.subdivisions = args

        self.Repitition = 0

        self.Measure = [Measure(key='C',subdiv=self.subdivisions) for i in range(self.measures)]
        '''container for Measure objects'''
        self.Motion = []
        '''list of the percentage measures are made up of conjunct motion'''
        self.MotionAvg = 0
        '''percentage of the phrase made up of conjunct motion'''

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
        self._repitition()
    
    def _motion(self):
        motion = []
        motionTotal = 0
        for measure in self.Measure:
            try:
                motion.append(measure.Motion)
                motionTotal += measure.Motion
            except TypeError:
                measure._motion()
        
        self.Motion = motion
        self.MotionAvg = motionTotal/self.measures
        

    def _repitition(self):
        sequence = []
        notes = 0
        for measure in self.Measure:
            subsequence = []
            for note in measure.Bar:
                notes += 1
                subsequence.append(note.note)
                if len(subsequence) > 1:
                    if set(subsequence).issubset(sequence):
                        self.Repitition += 1
                sequence.append(note.note)
        self.Repitition = self.Repitition / notes



###################################################
#                  Measure Class
###################################################
class Measure:
    '''third structure containing 8 subdivisions'''
    def __init__(self,**kwargs):
        self.subdiv = kwargs["subdiv"]
        '''no. of subdivisions'''
        self.div = int(kwargs["subdiv"]/2)
        '''no. of divisions'''
        self.key = kwargs['key']
        '''key of the measure'''
        self._score = float
        '''for fitness evaluation'''
        self.Bar = [Subdivision(length=1) for i in range(self.subdiv)]
        '''list of note objects'''
        self.Motion = float
        

    def generateMeasure(self, **kwargs):
        start = kwargs['start']
        if not start:
            measuremotion = random.random()
            subdivisions = 0
            bar = []
            for each in self.Bar:
                subdivisions += each.length
            
            while subdivisions > 0:
                if len(bar) > 0:
                    note = bar[len(bar)-1]
                else:
                    note = Note(length=random.randint(1,4),type='note',note=random.randint(0,15))
                    bar.append(note)
                    subdivisions -= bar[0].length
                    if random.random()>0.1:
                        note.type = 'pause'
                    continue
                motion = random.random()
                if motion < measuremotion:
                    steps = random.random()
                    if note.note == 15:
                        note = note.note + random.randint(-1,0)
                    elif note.note == 0:
                        note = note.note + random.randint(0,1)
                    else:
                        note = note.note + random.randint(-1,1)
                    
                    bar.append(Note(type = 'note',note = note, length = random.randint(1,4)))
                else:
                    leap = leapRange(bar)
                    bar.append(Note(type='note',note=note.note+leap,length=random.randint(1,4)))
                subdivisions -= bar[len(bar)-1].length
                if subdivisions < 0:
                    bar[len(bar)-1].length += subdivisions
                    
                for each in bar:
                    if not each.note in [0,3,5]:
                        pass
                    else:
                        start = False
                        break
        else:
            measuremotion = random.random()
            subdivisions = 0
            bar = []
            for each in self.Bar:
                subdivisions += each.length
            
            while subdivisions > 0:
                if len(bar) > 0:
                    note = bar[len(bar)-1]
                else:
                    note = Note(length=random.randint(1,4),type='note',note=random.randint(0,15))
                    bar.append(note)
                    subdivisions -= bar[0].length
                    if random.random()>0.1:
                        note.type = 'pause'
                    continue
                motion = random.random()
                if motion < measuremotion:
                    steps = random.random()
                    if steps < 0.5:
                        if note.note == 15:
                            note = note.note + 1
                        else:
                            note = note.note + random.randint(-1,0)
                    else:
                        note = note.note - 1
                    bar.append(Note(type = 'note',note = note, length = random.randint(1,4)))
                else:
                    leap = leapRange(bar)
                    bar.append(Note(type='note',note=note.note+leap,length=random.randint(1,4)))
                subdivisions -= bar[len(bar)-1].length
                if subdivisions < 0:
                    bar[len(bar)-1].length += subdivisions
        
        self.Bar=bar

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
            measure.append(Note(length=random.randint(1,4),note=random.randint(0,15),type="note"))
            subdivisions -= measure[count].length
            if subdivisions < 0:
                measure[count].length = measure[count].length + subdivisions
            count +=1

        condition = False
        note = self.Bar[len(self.Bar)-1]
        if not note in c:
            self.Bar[len(self.Bar)-1] = c[random.randint(0,2)]%8

            
        self.Bar = measure
        self._motion()

    
    def _shape(self):
        '''finds the musical shape of the measure'''
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
        '''finds the percentagerelationship of conjunct motion in a measure'''
        notes = []
        conjunct = 0
        disjunct = 0
        for each in self.Bar:
            notes.append(each.note)
        
        for i in range(len(notes)-1):
            if notes[i] - notes[i+1] < 2 and notes[i] - notes[i+1] > -2:
                conjunct += 1/(len(notes)-1)
            else:
                disjunct += 1/(len(notes)-1)
        self.Motion = conjunct

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
    '''Inherits from Subdivision'''
    def __init__(self,**kwargs):
        Subdivision.__init__(self,**kwargs)
        self.type = kwargs['type']
        if self.type == "note":
            self.note = kwargs["note"]
            self.velocity = 80


####################################################
#           Trained Algorithm Generator
####################################################

def sythesizedNewComposition(**kwargs):
    '''Synthesized a new individual based on the features passed in'''
    gFeatures = kwargs[0]
    pFeatures = kwargs[1]
    shape = pFeatures[0]
    motionRatio = pFeatures[1]
    repitition = kwargs['repitition']
    composition = Genome(length = kwargs['length'])

    for phrase in composition.Phrase:
        for measure in phrase.Measure:
            subdivisions = 0
            bar = []
            for each in measure.Bar:
                subdivisions += each.length
            
            while subdivisions > 0:
                if len(bar) >= 1:
                    if random.random() > motionRatio:
                        if not bar[len(bar)-1].note in [3,4,7,8]:
                            leap = random.randint(2,7)
                            if random.random() > 0.5:
                                leap = 0-leap
                            note = Note(length=random.randint(1,4),note = bar[len(bar)-1].note + leap, type="note")
                    else:
                        step = random.randint(-1,1)
                        note = Note(length=random.randint(1,4),note = bar[len(bar)-1].note + step, type="note")
                    if subdivisions - note.length > 0:
                        subdivisions -= note.length
                    else:
                        note.length = subdivisions
                        subdivisions = 0
                    bar.append(note)
                else:
                    note = (Note(length=random.randint(1,4),note=random.randint(0,15),type="note"))
                    if subdivisions - note.length > 0:
                            subdivisions -= note.length
                    else:
                        note.length = subdivisions
                        subdivisions = 0
                    bar.append(note)
    return composition
            
def leapRange(bar: list):
    if not len(bar) == 0:
        lastnote = bar[len(bar)-1].note

        if lastnote < 2:
            leap = random.randint(2,7)
            return leap
        elif lastnote < 7:
            low = lastnote - 2
            leap = random.randint(2,7)
            if random.random()>0.5:
                if low == 0:
                    leap = -2
                else:
                    leap = random.randint(-2-low,-2)
            return leap
        elif lastnote < 9:
            leap = random.randint(2,7)
            if random.random() > 0.5:
                leap = 0-leap
            return leap
        elif lastnote > 13:
            leap = random.randint(-7,-2)
            return leap
        else:
            up = 15-lastnote
            if random.random()>0.5:
                leap = random.randint(2,up)
            else:
                leap = random.randint(-7,-2)
            return leap
            