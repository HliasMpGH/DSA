import argparse
from collections import deque

# add switches to allow user choices of execution in cli
parser = argparse.ArgumentParser()
parser.add_argument('-v', action = 'store_true', help = 'print the s1 & s2 arrays along the results')
parser.add_argument('tinput', nargs='*', action = 'store', help = 'match the given strings in the file')
args = parser.parse_args()

patterns = args.tinput[0:len(args.tinput) - 1] # the patterns
patterns.sort(key = len)

if len(patterns) < 1:
    exit("invalid input. Program termination")
if ".txt" not in args.tinput[-1] :
    exit("invalid file input. Program termination")

file = args.tinput[-1] # the file that contains the text

def chain(word) :
    ''' Input :  word, a String
        Data  :  trie, a trie that represents some patterns
                 isEndNode, a dictionary that containts the nodes of the trie, where isEndNode[node] 
                 is True if the traversal from root to node represents a pattern
        Result:  word gets added in trie as a whole new pattern in new nodes and edges, trie and isEndNode are changed '''
    node = max(trie.keys())
    n = len(word) + 1
    for i in range(n) :
        trie.setdefault(node + i + 1, [])
    for index, i in enumerate(word) :
        trie[node + index + 1].append((node + index + 2, i))
        isEndNode[node + index + 1] = False

def DFS(trie, node, word) :
    ''' Input :  trie, a trie that represents some patterns
                 node, a node in trie
                 word, a String
        Data  :  isEndNode, a dictionary that containts the nodes of the trie, where isEndNode[node] 
                 is True if the traversal from root to node represents a pattern
        Result:  trie is traversed (Depth-First) from node to try to add word it it
                 word is added in trie, trie and isEndNode are changed '''
    found = False
    for i in trie[node] :
        if i[1] == word[0] :
            found = True
            if len(word) > 1 :
                DFS(trie, i[0], word[1:]) # while you match a letter in the trie, keep traversing the trie Depth-First
    if not found :
        trie[node].append((max(trie.keys()) + 1, word[0]))
        chain(word[1:]) # if you find a letter that does not match, add the rest of the word in trie as new nodes
    isEndNode[max(trie.keys())] = True

def hasChild(trie, node, weight) :
    ''' Input :  trie, a trie that represents some patterns
                 node, a node in trie
                 weight, a character
        Output:  True if node in trie has a child connected with weight, False otherwise '''    
    if node not in trie.keys() : return False # the node does not exist in the trie, return False
    data = [n[1] for n in trie[node]]
    return weight in data

def getChild(trie, node, weight):
    ''' Input :  trie, a trie that represents some patterns
                 node, a node in trie
                 weight, a character
        Output:  n, the child that is connected to node in trie with weight '''
    if hasChild(trie, node, weight) : # if the node does not exist in the trie, this will fail and the getChild() method will return None
        for n in trie[node] :
            if n[1] == weight :
                return n[0]
    else :
        return None

def getParent(trie, node) :
    ''' Input :  trie, a trie that represents some patterns
                 node, a node in trie
        Output:  k, the parent that is connected to node in trie
                 None, if node doesnt have a parent or does not exist in trie '''
    if isRoot(trie, node) : return None # the node is the root, it doesn't have a parent
    stack = deque()
    stack.appendleft(0) # start from node 0, the root
    while len(stack) > 0 :
        u = stack.popleft() # traverse the trie Depth-First to find the parent that connects to node
        for k in trie[u] :
            if k[0] == node : return u
            stack.appendleft(k[0])
    return None # the node does not exist in the trie

def isRoot(trie, node) :
    ''' Input :  trie, a trie that represents some patterns
                 node, a node in trie
        Output:  True if node is root of trie, False if not
                 None, if node does not exist in trie '''
    if node not in trie.keys() : return None # the node does not exist in the trie
    stack = deque()
    stack.appendleft(0) # start from node 0, the root
    while len(stack) > 0 :
        u = stack.popleft()
        for n in trie[u] :
            if n[0] == node : return False # if node is found while traversing the trie, it means that it's not the root
            stack.appendleft(n[0])
    return True # since we know node is in trie (line 93), if we didnt find it while traversing the trie this way, 
                # it means that node is the root

