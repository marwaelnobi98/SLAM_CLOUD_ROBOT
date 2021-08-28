##############################################################################

# import packages

##############################################################################

 

import numpy as np

import heapq

import cv2

import matplotlib.pyplot as plt

from matplotlib.pyplot import figure

##############################################################################

# heuristic function for path scoring

##############################################################################
prevDir=(0,0)
DirCost = 0

def wallProxyCost(location,CurrentDir):
    global DirCost
    global prevDir
    tmp= prevDir
    if CurrentDir is not tmp:
        DirCost=DirCost + 0.5

        
    return DirCost
        

def heuristic(a, b,extra):

    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)+extra



##############################################################################

# path finding function

##############################################################################

 

def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    
    close_set = set()

    came_from = {}

    gscore = {start:0}

    fscore = {start:heuristic(start, goal,0)}

    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
 

    while oheap:

        current = heapq.heappop(oheap)[1]
        
        if current == goal:

            data = []

            while current in came_from:

                data.append(current)

                current = came_from[current]

            return data

        close_set.add(current)
        #print(current)
        for i, j in neighbors:
            global prevDir
            prevDir=(i,j)
            neighbor = current[0] + i, current[1] + j
            extra=wallProxyCost(neighbor,(i,j))

            tentative_g_score = gscore[current] + heuristic(current, neighbor,extra)

            if 0 <= neighbor[0] < array.shape[0]:

                if 0 <= neighbor[1] < array.shape[1]:                

                    if array[neighbor[0]][neighbor[1]] == 1:

                        continue

                else:

                    # array bound y walls

                    continue

            else:

                # array bound x walls

                continue
 

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):

                continue
 

            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:

                came_from[neighbor] = current

                gscore[neighbor] = tentative_g_score

                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal,0)

                heapq.heappush(oheap, (fscore[neighbor], neighbor))
 
                
    return False

def createPath(goalPoints,plot=False):
    ####################without dialation#############
    img = cv2.imread("map2.png",0)
    grid = cv2.bitwise_not(img)
    ##################################################

    ###############with dialation##########################
    img = cv2.imread("map2.png",0)
    canned = cv2.Canny(img,150,200)
    kernel = np.ones((6, 6), 'uint8')
    grid = cv2.dilate(canned , kernel , iterations=1)
    ########################################################


    grid= (grid>250) * 1
    
    # start point and goal
    start = (32,19)

    FinalPath=[]
    for goal in goalPoints:
        
        route = astar(grid, start, goal)
        
        route = route + [start]
        
        route = route[::-1]
        route2 = route.copy()
        i= 0

        while i<len(route2)-2:
            if route2[i][0] == route2[i+2][0] :      
                del(route2[i+1])
                i = i-1       
            elif route2[i][1] == route2[i+2][1]:
                del(route2[i+1])
                i = i-1
            elif ( abs(route2[i+2][0]-route2[i][0])==abs(route2[i+2][1] - route2[i][1])):
                del(route2[i+1])
                i = i-1
            i = i+1
        start=goal
        FinalPath=FinalPath+route2
        FinalPath=FinalPath[0:-1]

    FinalPath.append(goal)

    if plot is True:
        x_coords = []

        y_coords = []

        for i in (range(0,len(FinalPath))):

            x = FinalPath[i][0]

            y = FinalPath[i][1]

            x_coords.append(x)

            y_coords.append(y)

        # plot map and path

        fig, ax = plt.subplots(figsize=(20, 20))

        ax.imshow(grid, cmap=plt.cm.Dark2)
        #ax.imshow(img, cmap=plt.cm.Dark2)
        ax.scatter(19,32, marker = "*", color = "yellow", s = 200)

        ax.scatter(goalPoints[0][1],goalPoints[0][0], marker = "*", color = "red", s = 200)
        if len(goalPoints)==2:
            ax.scatter(goalPoints[1][1],goalPoints[1][0], marker = "*", color = "red", s = 200)

        ax.plot(y_coords,x_coords,color = "black")
        #ax.plot(y_coords2,x_coords2, marker="*",color = "blue")



        plt.show()

    return FinalPath


