import pickle
import time
from creatPath import createPath
import collections
compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
prev=[('f','f'),('f','f')]
while(1):
        try:
                with open("robotPoints.txt", "rb") as fb:
                        array=pickle.load(fb)
                #print(array)
                #time.sleep(0.5)
                goalPoints=[]
                print(prev)
                print(array)
                if not compare(prev,array):
                        
                        for i in array:
                                if i == ('f','f'):
                                        continue
                                else:
                                        goalPoints.append(i)      
                        if len(goalPoints)>0:
                                print(goalPoints)
                                PathPoints=createPath(goalPoints,True)
                                print(PathPoints)

                                print(goalPoints)
                                with open('PathPoints.txt', 'wb') as fb:
                                        pickle.dump(PathPoints,fb)
                                        
                        prev=array
        except EOFError:
                array = list()


   