def d(node) :
    ''' Input :  node, a node in a trie
        Data  :  trie, a trie that represents some patterns
        Output:  d, the depth of node in trie
                 -1, if node does not exist in trie '''
    if node not in trie.keys() : return -1 # the node does not exist in the trie
    if isRoot(trie, node) : return 0; # the depth of the root is 0
    d = 0 # starting depth
    queue = deque([0])
    queue.append(len(trie)) # add a sentinel value that represents a border between different depths of children in the queue
    while len(queue) > 1 :
        u = queue.popleft()
        if u == len(trie) :
            d += 1
            queue.append(len(trie)) # if the sentinel value reaches the start of the queue, append it to the end again
            for q in queue :
                if q == node : return d # check the whole queue for the node, if it exists in it, then its depth will be d
            u = queue.popleft() # pop again to take a node
        for v in trie[u] :
            queue.append(v[0]) # add the children of the previously poped node and add them to the end of the queue

def createRt(pmin, trie, t) :
    ''' Input :  pmin, the length of the smallest pattern
                 trie, a trie that represents some patterns
                 t, the text that we will look to match our patterns
        Output:  rt, the right-most array of our patterns, where rt[c] containts the most right
                 appearance of c and pmin + 1 if c does not exist in the patterns '''
    chars = []
    rt = dict()
    full = patterns + [t] # the whole alphabet that we will be considering for the algorithm (the full set of the characters in the text and in the patterns)
    for p in full :
        for c in p :
            if c not in chars :
                chars.append(c) # list with the full set of characters that appear in the text and in the patterns
    for c in chars :
        k = []
        for list in trie.values() :
            for tuple in list :
                if tuple[1] == c : # append all the depths of the character we are traversing in the trie (if the char does not exist in the trie, k will be empty)
                    k.append(d(tuple[0]))
        k.append(pmin + 1) # append pmin + 1 in k so we can take the min of all
        rt[c] = min(k)
    return rt     
    
def createFailure(trie) :
    ''' Input :  trie, a trie that represents some patterns
        Output:  failure, an array where failure[n] = v so w[v] is the largest suffix of w(n), or 0
                 if it does not exist. w(i) is the pattern that is being formed if we traverse the trie 
                 from root to i '''
    failure = dict()
    nodes = [n[0] for n in trie[0]] # save the kids of the root node (the nodes that are on depth 1)
    failure[0] = 0 # root node
    for node in nodes :
        failure[node] = 0 
    queue = deque(nodes)
    while len(queue) > 0 :
        u = queue.popleft()
        for v in trie[u] :
            queue.append(v[0])
            ut = failure[u]
            c = v[1]
            while not hasChild(trie, ut, c) and not isRoot(trie, ut) :
                ut = failure[ut]
            if hasChild(trie, ut, c) :
                failure[v[0]] = getChild(trie, ut, c)
            else :
                failure[v[0]] = 0
    return failure

def createSet1(failure) :
    ''' Input :  failure, an array
        Output:  set1, a dictionary where set1[u] contains the nodes that are most close to u
                 that are of deeper depth in the trie from u and w(u) is the largest suffix of w(v) for every
                 v in set1[u] '''
    set1 = dict()
    for i in failure.values() :
        if i == 0 : continue # dont consider nodes that have 0 in the failure array
        s = set()
        for j in failure.keys() :
            if failure[j] == i :
                s.add(j)
        set1[i] = s
    return set1

def createSet2(set1) :
    ''' Input :  set1, a dictionary
        Data  :  isEndNode, a dictionary that containts the nodes of a trie, where isEndNode[node] 
                 is True if the traversal from root to node represents a pattern
        Output:  set2, a dictionary where set2[u] is a subset of set1[u] so that every
                 path from nodes in set1[u] is a pattern '''
    set2 = dict()
    for i in set1.keys() :
        s = set()
        for j in set1[i] :
            if isEndNode[j] :
                s.add(j)
        if len(s) > 0 :
            set2[i] = s
    return set2

