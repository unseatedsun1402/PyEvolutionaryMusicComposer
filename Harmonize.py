from Genome import *
chordDict = {1:[0,4,7],
             2:[2,5,9],
             3:[4,7,11],
             4:[5,8,12],
             5:[7,11,14],
             6:[4,7,11],
             7:[2,5,11]}

def harmonize(self):
    notes = []
    for note in self.Bar:
        notes.append(note)
    
    appropriate = []
    for i in range(len(chordDict)):
        score = 0
        values = chordDict.values()
        for each in notes:
            for chord in values:
                if each.note in chord:
                    score += 1/len(chordDict)
        appropriate.append(score)
    
    greatest = 0
    for i in range(len(appropriate)-1):
        if appropriate[i] < appropriate[i+1]:
            greatest = i

    return chordDict[greatest+1]
    


