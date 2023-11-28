from sys import argv

def addClusts(u, v) :
    ''' Input:  u,v, 2 lists representing 2 clusters to be joined 
        Output: l, a list representing the 2 conjoined clusters '''
    l = u + v
    l.sort()
    return l

def minIn(dist):
    ''' Input:  dist, a 2d matrix
        Output: minD, the minimum element of said matrix
                c1, collumn index of the element
                c2, row index of the element '''
    min_row = []
    for i in dist :
        min_row.append(min(i))
    minD = min(min_row)
    c1,c2 = -1,-1
    for i in range(len(dist)) :
        for j in range(len(dist[i])) :
            if minD == dist[i][j] and c1 == -1: # save the first occurance of min
                c1 = j
                c2 = i    
    return minD,c1,c2

def coefficients(method,node):
    ''' Input:  method, the specified method used for clustering data
                node, the node of the 'v' cluster in 'clusters'
        Data:   fcluster, the 's' cluster
                scluster, the 't' cluster
                clusters, a list containing all clusters
        Output: ai,aj,b,g, the coefficients needed to calculated the distance between 2 clusters '''    
    if method == "single" :
        return 0.5,0.5,0,-0.5 
    elif method == "complete" :
        return 0.5,0.5,0,0.5
    elif method == "average" :
        ai = len(fcluster) / (len(fcluster) + len(scluster))
        aj = len(scluster) / (len(fcluster) + len(scluster))
        return ai,aj,0,0
    else :
        ai = (len(fcluster) + len(clusters[node])) / (len(fcluster) + len(clusters[node]) + len(scluster))
        aj = (len(scluster) + len(clusters[node])) / (len(fcluster) + len(clusters[node]) + len(scluster))
        b = - len(clusters[node]) / (len(fcluster) + len(clusters[node]) + len(scluster))
        return ai,aj,b,0

available = ["single", "complete", "average", "ward"] 

method = argv[1]
file = argv[2]

if method not in available :
    exit("Not an acceptable method. Program termination")
                                  
try :
    with open(file) as numbers:
        content = numbers.readline() # take as input the numbers from file
        clusters = content.split(" ") # place each number in a seperate node of the list 'clusters'
        clusters = [[int(x)] for x in clusters] # typecast the list to int & make each element its own cluster
        clusters.sort()

        # find the starting distances
        dist = []
        for i in range(len(clusters)):
            col = []
            for j in range(len(clusters)):
                if i > j:
                    col.append(float(round(abs(clusters[i][0] - clusters[j][0]),2)))
                elif i == j :
                    col.append(float('inf'))
            dist.append(col) 

        while len(clusters) > 1:
            
            # get the minimum distance between two clusters & the indeces of said clusters
            minD,c1,c2 = minIn(dist)

            fcluster = clusters[c1] # cluster 1
            scluster = clusters[c2] # cluster 2
            newC = addClusts(fcluster,scluster) # the new cluster

            # print the 2 clusters to be joined
            print("(", end = "")
            print(*fcluster, end ="")
            print(")",end = " ")
            print("(",end = "")
            print(*scluster, end ="")
            print(")",end = " ")

            print(minD, end = "  ") # dist of clusters that are being conjoined
            print(len(newC)) # length of new cluster

            # update distances
            rows = []
            for i in range(len(dist)):
                if i == c2: continue # skip the second cluster               
                col = []
                for j in range(len(dist[i])):
                    if j == c2: continue # skip the second cluster
                    if i == j:
                        col.append(float('inf'))
                    elif i == c1:
                        ai,aj,b,g = coefficients(method, j)
                        dsv = dist[c1][j]  # d(s,v)
                        dtv = dist[c2][j]  # d(t,v)
                        dst = dist[c2][c1] # d(s,t)
                        duv = ai * dsv + aj * dtv + b * dst + g * abs(dsv - dtv) # d(u,v)
                        col.append(float(round(duv,2)))
                    elif j == c1:
                        ai,aj,b,g = coefficients(method, i)
                        dsv = dist[i][c1]  # d(s,v)
                        if c2 >= len(dist[i]) : # check that the cluster we are iterating is in the range of c2 (its distance w c2 is calculated in row c2)
                            dtv = dist[c2][i]  # d(t,v)
                        else :
                            dtv = dist[i][c2]
                        dst = dist[c2][c1] # d(s,t)
                        duv = ai * dsv + aj * dtv + b * dst + g * abs(dsv - dtv) # d(u,v)
                        col.append(float(round(duv,2)))
                    else :
                        col.append(dist[i][j])         
                rows.append(col)
            dist = rows
            
            # remove the 2 clusters
            clusters.remove(fcluster)
            clusters.remove(scluster)
            # add the new cluster in the old position of the first one
            clusters.insert(c1,newC)
except FileNotFoundError:
    print("404: File not Found")