def createS1(pmin, set1, r) :
    ''' Input :  pmin, the length of the smallest pattern
                 set1, a dictionary
                 r, the root of the trie
        Data  :  trie, a trie that represents some patterns
        Output:  s1, an array where s1[u] = min(pmin, {d(ut) - d(u) for every ut in set1[u]}) if u is not the root
                 and s1[u] = 1 if u is the root '''
    s1 = [0] * len(trie)
    stack = deque()
    stack.appendleft(r)
    while len(stack) > 0 :
        u = stack.popleft()
        for n in trie[u] :
            stack.appendleft(n[0])
        if u == r :
            s1[0] = 1
        else :
            k = []
            if u in set1.keys() : # if set1[u] does not exist, dont consider it in the computation and take pmin
                k = [d(ut) - d(u) for ut in set1[u]] # the difference of depth of the u we are traversing with every ut that belongs in set1[u]
            k.append(pmin) # append pmin in k so we can take the min of all
            s1[u] = min(k)       
    return s1

def createS2(pmin, set2, r) :
    ''' Input :  pmin, the length of the smallest pattern
                 set2, a dictionary
                 r, the root of the trie
        Data  :  trie, a trie that represents some patterns
        Output:  s2, an array where s2[u] = min(s2[parent(u)], {d(ut) - d(u) for every ut in set2[u]}) if u is not the root
                 and s1[u] = pmin if u is the root '''
    s2 = [0] * len(trie)
    stack = deque()
    stack.appendleft(r)
    while len(stack) > 0 :
        u = stack.popleft()
        for n in trie[u] :
            stack.appendleft(n[0])
        if u == r :
            s2[0] = pmin
        else :
            k = []
            if u in set2.keys() : # if set2[u] does not exist, dont consider it in the computation and take pmin
                k = [d(ut) - d(u) for ut in set2[u]] # the difference of depth of the u we are traversing with every ut that belongs in set2[u]
            k.append(s2[getParent(trie, u)]) # append in k so we can take the min of all
            s2[u] = min(k)
    return s2

def CommentzWalter(t) :
    ''' Input :  t, the text we will look to match our patterns
        Data  :  trie, a trie that represents the reversed patterns
                 pmin, the length of the smallest pattern
                 rt, the right-most array of appearances of characters
                 s1
                 s2
        Output:  q, a queue that contains (m, i) tuples where m is the pattern and i the index it was found it t '''
    q = deque()
    i = pmin - 1
    j = 0
    u = 0
    m = ''
    while i < len(t) :
        while hasChild(trie, u, t[i - j]) :
            u = getChild(trie, u, t[i - j])
            m += t[i - j]
            j += 1
            if isEndNode[u] :
                q.append((m[::-1], i - j + 1))
        if j > i :
            j = i
        s = min(s2[u], max(s1[u], rt[t[i - j]] - j - 1))
        i += s
        j = 0
        u = 0
        m = ''
    return q


# -- MAIN THREAD --

trie = {
    0: []
}

isEndNode = {
    0 : False
}

rpatterns = []
for p in patterns :
    rpatterns.append(p[::-1]) # reverse the patterns

for i in rpatterns :
    DFS(trie, 0, i) # construct the trie with the reverse patterns

try :
    with open(file) as text :
        t = text.readline()
        pmin = len(min(patterns, key = len))
        rt = createRt(pmin, trie, t)
        failure = createFailure(trie)
        set1 = createSet1(failure)
        set2 = createSet2(set1)
        s1 = createS1(pmin, set1, 0)
        s2 = createS2(pmin, set2, 0)
        if args.v : # print s1 & s2 arrays if user specified it (-v)
            for n in trie.keys() :
                print(n, ": ", s1[n], "," , s2[n], sep = "")
        q = CommentzWalter(t)
        for tuple in q : # print the patterns and where they were found
            print(tuple[0], ":", tuple[1])
except FileNotFoundError :
    print("404: File not Found")
