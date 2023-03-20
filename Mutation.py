from Genome import *
import random
import copy

Motif = []

def crossover(population):
    sorted = sortPopulation(population)
    fittest = len(sorted)//3

    for individual in range(0,fittest):
        parentA = random.randint(fittest,len(sorted)-1)
        parentB = random.randint(fittest,len(sorted)-1)
        while True:
            if parentB == parentA:
                parentB = random.randint(fittest,len(sorted)-1)
            else:
                break
        

        length = population[parentA].length
        measures = population[parentA].dimensions[0]
        
        parentA = sorted[parentA][0]
        parentB = sorted[parentB][0]
        child = Genome(length = length)

        for i in range(0,length*measures):
            if i > measures:
                p = i // measures
                m = i % measures
            else:
                p = 0
                m = i
            child.Phrase[p].Measure[m] = copy.copy(parentA.Phrase[p].Measure[m])

        for i in range(random.randint(0,length*measures),length*measures):
            if i > measures:
                p = i // measures
                m = i % measures
            else:
                p = 0
                m = i
            child.Phrase[p].Measure[m] = copy.copy(parentB.Phrase[p].Measure[m])
            if random.random() < 0.03:
                child.Phrase[p].Measure[m].mutation()
            
            child.motion()
            child._shape()
        population[individual] = copy.copy(child)
    
    for individual in range(fittest,len(population)):
        population[individual] = copy.copy(sorted[individual][0])
    
    return(True)
            

def mutation(self):
    self.Bar = random.randint(0,len(Motif))
    for each in self.Bar:
        if each.type == "note":
            each.note = random.randint(0,15)

        


def sortPopulation(population):
    sorted = []
    for each in population:
        sorted.append((each,each.Fitness))
        for motif in each.Motif:
            Motif.append(motif)
    
    arrange = True
    while arrange:
        changes = False
        for i in range(len(sorted)-1):
            if sorted[i][1] < sorted[i+1][1]:
                change = sorted[i]
                sorted[i+1] = change
                changes = True
            i +=1
        if changes == False:
            arrange = False
    return sorted