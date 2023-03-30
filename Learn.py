from Genome import *

class FitnessModel:
    '''Used as a formula by which top synthesize new trained genomes'''
    def __init__(self,length: int):
        self.genomeRepTotal = 0
        self.genomeMtnTotal = 0
        self.phraseMtnTotal = 0
        self.phraseRepTotal = 0
        self.measureMtnTotal = 0

        self.gRepAvg = 0
        self.gMtnAvg = 0
        self.pRepAvg = 0
        self.pMtnAvg = 0
        self.mMtnAvg = 0

        self.contextRepPhrase = [0 for each in range(length)]
        self.contextMtnPhrase = [0 for each in range(length)]

        self.init = 0
        self.Model = []
    
    def generateIndividual(self, **kwargs):
        length = kwargs['length']
        individual = Genome(length=length)
        start = False
        for phrase in individual.Phrase:
            count = 0
            for measure in phrase.Measure:
                if not start:
                    measuremotion =kwargs['mtnContext'][count]
                    subdivisions = 0
                    bar = []
                    for each in measure.Bar:
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
                    measuremotion =kwargs['mtnContext'][count]
                    subdivisions = 0
                    bar = []
                    for each in measure.Bar:
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
                measure.Bar=bar
            
        return individual

    def analyseIndividual(self,individual: Genome):
        pass
    
    def analyseGenome(self,individual: Genome):
            self.genomeRepTotal += individual.Repitition
            self.genomeMtnTotal += individual.AvgMotion

            
            for each in range(individual.length):
                self.contextMtnPhrase[each] += individual.Phrase[each].MotionAvg
                self.contextMtnPhrase[each] /= individual.length
                self.contextRepPhrase[each] += individual.Phrase[each].Repitition
                self.contextRepPhrase[each] /= individual.length
                
            
        
    def analysePhrase(self, phrase: Phrase):
        self.phraseRepTotal += phrase.Repitition
        self.phraseMtnTotal += phrase.MotionAvg

    
    def analyseMeasure(self,measure: Measure):
        self.measureMtnTotal += measure.Motion
    
    def avgResults(self,population: list[Genome]):
        self.gRepAvg = self.genomeRepTotal/(len(population)+self.init)
        self.gMtnAvg = self.genomeMtnTotal/(len(population)+self.init)
        self.pRepAvg = self.phraseRepTotal/(population[0].length*len(population)+self.init)
        self.pMtnAvg = self.phraseMtnTotal/(population[0].length*len(population)+self.init)
        self.mMtnAvg = self.measureMtnTotal/(len(population[0].Phrase[0].Measure)*len(population)+self.init)
        if self.init == 0:
            self.init = 1

        results = {0:population[0].length,
                   1:self.gRepAvg,
                   2:self.gMtnAvg,
                   3:self.pRepAvg,
                   4:self.pMtnAvg,
                   5:self.contextRepPhrase,
                   6:self.contextMtnPhrase,
                   7:self.mMtnAvg}
        
        '''self.generateIndividual(length=2,
                   genomeRep=self.gRepAvg,genomeMtn=self.gMtnAvg,
                   phraseRep=self.pRepAvg,
                   phraseMtn=self.pMtnAvg,
                   repContext=self.contextRepPhrase,
                   mtnContext=self.contextMtnPhrase,
                   measureAvg=self.mMtnAvg)'''
        return results

    def analysePopulation(self,population):#add totals together, take average, compare prediction to next round of fittest individuals and recalculate
        
        for each in population:
            self.analyseGenome(each)
            for phrase in each.Phrase:
                self.analysePhrase(phrase)
                for measure in phrase.Measure:
                    self.analyseMeasure(measure)
        
        self.Model = self.avgResults(population)
        return(self.Model)

    def predictFitness():
        pass

'''def leapRange(bar: list):
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
            return leap'''


    

        
        



        

