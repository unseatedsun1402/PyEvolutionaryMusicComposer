from Genome import *
import Mutation
import Listen
import Export

POPULATIONSIZE = 5
LENGTH = 1

population = [Genome(length=LENGTH) for each in range(POPULATIONSIZE)]


#generate the population of genomes 
for genome in population:
    for phrase in genome.Phrase:
        start = True
        for measure in phrase.Measure:
            if start:
                measure.generateMeasure(start = True)
                start = False
            else:
                measure.generateMeasure(start = False)
            measure._shape()
        phrase.Measure[len(phrase.Measure)-1].Closing()

        phrase._shape()
    genome.repitition()

while True:
    for each in population:
        Export.as_midi(each,harmony=True)
        Listen.playSequence(each)
        
        choice = int(input("rate melody between 1 and 5 "))
        if choice > 5 or choice < 0:
            print("incorrect range")
        else:
            each.Fitness = choice

    if Mutation.crossover(population):
        print("Success!")
