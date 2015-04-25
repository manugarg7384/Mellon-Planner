'''
Created on Oct 23, 2014

@author: Bill
'''

from Tkinter import *
import random, math
from graphUtil import *
from sparse import getFullSchedule

import time

def randomCVal():
    return int((255+ random.random()*256)/2)

def colorStr(r, g, b):
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

def randomColor():
    r = randomCVal()
    g = randomCVal()
    b = randomCVal()
    return colorStr(r,g,b)

def dot(v1, v2):
    x1,y1 = v1
    x2,y2 = v2
    return x1*x2 + y1*y2

def mkColors(items):
    n = len(items)

    colors = {}
    rv, gv, bv = (1.0,0.0), (-0.5, math.sqrt(3.0)/2.0), (-0.5, -math.sqrt(3.0)/2.0)
    dt = 2 * math.pi / n
    for i in range(n):
        v  = (math.cos(dt * i), math.sin(dt * i))
        rp = (255 + 2*int((dot(v, rv) + 1)/2.0 * 255))/3
        gp = (255 + 2*int((dot(v, gv) + 1)/2.0 * 255))/3
        bp = (255 + 2*int((dot(v, bv) + 1)/2.0 * 255))/3
        #print(v, rp, gp, bp)
        colors[items[i]] = colorStr(rp, gp, bp)
    #random.shuffle(colors)
    return colors




def intersects(t1,t2):
    for k in t1:
        if k in t2:
            for (x1,y1) in t1[k]:
                for (x2,y2) in t2[k]:
                    if x1 < y2 and y1 > x2:
                        return True
    return False

def flattenClasses(clss):
    #print('!%s!' % clss[0].tsplit())
    return [(fullId, t, cl) for cl in clss for (fullId,t) in cl.tsplit().items()]

def minStartTime(t):
    return min(v[0] for (_,v) in t.items())

def getScheds(clss):
    tsg = flattenClasses(clss)

    N = len(tsg)
    adj1 = [[j for j in range(N) if (i==j or tsg[i][2].cId == tsg[j][2].cId or intersects(tsg[i][1],tsg[j][1]))] for i in range(N)]
    sccs = stronglyConnectedComponents(adj1)

    maxIndepSets = [[]]

    for scc in sccs:
        idxTable = {scc[i]:i for i in range(len(scc))}
        idxMap = lambda j: idxTable[j]
        sccAdj = [map(idxMap, adj1[j]) for j in scc]
        compAdj = adjComplement(sccAdj)
        componentIndepSets = maximalCliques(compAdj)
        restoredIndepSets = [[scc[i] for i in row] for row in componentIndepSets]
        newMaxIndepSets = []
        for mis in restoredIndepSets:
            for prefix in maxIndepSets:
                newMaxIndepSets.append(prefix + mis)
        maxIndepSets = newMaxIndepSets


    scheds = [[tsg[i] for i in s] for s in maxIndepSets]
    units = [sum(t[2].units for t in s) for s in scheds]
    units_scheds = sorted(zip(units,scheds),key=lambda t: t[0])
    scheds = [t[1] for t in units_scheds]
    units = [t[0] for t in units_scheds]
    return scheds,units

def getAllSchedules(classNums, sem=0, minUnits=0, maxUnits=100, pref=None):
    sem = int(sem)
    minUnits = int(minUnits)
    maxUnits = int(maxUnits)

    classNums = map(lambda s: s.replace('-', ''), classNums)
    fullSched = getFullSchedule(sem)
    allClasses = [fullSched[cns] for cns in classNums if cns in fullSched]

    scheds, units = getScheds(allClasses)

    # FILTER MIN
    scheds_units = zip(scheds, units)
    scheds_units = filter(lambda p: p[1] >= minUnits, scheds_units)
    scheds = [s for (s,_) in scheds_units]
    units = [u for (_, u) in scheds_units]

    flatScheds = []
    for i in range(len(scheds)):
        thisSched = []
        for (name, tdict, _) in scheds[i]:
            newName = name.replace('.', ' ').replace('_', ' ')
            times = [(d, tstart, tend) for d in tdict for (tstart, tend) in tdict[d]]
            thisSched.append((newName, times))
        flatScheds.append((units[i], thisSched))
    return flatScheds


