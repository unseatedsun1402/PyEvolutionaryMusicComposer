from Genome import *
chordDict = {1:[0,2,4],
             2:[1,3,5],
             3:[2,4,6],
             4:[3,5,7],
             5:[4,6,8],
             6:[5,7,9],
             7:[6,8,10]}

def harmonize(self):
    notes = []
    for note in self.Bar:
        notes.append(note.note%8)
    
    appropriate = []
    for i in range(len(chordDict)):
        score = 0
        values = chordDict.values()
        values = [each for each in values]
        for each in values:
            for note in each:
                note = note%12
        for each in notes:
            if each in values[i]:
                score += 1/len(chordDict)
        appropriate.append(score)
    
    greatest = 0
    for i in range(len(appropriate)-1):
        if appropriate[i] < appropriate[i+1]:
            greatest = i

    return chordDict[greatest+1]
    


