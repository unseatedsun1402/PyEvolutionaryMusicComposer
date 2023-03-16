from Genome import *
import Listen

POPULATIONSIZE = 5
LENGTH = 2

population = [Genome(length=LENGTH) for each in range(POPULATIONSIZE)]

for genome in population:
    for phrase in genome.Phrase:
        start = True
        for measure in phrase.Measure:
            if start:
                measure.generateMeasure(start = True)
                start = False
            else:
                measure.generateMeasure(start = False)

Listen.playSequence(population[0])