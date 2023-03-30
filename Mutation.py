from Genome import *
import random
import copy
from Learn import *

Motif = []

def crossover(population):
    sorted = sortPopulation(copy.copy(population))
    fittest = len(sorted)//3
    pool = []
    for each in sorted:
        if each.Fitness == 1:
            pool.append(each)
    
    if len(pool) < 2:
        print('not enough parents')
        return

    for individual in range(fittest,len(sorted)-1):
        parentA = random.randint(0,len(pool)-1)
        parentB = random.randint(0,len(pool)-1)


        length = pool[parentA].length
        measures = pool[parentA].dimensions[0]
        while True:
            if parentA == parentB:
                parentB = random.randint(0,len(pool)-1)
            else:
                break
        
        parentA = pool[parentA]
        parentB = pool[parentB]


        child = Genome(length = length)
        population = [each for each in range(len(sorted))]

        for i in range(0,length*measures):
            p = i // measures
            m = i % measures
            child.Phrase[p].Measure[m] = copy.copy(parentA.Phrase[p].Measure[m])

        for i in range(random.randint(0,length*measures),length*measures):
            p = i // measures
            m = i % measures
            child.Phrase[p].Measure[m] = copy.copy(parentB.Phrase[p].Measure[m])
            if random.random() < 0.03:
                mutation(child.Phrase[p].Measure[m])
            
            child.motion()
            child._shape()
        population[individual] = copy.copy(child)
    
    for individual in range(fittest,len(population)):
        population[individual] = copy.copy(sorted[individual])
    
    shuffle(population)
    return(True)
            

def mutation(self: Measure):
    if len(Motif) > 1:
        self = Motif[random.randint(0,len(Motif)-1)]

    else:
        for each in self.Bar:
            if each.type == "note":
                each.note = random.randint(0,15)
    self._motion()

def shuffle(population):
    copies = []
    for each in population:
        copies.append(copy.copy(each))
    
    remaining = [each for each in range(len(copies))]
    index = random.randint(0,len(remaining)-1)
    population[index] = copies[index]

    remaining.pop(index)
    copies.pop(index)

def motifAnalysis():
    for each in Motif:
        tritoneWarning = False
        pCadance = False
        cadance = False
        notes = []
        for note in each.Bar:
            notes.append(note.note%8)
        if 3 in notes:
            if 6 in notes:
                tritoneWarning = True
        
        if set([4,0]).issubset(notes):
            if notes[len(notes)-1] in [3,4,0]:
                pCadance = True
        elif notes[len(notes)-1] in [3,4,6]:
            cadance = True
        
        if tritoneWarning:
            Motif.remove(each)
        
        if cadance:
            each.score = 1


def sortPopulation(population):
    sorted = []
    for each in population:
        sorted.append(each)
        for motif in each.Motif:
            if hasattr(motif,'Bar'):
                Motif.append(motif)
    motifAnalysis()
    
    arrange = True
    while arrange:
        changes = False
        for i in range(len(sorted)-1):
            if sorted[i].Fitness < sorted[i+1].Fitness:
                change = sorted[i]
                sorted[i] = sorted[i+1]
                sorted[i+1] = change
                changes = True
            i +=1
        if changes == False:
            arrange = False
    return sorted