if __name__ == '__main__':


    #print(getAllSchedules(['15213', '15440'], sem=0))

    #exit(0)

    fullSched = getFullSchedule(0)
    findClass = lambda cns: fullSched[cns] if cns in fullSched else None

    #classNums = fullSched.keys()
    #random.shuffle(classNums)
    #classNums = classNums[:35]

    #classNums = ['85340', '85442', '36309', '09217', '09221']
    #classNums = ['09221']

    #classNums = ['15122','21127','15150']

    classNums = ['15122', '21325']

    allClasses = map(findClass, classNums)

    ACTIVE_CLASS_LIST = filter(lambda v: v is not None, allClasses)

    scheds,units = getScheds(ACTIVE_CLASS_LIST)

    classes = ACTIVE_CLASS_LIST
    COLORS = mkColors(classNums)

    ###############################################################################

    WIDTH = 1000
    HEIGHT = 800

    START_HR = 8
    NUM_HRS = 12

    RECT_PAD = 3

    linedx = WIDTH/7
    linedy = HEIGHT/NUM_HRS

    root = Tk()
    root.resizable(0,0)

    ACTIVE_CANVAS = None
    def drawSchedule(sched):
        global ACTIVE_CANVAS
        if ACTIVE_CANVAS:
            ACTIVE_CANVAS.pack_forget()
        c = Canvas(root, background='floral white', width=WIDTH, height=HEIGHT)
        ACTIVE_CANVAS = c

        for i in range(1,7):
            x = i*linedx
            c.create_line(x,0,x,HEIGHT)

        for i in range(NUM_HRS):
            hr = START_HR + i
            y = i*linedy
            c.create_line(0,y,WIDTH,y)
            c.create_line(0,y+linedy/2,WIDTH,y+linedy/2, dash=(100,10))
            c.create_text(5,y+5,anchor=NW,text=str((hr-1)%12 + 1))

        for (idx,(cIdr, td, cl)) in enumerate(sched):
            col = COLORS[cl.cId]
            for (i,timeInts) in td.items():
                for (v0,v1) in timeInts:
                    x0 = (i+1)*linedx+RECT_PAD
                    x1 = (i+2)*linedx-RECT_PAD
                    y0 = (v0-START_HR)*linedy+RECT_PAD
                    y1 = (v1-START_HR)*linedy-RECT_PAD
                    c.create_rectangle(x0,y0,x1,y1, fill=col)
                    c.create_text((x0+x1)/2,(y0+y1)/2,text=str(cIdr))

        c.pack()


    activeClassVars = [IntVar() for _ in ACTIVE_CLASS_LIST]
    forceClassVars = [IntVar() for _ in ACTIVE_CLASS_LIST]
    def refreshLists():
        global classes, scheds, units

        classes = [ACTIVE_CLASS_LIST[i] for i in range(len(ACTIVE_CLASS_LIST)) if activeClassVars[i].get()]

        scheds, units = getScheds(classes)

        forceCIDs = [ACTIVE_CLASS_LIST[i].cId for i in range(len(ACTIVE_CLASS_LIST)) if forceClassVars[i].get()]
        def schedMatches(s):
            sat = {fId:0 for fId in forceCIDs}
            for (_,_,cl) in s:
                if cl.cId in sat:
                    sat[cl.cId] = 1
            sats = all(sat.values())
            return sats

        validIndices = [i for i in range(len(scheds)) if schedMatches(scheds[i])]
        scheds = [scheds[i] for i in validIndices]
        units = [units[i] for i in validIndices]

        loadList()

    lFrame = Frame(root)

    includeCBFrame = Frame(lFrame)
    Label(includeCBFrame, text="Include:").pack(side=TOP,anchor=W)

    for i in range(len(classes)):
        cl = classes[i]
        cb0 = Checkbutton(includeCBFrame, text=cl.cId, var=activeClassVars[i])
        cb0.select()
        cb0.pack(side=TOP, anchor=W)
    includeCBFrame.pack(side=LEFT, fill=Y)

    forceCBFrame = Frame(lFrame)
    Label(forceCBFrame, text="Force:").pack(side=TOP,anchor=W)

    for i in range(len(classes)):
        cl = classes[i]
        cb0 = Checkbutton(forceCBFrame, text=cl.cId, var=forceClassVars[i])
        cb0.pack(side=TOP, anchor=W)
    forceCBFrame.pack(side=LEFT, fill=Y)

    Button(lFrame, text="Get", command=refreshLists).pack(side=BOTTOM)

    lFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)

    scrollbar = Scrollbar(root)

    schedLb = Listbox(root, width=30, selectmode=SINGLE)

    def loadList():
        schedLb.delete(0,END)

        for i in range(len(scheds)):
            schedLb.insert(END,'%s (%s)' % (i,units[i]))

    loadList()

    schedLb.selection_set(END)

    def switchSched(event):
        i = int(schedLb.curselection()[0])
        #print(scheds[i])
        drawSchedule(scheds[i])


    schedLb.bind("<<ListboxSelect>>", switchSched)
    schedLb.pack(side=LEFT,anchor=W,fill=Y,expand=True)
    scrollbar.pack(side=LEFT, fill=Y)

    schedLb.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=schedLb.yview)

    drawSchedule(scheds[-1])
    root.mainloop()
