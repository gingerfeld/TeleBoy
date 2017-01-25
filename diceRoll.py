import random
import typeCheck

class diceRoll:

    def __init__(self, _num, _sides):
        self.number = _num
        self.sides = _sides

    def roll(self):
        total = []
        random.seed()
        if self.sides > 100000 or self.number > 100000:
            return False
        if self.number >= 1 and self.sides >= 1:
            for i in range(self.number):
                total.append(random.randint(1, int(self.sides)))
            return total
        return False

    def analyzedRoll(self):
        rawRoll = self.roll()
        if(rawRoll):
            if(self.number == 1):
                if(rawRoll[0] == 8):
                    lilBit = 'n'
                else:
                    lilBit = ''
                analysis = 'You rolled a%s *%d*'%(lilBit, rawRoll[0])
            else:
                analysis = 'You rolled a ' + ', '.join(str(x) for x in rawRoll[:-1]) + ' and %d'%(rawRoll[-1]) + ', resulting in: *%d*'%(sum(rawRoll))
            return analysis
        return False
def roll(rollInput):
    rollParameters = diceRoll(1,1)
    
    if('d' in rollInput):
        split = rollInput.rpartition('d')
        if(typeCheck.isint(split[0]) and typeCheck.isint(split[2])):
            rollParameters = diceRoll(int(split[0]),int(split[2]))
        else:
            return False
    elif(typeCheck.isint(rollInput)):
        rollParameters = diceRoll(1,int(rollInput))
    else:
        return False

    return rollParameters
def flip():
    return ['Heads','Tails'][random.randint(0,1)]
