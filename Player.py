from Genome import *
import Mutation
import Listen
import Export
from functools import partial
import tkinter
from tkinter import *

POPULATIONSIZE = 5
LENGTH = 2
individual = 0

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

def __main__():
    root = Tk()
    root.title('eMC Player')

    def playSequence():
        global individual
        Listen.playSequence(population[individual])
        if individual == len(population):
            Mutation.crossover(population)
            individual = 0
        return

    def Save():
        Export.as_midi(population[individual],harmony = True)
        return

    def passIndividual():
        global individual
        population[individual].Fitness = 1
        individual += 1

        if individual == len(population):
            if Mutation.crossover(population):
                print('Success')
            else:
                print('Not enough parents')
            individual = 0
        indLabel.configure(text=str(individual+1))
        return
    
    def failIndividual():
        global individual
        population[individual].Fitness = 0
        individual += 1

        if individual == len(population):
            if Mutation.crossover(population):
                print('Success')
            else:
                print('Not enough parents')
            individual = 0
        indLabel.configure(text=str(individual+1))
        return
    
    play = Button(root, text='Play',command=lambda:playSequence())
    play.grid(row=0,column=0)

    save = Button(root, text='Save',command=lambda:Save())
    save.grid(row=0,column=1)

    good = Button(root,text='Pass',command=lambda:passIndividual())
    good.grid(column=0,row=1)

    bad = Button(root,text='Fail',command=lambda:failIndividual())
    bad.grid(column=1,row=1)

    indLabel = Label(root,text=str(individual+1))
    indLabel.grid(column=2,row=0)
    root.mainloop()


if __name__ == '__main__':
    individual = 0
    __main__()