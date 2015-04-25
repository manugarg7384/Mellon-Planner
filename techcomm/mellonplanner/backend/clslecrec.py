'''
Created on Mar 22, 2015

@author: Bill
'''

dDict = {'U': -1, 'M':0, 'T':1, 'W':2, 'R':3, 'F':4, 'S': 5}

def getDay(s):
    return dDict[s]

class Rec:
    def __init__(self, rDays, rTimeStart, rTimeEnd):
        self.rDays = [dDict[c] for c in rDays]
        self.timeInt = (rTimeStart, rTimeEnd)

    def tsplit(self):
        return {d: self.timeInt for d in self.rDays}

class Lec:
    def __init__(self, lDays, lTimeStart, lTimeEnd):
        self.lDays = [dDict[c] for c in lDays]
        self.timeInt = (lTimeStart, lTimeEnd)
        self.recs = {}

    def tsplit(self):
        if len(self.recs) == 0:
            return {'' : {d: [self.timeInt] for d in self.lDays}}
        else:
            options = {}
            #base = {d: [self.timeInt] for d in self.lDays}
            for (rn, rec) in self.recs.items():
                b2 = {d: [self.timeInt] for d in self.lDays}

                for d in rec.rDays:
                    if d in b2:
                        b2[d].append(rec.timeInt)
                    else:
                        b2[d] = [rec.timeInt]
                options['.%s' % rn.replace(' ', '_')] = b2
            return options

class Cls:
    def __init__(self, cId, units=9):
        self.cId = cId
        self.lecs = {}

        self.units = units

    def tsplit(self):
        return {'%s.%s%s' % (self.cId, ln.replace(' ', '_'), rns) : cal for (ln, lec) in self.lecs.items() for (rns, cal) in lec.tsplit().items()}
