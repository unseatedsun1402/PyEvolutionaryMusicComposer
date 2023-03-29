import Genome

class FitnessModel:
    '''Used as a formula by which top synthesize new trained genomes'''
    def __init__(self,dimensions: tuple):
        self.Phrases = ['' for i in range(dimensions[0])]
        self.Measures = ['' for i in range(dimensions[1])]
        self.init = False
        self.Model = []


    def analyseIndividual(self,individual: Genome):
        if self.init == False:
            for i in range(len(individual.Phrase)):
                each = individual.Phrase[i]
                self.Phrases[i]([each.shape,each.motionRatio,each.repitition])
                for j in range(len(each.Measure)):
                    measure = each.Measure[j] 
                    self.Measures[j]=[measure.shape, measure.Motion]
    
    def analyseGenome(self,individual: Genome.Genome):
            self.genomeRepTotal += individual.Repitition
            self.genomeMtnTotal += individual.Motion
        
    def analysePhrase(self,phrase: Genome.Phrase):
        self.phraseRepTotal += phrase.repitition
        self.phraseMtnTotal += phrase.Motion
    
    def analyseMeasure(self,measure: Genome.Measure):
        self.measureMtnTotal += measure.Motion
    
    def avgResults(self,population: list[Genome.Genome]):
        gRepAvg = self.genomeRepTotal/len(population)
        gMtnAvg = self.genomeMtnTotal/len(population)
        pRepAvg = self.phraseRepTotal/len(population[0].length)*len(population)
        pMtnAvg = self.phraseMtnTotal/len(population[0].length)*len(population)
        mMtnAvg = self.measureMtnTotal/len(population[0].Phrase[0].Measure)*len(population)

        return [gRepAvg,gMtnAvg,pRepAvg,pMtnAvg,mMtnAvg]

    def analysePopulation(self,population):#add totals together, take average, compare prediction to next round of fittest individuals and recalculate
        self.genomeRepTotal = 0
        self.genomeMtnTotal = 0

        self.phraseRepTotal = 0
        self.phraseMtnTotal = 0

        self.measureMtnTotal = 0
        
        for each in population:
            self.analyseGenome(each)
            for phrase in each.Phrase:
                self.analysePhrase(phrase)
                for measure in phrase.Measure:
                    self.analyseMeasure(measure)
        
        self.avgResults(population)
        
        



        

