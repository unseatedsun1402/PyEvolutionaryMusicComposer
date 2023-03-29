import Genome

class FitnessModel:
    '''Used as a formula by which top synthesize new trained genomes'''
    def __init__(self,dimensions: tuple):
        self.Phrases = ['' for i in range(dimensions[0])]
        self.Measures = ['' for i in range(dimensions[1])]
        self.init = False


    def analyseIndividual(self,individual: Genome):
        if self.init == False:
            for i in range(len(individual.Phrase)):
                each = individual.Phrase[i]
                self.Phrases[i]([each.shape,each.motionRatio,each.repitition])
                for j in range(len(each.Measure)):
                    measure = each.Measure[j] 
                    self.Measures[j]=[measure.shape, measure.Motion]
        

