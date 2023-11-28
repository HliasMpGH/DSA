from sys import argv
from collections import deque

task = argv[1]
file = argv[2]

available = ['lexbfs', 'chordal', 'interval']

if task not in available :
    exit("Not an acceptable task. Program termination")

def createAdjList(nodes, edges) :
    ''' Input:  nodes, a list containing the nodes of a graph
                edges, a list containing the edges of a graph
                where edge[i] has elements k,j if k and j are strongly connected 
        Output: adjList, the Adjacency List of the graph ''' 
    values =[[] for node in nodes]
    adjList = dict(zip(nodes,values))
    for e in edges :
        adjList[e[0]].append((e[1]))
        adjList[e[1]].append((e[0]))
    return adjList

def LexBFSseq(nodes, adjList) :
    ''' Input:  nodes, a list containing the nodes of a graph
                adjList, the Adjacency List of the graph 
        Output: LexBFSList, the sequence that we would follow to traverse the graph using
                the Lexicographical Breadth-First Search '''     
    S = [set(node for node in nodes)]
    LexBFSList = []
    while len(S) > 0 :
        node = S[0].pop()
        if len(S[0]) == 0 :
            S.remove(S[0])
        LexBFSList.append(node)
        nb = adjList[node]
        index = 0
        S2 = S[:]
        for sets in S :
            nbs = set()
            for n in nb :
                if n in LexBFSList : continue # dont check the neighbors that we have already visited
                if n in sets :
                    sets.remove(n)
                    index = S2.index(sets)
                    if len(sets) == 0 :
                        S2.remove(sets)
                    nbs.add(n)
            if len(nbs) > 0 :
                S2.insert(index, nbs)
        S = S2
    return LexBFSList

def isChordal(LexBFSList, adjList) :
    ''' Input:  LexBFSList, the Lexicographical BFS ordering of a graph
                adjList, the Adjacency List of said graph
        Output: True if the given graph is chordal ''' 
    rLexBFSList = deque(LexBFSList[:])
    rLexBFSList.reverse() # reversed LexBFS sequence
    for uIndex,u in enumerate(rLexBFSList) :
        nbs = adjList[u] # the full neighbor list of u
        rnu = {n for n in nbs if rLexBFSList.index(n) > uIndex} # the right neighbors of u
        foundFirstNB = False
        for jIndex in range(uIndex + 1,len(rLexBFSList)) :
            j = rLexBFSList[jIndex]
            if j in nbs and not foundFirstNB: # found v
                foundFirstNB = True
                temp = rnu.copy()
                temp = temp - {j}
                rnv = {n for n in adjList[j] if rLexBFSList.index(n) > jIndex} # the right neighbors of v
                if not temp.issubset(rnv) :
                    return False
    return True

def splitComponents(adjList) :
    ''' Input:  adjList, The Adjacency List of a graph
        Output: components, a list where components[i] holds the
                components that are left after removing node i
                and its neighbors from the graph '''
    components = [[] for c in nodes]
    for i in adjList :
        newAdjList = {key : adjList[key][:] for key in adjList}
        newAdjList.pop(i) # remove the node
        nbs = adjList[i]
        for n in nbs :
            newAdjList.pop(n) # remove the neighbors of the node
        for k in newAdjList :
            for n in nbs :
                if n in adjList[k] :
                    newAdjList[k].remove(n) # remove the edges between each node and the previously deleted nodes
        inQueue = {key : False for key in newAdjList}
        looped = {key : False for key in newAdjList}
        for u in newAdjList :
            visited = {key : False for key in newAdjList}
            if not looped[u] :
                queue = deque([u])
                inQueue[u] = True
                while len(queue) > 0 :
                    node = queue.pop()
                    inQueue[node] = False
                    visited[node] = True
                    looped[node] = True
                    for v in newAdjList[node] :
                        if not visited[v] and not inQueue[v] :
                            queue.appendleft(v)
                            inQueue[v] = True
                comp = []
                for n in visited :
                    if visited[n] :
                        comp.append(n)
                if comp not in components[i] :
                    components[i].append(comp)
                visited.clear()
    return components

def isATFree(adjList) :
    ''' Input:  adjList, the Adjacency List of a graph
        Output: True if the given graph is free of Asteroidal Triples '''
    components = splitComponents(adjList)
    C = []
    for i in nodes :
        row = []
        for j in nodes :
            if j in adjList[i] or i == j:
                row.append(0)
            else :
                for c in components[i] :
                    if j in c :
                        row.append(c)
                        break
        C.append(row)
    for u in range(len(nodes)) :
        for v in range(len(nodes)) :
            if C[u][v] == 0 : continue # dont check nodes that are neighbors to each other
            for w in range(len(nodes)) : 
                if C[u][w] == 0 or C[w][v] == 0 : continue # dont check nodes that are neighbors to each other
                if (C[u][v] == C[u][w]) \
                    and (C[v][u] == C[v][w]) \
                    and (C[w][u] == C[w][v]) :
                    return False
    return True

def isInterval(LexBFSList,adjList) :
    ''' Input:  LexBFSList, the Lexicographical BFS ordering of a graph 
                adjList, the Adjacency List of a graph
        Output: True if the given graph is Interval '''   
    return isATFree(adjList) and isChordal(LexBFSList,adjList)

# ---MAIN THREAD---

# construct the graph
try :
    with open(file) as graph :
        nodes = []
        edges = []
        line = graph.readline()
        while line:
            nums = line.split(" ")
            nums = [int(x) for x in nums]
            edges.append([nums[0],nums[1]])
            for i in nums :
                if i not in nodes :
                    nodes.append(i)
            line = graph.readline()
except FileNotFoundError :
        print("404: File not Found")
# create the adjancency list of given graph
adjList = createAdjList(nodes, edges)
# get the LexBFS sequence of said graph
LexBFSList = LexBFSseq(nodes, adjList)
if task == "lexbfs" :
    print(LexBFSList)
elif task == "chordal" :
    print(isChordal(LexBFSList, adjList))
else :
    print(isInterval(LexBFSList,adjList))
