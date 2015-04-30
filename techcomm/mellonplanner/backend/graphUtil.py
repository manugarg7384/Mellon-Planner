'''
Created on Oct 22, 2014

@author: Bill
'''

import sets
import time

def dual(adjMatrix):
    return [[1-v for v in r] for r in adjMatrix]

def adjComplement(adjList):
    N = len(adjList)
    compAdjList = []
    for nbrs in adjList:
        newNbrs = []
        m = len(nbrs)
        j = 0
        for v in range(N):
            if j >= m or (nbrs[j] != v):
                newNbrs.append(v)
            else:
                j += 1
        compAdjList.append(newNbrs)
    return compAdjList


def makeGraphAdjList(adjMatrix):
    #assm NxN
    N = len(adjMatrix)
    return [[j for j in range(N) if adjMatrix[i][j]] for i in range(N)]

def makeGraphAdjMatrix(adjList):
    N = len(adjList)
    M = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for w in adjList[i]:
            M[i][w] = 1
    return M

def maximalCliques(adjList):
    N = len(adjList)
    ablist = [sum(1<<j for j in nbrs) for nbrs in adjList]
    #print([bin(r)[2:] for r in ablist])
    V = 2**N - 1
    R0,X0 = 0,0
    P0 = V

    maxCliques = []

    def BK(R,P,X):
        #print(bin(P)[2:])
        if P == 0 and X == 0:
            maxCliques.append(R)
            return
        for i in range(N):
            v = 1<<i
            nbrs = ablist[i]
            if P & v:
                BK(R | v, P & nbrs, X & nbrs)
                P = P & (V - v)
                X = X | v

    BK(R0,P0,X0)
    return [[i for i in range(N) if c&(1<<i)] for c in maxCliques]




def stronglyConnectedComponents(adjList):
    N = len(adjList)
    visited = [0 for _ in range(N)]
    components = []
    while not all(visited):
        scc = [0 for _ in range(N)]
        i = 0
        while visited[i]:
            i+=1
        F = [i]
        while len(F)>0:
            for j in F:
                visited[j] = 1
                scc[j] = 1
            F = [j for r in F for j in adjList[r] if not visited[j]]
        components.append([i for i in range(N) if scc[i]])
    return components

def independentSet(adjMatrix):
    G = makeGraphAdjList(dual(adjMatrix))
    return maximalCliques(G)


#all maximal knapsack solutions
#solns returned in reverse of lexicographic order by index
def knapsack(sizes, maxSize):

    n = len(sizes)
    k_memo = [[None for _ in range(maxSize)] for _ in range(n)]

    def knapsackRec(i, t):
        if t == maxSize or i == n:
            return [(0, [])]
        if k_memo[i][t]:
            return k_memo[i][t]

        valid = []

        #do not include this value
        #filter solutions where there is room for this value
        valid.extend(filter(lambda (sz, ss) : sz + sizes[i] > maxSize - t,
                            knapsackRec(i+1, t)))

        #include this value if it fits
        if sizes[i] <= maxSize - t:
            subsols = knapsackRec(i+1, t+sizes[i])
            newSols = [(sizes[i] + sz, [i] + subsol) for (sz, subsol) in subsols]
            valid.extend(newSols)

        k_memo[i][t] = valid
        return valid

    return knapsackRec(0, 0)


if __name__ == '__main__':

    #M = [[1,1,0],[0,1,1],[0,0,0]]


    #print(makeGraphAdjList(M))

    #G = [[1, 2, 3, 4, 20, 22], [0, 2, 3, 4, 11, 15, 16, 17, 20, 27, 28], [0, 1, 3, 4, 6, 15, 16, 17, 20, 26], [0, 1, 2, 4, 7, 20, 24], [0, 1, 2, 3, 12, 19, 20, 21, 23, 29], [15], [2, 7, 15, 16, 17, 18, 19, 21, 26], [3, 6, 18, 19, 21, 24], [9, 10, 13, 16, 22, 27], [8, 10, 11, 13, 16, 28], [8, 9, 13, 16, 26], [1, 9, 15, 16, 17, 27, 28], [4, 19, 20, 21, 23, 25, 29], [8, 9, 10, 16], [17], [1, 2, 5, 6, 11, 16, 17, 26, 27, 28], [1, 2, 6, 8, 9, 10, 11, 13, 15, 17, 26, 27, 28], [1, 2, 6, 11, 14, 15, 16, 26, 27, 28], [6, 7], [4, 6, 7, 12, 20, 21, 23, 29], [0, 1, 2, 3, 4, 12, 19, 21, 23, 29], [4, 6, 7, 12, 19, 20, 23, 29], [0, 8, 27], [4, 12, 19, 20, 21, 29], [3, 7], [12, 29], [2, 6, 10, 15, 16, 17], [1, 8, 11, 15, 16, 17, 22, 28], [1, 9, 11, 15, 16, 17, 27], [4, 12, 19, 20, 21, 23, 25]]
    #GT = [[9, 11], [2, 5], [1, 7], [7], [], [1], [7, 8], [2, 3, 6], [6], [0, 11], [], [0, 9]]

    M = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0], [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0], [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1]]

    TM = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]]

    tmDual = makeGraphAdjList(dual(M))

    t0 = time.clock()
    for _ in range(100):
        balls = adjComplement(tmDual)
    print(time.clock() - t0)

    #cqs= maximalCliques(tmDual)
    #print(len(cqs))
    #print('\n'.join(str(cq) for cq in cqs))

    #G = makeGraphAdjList(M)

    #G = [[1,2,3],[0,2],[0,1],[0,4],[3]]

    #print(GT)
    #print(stronglyConnectedComponents(GT))

    #print(M)
    #print(dual(M))

    #print('{%s}' % (',\n'.join('{%s}' % ','.join(map(str,r)) for r in M)))





