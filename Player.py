from Genome import *
import Listen

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
        phrase._shape()
    genome.repitition()

while True:
    choice = int(input("Choose number to listen to between 1 and "+str(POPULATIONSIZE)+" ")) -1
    Listen.playSequence(population[choice])