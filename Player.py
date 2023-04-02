from Genome import *
import Mutation, Listen, Learn, Export
from functools import partial
import tkinter
from tkinter import *

POPULATIONSIZE = 5
'''No of individuals for training'''

LENGTH = 2
'''Phrases per genome'''


trainingcycles = 5
individual = 0
parentPool = 0
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

fitnessModel = Learn.FitnessModel(population[0].length)
fitnessModel.analyseIndividual(population[0])


############## Visual Interface #################
def __main__():
    global root
    root = Tk()
    root.title('eMC Player')
    root.configure(bg='#ef6f6c',width=400,height=200,highlightthickness=0, highlightcolor='#ef6f6c')

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
        '''Assigns a pass to the fitness score'''
        global individual
        population[individual].Fitness = 1
        individual += 1
        global parentPool
        parentPool += 1
        
        if individual == len(population):
            if Mutation.crossover(population):
                print('Success')
                fitnessModel.analysePopulation(population)
                global trainingcycles
                trainingcycles -= 1
                if trainingcycles == 0:
                    testAlgorithm()
                    return                

            individual = 0
            parentPool = 0
        indLabel.configure(text='Individual: '+str(individual+1))
        parentsLable.configure(text='Parents: '+str(parentPool))
        return
    
    def chanceIndividual():
        '''Assigns a possible pass to the fitness score'''
        global individual
        if random.random() > 0.5:
            population[individual].Fitness = 1 
            global parentPool
            parentPool += 1
        else:
            population[individual].Fitness = 0 
        
        individual += 1
        
        
        if individual == len(population):
            if Mutation.crossover(population):
                print('Success')
                fitnessModel.analysePopulation(population)
                global trainingcycles
                trainingcycles -= 1
                if trainingcycles == 0:
                    testAlgorithm()
                    return                

            individual = 0
            parentPool = 0
        indLabel.configure(text='Individual: '+str(individual+1))
        parentsLable.configure(text='Parents: '+str(parentPool))
        return
    
    def failIndividual():
        '''does not add indiviual to parent pool'''
        global individual
        population[individual].Fitness = 0
        individual += 1
        if individual == len(population):
            if Mutation.crossover(population):
                print('Success')
                fitnessModel.analysePopulation(population)
                global trainingcycles
                trainingcycles -= 1
                if trainingcycles == 0:
                    testAlgorithm()
                    return 

            individual = 0
            global parentPool
            parentPool = 0
        indLabel.configure(text='Individual: '+str(individual+1))
        parentsLable.configure(text='Parents: '+str(parentPool))
        return
    frame = tkinter.Frame(root)
    frame.configure(width=Tk.geometry(root)[0],bg='#ef6f6c')
    frame.pack()

    play = Button(frame, text='Play',command=lambda:playSequence())
    play.configure(bg='#ef6f6c',highlightthickness=0, bd=0)
    play.grid(row=0,column=0,sticky='EW')

    save = Button(frame, text='Save',command=lambda:Save())
    save.configure(bg='#ef6f6c',highlightthickness=0, bd=0)
    save.grid(row=0,column=1)

    good = Button(frame,text='Pass',command=lambda:passIndividual())
    good.configure(bg='#ef6f6c',highlightthickness=0, bd=0)
    good.grid(column=0,row=1,sticky='EW')

    neutral = Button(frame,text='Indifferent',command=lambda:chanceIndividual())
    neutral.configure(bg='#ef6f6c',highlightthickness=0, bd=0)
    neutral.grid(column=1,row=1,sticky='EW')

    bad = Button(frame,text='Fail',command=lambda:failIndividual())
    bad.configure(bg='#ef6f6c',highlightthickness=0, bd=0)
    bad.grid(column=2,row=1,sticky='EW')

    indLabel = Label(frame,text='Individual: '+str(individual+1))
    indLabel.configure(bg='#ef6f6c')
    indLabel.grid(column=3,row=0,sticky='EW')

    parentsLable = Label(frame,text='Parents: '+ str(parentPool))
    parentsLable.configure(bg='#ef6f6c')
    parentsLable.grid(column=3,row=1,sticky='EW')

    ###################   Tempo Slider   #################
    tmp = Variable
    tempoSlider = Scale(frame,digits=3,from_=180,to=40, variable=tmp,command=lambda x:Listen.setTempo(int(x)))
    tempoSlider.configure(bg='#ef6f6c')
    tempoSlider.set(120)
    tempoSlider.grid(row=0,column=4,rowspan=2)
    

    #################### Draw the keyboard ###############
    canvas = Canvas(root)
    canvas.configure(width=180,height=50, bg = '#ef6f6c')
    class Key:
        def __init__(self, canvas, id):
            self.canvas = canvas
            self.type = id

    

    wKeys = {i: Key(canvas,1) for i in range(0,15)}
    bKeys = {i: Key(canvas,0)for i in range(10)}

    for each in wKeys:
        wKeys[each].canvas.create_rectangle(each*10+15,0,each*10+25,30,fill='#ffffff')
    
    count = 0
    for each in bKeys:
        if each in [0,2,5,7]:
            count += 1
        bKeys[each].canvas.create_rectangle((count*10)+(each*10)+12,0,(count*10)+(each*10)+18,20,fill = '#222222')

        
    canvas.pack()
    
    
    root.mainloop()

def testAlgorithm():
    results = (fitnessModel.analysePopulation(population))
    print(results)
    synthesized = fitnessModel.generateIndividual(length=LENGTH,genomeRep=results[1],genomeMtn=results[2],phraseRep=results[3],phraseMtn=results[4],repContext=results[5],mtnContext=results[6],measureMtn=results[7])
    control = Genome(length=LENGTH)
    for phrase in control.Phrase:
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

    global root
    root.destroy()

    def SaveOutcome():
        Export.as_midi(synthesized,harmony=True,title='synthesized')
        Export.as_midi(control,harmony=True,title='control')

    testScreen = Tk()
    option1 = Button(testScreen,text='Option 1',command=lambda:Listen.playSequence(synthesized))
    option2 = Button(testScreen,text = 'Option 2',command=lambda:Listen.playSequence(control))
    save = Button(testScreen,text='Save',command=lambda:SaveOutcome())
    option1.pack()
    option2.pack()
    save.pack()




if __name__ == '__main__':
    individual = 0
    __main__()