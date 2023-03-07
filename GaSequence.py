import mido
import random

def __generate_random_notes(_length: int,_ticks: int):
    """Generates a random series of notes and returns them as a mido message sequence"""
    sequence = []
    msg = mido.Message
    rVelocity = int
    rNote = int
    genome = _length
    oldNote = int
    while len(sequence) < _length:
        if random.random() > 0.1:
            rVelocity = random.randint(50,100)
            rNote = random.randint(45,71)
            octave = rNote // 12
            try:
                if oldNote // 12 < (rNote // 12):
                    rNote -= 12
                elif oldNote // 12 > (rNote // 12):
                    rNote += 12
            except:
                pass
        else:
            rVelocity = (0)
            rNote = (0)
        
        length = random.randint(2,4)
        length *= 2
        
        time = length*_ticks
        if time >= ((genome*_ticks)-time):
            time = int(genome*_ticks)
        
        msg = mido.Message('note_on',note = rNote,velocity = rVelocity, time = 0)
        sequence.append(msg)
        
        msg = mido.Message('note_off',note=rNote,velocity = rVelocity, time = time)
        sequence.append(msg)
        
        genome -= int(time/_ticks)
        for each in range(int(time/_ticks)-2):
            sequence.append('')
        oldNote = rNote
    return sequence