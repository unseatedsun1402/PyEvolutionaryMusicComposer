from Genome import *
import Listen

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
        individual = Genome(kwargs['length'])
        for phrase in individual.Phrase:
            
            count = 0
            for measure in phrase.Measure:
                measuremotion =kwargs['mtnContext'][count]
                subdivisions = 0
                for each in measure.Bar:
                    subdivisions += each.length
                
                while subdivisions > 0:
                    if len(measure.Bar) > 0:
                        note = measure.Bar[len(measure.Bar)-1]
                    motion = random.random()
                    if motion < measuremotion:
                        steps = random.Random()
                        if steps < 0.5:
                            note = note + 1
                        else:
                            note = note - 1
                        measure.Bar.append(Note(type = 'note',note = note, length = random.randint(1,4)))
                    else:
                        leap = leapRange(measure)
                        measure.Bar.append(Note(type='note',note=note+leap,length=random.randint(1,4)))
                    subdivisions -= measure.Bar[len(measure.Bar)-1]
                    if subdivisions < 0:
                        measure.Bar[len(measure.Bar)-1].length += subdivisions
    
        Listen.playSequence(individual)


    def analyseIndividual(self,individual: Genome):
        '''if self.init == False:
            for i in range(len(individual.Phrase)):
                each = individual.Phrase[i]
                self.Phrases[i]([each.shape,each.motionRatio,each.repitition])
                for j in range(len(each.Measure)):
                    measure = each.Measure[j] 
                    self.Measures[j]=[measure.shape, measure.Motion]'''
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

        results = {'length':population[0].length,
                   'genomeRep':self.gRepAvg,'genomeMtn':self.gMtnAvg,
                   'phraseRep':self.pRepAvg,
                   'phraseMtn':self.pMtnAvg,
                   'repContext':self.contextRepPhrase,
                   'mtnContext':self.contextMtnPhrase,
                   'measureAvg':self.mMtnAvg}
        
        self.generateIndividual(results)
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

def leapRange(measure: Measure):
    if not len(measure.Bar) == 0:
        lastnote = measure.Bar[len(measure.Bar)-1].note

        if lastnote < 2:
            leap = random.randint(2,7)
            return leap
        elif lastnote < 7:
            low = 7 - lastnote
            if random.random()>0.5:
                leap = random.randint(-2,-low)
            else:
                leap = random.randint(2,7)
            return leap
        elif lastnote < 9:
            leap = random.randint(2,7)
            if random.random() > 0.5:
                leap = 0-leap
            return leap
        elif lastnote > 13:
            leap = random.randint(-2,-7)
            return leap
        else:
            up = 15-lastnote
            if random.random()>0.5:
                leap = random.randint(2,up)
            else:
                leap = random.randint(-2,-7)
            return leap


    

        
        



        

