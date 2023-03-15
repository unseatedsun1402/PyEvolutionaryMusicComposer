import random
tonicChord = {'one': [0,5,7],
              'two':[2,5,9],
              'three':[4,7,11],
              'four':[5,8,0],
              'five':[7,11,2],
              'six':[8,0,4],
              'dim':[11,2,5]}
class Genome:
    def __init__(self):
        pass

    def _shape(self):
        pass

    def _reptition(self):
        pass

class Phrase:
    def __init__(self):
        pass

    def _shape(self):
        pass

class Measure:
    def __init__(self,**kwargs):
        self.subdiv = kwargs.items()["subdiv"]
        self.div = kwargs.items()["div"]
        self.key = kwargs.items()['key']
        self.__divisions = [each for each in self.subdiv]

    def generateMeasure(self, **kwargs):
        if kwargs.items()['start']:
            for each in self.__divisions:
                each = random.randint(0,15)
            
            #contains root function
            cond = False
            for each in self.__division:
                if not (each%12) in tonicChord['one']:
                    continue
                else:
                    cond = True
            
            if not cond:
                match random.randint(0,2):
                    case 0:
                        note = 0
                    case 1:
                        note = 5
                    case 2:
                        note = 7
                    case _:
                        note = 0
                each[0] = note

        else:
            for each in self.__divisions:
                each = random.randint(0,15)
                    

    
    def _shape(self):
        pass

    def __getattribute__(self, __name: str) -> Any:
        return self.__name